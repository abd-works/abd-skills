path = r'C:\dev\agilebydesign-skills\skills\story-driven-delivery\abd-acceptance-criteria\SKILL.md'
content = open(path, encoding='utf-8').read()

old = (
    '- **Non-negotiable before writing any Domain terms section:** every term must already exist in a domain model artifact '
    '(ubiquitous language, CRC, or object model). If a term is missing from all artifacts, add it to `domain-terms.md` in '
    'the deliverables folder first. See rule **Domain terms must come from the domain model**.'
)
new = (
    '- **Non-negotiable before writing any Domain terms section:** every term must already exist in a domain model artifact '
    '(ubiquitous language, CRC, or object model). If a term is not found in any artifact, **flag it in your output and ask '
    'the user how to proceed** (add to UL, skip, use an existing term, etc.) before including it in AC. Only create '
    '`domain-terms.md` when no domain model artifact exists at all for the engagement. '
    'See rule **Domain terms must come from the domain model**.'
)

if old in content:
    content = content.replace(old, new, 1)
    open(path, 'w', encoding='utf-8').write(content)
    print('replaced OK')
else:
    # show the actual line for debugging
    idx = content.find('Non-negotiable before writing')
    print('NOT FOUND, nearby text:')
    print(repr(content[idx:idx+400]))
