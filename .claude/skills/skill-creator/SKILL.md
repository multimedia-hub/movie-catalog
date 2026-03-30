---
name: skill-creator
description: >
  Expert skill for creating, designing, and iterating on Claude Code skills.
  Use this skill whenever the user mentions "skill", "create a skill", "build a skill",
  "new skill", "SKILL.md", "make Claude better at X", "teach Claude to do X",
  "automate this workflow as a skill", "turn this into a skill", or wants to
  capture any repeatable workflow into a reusable skill. Also trigger when the user
  wants to improve, test, evaluate, or debug an existing skill. Even if they just say
  "I want Claude to always do X" — that's a skill request.
---

# Skill Creator — Claude Code Expert

You are an expert at designing, writing, testing, and iterating on Claude Code skills. A skill is a reusable set of instructions (primarily a `SKILL.md` file) that teaches Claude how to perform a specific task with high quality and consistency.

## When to Use

**In scope:**
- Creating new skills from scratch or from observed workflows
- Upgrading or iterating on existing skills
- Designing skill system architecture (categories, cross-references)
- Writing evals and test prompts for skills
- Validating skill structure with `scripts/validate_skill.py`
- Scaffolding new skill directories with `scripts/init_skill.py`

**Out of scope (use these skills instead):**
- Building Azure Functions endpoints → use `api-endpoint-builder`
- Implementing signal types in the frontend → use `hub-signal-implementer`
- Writing tests for existing code → use `api-tester` or `hub-tester`
- Managing Azure infrastructure → use `azure-manager`
- Coordinating multi-step feature work → use `project-manager`

For comprehensive guidance on designing an entire skill system (categories, layering, discovery), see `.claude/CREATE_SKILL_SYSTEM.md`.

## What Makes a Great Skill

A great skill is one that a million different users could trigger with a million different prompts and get consistently excellent results. It generalizes well, explains the *why* behind every instruction, and stays lean — no dead weight.

## Skill Anatomy

```
skill-name/
├── SKILL.md              # Required — main instructions
├── scripts/              # Optional — deterministic helpers (Python, Bash)
├── references/           # Optional — docs loaded on demand for detail
└── assets/               # Optional — templates, fonts, icons, images
```

Do NOT create README.md, CHANGELOG.md, or INSTALLATION_GUIDE.md. Skills are for AI agents, not human onboarding.

---

## Local Environment Context

This project has **27 existing skills** organized into distinct layers:

### Backend API (4 skills)
| Skill | Purpose |
|-------|---------|
| `api-debugger` | Debug pipeline errors, decorator chains, signal calculations |
| `api-endpoint-builder` | Create Azure Functions HTTP trigger endpoints |
| `api-pipeline-developer` | Implement Durable Functions activities and decorator chains |
| `api-tester` | Write xUnit tests with FluentAssertions and Moq |

### Frontend Hub (4 skills)
| Skill | Purpose |
|-------|---------|
| `hub-signal-implementer` | Scaffold all frontend files for new signal types |
| `hub-chart-builder` | Build chart views with TradingView Lightweight Charts v5 |
| `hub-auth-subscription` | Handle auth, subscriptions, and feature gating |
| `hub-tester` | Write Vitest, Playwright, and Testing Library tests |

### Orchestration (3 skills)
| Skill | Purpose |
|-------|---------|
| `project-manager` | Analyze requirements, create ordered implementation plans |
| `signal-sync` | Detect and resolve C# ↔ Zod schema drift |
| `azure-manager` | Manage Azure resources (deploy, configure, monitor) |

### Standards (15 skills)
Lightweight reference pointers (~13 lines each) to `agent-os/standards/`:
- **Backend:** `backend-api`, `backend-migrations`, `backend-models`, `backend-queries`
- **Frontend:** `frontend-accessibility`, `frontend-components`, `frontend-css`, `frontend-responsive`
- **Global:** `global-coding-style`, `global-commenting`, `global-conventions`, `global-error-handling`, `global-tech-stack`, `global-validation`
- **Testing:** `testing-test-writing`

### Meta (1 skill)
| Skill | Purpose |
|-------|---------|
| `skill-creator` | This skill — create, design, and iterate on skills |

When creating new skills, place them in the appropriate category and establish cross-references to existing skills.

---

## Creating a New Skill

### Quick Start: Scaffolding

Use the init script to create a new skill directory with a template SKILL.md:

```bash
python .claude/skills/skill-creator/scripts/init_skill.py my-new-skill --with-references
```

Options: `--with-scripts`, `--with-references`, `--with-assets`, `--force`, `--list`

### Phase 1: Capture Intent

Start by understanding what the user wants. Ask these questions (skip any already answered from context):

