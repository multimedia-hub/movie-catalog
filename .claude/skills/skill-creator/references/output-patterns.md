# Output Patterns — Skill Creator Reference

Standard output patterns, templates, and checklists for crafting well-structured skill SKILL.md files. Replace the bracketed placeholders with your actual content.

## Table of Contents

1. [Frontmatter Templates](#frontmatter-templates)
2. [Section Templates](#section-templates)
3. [Example Patterns](#example-patterns)
4. [Checklist](#checklist)

---

## Frontmatter Templates

### Detailed Skill (with aggressive triggers)

```yaml
---
name: api-endpoint-builder
description: >
  Guides creation of Azure Functions HTTP trigger endpoints using the
  isolated worker model. Use this skill when creating new endpoints,
  adding API routes, exposing data via HTTP, or building REST endpoints
  with pagination. Trigger keywords: new endpoint, add API, HTTP trigger,
  REST endpoint, expose data, GET endpoint, POST endpoint, query endpoint,
  API route, add function.
---
```

### Lightweight Standards Skill

```yaml
---
name: backend-api
description: >
  Your approach to handling backend API.
  Use this skill when working on files where backend API comes into play.
---
```

### Cross-Layer Skill (broad triggers)

```yaml
---
name: signal-sync
description: >
  Detects and resolves drift between C# backend models and Zod frontend
  schemas. Use when: syncing models, updating contracts, fixing schema
  mismatches, adding or renaming fields, handling breaking changes,
  checking field mismatches, updating Zod schemas from C# model changes,
  resolving type mismatches, or when the frontend doesn't match the
  backend. Triggers on: "sync", "contract", "schema mismatch",
  "field mismatch", "breaking change", "add field", "rename field".
---
```

---

## Section Templates

### When to Use (with cross-references)

```markdown
## When to Use

**In scope:**
- Creating new Azure Functions HTTP trigger endpoints
- Adding pagination, filtering, and sorting to endpoints
- Setting up DI constructor injection for new functions
- Configuring route templates and HTTP methods

**Out of scope (use these skills instead):**
- Durable Functions orchestration and activities → use `api-pipeline-developer`
- Debugging endpoint errors → use `api-debugger`
- Writing xUnit tests for endpoints → use `api-tester`
- Frontend data fetching from endpoints → use `hub-signal-implementer`
```

### Key Rules (with WHY)

```markdown
## Key Rules

1. **Use constructor injection for all dependencies** — Azure Functions
   isolated worker model supports constructor DI natively. Inject services
   through constructors because it makes dependencies explicit, enables
   testing with mocks, and follows the same pattern used across all
   existing endpoints.

2. **Return `IActionResult`, not raw types** — Wrap responses in
   `OkObjectResult` or `BadRequestObjectResult` because this gives
   control over HTTP status codes, headers, and error formatting.
   Raw type returns lose this control and make error handling inconsistent.

3. **Validate pagination parameters defensively** — Clamp page size to
   a maximum (e.g., 100) because unbounded page sizes let a single
   request return thousands of rows, causing database timeouts and
   excessive memory usage.
```

### Workflow Steps

```markdown
## Workflow

### Step 1: Determine Endpoint Requirements
Read the request to identify:
- HTTP method (GET, POST, PUT, DELETE)
- Route template (e.g., `/api/signals/{signalType}`)
- Query parameters (pagination, filters, sorting)
- Request/response body shape

### Step 2: Create the Function Class
Create a new file in `Functions/` following the naming convention:
- File: `Get{Resource}Function.cs`
- Class: `Get{Resource}Function`
- Method: `Run` with `[Function("Get{Resource}")]` attribute

```csharp
public class GetSignalsFunction
{
    private readonly ISignalRepository _repository;

    public GetSignalsFunction(ISignalRepository repository)
    {
        _repository = repository;
    }

    [Function("GetSignals")]
    public async Task<IActionResult> Run(
        [HttpTrigger(AuthorizationLevel.Anonymous, "get",
         Route = "signals/{signalType}")] HttpRequestData req,
        string signalType)
    {
        // Implementation
    }
}
```

### Step 3: Add Zod Schema (Frontend Contract)
Create a matching Zod schema in the Signal Hub frontend:

```typescript
import { z } from 'zod';

export const signalResponseSchema = z.object({
  data: z.array(signalSchema),
  totalRecords: z.number(),
  page: z.number(),
  pageSize: z.number(),
});

export type SignalResponse = z.infer<typeof signalResponseSchema>;
```
```

### Output Format

```markdown
## Output Format

Each new endpoint produces:

1. **Function file** — `Functions/Get{Resource}Function.cs`
   - Class with constructor DI
   - `[Function]` attribute with route
   - Input validation
   - Repository call with pagination
   - `IActionResult` return

2. **Zod schema** — `signal-hub/src/schemas/{resource}.ts`
   - Response shape matching C# model
   - Request params schema for type-safe fetching

3. **Unit test** — `Tests/Functions/Get{Resource}FunctionTests.cs`
   - Happy path test
   - Validation error test
   - Empty result test
```

### Examples

```markdown
## Examples

**Example 1: Simple GET endpoint**
Input: "Create an endpoint that returns all gap signals with pagination"
Output:
- `Functions/GetGapSignalsFunction.cs` with pagination params
- Route: `GET /api/signals/gap?page=1&pageSize=20`
- Returns: `{ data: [...], totalRecords: 150, page: 1, pageSize: 20 }`

**Example 2: Filtered endpoint**
Input: "Add a search endpoint for stocks by ticker symbol"
Output:
- `Functions/SearchStocksFunction.cs` with ticker query param
- Route: `GET /api/stocks/search?q=AAPL&limit=10`
- Returns: `{ results: [...], query: "AAPL", count: 3 }`
```

### Edge Cases

```markdown
## Edge Cases

- **Empty results** — Return `{ data: [], totalRecords: 0, page: 1, pageSize: 20 }`
  with 200 status, not 404. An empty result set is a valid response because the
  query succeeded — there's just no matching data.

- **Invalid pagination params** — Clamp to defaults rather than returning 400.
  `page=-1` → use page 1. `pageSize=5000` → use max (100). This is more forgiving
  for API consumers and prevents unnecessary error handling on the frontend.

- **Missing route parameter** — Return 400 with a descriptive error message:
  `{ error: "signalType is required", validTypes: ["gap", "squeeze", "breakout"] }`.
```

---

## Example Patterns

### Code-Heavy Example (C# Backend)

````markdown
**Example: Adding a decorator to the pipeline**

Before (raw activity):
```csharp
public async Task<StockData> PopulateGapData(StockData stock)
{
    var gaps = await _gapService.Calculate(stock.Ticker);
    stock.GapSignals = gaps;
    return stock;
}
```

After (with decorator):
```csharp
[ActivityTrigger]
public async Task<StockData> PopulateGapData(
    [ActivityTrigger] StockData stock)
{
    var gaps = await _gapService.Calculate(stock.Ticker);
    stock.GapSignals = gaps;
    stock.LastUpdated = DateTime.UtcNow;
    return stock;
}
```
````

### Frontend Example (TypeScript/React)

````markdown
**Example: Signal list component**

```typescript
// Schema validation with Zod
const response = await fetch(`/api/signals/gap?page=${page}`);
const json = await response.json();
const validated = gapSignalResponseSchema.parse(json);

// Type-safe component rendering
{validated.data.map((signal) => (
  <SignalCard
    key={signal.id}
    ticker={signal.ticker}
    gapPercent={signal.gapPercent}
    direction={signal.direction}
  />
))}
```
````

### Decision Tree Example

```markdown
**Choosing the right testing approach:**

```
Is it a pure function (no side effects)?
├── Yes → Unit test with direct assertion
│         expect(calculateGap(open, close)).toBe(5.2)
└── No → Does it call external services?
    ├── Yes → Mock the service, test behavior
    │         mock(IStockRepository).setup(...)
    └── No → Does it render UI?
        ├── Yes → Testing Library render + assertions
        │         render(<SignalCard signal={mockSignal} />)
        └── No → Integration test with test fixtures
```
```

---

## Checklist

Use this checklist when reviewing a new or updated skill:

### Structure
- [ ] Frontmatter has `name` and `description`
- [ ] Description includes trigger keywords and is "pushy" enough
- [ ] SKILL.md is under 500 lines
- [ ] H1 title matches the skill purpose
- [ ] Sections follow standard order (When to Use → Key Rules → Workflow → Output → Examples → Edge Cases → References)

### Content Quality
- [ ] Every rule explains WHY, not just WHAT
- [ ] No ALL-CAPS directives (ALWAYS, NEVER) without accompanying reasoning
- [ ] At least 2 concrete input → output examples
- [ ] Examples use project-appropriate languages (C#, TypeScript, not Python or Pine Script)
- [ ] Output format is explicitly defined with templates
- [ ] Edge cases cover the most common failure modes

### Scope & Cross-References
- [ ] "When to Use" section exists with In scope / Out of scope
- [ ] Out of scope items name the correct alternative skill
- [ ] All cross-referenced skills actually exist
- [ ] No overlap with existing skills (check `local-conventions.md` inventory)

### Testing
- [ ] Tested with 2-3 realistic user prompts
- [ ] Passes `validate_skill.py` without errors
- [ ] Works for diverse inputs, not just test cases
