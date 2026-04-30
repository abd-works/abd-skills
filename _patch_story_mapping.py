import pathlib
p = pathlib.Path(r"c:\dev\agilebydesign-skills\skills\abd-story-mapping\SKILL.md")
text = p.read_text(encoding="utf-8")
em = "\u2014"
old = (
    "that turns out to be wrong.\n\n"
    "### Recording context gaps in the story map"
)
new_paras = (
    f"that turns out to be wrong.\n\n"
    "**Don't defer analysis the source material supports.** If the source describes how a workflow or entity type works, map it now {em} don't write \"not yet mapped\" as a gap. Gaps are for missing information, not unfinished work.\n\n"
    "**Don't add scope the user didn't ask for.** If the user describes one path (e.g., manual onboarding), don't add a second (e.g., self-service onboarding) and present it as part of the map. When a choice exists, ask.\n\n"
    "### Recording context gaps in the story map"
)
if old not in text:
    raise SystemExit("anchor not found")
text = text.replace(old, new_paras, 1)
p.write_text(text, encoding="utf-8", newline="\n")
print("OK: inserted paragraphs")
