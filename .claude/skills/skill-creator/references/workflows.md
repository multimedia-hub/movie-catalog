# Workflow Patterns — Skill Creator Reference

Common workflow patterns for skill SKILL.md files. These patterns can be composed
to create complex multi-step workflows.

## Table of Contents

1. [Sequential Workflow](#sequential-workflow)
2. [Conditional Workflow](#conditional-workflow)
3. [Orchestration Workflow](#orchestration-workflow)
4. [Validation Workflow](#validation-workflow)
5. [Progressive Disclosure](#progressive-disclosure)
6. [Error Recovery](#error-recovery)

---

## Sequential Workflow

The simplest pattern — steps executed in order, each depending on the previous.

```markdown
## Workflow

### Step 1: Gather Context
Read the relevant files to understand current state:
- Check existing implementations for patterns
- Identify the target directory and naming conventions

### Step 2: Plan the Implementation
Based on the gathered context:
- Determine which files need to be created or modified
- Identify dependencies and imports needed
- Choose the appropriate patterns

### Step 3: Implement
Create/modify files in dependency order:
1. Data models / types first (other code depends on them)
2. Service / logic layer second
3. UI / presentation layer last

### Step 4: Validate
Before presenting output:
- Check for compilation errors
- Verify imports resolve correctly
- Ensure consistent naming throughout
```

**When to use:** Most skills follow this pattern. Use it for straightforward
tasks where each step logically follows the previous one.

---

## Conditional Workflow

Steps that branch based on input analysis. Use decision trees to clarify routing.

```markdown
## Workflow

### Step 1: Analyze the Request

Determine the request type:

```
Is this a new resource or modification of an existing one?
├── New resource
│   ├── Simple (single entity) → Go to Step 2a
│   └── Complex (relationships) → Go to Step 2b
└── Modification
    ├── Adding a field → Go to Step 3a
    └── Changing behavior → Go to Step 3b
```

### Step 2a: Create Simple Resource
[Instructions for single-entity creation]

### Step 2b: Create Complex Resource
[Instructions for multi-entity creation with relationships]

### Step 3a: Add Field to Existing Resource
[Instructions for field additions — model, migration, schema, UI]

### Step 3b: Modify Existing Behavior
[Instructions for behavioral changes — identify impact, update tests]
```

**When to use:** Skills that handle multiple related but distinct tasks.
The `api-endpoint-builder` skill uses this for GET vs POST vs PUT endpoints.

---

## Orchestration Workflow

A coordination pattern where one skill delegates to others based on project phase.

```markdown
## Workflow

### Phase 1: Requirements Analysis
Analyze the user's request and decompose into implementation phases.
Create a phase plan with clear dependencies.

### Phase 2: Backend Pipeline
**Delegate to:** `api-pipeline-developer`
- Implement data models and pipeline activities
- Create decorator chain for data population

### Phase 3: HTTP Endpoints
**Delegate to:** `api-endpoint-builder`
- Create API endpoints that expose the pipeline data
- Add pagination and filtering

### Phase 4: Backend Testing
**Delegate to:** `api-tester`
- Write xUnit tests for pipeline activities and endpoints
- Mock external dependencies

### Phase 5: Contract Sync
**Delegate to:** `signal-sync`
- Generate Zod schemas matching C# response models
- Verify field mapping (PascalCase → camelCase)

### Phase 6: Frontend Implementation
**Delegate to:** `hub-signal-implementer`
- Scaffold all frontend files (14-file checklist)
- Wire up API calls with type-safe schemas

### Phase 7: Frontend Testing
**Delegate to:** `hub-tester`
- Write Vitest unit tests for components
- Add Playwright E2E tests for critical flows

### Handoff Template
When pausing between phases:
```
## Status: Phase [N] Complete
### Completed:
- [What was done]
### Next:
- Phase [N+1]: [What's next]
### Context for Next Session:
- [Key decisions made]
- [Files created/modified]
```
```

**When to use:** The `project-manager` skill uses this pattern. Appropriate
for skills that coordinate multi-step feature development across multiple
skill domains.

---

## Validation Workflow

A pattern for skills that check, verify, or sync existing artifacts.

```markdown
## Workflow

### Step 1: Discover Artifacts
Find all relevant files that need to be checked:
- Backend models in `Models/`
- Frontend schemas in `src/schemas/`
- API response contracts

### Step 2: Compare Pairs
For each backend ↔ frontend pair:
1. Parse the C# model properties
2. Parse the Zod schema fields
3. Compare field names (accounting for casing conventions)
4. Compare field types (using type mapping table)
5. Flag mismatches

### Step 3: Report Findings
```
## Sync Status

### ✓ In Sync
- `StockModel` ↔ `stockSchema`: All 12 fields match

### ✗ Drift Detected
- `GapSignal.GapPercent` (decimal) → Missing in `gapSignalSchema`
- `SqueezeSignal.BollingerWidth` → Frontend has `bollingerBandWidth` (name mismatch)

### Recommended Fixes
1. Add `gapPercent: z.number()` to `gapSignalSchema`
2. Rename `bollingerBandWidth` to `bollingerWidth` in `squeezeSignalSchema`
```

### Step 4: Apply Fixes (if authorized)
Only modify files after presenting findings and getting user approval.
```

**When to use:** Skills like `signal-sync` that detect drift between
paired artifacts. Also useful for lint-style skills and migration verification.

---

## Progressive Disclosure

A pattern for managing context window usage — load detail only when needed.

```markdown
## Workflow

### Step 1: Quick Assessment
Read only the high-level structure:
- File list and directory layout
- Public API signatures (not implementations)
- Import statements

Make an initial determination of what's needed.

### Step 2: Targeted Deep Dive
Based on Step 1, load detailed content only for the relevant areas:
- If adding an endpoint → read existing endpoint implementations
- If fixing a bug → read the specific function and its tests
- If adding a signal type → read the reference implementation

```
For Azure-specific deployment steps, read `references/azure.md`.
For authentication patterns, read `references/auth-patterns.md`.
For chart component APIs, read `references/chart-api.md`.
```

### Step 3: Implement with Context
Now that you have the right detail loaded, implement the solution.
```

**When to use:** Any skill that might need detailed reference material
but doesn't always. Prevents loading 1000+ lines of context when only
a subset is relevant.

---

## Error Recovery

A pattern for graceful handling when things go wrong during execution.

```markdown
## Error Handling

### Build Errors
If the code doesn't compile after implementation:
1. Read the error message carefully
2. Check for missing imports or typos
3. Verify the method signature matches the interface
4. Fix and retry — do not move to the next step until this compiles

### Test Failures
If tests fail after implementation:
1. Read the failure message and stack trace
2. Distinguish between:
   - **Assertion failure** → the logic is wrong, fix the implementation
   - **Setup failure** → mocks or fixtures are misconfigured, fix the test setup
   - **Compilation failure** → a contract changed, update the test
3. Fix the root cause, not the symptom

### External Service Errors
If an API call or database query fails:
1. Check if the service is available
2. Verify credentials and connection strings
3. If transient → inform the user and suggest retry
4. If persistent → suggest alternative approach

### Fallback Strategy
If the primary approach is blocked:
1. Explain what's blocking progress
2. Propose an alternative approach
3. Ask the user which path to take
4. Do not silently change strategy
```

**When to use:** Include error recovery patterns in any skill that interacts
with external systems, runs code, or produces artifacts that need to compile.

---

## Composing Patterns

Most real skills combine multiple patterns:

```
project-manager = Orchestration + Error Recovery
api-endpoint-builder = Sequential + Conditional + Validation
signal-sync = Validation + Error Recovery
hub-signal-implementer = Sequential + Progressive Disclosure
skill-creator = Sequential + Validation + Error Recovery
```

When designing a new skill's workflow:
1. Start with the simplest pattern that fits (usually Sequential)
2. Add Conditional branches only for genuinely different paths
3. Add Validation at the end to catch issues before output
4. Add Error Recovery for steps that can fail
5. Use Progressive Disclosure when reference material is large
