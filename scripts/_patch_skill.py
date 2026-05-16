import sys

path = r'C:\dev\agilebydesign-skills\skills\story-driven-delivery\abd-acceptance-criteria\SKILL.md'
content = open(path, encoding='utf-8').read()

old_snip = (
    '2. **Rules**\n'
    '- Generate content following rules attached to this skill, listed below, assembled from rule files in `rules/`.\n'
    '- Validate - once content is generated, take on the role of a *Peer Reviewer*  and validate that the content is correct by going through each of the skills rules one at a time and looking deeply for violations. Be helpful but critccal - compare contenct againstg each rules constraints, DO/DON\u2019T sections and examples.'
)

new_snip = (
    '2. **Rules**\n'
    '- Generate content following rules attached to this skill, listed below, assembled from rule files in `rules/`.\n'
    '- **Non-negotiable before writing any Domain terms section:** every term must already exist in a domain model artifact (ubiquitous language, CRC, or object model). If a term is missing from all artifacts, add it to `domain-terms.md` in the deliverables folder first. See rule **Domain terms must come from the domain model**.\n'
    "- Validate \u2014 once content is generated, take on the role of a *Peer Reviewer* and validate the content against each rule's DO/DON'T constraints and examples."
)

if old_snip in content:
    content = content.replace(old_snip, new_snip, 1)
    open(path, 'w', encoding='utf-8').write(content)
    print('replaced OK')
else:
    print('NOT FOUND')
    idx = content.find('Validate - once content')
    print(repr(content[idx:idx+300]))
