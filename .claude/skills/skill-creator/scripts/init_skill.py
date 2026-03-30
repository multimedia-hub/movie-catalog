#!/usr/bin/env python3
"""
init_skill.py — Scaffolds a new Claude Code skill directory.

Creates a skill directory with a template SKILL.md, optional scripts/
and references/ subdirectories, and validates naming conventions.

Usage:
    python init_skill.py <skill-name> [--with-scripts] [--with-references] [--with-assets]

The script auto-detects the .git root and places skills in .claude/skills/.
"""

import argparse
import os
import subprocess
import sys
import re
from pathlib import Path


def find_git_root() -> Path:
    """Walk up from cwd to find the nearest .git directory."""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    # Fallback: try git rev-parse
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Not inside a git repository.", file=sys.stderr)
        sys.exit(1)


def validate_skill_name(name: str) -> bool:
    """
    Validate skill name follows conventions:
    - Lowercase letters, numbers, hyphens only
    - Must start with a letter
    - No consecutive hyphens
    - Between 3 and 40 characters
    """
    if not re.match(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$', name):
        return False
    if len(name) < 3 or len(name) > 40:
        return False
    return True


SKILL_TEMPLATE = '''---
name: {name}
description: >
  [What this skill does — be specific about capabilities].
  Use this skill when [trigger phrase 1], [trigger phrase 2],
  [trigger phrase 3], or [broader context description].
  Trigger keywords: [keyword1], [keyword2], [keyword3].
---

# {title}

[1-2 sentence overview of what this skill accomplishes and why it matters.]

## When to Use

**In scope:**
- [Primary use case]
- [Secondary use case]
- [Edge case that should still trigger]

**Out of scope (use these skills instead):**
- [Excluded task] → use `[other-skill-name]`
- [Another excluded task] → use `[another-skill-name]`

## Key Rules

1. **[Rule name]** — [Instruction with WHY reasoning].
   Because [explanation of why this matters].

2. **[Rule name]** — [Instruction with WHY reasoning].
   Because [explanation of why this matters].

## Workflow

### Step 1: [Understand the Request]
[Instructions for gathering context]

### Step 2: [Plan the Approach]
[Instructions for determining the right strategy]

### Step 3: [Execute]
[Instructions for doing the work]

### Step 4: [Validate]
[Quality checks before presenting output]

## Output Format

[Explicit template or structure definition for deliverables]

## Examples

**Example 1: [Scenario name]**
Input: [realistic input]
Output: [expected output]

**Example 2: [Different scenario]**
Input: [realistic input]
Output: [expected output]

## Edge Cases

- **[Edge case 1]** — [How to handle it and why]
- **[Edge case 2]** — [How to handle it and why]

## References

- For [topic], read `references/[file].md`
'''


def create_skill(
    name: str,
    with_scripts: bool = False,
    with_references: bool = False,
    with_assets: bool = False,
    force: bool = False
) -> Path:
    """Create a new skill directory with template files."""
    git_root = find_git_root()
    skills_dir = git_root / ".claude" / "skills"
    skill_dir = skills_dir / name

    if skill_dir.exists() and not force:
        print(f"Error: Skill directory already exists: {skill_dir}", file=sys.stderr)
        print("Use --force to overwrite.", file=sys.stderr)
        sys.exit(1)

    # Create skill directory
    skill_dir.mkdir(parents=True, exist_ok=True)

    # Generate title from name
    title = name.replace("-", " ").title()

    # Write SKILL.md
    skill_md = skill_dir / "SKILL.md"
    content = SKILL_TEMPLATE.format(name=name, title=title)
    skill_md.write_text(content, encoding="utf-8")
    print(f"  Created: {skill_md.relative_to(git_root)}")

    # Create optional directories
    if with_scripts:
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        # Create a placeholder script
        placeholder = scripts_dir / "__init__.py"
        placeholder.write_text("# Skill scripts\n", encoding="utf-8")
        print(f"  Created: {scripts_dir.relative_to(git_root)}/")

    if with_references:
        refs_dir = skill_dir / "references"
        refs_dir.mkdir(exist_ok=True)
        print(f"  Created: {refs_dir.relative_to(git_root)}/")

    if with_assets:
        assets_dir = skill_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        print(f"  Created: {assets_dir.relative_to(git_root)}/")

    return skill_dir


def list_existing_skills(git_root: Path) -> list[str]:
    """List all existing skill directories."""
    skills_dir = git_root / ".claude" / "skills"
    if not skills_dir.exists():
        return []
    return sorted([
        d.name for d in skills_dir.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    ])


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new Claude Code skill directory"
    )
    parser.add_argument(
        "name",
        nargs="?",
        help="Skill name (lowercase-with-hyphens, e.g. 'api-debugger')"
    )
    parser.add_argument(
        "--with-scripts", action="store_true",
        help="Create a scripts/ subdirectory"
    )
    parser.add_argument(
        "--with-references", action="store_true",
        help="Create a references/ subdirectory"
    )
    parser.add_argument(
        "--with-assets", action="store_true",
        help="Create an assets/ subdirectory"
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Overwrite existing skill directory"
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List existing skills and exit"
    )

    args = parser.parse_args()

    git_root = find_git_root()

    if args.list:
        skills = list_existing_skills(git_root)
        if skills:
            print(f"Found {len(skills)} skills:")
            for s in skills:
                print(f"  - {s}")
        else:
            print("No skills found.")
        return

    if not args.name:
        parser.error("Skill name is required (or use --list)")

    if not validate_skill_name(args.name):
        print(f"Error: Invalid skill name '{args.name}'.", file=sys.stderr)
        print("Rules: lowercase letters/numbers/hyphens, start with letter,", file=sys.stderr)
        print("       no consecutive hyphens, 3-40 characters.", file=sys.stderr)
        sys.exit(1)

    print(f"Creating skill: {args.name}")
    skill_dir = create_skill(
        args.name,
        with_scripts=args.with_scripts,
        with_references=args.with_references,
        with_assets=args.with_assets,
        force=args.force
    )
    print(f"\nSkill created at: {skill_dir.relative_to(git_root)}")
    print(f"\nNext steps:")
    print(f"  1. Edit {skill_dir.relative_to(git_root)}/SKILL.md")
    print(f"  2. Fill in the description, triggers, and workflow")
    print(f"  3. Run validate_skill.py to check structure")


if __name__ == "__main__":
    main()
