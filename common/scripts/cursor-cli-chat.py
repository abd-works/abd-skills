"""cursor-cli-chat — streaming CLI using cursor-agent.
Commands: /clear /system /workspace /save /load /retry /model /run /agent /state
Esc while agent is running: pause and prompt for command
"""
import json, os, subprocess, sys, tempfile, threading, datetime, time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = REPO_ROOT / "state.json"
SECRETS_FILE = REPO_ROOT / "conf" / ".secrets"

COMMANDS = [
    "/clear", "/system ", "/workspace ", "/save", "/load ",
    "/retry", "/model ", "/models", "/agent", "/skill", "/run", "/run ", "/state", "/help",
]

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import Completer, Completion
    from prompt_toolkit.history import InMemoryHistory

    class _ChatCompleter(Completer):
        def get_completions(self, document, complete_event):
            text = document.text_before_cursor

            if text.startswith("/skill "):
                prefix = text[7:]
                for s in sorted((Path(workspace) / ".cursor" / "skills").glob("*/SKILL.md")):
                    name = s.parent.name
                    if name.startswith(prefix):
                        yield Completion(name, start_position=-len(prefix))

            elif text.startswith("/agent "):
                prefix = text[7:]
                for a in sorted((Path(workspace) / ".cursor" / "agents").glob("*/AGENT.md")):
                    name = a.parent.name
                    if name.startswith(prefix):
                        yield Completion(name, start_position=-len(prefix))

            elif text.startswith("/"):
                for cmd in COMMANDS:
                    if cmd.startswith(text):
                        yield Completion(cmd, start_position=-len(text))

    _session = PromptSession(
        completer=_ChatCompleter(),
        history=InMemoryHistory(),
        complete_while_typing=True,
    )

    def _input(prompt: str) -> str:
        if not sys.stdin.isatty():
            print(prompt, end="", flush=True)
            return input()
        return _session.prompt(prompt)

except ImportError:
    def _input(prompt: str) -> str:  # type: ignore
        return input(prompt)

# Windows keypress detection
try:
    import msvcrt
    def _getkey() -> bytes | None:
        if msvcrt.kbhit():
            return msvcrt.getch()
        return None
except ImportError:
    def _getkey() -> bytes | None:  # type: ignore
        return None

BINARY = os.environ.get(
    "CURSOR_AGENT_BIN",
    r"C:\Users\thoma\AppData\Local\cursor-agent\cursor-agent.cmd",
)


def _default_workspace() -> str:
    cfg = REPO_ROOT / "skill-config.json"
    if cfg.is_file():
        try:
            data = json.loads(cfg.read_text(encoding="utf-8"))
            ws = data.get("workspace") if isinstance(data.get("workspace"), dict) else {}
            active = ws.get("active_skill_workspace")
            if active:
                return str(active)
        except (json.JSONDecodeError, OSError):
            pass
    return r"C:\dev\abd-pet-store-demo"


def _kill_tree(proc: subprocess.Popen) -> None:
    """Kill process and all children (Windows process tree kill)."""
    try:
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
            capture_output=True,
        )
    except Exception:
        proc.kill()


DEFAULT_WORKSPACE = _default_workspace()
DEFAULT_SYSTEM = "You are a helpful assistant. Answer concisely."

# Load API key
api_key = None
if not SECRETS_FILE.is_file():
    sys.exit(f"ERROR: missing {SECRETS_FILE}")
for line in SECRETS_FILE.read_text(encoding="utf-8").splitlines():
    if line.startswith("CURSOR_API_KEY="):
        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
        break
if not api_key:
    sys.exit(f"ERROR: no CURSOR_API_KEY in {SECRETS_FILE}")

# Mutable state
workspace = DEFAULT_WORKSPACE
system_prompt = DEFAULT_SYSTEM
model = "composer-2.5"
history: list[str] = []
last_user_msg: str = ""
agent_name: str | None = None
skill_names: list[str] = []
saved_instruction: str | None = None
MAX_HISTORY = 10  # keep last N exchanges (user+assistant pairs)

# Shared refs for Ctrl+P interrupt
_active_proc: subprocess.Popen | None = None
_pause_event = threading.Event()


def rebuild_system_prompt() -> None:
    global system_prompt
    parts: list[str] = []
    if agent_name:
        path = Path(workspace) / ".cursor" / "agents" / agent_name / "AGENT.md"
        if path.exists():
            parts.append(
                f"You are the {agent_name} agent.\n"
                f"Your full instructions are in: {path.resolve()}\n"
                f"Read that file before doing anything else."
            )
    for name in skill_names:
        path = Path(workspace) / ".cursor" / "skills" / name / "SKILL.md"
        if path.exists():
            parts.append(f"Also use skill '{name}' — instructions at: {path.resolve()}")
    if not parts:
        system_prompt = DEFAULT_SYSTEM
    elif agent_name:
        system_prompt = parts[0]
        if len(parts) > 1:
            system_prompt += "\n" + "\n".join(parts[1:])
    else:
        system_prompt = DEFAULT_SYSTEM + "\n" + "\n".join(parts)


