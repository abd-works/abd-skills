import subprocess, re, sys

result = subprocess.run(
    [sys.executable,
     r"c:\dev\abd-pet-store-demo\.cursor\skills\execute-skill-using-skills-rules\scripts\run_scanners.py",
     "--skill-root", r"c:\dev\abd-pet-store-demo\.cursor\skills\abd-ubiquitous-language",
     "--workspace", r"c:\dev\abd-works\abd-delivery-agent-kanban\docs\domain"],
    capture_output=True, text=True, cwd=r"c:\dev\abd-pet-store-demo"
)
output = result.stdout + result.stderr
counts = {}
for line in output.splitlines():
    m = re.search(r"'rule': '([^']+)'", line)
    if m:
        r = m.group(1)
        counts[r] = counts.get(r, 0) + 1
for r, n in sorted(counts.items()):
    print(f"{n:3}  {r}")
if not counts:
    print("No violations found")