1. **What should this skill enable Claude to do?** — Get a concrete description of the task.
2. **When should it trigger?** — What phrases, file types, or contexts should activate it.
3. **What's the expected output?** — File type, format, structure, quality bar.
4. **Are there edge cases or gotchas?** — Things that commonly go wrong.
5. **Should we set up test cases?** — Skills with objectively verifiable outputs (file transforms, data extraction, code generation) benefit from evals. Subjective outputs (writing style, creative work) often don't.

If the conversation already contains a workflow the user wants to capture (e.g., "turn this into a skill"), extract answers from the conversation history first — the tools used, the sequence of steps, corrections the user made, input/output patterns observed. Confirm with the user before proceeding.

### Phase 2: Design the Skill Structure

Decide what goes where:

- **SKILL.md body** (< 500 lines ideal): Core workflow, decision logic, output format, examples. This is loaded into context when the skill triggers, so keep it focused.
- **references/**: Detailed docs for specific domains, frameworks, or edge cases. Only loaded when needed. For large files (> 300 lines), include a table of contents.
- **scripts/**: Deterministic or repetitive tasks — file parsing, validation, template generation, data transforms. Scripts can execute without being loaded into context.
- **assets/**: Templates, fonts, images, or other static files used in output.

**Domain organization** — when a skill supports multiple variants:
```
cloud-deploy/
├── SKILL.md            # Workflow + variant selection logic
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude reads only the relevant reference file based on context.

### Phase 3: Write the SKILL.md

#### Frontmatter (YAML)

```yaml
---
name: skill-name
description: >
  Clear description of what the skill does AND when to trigger it.
  Be slightly "pushy" — Claude tends to undertrigger skills, so include
  specific contexts, keywords, file types, and user phrases that should
  activate this skill. Example: "Use this skill whenever the user mentions
  dashboards, data visualization, internal metrics, or wants to display
  any kind of data, even if they don't explicitly ask for a 'dashboard'."
---
```

The `description` field is the primary triggering mechanism. All "when to use" info goes here, not in the body.

#### Body — Writing Principles

1. **Explain the WHY behind instructions.** Today's LLMs are smart — they have good theory of mind and can go beyond rote instructions when they understand the reasoning. Instead of "ALWAYS use semantic HTML", write "Use semantic HTML because it improves accessibility and SEO, and screen readers depend on it for navigation." If you find yourself writing ALWAYS or NEVER in all caps, that's a yellow flag — reframe with reasoning.

2. **Use imperative form.** "Check the file extension", "Parse the CSV header", "Validate the output against the schema."

3. **Include concrete examples.** Show expected input → output patterns. This is often the single most effective way to communicate what you want:
   ```markdown
   ## Example: New endpoint skill trigger
   Input: "I need a GET endpoint that returns paginated stock signals"
   Output: Creates Azure Function with HTTP trigger, pagination params,
   Zod schema, and unit test following `api-endpoint-builder` patterns.
   ```

4. **Define "When to Use / Out of scope" explicitly.** Every skill should clearly state what triggers it and, crucially, what does NOT trigger it — with pointers to the correct skill for excluded tasks. This prevents both over-triggering and confusion between similar skills.

5. **Keep it lean.** Every line should earn its place. If an instruction isn't improving outcomes, remove it. Read transcripts of the skill in action — if Claude wastes time on unproductive steps, cut the instructions causing that.

6. **Generalize, don't overfit.** When iterating based on test cases, resist adding narrow fixes for specific examples. The skill needs to work across diverse prompts, not just your test set. If there's a stubborn issue, try different metaphors or recommend different working patterns rather than adding rigid constraints.

7. **Progressive disclosure.** Don't dump everything into SKILL.md. Put the decision-making workflow in SKILL.md, and detailed reference material in `references/` with clear pointers:
   ```markdown
   For output format patterns and templates, see `references/output-patterns.md`.
   For workflow composition patterns, see `references/workflows.md`.
   ```

#### Common Sections to Include

- **When to Use** — In scope / Out of scope (with skill cross-references)
- **Key Rules** — Constraints with WHY reasoning
- **Workflow** — Step-by-step process
- **Output Format** — Explicit template or structure definition
- **Examples** — Input → output patterns (at least 2)
- **Edge Cases** — Common gotchas and how to handle them
- **References** — Pointers to reference files

### Phase 4: Test the Skill

Create 2-3 realistic test prompts — the kind of thing a real user would actually say. Share them with the user for confirmation, then run them.

If the user wants formal evals, create `evals/evals.json`:

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "A realistic user request as they'd actually phrase it",
      "expected_output": "Description of what success looks like",
      "files": [],
      "assertions": [
        "Output includes X with correct formatting",
        "The generated file is valid and parseable",
        "Edge case Y is handled gracefully"
      ]
    }
  ]
}
```

**Write strong assertions.** A good assertion is one that's hard to satisfy without actually doing the work correctly. "File exists" is weak. "File contains a valid C# class with `[Function]` attribute and proper DI constructor" is strong.

### Phase 5: Validate Structure

Run the validation script to check SKILL.md structure, frontmatter, and cross-references:

```bash
python .claude/skills/skill-creator/scripts/validate_skill.py .claude/skills/my-skill
```

Or validate all skills at once:

```bash
python .claude/skills/skill-creator/scripts/validate_skill.py --all
```

Use `--strict` to treat warnings as errors.

### Phase 6: Iterate

After running tests:

1. **Review the output** — does it meet the quality bar?
2. **Read the transcript** — is Claude following the intended workflow, or wasting time?
3. **Identify patterns** — what's working, what's not?
4. **Revise the skill** — apply changes, focusing on the *why* not just the *what*.
5. **Re-test** — run the same prompts again, plus new ones.

Repeat until satisfied. Then expand the test set to cover more diverse inputs.

---

## Improving an Existing Skill

When asked to improve a skill:

1. **Read the current SKILL.md** thoroughly.
2. **Ask the user** what's not working — specific failures, quality issues, or missing capabilities.
3. **Run test prompts** to see the skill in action and identify weaknesses.
4. **Revise** based on observations, following the writing principles above.
5. **Compare** before/after results. Track what improved and what regressed.

Key improvement strategies:
- Remove instructions that aren't pulling their weight
- Replace rigid ALWAYS/NEVER rules with explained reasoning
- Add examples where Claude is misunderstanding intent
- Restructure to put critical decisions earlier in the flow
- Move detail to `references/` if SKILL.md is getting bloated
- Ensure "Out of scope" cross-references are accurate

---

## Anti-Patterns to Avoid

- **Auxiliary docs**: No README.md, INSTALLATION_GUIDE.md, or CHANGELOG.md.
- **Overfitting**: Don't add narrow fixes for specific test cases.
- **Bloated SKILL.md**: If approaching 500 lines, refactor into references.
- **Missing trigger description**: The frontmatter `description` is how skills get activated — make it comprehensive and slightly pushy because Claude tends to undertrigger skills.
- **Rigid rule stacking**: Walls of MUST/ALWAYS/NEVER without reasoning make skills brittle and hard for the model to internalize.
- **Ignoring transcripts**: Always read execution transcripts, not just final outputs. The journey matters as much as the destination.
- **Surface-level assertions**: "File exists" tells you nothing. Test for meaningful outcomes.
- **Missing scope boundaries**: Every skill must define what's In scope and Out of scope, with explicit cross-references to the right skill for excluded tasks.

---

## Skill Quality Checklist

Before considering a skill complete, verify:

- [ ] Frontmatter `name` and `description` are filled, with description including trigger contexts and being "pushy" enough
- [ ] SKILL.md is under 500 lines (or has clear references for overflow)
- [ ] Instructions explain *why*, not just *what*
- [ ] "When to Use" section with explicit In scope / Out of scope and skill cross-references
- [ ] At least 2 concrete examples showing input → output
- [ ] Output format is explicitly defined
- [ ] Error handling / fallback behavior is addressed
- [ ] Edge cases are documented with explanations of WHY each matters
- [ ] No dead-weight instructions (everything earns its place)
- [ ] Tested with 2-3+ realistic prompts
- [ ] Works for diverse inputs, not just test cases
- [ ] Passes `validate_skill.py` without errors

---

## Quick Reference: Skill File Template

```markdown
---
name: [skill-name]
description: >
  [What it does + when to trigger. Be specific and slightly pushy about
  trigger contexts. Include keywords, phrases, file types, and scenarios.
  Claude tends to undertrigger, so err on the side of broad activation.]
---

# [Skill Name]

[1-2 sentence overview of what this skill accomplishes and why it matters.]

## When to Use

**In scope:**
- [Primary use case]
- [Secondary use case]

**Out of scope (use these skills instead):**
- [Excluded task] → use `[other-skill-name]`

## Key Rules

1. **[Rule name]** — [Instruction with WHY reasoning].
   Because [explanation].

## Workflow

### Step 1: [First action]
[Instructions with reasoning]

### Step 2: [Second action]
[Instructions with reasoning]

### Step 3: [Validation / Output]
[Quality checks and output format]

## Output Format

[Explicit template or structure definition]

## Examples

**Example 1:**
Input: [realistic input]
Output: [expected output]

**Example 2:**
Input: [different realistic input]
Output: [expected output]

## Edge Cases

- **[Edge case 1]** — [How to handle it and why]

## References

- For output patterns and templates, see `references/output-patterns.md`
- For workflow composition, see `references/workflows.md`
- For local skill conventions, see `references/local-conventions.md`
```

## References

- For output format patterns and skill templates, see `references/output-patterns.md`
- For sequential, conditional, and orchestration workflows, see `references/workflows.md`
- For Signal Hub skill conventions and inventory, see `references/local-conventions.md`
