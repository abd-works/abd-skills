#!/usr/bin/env bash
# detect-correction.sh — userPromptSubmitted hook for CDD correction detection.
# Parses the prompt for correction signals. If found, writes a pending entry to
# docs/sessions/corrections-pending.md so the sessionStart-primed AI processes
# it on the next (or current) turn.
set -euo pipefail

TMPFILE=$(mktemp)
trap 'rm -f "$TMPFILE"' EXIT
cat > "$TMPFILE"

python3 - "$TMPFILE" << 'PYEOF'
import json, sys, re, os, datetime

with open(sys.argv[1], encoding='utf-8') as f:
    raw = f.read()

try:
    data = json.loads(raw)
except Exception:
    sys.exit(0)

prompt = (data.get('prompt') or data.get('Prompt') or '').lower()

CORRECTION_PATTERNS = [
    r"that'?s? (was )?wrong",
    r"you'?re? wrong",
    r"you (were|are) wrong",
    r"you assumed",
    r"made an assumption",
    r"you'?re? assuming",
    r"you generated (when|instead)",
    r"should have grilled",
    r"should have asked (first|me|one)",
    r"you grilled all",
    r"asked all (at once|questions)",
    r"all questions at once",
    r"(that'?s?|that was|not) (right|correct)",
    r"\bincorrect\b",
    r"correct that",
    r"you made a mistake",
    r"that was a mistake",
    r"you skipped (the )?grill",
    r"you didn'?t? grill",
    r"you didn'?t? ask (first|me)",
    r"you should have (grilled|asked)",
    r"wrong approach",
    r"wrong answer",
]

matched = any(re.search(p, prompt) for p in CORRECTION_PATTERNS)

if not matched:
    sys.exit(0)

cwd = data.get('cwd') or os.getcwd()
corrections_dir = os.path.join(cwd, 'docs', 'sessions')
os.makedirs(corrections_dir, exist_ok=True)
corrections_file = os.path.join(corrections_dir, 'corrections-pending.md')

ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
excerpt = prompt[:200].replace('\n', ' ')

with open(corrections_file, 'a', encoding='utf-8') as f:
    f.write(f'- [ ] {ts} — correction signal detected: "{excerpt}"\n')

sys.exit(0)
PYEOF
