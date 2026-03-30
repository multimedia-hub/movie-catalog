# Local Conventions — Signal Hub Skill System

This document describes the patterns, conventions, and inventory of the Signal Hub project's skill system. Use this as a reference when creating new skills to ensure consistency.

## Table of Contents

1. [Skill Inventory](#skill-inventory)
2. [Two-Tier Skill System](#two-tier-skill-system)
3. [Frontmatter Conventions](#frontmatter-conventions)
4. [Body Structure](#body-structure)
5. [Naming Conventions](#naming-conventions)
6. [Size Guidelines](#size-guidelines)
7. [Cross-Referencing](#cross-referencing)

---

## Skill Inventory

### Backend API Skills (4)

| Skill | Lines | Type | Key Patterns |
|-------|-------|------|-------------|
| `api-debugger` | ~238 | Detailed | When to Use, Key Rules with WHY, Common Issues catalog, Edge Cases |
| `api-endpoint-builder` | ~293 | Detailed | When to Use, Key Rules, Workflow, Code examples, Edge Cases |
| `api-pipeline-developer` | ~201 | Detailed | When to Use, Key Rules, Workflow, Output Format |
| `api-tester` | ~336 | Detailed | When to Use, Key Rules, Workflow, xUnit patterns, FluentAssertions |

### Frontend Hub Skills (4)

| Skill | Lines | Type | Key Patterns |
|-------|-------|------|-------------|
| `hub-signal-implementer` | ~271 | Detailed | When to Use, 14-step Workflow, 14-File Checklist |
| `hub-chart-builder` | ~227 | Detailed | When to Use, 7-step Workflow, TradingView LW Charts v5 |
| `hub-auth-subscription` | ~274 | Detailed | When to Use, Security Rules, Auth/Stripe flows |
| `hub-tester` | ~367 | Detailed | When to Use, 6-step Workflow, Vitest/Playwright/Testing Library |

### QA/Verification Skills (1)

| Skill | Lines | Type | Key Patterns |
|-------|-------|------|-------------|
| `app-verifier` | ~310 | Detailed | When to Use, 8-step Workflow, MCP tool detection, Verification checklist, Report format |

### Orchestration Skills (3)

| Skill | Lines | Type | Key Patterns |
|-------|-------|------|-------------|
| `project-manager` | ~369 | Detailed | When to Use, Phases, Delegation Matrix, Handoff Template |
| `signal-sync` | ~251 | Detailed | When to Use, C# ↔ Zod Type Mapping Table, Workflow |
| `azure-manager` | ~230 | Detailed | 16 resource categories, Authentication, Operations |

### Standards Skills (15)

| Skill | Lines | Type | References |
|-------|-------|------|-----------|
| `backend-api` | 13 | Lightweight | `agent-os/standards/backend/api.md` |
| `backend-migrations` | 13 | Lightweight | `agent-os/standards/backend/migrations.md` |
| `backend-models` | 13 | Lightweight | `agent-os/standards/backend/models.md` |
| `backend-queries` | 13 | Lightweight | `agent-os/standards/backend/queries.md` |
| `frontend-accessibility` | 13 | Lightweight | `agent-os/standards/frontend/accessibility.md` |
| `frontend-components` | 13 | Lightweight | `agent-os/standards/frontend/components.md` |
| `frontend-css` | 13 | Lightweight | `agent-os/standards/frontend/css.md` |
| `frontend-responsive` | 13 | Lightweight | `agent-os/standards/frontend/responsive.md` |
| `global-coding-style` | 13 | Lightweight | `agent-os/standards/global/coding-style.md` |
| `global-commenting` | 13 | Lightweight | `agent-os/standards/global/commenting.md` |
| `global-conventions` | 13 | Lightweight | `agent-os/standards/global/conventions.md` |
| `global-error-handling` | 13 | Lightweight | `agent-os/standards/global/error-handling.md` |
| `global-tech-stack` | 13 | Lightweight | `agent-os/standards/global/tech-stack.md` |
| `global-validation` | 13 | Lightweight | `agent-os/standards/global/validation.md` |
| `testing-test-writing` | 13 | Lightweight | `agent-os/standards/testing/test-writing.md` |

### Meta Skills (2)

| Skill | Lines | Type | Key Patterns |
|-------|-------|------|-------------|
| `skill-creator` | ~310 | Detailed | Phases, Scaffolding scripts, Validation, Quality Checklist |
| `video-analyzer` | ~210 | Detailed | Processing Pipeline, Frame extraction, Audio transcription |

---

## Two-Tier Skill System

The project uses two complementary types of skills:

### Tier 1: Detailed Custom Skills (200-370 lines)

These teach domain-specific knowledge about the Signal Hub project:
- **What to build** — API endpoints, signal types, chart views, auth flows
- **How to build it** — Workflows, patterns, code templates
- **What to avoid** — Edge cases, anti-patterns, common mistakes

Structure: Full SKILL.md with frontmatter, When to Use, Key Rules, Workflow, Examples, Edge Cases.

### Tier 2: Lightweight Standards Skills (~13 lines)

These enforce coding standards across the project:
- **How to code** — Style, conventions, error handling, testing
- **Thin wrappers** — Each contains only frontmatter + a pointer to an external standards file
- **Always-on** — Triggered by file type/context, not explicit user requests

Structure: Frontmatter with auto-trigger description + single instruction to read external file.

### When to Use Each Tier

| Scenario | Tier |
|----------|------|
| Teaching Claude a project-specific workflow | Tier 1 (Detailed) |
| Enforcing a coding standard across all files | Tier 2 (Lightweight) |
| Adding a new signal type with 14+ files | Tier 1 (Detailed) |
| Ensuring consistent error handling patterns | Tier 2 (Lightweight) |
| Orchestrating multi-step feature development | Tier 1 (Detailed) |

---

## Frontmatter Conventions

### Description Pattern: What + When + Triggers

Detailed skills use a 3-part description:

```yaml
description: >
  [What it does — one sentence].
  Use this skill when [context 1], [context 2],
  [context 3], or [broader scenario].
  Trigger keywords: [keyword1], [keyword2], [keyword3].
```

**Key principle: Be "pushy" about triggers.** Claude tends to undertrigger skills, so descriptions should cast a wide net. Include:
- Explicit user phrases ("create a new endpoint", "add signal type")
- File patterns (when working on `*.cs` files in `Functions/`)
- Contextual triggers ("any request involving authentication")
- Even tangential triggers ("even if they don't explicitly ask for a 'dashboard'")

### Lightweight Skills Description Pattern

```yaml
description: >
  Your approach to handling [domain].
  Use this skill when working on files where [domain] comes into play.
```

These are intentionally broad so they activate alongside other skills as contextual support.

---

## Body Structure

### Standard Section Order for Detailed Skills

```
# [Skill Name]
[1-2 sentence overview]

## When to Use
**In scope:**
- [Use case 1]
- [Use case 2]

**Out of scope (use these skills instead):**
- [Excluded task] → use `[skill-name]`

## Key Rules
1. **[Rule]** — [Instruction + WHY reasoning]

## Workflow
### Step 1: [Action]
### Step 2: [Action]
### Step 3: [Action]

## Output Format
[Template or structure]

## Examples
**Example 1:** ...
**Example 2:** ...

## Edge Cases
- **[Case]** — [Handling + WHY]

## References
- For [topic], see `references/[file].md`
```

### Key Principles

1. **WHY-based writing** — Every rule and instruction should explain its reasoning. "Use pagination because unbounded queries can return thousands of rows and cause timeouts" is better than "ALWAYS paginate."

2. **In scope / Out of scope** — Every detailed skill explicitly lists what it handles and what it doesn't, with cross-references to the correct skill for excluded tasks.

3. **Concrete examples** — At least 2 input → output examples. These are often the most effective teaching tool.

---

## Naming Conventions

### Pattern: `{layer}-{role}`

Skills follow a `{layer}-{role}` naming pattern where:
- **layer** identifies the project area: `api-`, `hub-`, `backend-`, `frontend-`, `global-`
- **role** identifies the function: `debugger`, `builder`, `tester`, `implementer`

### Examples

| Name | Layer | Role |
|------|-------|------|
| `api-endpoint-builder` | `api` (Azure Functions) | `endpoint-builder` |
| `hub-chart-builder` | `hub` (Signal Hub frontend) | `chart-builder` |
| `hub-signal-implementer` | `hub` | `signal-implementer` |
| `api-tester` | `api` | `tester` |
| `frontend-css` | `frontend` (standard) | `css` |
| `global-error-handling` | `global` (standard) | `error-handling` |

### Exceptions

Some skills don't follow the layer-role pattern because they span layers:
- `project-manager` — Orchestrates across both API and Hub
- `signal-sync` — Bridges backend ↔ frontend contracts
- `azure-manager` — Infrastructure management (outside app code)
- `skill-creator` — Meta skill for the skill system itself
- `video-analyzer` — Cross-cutting analysis tool

---

## Size Guidelines

| Skill Type | Target Lines | Max Lines |
|------------|-------------|-----------|
| Standards (Tier 2) | ~13 | 50 |
| Regular detailed skill | 200-300 | 400 |
| Orchestrator skill | 300-370 | 500 |
| Meta skill (skill-creator) | 250-310 | 500 |

If a SKILL.md exceeds 400 lines, move detailed content to `references/` files.

---

## Cross-Referencing

### Rules

1. **Every detailed skill's "Out of scope" section must name the skill that handles the excluded task.** This prevents ambiguity and helps Claude route requests correctly.

2. **Cross-references use backtick-quoted skill names.** Example: `→ use \`api-tester\``

3. **Orchestrator skills reference all skills they delegate to.** `project-manager` has a delegation matrix listing every skill and when it's invoked.

4. **Skill cross-references must point to skills that exist.** The `validate_skill.py` script checks this.

### Coordination Pipeline

The Signal Hub skills form a coordinated pipeline for feature development:

```
project-manager (orchestrator)
    ├── api-pipeline-developer (Phase 1-2: Backend pipeline)
    ├── api-endpoint-builder (Phase 3: HTTP endpoints)
    ├── api-tester (Phase 4: Backend tests)
    ├── signal-sync (Phase 5: Contract sync)
    ├── hub-signal-implementer (Phase 6-7: Frontend scaffold)
    ├── hub-chart-builder (Phase 8: Chart views)
    ├── hub-auth-subscription (Phase 9: Feature gating)
    ├── hub-tester (Phase 10: Frontend tests)
    └── app-verifier (Phase 11: Interactive QA)

api-debugger (horizontal — cross-layer debugging)
    └── References api-pipeline-developer, api-endpoint-builder, api-tester

signal-sync (contract bridge)
    └── Bridges C# backend models ↔ TypeScript Zod schemas
```

### Standards Skills Relationship

Standards skills are **contextual companions** — they activate alongside detailed skills to enforce coding quality:

```
[User request: "add a new endpoint"]
  → api-endpoint-builder (primary skill — workflow)
  → backend-api (companion — coding standards)
  → global-error-handling (companion — error patterns)
```

This layering means detailed skills focus on *what* to build, while standards skills enforce *how* to code it.
