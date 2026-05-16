path = r'C:\dev\agilebydesign-skills\skills\story-driven-delivery\abd-acceptance-criteria\SKILL.md'
content = open(path, encoding='utf-8').read()

old = (
    '- **Non-negotiable before writing any Domain terms section:** every term must already exist in a domain model artifact '
    '(ubiquitous language, CRC, or object model). If a term is not found in any artifact, **flag it in your output and ask '
    'the user how to proceed** (add to UL, skip, use an existing term, etc.) before including it in AC. Only create '
    '`domain-terms.md` when no domain model artifact exists at all for the engagement. '
    'See rule **Domain terms must come from the domain model**.'
)
new = (
    '- **Non-negotiable before writing any Domain terms section:** every term must already exist in a domain source artifact '
    '(ubiquitous language, domain sketch, CRC, object model, or any team-designated vocabulary file). '
    'If a term is missing, **stop — list every missing term and ask the user how to proceed** before writing it into AC. '
    '**NEVER create `domain-terms.md` if any domain source file already exists.** '
    'Only use `domain-terms.md` as a bootstrap when the engagement has no domain sources at all. '
    'See rule **Domain terms must come from the domain model**.'
)

if old in content:
    content = content.replace(old, new, 1)
    open(path, 'w', encoding='utf-8').write(content)
    print('replaced OK')
else:
    idx = content.find('Non-negotiable before writing')
    print('NOT FOUND, nearby:')
    print(repr(content[idx:idx+500]))
