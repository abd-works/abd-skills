"""One-off: load conf/.secrets and make one OpenAI call to surface the real error."""
import os
import sys
from pathlib import Path

# Same secrets load as classify_chunks
skill_root = Path(__file__).resolve().parent.parent
secrets_path = (skill_root / "conf" / ".secrets").resolve()
print(f"Secrets path (absolute): {secrets_path}")
print(f"Exists: {secrets_path.exists()}")
if secrets_path.exists():
    for line in secrets_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if key:
                os.environ[key] = value  # file wins over any existing env
                print(f"Set {key}=***")
        elif line.startswith("sk-"):
            os.environ["OPENAI_API_KEY"] = line
            print("Set OPENAI_API_KEY=*** (from bare key line)")
key = os.environ.get("OPENAI_API_KEY", "")
print(f"OPENAI_API_KEY set: {bool(key)}")
if key:
    p, s = key[:10], key[-4:] if len(key) >= 4 else ""
    print(f"Key prefix/suffix: {p}...{s}  (confirm this changed if you updated .secrets)")

try:
    import openai
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    print("Calling chat.completions.create(model='gpt-4o-mini', ...)")
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say OK"}],
        max_tokens=10,
        temperature=0,
    )
    print("Success:", r.choices[0].message.content)
except Exception as e:
    print(f"Exception type: {type(e).__name__}")
    print(f"Exception: {e}")
    if hasattr(e, "response") and e.response is not None:
        print(f"Response status: {getattr(e.response, 'status_code', '?')}")
        print(f"Response body: {getattr(e.response, 'text', getattr(e.response, 'body', '?'))}")
    sys.exit(1)
