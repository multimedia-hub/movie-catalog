# Choosing the Right Browser Skill

Three browser-related skills exist in this project. Use this guide to pick the right one.

## Quick Decision Tree

```
Need to interact with a site you're logged into?
  → YES → claude-chrome

Need isolated, repeatable test execution?
  → YES → agent-browser

Need a structured QA verification report?
  → YES → app-verifier

Need to write test scripts (Playwright/Vitest)?
  → YES → hub-tester
```

## Feature Comparison

| Feature | claude-chrome | agent-browser | app-verifier |
|---------|--------------|---------------|--------------|
| **Browser type** | Real Chrome (user's browser) | Headless Playwright | Playwright or BrowserMCP |
| **Sessions/cookies** | Shared with user | Isolated per context | Isolated per context |
| **Authentication** | Already logged in | Must authenticate or load state | Must authenticate or load state |
| **API keys needed** | None (uses browser sessions) | None (but no auth either) | None |
| **Use case** | Productivity, real-world automation | Testing, scraping, CI/CD | QA verification reports |
| **Side effects** | Real (sends real emails, etc.) | Isolated (safe for testing) | Isolated (safe for testing) |
| **GIF recording** | Yes | Video (.webm) recording | Screenshot-based |
| **Scheduled tasks** | Yes (sidebar only) | No | No |
| **Tab groups** | Yes (visible Claude group) | Parallel sessions | Single session |
| **Console/network** | Yes | Yes | Yes |
| **JavaScript execution** | Yes | Yes | Yes (Playwright only) |
| **File system** | Via Claude Code | Direct | Via Claude Code |
| **Responsive testing** | Manual resize | Viewport emulation, device profiles | Viewport resize (Playwright) |
| **Output format** | Conversational | Conversational / JSON | Structured verification report |
| **Setup required** | Chrome extension + Anthropic plan | None (built-in) | MCP server available |

## When to Use Each

### claude-chrome

Best for tasks that need your real browser identity:

- "Fill out this expense report in our company tool"
- "Post this update to our team Slack channel"
- "Draft an email in Gmail based on these notes"
- "Use Gemini to generate an image and save it locally"
- "Check my Google Calendar for conflicts"
- "Go to the Stripe Dashboard and verify the subscription"
- "Record a GIF demo of the signup flow on the live site"

### agent-browser

Best for isolated testing and automation:

- "Test the login form with invalid credentials"
- "Scrape product prices from this public website"
- "Fill out a form 50 times with different test data"
- "Take screenshots at mobile, tablet, and desktop sizes"
- "Test that the error page renders correctly for 404s"
- "Run this interaction sequence without affecting prod data"

### app-verifier

Best for structured QA with systematic checklists:

- "Verify the gap signals page works correctly"
- "Run a full QA check on the dashboard after my changes"
- "Check if the squeeze page data matches the API response"
- "Verify the paywall appears correctly for Free users"
- "Generate a verification report for the pricing page"

## Combining Skills

These skills complement each other in a development workflow:

1. **Build** code with Claude Code
2. **Test** with `agent-browser` (isolated, safe)
3. **Verify** with `app-verifier` (structured report)
4. **Demo** with `claude-chrome` (record GIF on real browser)
5. **Deploy** and verify production with `claude-chrome` (real sessions)

## Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|---------------|-----------------|
| Using claude-chrome for test automation | Real side effects (emails sent, data modified) | Use `agent-browser` for tests |
| Using agent-browser to check authenticated dashboards | No cookies, will hit login page | Use `claude-chrome` (already logged in) |
| Using app-verifier for quick browser checks | Overkill — generates a formal report | Use `claude-chrome` for quick checks |
| Using claude-chrome for responsive testing | No device emulation, manual resize only | Use `agent-browser` with device profiles |
| Using agent-browser to post to Slack/Gmail | Isolated context, can't authenticate | Use `claude-chrome` (shares sessions) |