def save_state() -> None:
    STATE_FILE.write_text(
        json.dumps(
            {
                "workspace": workspace,
                "agent": agent_name,
                "skills": skill_names,
                "instruction": saved_instruction,
                "model": model,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def load_state() -> bool:
    global workspace, agent_name, skill_names, saved_instruction, model
    if not STATE_FILE.exists():
        return False
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print(f"Warning: could not read {STATE_FILE}\n")
        return False
    workspace = data.get("workspace") or DEFAULT_WORKSPACE
    agent_name = data.get("agent")
    skill_names = list(data.get("skills") or [])
    saved_instruction = data.get("instruction")
    model = data.get("model") or model
    rebuild_system_prompt()
    return True


def clear_state() -> None:
    global workspace, system_prompt, agent_name, skill_names, saved_instruction, model, last_user_msg
    history.clear()
    last_user_msg = ""
    workspace = DEFAULT_WORKSPACE
    agent_name = None
    skill_names = []
    saved_instruction = None
    model = "composer-2.5"
    system_prompt = DEFAULT_SYSTEM
    if STATE_FILE.exists():
        STATE_FILE.unlink()


def print_state() -> None:
    print("Session state:")
    print(f"  workspace:   {workspace}")
    print(f"  agent:       {agent_name or '(none)'}")
    print(f"  skills:      {', '.join(skill_names) if skill_names else '(none)'}")
    print(f"  instruction: {saved_instruction or '(none)'}")
    print(f"  model:       {model}")
    print(f"  state file:  {STATE_FILE}\n")


def ask(user_input: str) -> tuple[str, bool]:
    """Send a message. Returns (response, was_paused)."""
    global last_user_msg, _active_proc
    last_user_msg = user_input
    history.append(f"User: {user_input}")

    # Keep only the last MAX_HISTORY exchanges (each exchange = 2 entries: user + assistant)
    trimmed = history[-(MAX_HISTORY * 2):]

    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8")
    tmp.write(
        f"{system_prompt}\n\n"
        "Conversation:\n\n"
        + "\n\n".join(trimmed)
        + "\n\nAssistant:"
    )
    tmp.close()

    cmd = [
        BINARY, "-p", "--trust", "--force",
        "--output-format", "text",
        "--workspace", workspace,
    ]
    if model:
        cmd.extend(["--model", model])
    cmd.append(f"@{tmp.name}")
    env = {**os.environ, "CURSOR_API_KEY": api_key}

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    except FileNotFoundError:
        print(f"\r\033[K  [error] cursor-agent binary not found: {BINARY}\n", flush=True)
        os.unlink(tmp.name)
        history.pop()
        return ("", False)
    _active_proc = proc
    assert proc.stdout is not None
    assert proc.stderr is not None

    # Relay stderr in background so it doesn't block
    stderr_lines: list[str] = []
    def _read_stderr() -> None:
        for line in proc.stderr:
            stderr_lines.append(line.decode("utf-8", errors="replace"))
    threading.Thread(target=_read_stderr, daemon=True).start()

    TIMEOUT_SECONDS = 180
    done = threading.Event()
    start_time = time.time()
    timed_out = threading.Event()

    def _spin() -> None:
        frames = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        i = 0
        while not done.is_set():
            elapsed = int(time.time() - start_time)
            remaining = TIMEOUT_SECONDS - elapsed
            if remaining <= 10:
                label = f"thinking... ({elapsed}s, killing in {remaining}s)"
            else:
                label = f"thinking... ({elapsed}s)  Esc to pause"
            print(f"\r\033[K  {frames[i % len(frames)]} {label}", end="", flush=True)
            i += 1
            time.sleep(0.1)

    def _watchdog() -> None:
        """Kill the process after TIMEOUT_SECONDS if no output yet."""
        deadline = start_time + TIMEOUT_SECONDS
        while not done.is_set():
            if time.time() > deadline:
                timed_out.set()
                _kill_tree(proc)
                break
            time.sleep(0.5)

    threading.Thread(target=_spin, daemon=True).start()
    threading.Thread(target=_watchdog, daemon=True).start()

    chunks: list[str] = []
    first = True
    paused = False

    while True:
        # Esc key pauses
        key = _getkey()
        if key == b'\x1b':
            paused = True
            _kill_tree(proc)
            break

        chunk = proc.stdout.read(32)
        if not chunk:
            # EOF — could be timeout kill or normal end
            if timed_out.is_set() and first:
                print(f"\r\033[K  [timeout] No response after {TIMEOUT_SECONDS}s — killed.\n", flush=True)
            break
        text = chunk.decode("utf-8", errors="replace")
        if first:
            done.set()  # got output — cancel watchdog
            print(f"\r\033[KAssistant: {text}", end="", flush=True)
            first = False
        else:
            print(text, end="", flush=True)
        chunks.append(text)

    done.set()
    _active_proc = None
    if not paused:
        rc = proc.wait()
        if rc != 0 and not chunks and not timed_out.is_set():
            print(f"  [error] cursor-agent exited with code {rc}", flush=True)
            if stderr_lines:
                print("  stderr:\n" + "".join(f"    {l}" for l in stderr_lines), flush=True)
    print("\n")

    # On timeout: ask user whether to retry or give up
    if timed_out.is_set():
        os.unlink(tmp.name)
        history.pop()  # remove the unanswered user message
        try:
            choice = input("  [timeout] r=retry  s=skip  q=quit: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            choice = "q"
        if choice == "r":
            return ask(user_input)
        elif choice == "q":
            print("Bye.\n")
            sys.exit(0)
        else:
            return ("", False)

    response = "".join(chunks).strip()
    if response:
        history.append(f"Assistant: {response}")
    return response, paused


def cmd_save() -> None:
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = Path(f"chat-{ts}.md")
    path.write_text(
        f"# Chat {ts}\n\n**Workspace:** {workspace}\n\n---\n\n"
        + "\n\n".join(history) + "\n",
        encoding="utf-8",
    )
    print(f"Saved to {path}\n")


def cmd_load(arg: str) -> None:
    path = Path(arg.strip())
    if not path.exists():
        print(f"File not found: {path}\n")
        return
    history.clear()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("User: ") or line.startswith("Assistant: "):
            history.append(line)
    print(f"Loaded {len(history)} turns from {path}\n")


def cmd_list_models() -> None:
    env = {**os.environ, "CURSOR_API_KEY": api_key}
    try:
        subprocess.run([BINARY, "--list-models"], env=env, check=False)
    except FileNotFoundError:
        print(f"cursor-agent not found: {BINARY}\n")
    print()


HELP = """Commands:
  /clear              wipe history + reset state.json
  /state              show workspace, agent, skills, instruction
  /system <text>      set system prompt
  /workspace <path>   change workspace
  /save               save conversation to file
  /load <file>        restore conversation from file
  /retry              resend last message
  /model <name>       set model (passed to cursor-agent --model)
  /models             list available models
  /agent              pick agent from menu
  /agent <name>       load agent by name
  /skill              pick skill from menu (appends)
  /skill <name>       load skill by name
  /run                resume last /run instruction from state.json
  /run <instruction>  autonomous loop — runs until you stop (Esc → stop)
  /help               show this
  Esc                 pause running agent, enter a command
  Ctrl+C              quit

Session state auto-saves to state.json at the skills repo root.
Restart scripts/cursor-cli-chat.py to restore settings (not auto-run). /clear deletes state.json.
"""


def run_loop(instruction: str) -> None:
    global saved_instruction
    saved_instruction = instruction
    save_state()
    print(f"\n[run] Starting — Esc → stop, Ctrl+C to quit\n")
    msg = instruction
    turn = 0

    while True:
        turn += 1
        print(f"[run] Turn {turn}", flush=True)
        response, paused = ask(msg)

        if paused:
            print("\r\033[K[run] Paused by operator.\n")
            try:
                cmd = input("[paused] stop / continue / <new instruction>: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n[run] Stopped.\n")
                return
            if cmd.lower() == "stop":
                print("[run] Stopped by operator.\n")
                return
            if not cmd or cmd.lower() == "continue":
                msg = "Continue from where you left off. Do the next slot or step."
                continue
            msg = cmd
            continue

        # Auto-continue every turn — only the operator stops the run (Esc → stop)
        msg = "Continue. Do the next slot or step until the full plan is complete."


# ── Startup ────────────────────────────────────────────────────────────────
print("cursor-agent chat  |  /help for commands  |  Esc to pause agent")
print("=" * 60)

if load_state():
    print(f"Loaded {STATE_FILE.name}:")
else:
    print(f"No {STATE_FILE.name} — using defaults.")
print_state()
if saved_instruction:
    print("Saved instruction loaded. Type /run to start (or edit with /run <new text>).\n")

# ── Main loop ──────────────────────────────────────────────────────────────
while True:
    try:
        msg = _input("You: ").strip()
    except KeyboardInterrupt:
        print("\nBye.")
        break
    except EOFError:
        print("\nBye.")
        break

    if not msg:
        continue

    if msg == "/clear":
        clear_state()
        print("History and state.json cleared.\n")

    elif msg == "/state":
        print_state()

    elif msg.startswith("/system "):
        system_prompt = msg[8:].strip()
        save_state()
        print(f"System prompt: {system_prompt!r}\n")

    elif msg.startswith("/workspace "):
        workspace = msg[11:].strip()
        rebuild_system_prompt()
        save_state()
        print(f"Workspace: {workspace}\n")

    elif msg == "/save":
        cmd_save()

    elif msg.startswith("/load "):
        cmd_load(msg[6:])

    elif msg == "/retry":
        if not last_user_msg:
            print("Nothing to retry.\n")
        else:
            if len(history) >= 2:
                history.pop(); history.pop()
            ask(last_user_msg)

    elif msg == "/models":
        cmd_list_models()

    elif msg.startswith("/model "):
        model = msg[7:].strip()
        save_state()
        print(f"Model: {model!r}\n")

    elif msg == "/agent":
        agents = list((Path(workspace) / ".cursor" / "agents").glob("*/AGENT.md"))
        if not agents:
            print(f"No agents found in {workspace}/.cursor/agents\n")
        else:
            picked: list[str] = []
            while True:
                print("\nAgents (0 = done):")
                for i, a in enumerate(agents, 1):
                    tick = "✓" if a.parent.name == agent_name else " "
                    print(f"  {i}. [{tick}] {a.parent.name}")
                try:
                    choice = input("Pick number (0 to finish): ").strip()
                    if choice == "0" or choice == "":
                        break
                    idx = int(choice) - 1
                    picked = [agents[idx].parent.name]
                    print(f"  Added: {picked[0]}")
                    break
                except (ValueError, IndexError):
                    print("  Invalid choice.")
                except (EOFError, KeyboardInterrupt):
                    break
            if picked:
                agent_name = picked[0]
                rebuild_system_prompt()
                save_state()
            print(f"\nAgent context set\n")

    elif msg.startswith("/agent "):
        arg = msg[7:].strip()
        path = Path(arg)
        if not path.exists():
            path = Path(workspace) / ".cursor" / "agents" / arg / "AGENT.md"
        if not path.exists():
            print(f"Agent not found: {arg}\n")
        else:
            agent_name = path.parent.name
            rebuild_system_prompt()
            save_state()
            print(f"Agent loaded: {agent_name} (instructions via file reference)\n")

    elif msg == "/skill":
        skills = list((Path(workspace) / ".cursor" / "skills").glob("*/SKILL.md"))
        if not skills:
            print(f"No skills found in {workspace}/.cursor/skills\n")
        else:
            while True:
                print("\nSkills (0 = done):")
                for i, s in enumerate(skills, 1):
                    tick = "✓" if s.parent.name in skill_names else " "
                    print(f"  {i}. [{tick}] {s.parent.name}")
                try:
                    choice = input("Pick number (0 to finish): ").strip()
                    if choice == "0" or choice == "":
                        break
                    idx = int(choice) - 1
                    name = skills[idx].parent.name
                    if name not in skill_names:
                        skill_names.append(name)
                    rebuild_system_prompt()
                    save_state()
                    print(f"  Added: {name}")
                except (ValueError, IndexError):
                    print("  Invalid choice.")
                except (EOFError, KeyboardInterrupt):
                    break
            print(f"\nSkills added (file references)\n")

    elif msg.startswith("/skill "):
        arg = msg[7:].strip()
        path = Path(arg)
        if not path.exists():
            path = Path(workspace) / ".cursor" / "skills" / arg / "SKILL.md"
        if not path.exists():
            print(f"Skill not found: {arg}\n")
        else:
            name = path.parent.name
            if name not in skill_names:
                skill_names.append(name)
            rebuild_system_prompt()
            save_state()
            print(f"Skill appended: {name} (file reference)\n")

    elif msg == "/run":
        if not saved_instruction:
            print("No saved instruction. Use: /run <instruction>\n")
        else:
            try:
                run_loop(saved_instruction)
            except KeyboardInterrupt:
                if _active_proc:
                    _kill_tree(_active_proc)
                print("\n[run] Stopped.\n")

    elif msg.startswith("/run "):
        try:
            run_loop(msg[5:].strip())
        except KeyboardInterrupt:
            if _active_proc:
                _kill_tree(_active_proc)
            print("\n[run] Stopped.\n")

    elif msg == "/help":
        print(HELP)

    elif msg.startswith("/"):
        print(f"Unknown command.\n{HELP}")

    else:
        ask(msg)
