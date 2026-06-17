import pathlib
p = pathlib.Path(r"c:\dev\agilebydesign-skills\skills\abd-story-mapping\SKILL.md")
text = p.read_text(encoding="utf-8")
for line in text.split("\n"):
    if "fabricate" in line:
        print("prefix codepoints:", [hex(ord(c)) for c in line[:30]])
    if "incomplete" in line and "fabricate" in text[text.find(line)-200:text.find(line)+10]:
        pass
# show dash in incomplete line
for line in text.split("\n"):
    if "incomplete" in line and "business rule" in line:
        for ch in line:
            if ord(ch) > 127:
                print("non-ascii:", hex(ord(ch)), repr(ch))
