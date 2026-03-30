#!/usr/bin/env python3
"""
validate_skill.py — Validates a Claude Code skill's SKILL.md structure.

Checks frontmatter, required sections, cross-references, line count,
and common anti-patterns. Returns exit code 0 on success, 1 on failure.

Usage:
    python validate_skill.py <skill-directory>
    python validate_skill.py .claude/skills/api-debugger
    python validate_skill.py --all  # validate all skills
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Collects validation errors and warnings."""
    skill_name: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    def add_info(self, msg: str):
        self.info.append(msg)

    def print_report(self):
        status = "PASS" if self.passed else "FAIL"
        print(f"\n{'=' * 60}")
        print(f"  Skill: {self.skill_name}  [{status}]")
        print(f"{'=' * 60}")

        if self.info:
            for msg in self.info:
                print(f"  INFO: {msg}")

        if self.warnings:
            print()
            for msg in self.warnings:
                print(f"  WARNING: {msg}")

        if self.errors:
            print()
            for msg in self.errors:
                print(f"  ERROR: {msg}")

        if self.passed and not self.warnings:
            print(f"  All checks passed.")

        print()


def find_git_root() -> Path:
    """Walk up from cwd to find the nearest .git directory."""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Not inside a git repository.", file=sys.stderr)
        sys.exit(1)


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from SKILL.md content."""
    frontmatter = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            body = parts[2].strip()

            for line in fm_text.split("\n"):
                line = line.strip()
                if ":" in line and not line.startswith("#"):
                    key, _, value = line.partition(":")
                    key = key.strip()
                    value = value.strip()
                    if key in frontmatter:
                        # Multi-line value continuation
                        frontmatter[key] += " " + value
                    else:
                        frontmatter[key] = value
                elif line and not line.startswith("-") and not line.startswith("#"):
                    # Continuation of previous value
                    if frontmatter:
                        last_key = list(frontmatter.keys())[-1]
                        frontmatter[last_key] += " " + line

    return frontmatter, body


def extract_headings(body: str) -> list[tuple[int, str]]:
    """Extract all markdown headings with their levels."""
    headings = []
    for line in body.split("\n"):
        match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            headings.append((level, title))
    return headings


def extract_references(body: str) -> list[str]:
    """Find all file references in backticks (references/*.md, scripts/*.py)."""
    refs = []
    # Match references like `references/file.md` or `scripts/file.py`
    for match in re.finditer(r'`((?:references|scripts|assets)/[^`]+)`', body):
        refs.append(match.group(1))
    return refs


def extract_skill_refs(body: str) -> list[str]:
    """Find cross-references to other skills (backtick-quoted skill names)."""
    # Match patterns like `skill-name` that look like skill references
    refs = []
    for match in re.finditer(r'`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`', body):
        candidate = match.group(1)
        # Filter out things that look like file paths or code
        if "/" not in candidate and "." not in candidate:
            refs.append(candidate)
    return refs


def validate_frontmatter(frontmatter: dict, result: ValidationResult):
    """Validate YAML frontmatter fields."""
    if not frontmatter:
        result.error("Missing frontmatter (--- delimited YAML block)")
        return

    # Check name
    if "name" not in frontmatter:
        result.error("Frontmatter missing 'name' field")
    else:
        name = frontmatter["name"]
        if not re.match(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$', name):
            result.error(f"Invalid skill name '{name}' — must be lowercase-with-hyphens")

    # Check description
    if "description" not in frontmatter:
        result.error("Frontmatter missing 'description' field")
    else:
        desc = frontmatter["description"]
        # Remove the > indicator for multi-line YAML
        desc = desc.lstrip(">").strip()
        if len(desc) < 50:
            result.warn(f"Description is short ({len(desc)} chars) — consider adding trigger keywords")

        # Check for trigger guidance
        trigger_words = ["use this skill", "trigger", "when", "keyword"]
        has_trigger = any(w in desc.lower() for w in trigger_words)
        if not has_trigger:
            result.warn("Description doesn't include trigger guidance — skills may undertrigger")


def validate_structure(body: str, headings: list[tuple[int, str]], result: ValidationResult):
    """Validate SKILL.md body structure."""
    heading_titles = [h[1].lower() for _, h in enumerate(headings) if True for h in [headings[_]]]
    heading_titles = [title.lower() for _, title in headings]

    # Check for H1 title
    h1_count = sum(1 for level, _ in headings if level == 1)
    if h1_count == 0:
        result.error("Missing H1 title (# Title)")
    elif h1_count > 1:
        result.warn(f"Multiple H1 headings found ({h1_count}) — prefer a single top-level title")

    # Check for recommended sections
    recommended = {
        "when to use": "Scope boundaries help prevent over/under-triggering",
        "workflow": "Step-by-step process guides consistent execution",
        "examples": "Concrete examples are the most effective teaching tool",
    }

    for section, reason in recommended.items():
        found = any(section in title for title in heading_titles)
        if not found:
            result.warn(f"Missing recommended section '{section}' — {reason}")

    # Check for output format or template
    has_output = any(
        term in title
        for title in heading_titles
        for term in ["output", "format", "template", "deliverable"]
    )
    if not has_output:
        result.warn("No 'Output Format' section — define expected deliverables for consistency")

    # Check for edge cases
    has_edges = any("edge" in title or "gotcha" in title for title in heading_titles)
    if not has_edges:
        result.warn("No 'Edge Cases' section — document common gotchas")


def validate_content_quality(body: str, result: ValidationResult):
    """Check for content quality anti-patterns."""
    lines = body.split("\n")
    line_count = len(lines)

    result.add_info(f"Body: {line_count} lines")

    if line_count > 500:
        result.warn(f"SKILL.md body is {line_count} lines — consider moving detail to references/")

    # Check for ALWAYS/NEVER without reasoning
    for i, line in enumerate(lines, 1):
        # Look for ALL CAPS directives
        if re.search(r'\b(ALWAYS|NEVER|MUST NOT|DO NOT)\b', line):
            # Check if the next few lines provide reasoning
            context = "\n".join(lines[i:i+3]) if i < len(lines) else ""
            has_reasoning = any(
                word in context.lower()
                for word in ["because", "since", "reason", "why", "this ensures", "this prevents"]
            )
            if not has_reasoning:
                result.warn(
                    f"Line {i}: ALL-CAPS directive without reasoning — "
                    f"add 'because...' to help the model internalize the rule"
                )
                break  # Only report once

    # Check for examples
    example_count = len(re.findall(r'(?i)\b(example|input.*output|before.*after)\b', body))
    if example_count < 2:
        result.warn("Fewer than 2 examples found — concrete examples improve skill quality")

    # Check for code blocks
    code_blocks = len(re.findall(r'```', body)) // 2
    if code_blocks > 0:
        result.add_info(f"Contains {code_blocks} code block(s)")


def validate_references(
    skill_dir: Path,
    body: str,
    result: ValidationResult
):
    """Validate that referenced files exist."""
    file_refs = extract_references(body)

    for ref in file_refs:
        ref_path = skill_dir / ref
        if not ref_path.exists():
            result.error(f"Referenced file does not exist: {ref}")
        else:
            result.add_info(f"Reference OK: {ref}")

    # Check for skill cross-references
    skill_refs = extract_skill_refs(body)
    if skill_refs:
        git_root = find_git_root()
        skills_dir = git_root / ".claude" / "skills"
        for skill_ref in skill_refs:
            skill_path = skills_dir / skill_ref
            if not skill_path.exists():
                result.warn(f"Cross-referenced skill '{skill_ref}' not found in {skills_dir}")
            elif not (skill_path / "SKILL.md").exists():
                result.warn(f"Cross-referenced skill '{skill_ref}' exists but has no SKILL.md")
            else:
                result.add_info(f"Skill cross-reference OK: {skill_ref}")


def validate_skill(skill_dir: Path) -> ValidationResult:
    """Run all validations on a skill directory."""
    skill_name = skill_dir.name
    result = ValidationResult(skill_name=skill_name)

    # Check SKILL.md exists
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        result.error(f"SKILL.md not found in {skill_dir}")
        return result

    # Read content
    content = skill_md.read_text(encoding="utf-8")
    result.add_info(f"Total: {len(content.splitlines())} lines, {len(content)} chars")

    # Parse
    frontmatter, body = parse_frontmatter(content)
    headings = extract_headings(body)

    # Run validations
    validate_frontmatter(frontmatter, result)
    validate_structure(body, headings, result)
    validate_content_quality(body, result)
    validate_references(skill_dir, body, result)

    # Check directory structure
    subdirs = [d.name for d in skill_dir.iterdir() if d.is_dir()]
    valid_subdirs = {"scripts", "references", "assets", "evals"}
    unexpected = set(subdirs) - valid_subdirs
    if unexpected:
        result.warn(f"Unexpected subdirectories: {', '.join(unexpected)}")

    if subdirs:
        result.add_info(f"Subdirectories: {', '.join(sorted(subdirs))}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Validate a Claude Code skill's SKILL.md structure"
    )
    parser.add_argument(
        "skill_dir",
        nargs="?",
        help="Path to the skill directory to validate"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Validate all skills in .claude/skills/"
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Treat warnings as errors"
    )

    args = parser.parse_args()

    if args.all:
        git_root = find_git_root()
        skills_dir = git_root / ".claude" / "skills"
        if not skills_dir.exists():
            print("No skills directory found.", file=sys.stderr)
            sys.exit(1)

        results = []
        for skill_path in sorted(skills_dir.iterdir()):
            if skill_path.is_dir() and (skill_path / "SKILL.md").exists():
                results.append(validate_skill(skill_path))

        if not results:
            print("No skills found to validate.")
            sys.exit(0)

        # Print all reports
        for r in results:
            r.print_report()

        # Summary
        passed = sum(1 for r in results if r.passed)
        failed = len(results) - passed
        total_warnings = sum(len(r.warnings) for r in results)

        print(f"{'=' * 60}")
        print(f"  Summary: {passed}/{len(results)} passed, "
              f"{failed} failed, {total_warnings} warnings")
        print(f"{'=' * 60}")

        if args.strict:
            has_warnings = any(r.warnings for r in results)
            sys.exit(1 if failed > 0 or has_warnings else 0)
        sys.exit(1 if failed > 0 else 0)

    elif args.skill_dir:
        skill_path = Path(args.skill_dir)
        if not skill_path.is_absolute():
            skill_path = Path.cwd() / skill_path

        result = validate_skill(skill_path)
        result.print_report()

        if args.strict and result.warnings:
            sys.exit(1)
        sys.exit(0 if result.passed else 1)

    else:
        parser.error("Provide a skill directory path or use --all")


if __name__ == "__main__":
    main()
