import re
from pathlib import Path

path = Path(
    r"c:\dev\agilebydesign-skills\skills\abd-ooad\content\parts\phases\nouns-verbs-rules-and-states.md"
)
s = path.read_text(encoding="utf-8")


def fix(m):
    return "**" + m.group(1) + "**"


pattern = r"`\*\*([^`]+?)\*\*`"
count_before = len(re.findall(pattern, s))
s2 = re.sub(pattern, fix, s)
count_after = len(re.findall(pattern, s2))
path.write_text(s2, encoding="utf-8", newline="\n")
print(f"fixed {count_before} -> remaining {count_after}")

# verify sample
sample = "foo `**domain-noun-verb.md`** bar"
print("sample:", re.sub(pattern, fix, sample))
