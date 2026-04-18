#!/usr/bin/env python3
"""
build_domain_scan_diagram.py

Parse domain-scan-model.md and build the diagram using drawio_cli.py with
field-level exit/entry anchoring for all composition relationships.

Usage:
    python3 build_domain_scan_diagram.py --md domain-scan-model.md --out domain-scan-model.drawio
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def parse_md(md_path):
    """Parse the domain-scan MD file and return structured data.

    Returns:
        {
            'classes': {
                'ClassName': {
                    'stereotype': 'scan',
                    'module': 'ModuleName',
                    'fields': [
                        {'name': 'powerLevel', 'type': 'int', 'multiplicity': None},
                        {'name': 'abilities', 'type': 'Ability', 'multiplicity': '[1..*]'},
                        ...
                    ],
                    'invariants': [
                        { constraint text },
                        ...
                    ]
                },
                ...
            },
            'relationships': [
                {
                    'type': 'composition',  # or 'association'
                    'source': 'ClassName',
                    'target': 'ClassName',
                    'source_field': 'abilities: Ability [1..*]',  # full field declaration
                    'multiplicity': '1..*',
                    'field_key': 'abilities',  # key for matching field row
                },
                ...
            ]
        }
    """
    content = Path(md_path).read_text(encoding='utf-8')
    lines = content.split('\n')

    classes = {}
    relationships = []
    current_class = None
    current_module = None

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1

        # Skip empty and comment lines
        if not line or line.startswith('_') or line.startswith('#'):
            continue

        # Module header: ## [ModuleName module]
        if line.startswith('## [') and 'module]' in line:
            current_module = line.replace('## [', '').replace(' module]', '').strip()
            continue

        # Class header: ClassName : <<scan>>
        if ':' in line and '<<scan>>' in line:
            class_name = line.split(':')[0].strip()
            current_class = class_name
            classes[current_class] = {
                'stereotype': 'scan',
                'module': current_module,
                'fields': [],
                'invariants': [],
            }
            continue

        # Skip divider line (-----)
        if line.startswith('-----'):
            current_class = None
            continue

        # Process fields and invariants if we're in a class
        if current_class and current_class in classes:
            # Field: + fieldName: Type
            if line.startswith('+ '):
                # Extract field declaration
                field_decl = line[2:].strip()  # Remove '+ '
                classes[current_class]['fields'].append({
                    'declaration': field_decl,
                })

            # Invariant: { ... }
            elif line.startswith('{') and line.endswith('}'):
                invariant_text = line[1:-1].strip()
                classes[current_class]['invariants'].append({
                    'text': invariant_text,
                })

    # Build relationships from fields
    for class_name, class_info in classes.items():
        for field in class_info['fields']:
            decl = field['declaration']
            # Parse: fieldName: TargetClass [multiplicity]
            # Examples:
            #   abilities: Ability [1..*]
            #   skills: Skill [0..*]
            #   ability: Ability
            #   powerPoints: int

            # Try to match: name: Type [mult]
            match = re.match(r'(\w+):\s+(\w+)\s*(\[[^\]]*\])?', decl)
            if not match:
                continue

            field_name = match.group(1)
            type_name = match.group(2)
            mult = match.group(3) or ''

            # Skip scalar types (primitives)
            if type_name.lower() in ('int', 'string', 'bool', 'float', 'double'):
                continue

            # Skip if target type doesn't exist as a class
            if type_name not in classes:
                continue

            # This is a reference to another class
            # Composition: the field is a reference inside the source class
            relationships.append({
                'type': 'composition',
                'source': type_name,          # The referenced class
                'target': class_name,         # The class that declares the field
                'source_field': None,         # No field in the source
                'entry_field': decl,          # Field in target where arrow enters
                'multiplicity': mult.strip('[]') if mult else '1',
            })

    return {
        'classes': classes,
        'relationships': relationships,
    }


def cli_call(cmd_parts, diagram_path):
    """Call drawio_cli.py with the given command parts.

    Note: --file must come before the command.
    """
    full_cmd = (
        ['python3', str(Path(__file__).parent / 'drawio_cli.py'), '--file', str(diagram_path)]
        + cmd_parts
    )
    result = subprocess.run(full_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return False
    print(result.stdout.strip())
    return True


def build_diagram(md_path, out_path):
    """Build the diagram from the MD file."""
    # Parse the MD
    data = parse_md(md_path)
    classes = data['classes']
    relationships = data['relationships']

    out_path = Path(out_path)

    # Create a new diagram
    print(f"Creating new diagram: {out_path}")
    cli_call(['new'], out_path)

    # Add all classes with explicit positions (following Part B layout spec)
    # Character module: Character centered over 6 children
    # Children in 2 rows: Ability, Skill, HeroPoint (top row); Advantage, Power, Complication (bottom row)
    # Effect/Modifier modules to the right

    positions = {
        # Character module (centered over 6 children)
        # Row 1: Ability (50, 380), Skill (260, 380), HeroPoint (470, 380)
        # Row 2: Advantage (50, 560), Power (260, 560), Complication (470, 560)
        # Character center x = 50 + 305 = 355, width=280, so x = 215
        'Character': (215, 100),

        # Row 1 (y=380) - 3 children spaced 190px wide, 20px gaps
        'Ability': (50, 380),
        'Skill': (260, 380),
        'HeroPoint': (470, 380),

        # Row 2 (y=560)
        'Advantage': (50, 560),
        'Power': (260, 560),
        'Complication': (470, 560),

        # Check module - far right, row 1 level
        'Check': (800, 380),

        # Condition module - far right, row 2 level
        'Condition': (800, 560),

        # Effect module - below Character center, offset left
        'Effect': (100, 780),
        'Modifier': (320, 780),
    }

    for class_name, class_info in sorted(classes.items()):
        x, y = positions.get(class_name, (100, 100))
        if not cli_call(['add-class', class_name, '--x', str(x), '--y', str(y)], out_path):
            return False

    # Add fields and invariants
    for class_name, class_info in sorted(classes.items()):
        for field in class_info['fields']:
            decl = field['declaration']
            if not cli_call(['add-field', class_name, f'+ {decl}'], out_path):
                return False

        for invariant in class_info['invariants']:
            if not cli_call(['add-field', class_name, f'{{ {invariant["text"]} }}'], out_path):
                return False

    # Add module frames
    # Character module
    if not cli_call(['add-frame', 'Character', '--classes',
                     'Character,Ability,Skill,HeroPoint,Advantage,Power,Complication'],
                    out_path):
        return False

    # Check module
    if 'Check' in classes:
        if not cli_call(['add-frame', 'Check', '--classes', 'Check'], out_path):
            return False

    # Condition module
    if 'Condition' in classes:
        if not cli_call(['add-frame', 'Condition', '--classes', 'Condition'], out_path):
            return False

    # Effect module
    if 'Effect' in classes:
        classes_in_effect = ['Effect']
        if 'Modifier' in classes:
            classes_in_effect.append('Modifier')
        if not cli_call(['add-frame', 'Effect', '--classes', ','.join(classes_in_effect)], out_path):
            return False

    # Add relationships
    for rel in relationships:
        if rel['type'] == 'composition':
            cmd = [
                'add-composition',
                rel['target'],  # whole
                rel['source'],  # part
                '--mult', rel['multiplicity'],
            ]
            if rel['entry_field']:
                cmd.extend(['--entry-field', rel['entry_field']])
            if not cli_call(cmd, out_path):
                return False

    # Fix edge styles
    print("Fixing edge styles...")
    if not cli_call(['fix-edge-styles'], out_path):
        return False

    # Fix shared endpoints
    print("Fixing shared endpoints...")
    if not cli_call(['fix-shared-endpoints'], out_path):
        return False

    # Fix arrow overlaps
    print("Fixing arrow overlaps...")
    if not cli_call(['fix-arrow-overlaps'], out_path):
        return False

    # Verify
    print("Verifying diagram...")
    if not cli_call(['verify'], out_path):
        return False

    print(f"\nDiagram built successfully: {out_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description='Build domain-scan diagram from MD')
    parser.add_argument('--md', required=True, help='Path to domain-scan-model.md')
    parser.add_argument('--out', required=True, help='Path to output .drawio file')
    args = parser.parse_args()

    if not build_diagram(args.md, args.out):
        sys.exit(1)


if __name__ == '__main__':
    main()
