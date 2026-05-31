import subprocess, re, sys

result = subprocess.run(
    [sys.executable,
     r"c:\dev\abd-pet-store-demo\.cursor\skills\execute-skill-using-skills-rules\scripts\run_scanners.py",
     "--skill-root", r"c:\dev\abd-pet-store-demo\.cursor\skills\abd-ubiquitous-language",
     "--workspace", r"c:\dev\abd-works\abd-delivery-agent-kanban\docs\domain"],
    capture_output=True, text=True, cwd=r"c:\dev\abd-pet-store-demo"
)
output = result.stdout + result.stderr
print(repr(output[:500]))
