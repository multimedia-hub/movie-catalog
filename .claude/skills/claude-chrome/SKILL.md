---
name: claude-chrome
description: >
  Expert guide for using the Claude in Chrome browser extension with Claude Code.
  Connects Claude Code CLI to the user's real Chrome browser — uses existing sessions,
  cookies, and logins (Gmail, Notion, Slack, Stripe, etc.) without API keys or headless
  browsers. Use when the user mentions: "chrome extension", "claude chrome", "claude in chrome",
  "browser automation with chrome", "use my browser", "chrome sidebar", "schedule browser task",
  "record browser demo", "GIF recording", "record a demo", "debug in chrome", "test in my browser",
  "claude --chrome", "/chrome", "cross-tab workflow", "fill forms in chrome", "extract data from chrome",
  "automate chrome", "real browser", "authenticated browser", "browser session", "chrome MCP",
  "claude-in-chrome", "interact with web app", "use gemini from claude", "use chatgpt from claude",
  "multi-tab", "tab group", "chrome sidebar chat".
---

# Claude in Chrome Extension

Connects Claude Code to your **real Chrome browser** via the Claude in Chrome extension. Claude can navigate, click, type, screenshot, read console logs, execute JavaScript, and record GIF demos — all using your existing browser sessions. No API keys needed for authenticated services.

## When to Use

**In scope:**
- Automating tasks in your real browser (forms, data entry, navigation)
- Interacting with authenticated web apps (Gmail, Notion, Slack, Google Docs, Stripe Dashboard)
- Using other AI web apps from Claude Code (Gemini, ChatGPT, Perplexity)
- Cross-tab workflows (copy data between tabs, multi-site tasks)
- Debugging web apps with console log reading
- Testing local web apps at localhost with real browser
- Recording GIF demos for documentation or sharing
- Scheduling recurring browser tasks (daily, weekly, monthly)
- Extracting structured data from web pages
- Design verification (build UI, then check it in the browser)

**Out of scope (use these skills instead):**
- Headless browser testing with isolated contexts → use `agent-browser`
- Structured QA verification reports with checklists → use `app-verifier`
- Writing Playwright/Vitest test scripts → use `hub-tester`
- Backend API debugging → use `api-debugger`

## Key Rules

### 1. Use ONLY `mcp__claude-in-chrome__*` tools — NOT Playwright or BrowserMCP

This skill uses the **claude-in-chrome MCP server** which controls the user's real Chrome browser. Do NOT use `mcp__playwright__*` or `mcp__browsermcp__*` tools — those are separate headless/isolated browsers.

**WHY:** Playwright and BrowserMCP spin up isolated browser contexts without the user's cookies or sessions. The whole point of Claude Chrome is using the real browser with existing logins. Using the wrong MCP tools defeats the purpose and will fail for authenticated workflows.

**HOW TO APPLY:** Always use tools prefixed with `mcp__claude-in-chrome__`. Start with `mcp__claude-in-chrome__tabs_context_mcp` to get tab context, then use `mcp__claude-in-chrome__navigate`, `mcp__claude-in-chrome__computer` (for clicks, typing, screenshots, scrolling), `mcp__claude-in-chrome__form_input`, etc.

### 2. Check connection and kill competing sessions first

Before any browser work, ensure only ONE Claude Code session is running, then verify the Chrome extension connection.

**WHY:** Multiple Claude Code processes compete for the Chrome extension connection, causing "Multiple Chrome extensions connected" errors. This was the #1 setup issue during testing. The Chrome extension can only talk to one Claude Code instance at a time.

**HOW TO APPLY:**
1. Run `tasklist | findstr -i "claude"` (Windows) or `ps aux | grep claude` (Mac/Linux) to check for multiple Claude Code processes
2. Close any extra Claude Code sessions (other terminals, VS Code instances)
3. Run `/chrome` in Claude Code to verify the connection
4. If you get "Multiple Chrome extensions connected" — also check for multiple Chrome profiles or Edge with the extension installed

### 2. Respect domain-level permissions

Never auto-approve unknown domains. Each new domain requires explicit user approval through the extension's permission system.

**WHY:** Claude operates with the user's real authenticated sessions. A malicious web page could contain hidden prompt injection instructions that trick Claude into taking harmful actions on other authenticated sites (sending emails, modifying documents, transferring data). Domain-by-domain approval limits blast radius.

**HOW TO APPLY:** When Claude encounters a new domain during a workflow, it will ask for permission. Approve only domains you trust. For sensitive workflows, use the "Ask Before Acting" mode in the extension settings to require approval for every action.

### 3. Use real browser for authenticated work, headless for testing

Choose Claude Chrome when you need to interact with services you're already logged into. Choose `agent-browser` (Playwright) when you need isolated, repeatable test runs.

**WHY:** Claude Chrome shares all your cookies and sessions — powerful for productivity but dangerous for testing (real API calls, real side effects). Headless Playwright gives isolated contexts that can't accidentally modify production data.

**HOW TO APPLY:** Ask yourself: "Would I want this action to happen on my real account?" If yes → Claude Chrome. If it's a test scenario that should be isolated → `agent-browser`.

### 4. Request specific console patterns, not "all logs"

When debugging, tell Claude what patterns to look for rather than asking for all console output.

**WHY:** Browser consoles can produce hundreds of lines of noise (info logs, third-party analytics, extension output). Asking for "all console output" wastes context and makes it harder to find the actual problem.

**HOW TO APPLY:** Say "check the console for errors when the page loads" or "look for network failures related to the API" instead of "show me all console logs."

### 5. Take screenshots at every significant step

Screenshot after every navigation, interaction, or state change during browser workflows.

**WHY:** Screenshots are objective evidence. Text descriptions of visual state miss details, and the user needs to verify that Claude is interacting with the right elements. Screenshots also serve as documentation if the workflow needs to be repeated.

**HOW TO APPLY:** After navigating to a page, clicking a button, filling a form, or waiting for a response — take a screenshot before proceeding.

### 6. New tabs for browser tasks, never hijack existing tabs

Claude opens new tabs for browser tasks in a visible "Claude" tab group. It does not take over the user's existing tabs.

**WHY:** The user may have unsaved work in existing tabs. Claude's tab group keeps automated work separate and visible so the user can watch actions in real time.

**HOW TO APPLY:** Let Claude manage its own tabs. If you need to interact with a specific page the user has open, ask Claude to open a new tab to that same URL rather than taking over the existing tab.

## Setup & Prerequisites

### Requirements

| Requirement | Details |
|-------------|---------|
| Browser | Google Chrome or Microsoft Edge (not Brave, Arc, or other Chromium browsers) |
| Extension | [Claude in Chrome](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) v1.0.36+ |
| CLI | Claude Code v2.0.73+ |
| Plan | Anthropic Pro, Max, Teams, or Enterprise (not third-party providers) |
| Platform | macOS, Linux, or Windows (WSL not supported) |

### Launch Methods

```bash
# Method 1: Start Claude Code with Chrome enabled
claude --chrome

# Method 2: Enable Chrome from within an existing session
/chrome

# Method 3: Enable Chrome by default (no --chrome flag needed)
/chrome  →  select "Enabled by default"
```

**Note:** Enabling Chrome by default increases context usage since browser tools are always loaded. Use `--chrome` only when needed if context consumption is a concern.

### First-Time Setup

1. Install the Claude in Chrome extension from the Chrome Web Store
2. Pin the extension (puzzle piece icon → thumbtack)
3. Sign in with your Claude account
4. Start Claude Code with `claude --chrome`
5. On first run, Claude Code installs a native messaging host config — restart Chrome to pick it up

### Windows Native Messaging Host

If the extension isn't detected on Windows, verify the registry entry exists at:
- **Chrome:** `HKCU\Software\Google\Chrome\NativeMessagingHosts\com.anthropic.claude_code_browser_extension.json`
- **Edge:** `HKCU\Software\Microsoft\Edge\NativeMessagingHosts\com.anthropic.claude_code_browser_extension.json`

## Available MCP Tools

The `claude-in-chrome` MCP server provides browser control tools. View the full list with `/mcp` → select `claude-in-chrome`.

### Core Capabilities

| Capability | What Claude Can Do |
|------------|-------------------|
| **Navigate** | Open URLs, go back/forward, create tabs, switch tabs |
| **Read** | Get page text, DOM state, tab context, console logs, network requests |
| **Interact** | Click elements, type text, fill forms, upload/download files |
| **Visual** | Take screenshots, resize windows |
| **Execute** | Run JavaScript on the page |
| **Record** | Create GIF recordings of browser interactions |
| **Tabs** | Manage multiple tabs, parallel actions across tabs |

See `references/mcp-tools-reference.md` for detailed tool listings.

## Workflow: Build-Test-Debug Cycle

The primary value of Claude Chrome in a development workflow:

```
1. BUILD  →  Write/edit code with Claude Code in the terminal
2. TEST   →  Open the page in Chrome, interact, check behavior
3. DEBUG  →  Read console errors, inspect network requests
4. FIX    →  Go back to the code, fix the issue
5. VERIFY →  Re-test in Chrome, take screenshots as evidence
6. RECORD →  Create a GIF demo for documentation/PRs
```

All steps happen in a single Claude Code session without switching contexts.

## Common Workflows

### Test a local web app

```text
Open localhost:3000, try submitting the login form with invalid data,
and check if the error messages appear correctly.
```

Claude navigates to your local server, interacts with the form, takes screenshots, and reports what it observes.

### Debug with console logs

```text
Open the dashboard page and check the console for any errors
when the page loads.
```

Claude reads console messages and filters for error patterns. It can then switch back to the code to fix issues.

### Automate form filling

```text
I have customer contacts in contacts.csv. For each row, go to
crm.example.com, click "Add Contact", and fill in the name,
email, and phone fields.
```

Claude reads your local file, navigates the web interface, and enters data for each record.

### Draft content in authenticated apps

```text
Draft a project update based on the recent commits and add it to
my Google Doc at docs.google.com/document/d/abc123
```

Claude opens the document (already authenticated), clicks into the editor, and types the content. Works with Gmail, Notion, Sheets, and more.

### Extract data from web pages

```text
Go to the product listings page and extract the name, price, and
availability for each item. Save the results as a CSV file.
```

Claude navigates, reads the content, and saves structured data locally.

### Multi-site cross-tab workflows

```text
Check my calendar for meetings tomorrow, then for each meeting with
an external attendee, look up their company website and add a note
about what they do.
```

Claude works across multiple tabs, gathering information and completing the workflow.

### Record a demo GIF

```text
Record a GIF showing how to complete the checkout flow, from adding
an item to the cart through to the confirmation page.
```

Claude records the interaction sequence and saves it as a GIF file.

### Use other AI tools via browser

```text
Go to Gemini, generate an image with "hello world" text, then
download it and save it to this directory.
```

Claude navigates to Gemini (already authenticated), enters the prompt, waits for the result, downloads the image, and moves it to the local project directory. No Gemini API key needed.

## Testing SignalFinder Pro

### Test Account

| Field | Value |
|-------|-------|
| **Email** | `testuser@gmail.com` |
| **Password** | `Lore2121#` |
| **Tier** | Premium Member (active subscription) |
| **Admin** | No |

This account works on both production and localhost.

### Login Flow (Step-by-Step)

When Claude needs to sign in via the Chrome extension, follow these exact steps:

1. Navigate to the site (prod or localhost)
2. Click **"Sign In"** in the **top nav bar** (top-right corner of the page, next to "Get Started Free")
3. The auth modal opens showing **"Welcome back"** — it defaults to the **"Login"** tab (already selected). If you see "Create an account", click the **"Login"** tab to switch.
4. Click the **email input field** (placeholder: "you@example.com") and type `testuser@gmail.com`
5. Click the **password input field** (placeholder: "Enter your password") and type `Lore2121#`
6. Click the blue **"Sign In"** button at the bottom of the modal (NOT the "Sign In" in the nav bar behind it)
7. Wait 3 seconds for redirect — the URL should change to `/dashboard`
8. Verify login: the **sidebar** should show the user's name and subscription badge at the bottom-left (e.g., "Test User" / "Premium Member") instead of the "Sign In" button
9. Take a screenshot to confirm logged-in state

**Common login issues:**
- **Modal overlay blocks clicks:** If clicking "Sign In" fails, the dark overlay behind the modal can intercept clicks. Make sure you click the button **inside the modal**, not behind it.
- **Account doesn't exist:** The E2E smoke tests may delete and recreate this account daily. If login fails with "Invalid credentials", the user may need to sign up first.
- **Already logged in:** If navigating to the site shows the sidebar with user info, you're already logged in — skip the login flow.

### Key Pages & Expected Behavior

The test account is a **Premium tier** user. Expected behavior per page:

| Route | Auth Required | Min Tier | Expected Behavior (Premium User) |
|-------|:------------:|:--------:|-------------------------------|
| `/` | No | — | Landing page with hero section (GSAP pinned — use scroll wheel, not Page_Down) |
| `/gaps` | No | Free | Gap signals list with full access (no daily limit) |
| `/squeeze` | No | Free | Coil/squeeze signals list with full access |
| `/market` | No | Free | Market drill-down analysis |
| `/best-of-best` | No | Free | Featured "Best of Best" signals |
| `/pricing` | No | — | Subscription plans (Pro/Premium) |
| `/blog` | No | — | Blog listing page |
| `/dashboard` | Yes | Free | Signal dashboard with all signals (redirects to `/?auth=login` if not signed in) |
| `/charts` | Yes | Free | Multi-chart view |
| `/performance` | Yes | Free | Performance analytics |
| `/settings` | Yes | Free | Account settings (profile, security) |
| `/profile` | Yes | Free | User profile page |
| `/portfolio` | Yes | **Pro** | Full access (Premium user has Pro+ features) |
| `/watchlists` | Yes | **Pro** | Full access (Premium user has Pro+ features) |
| `/admin/*` | Yes | **Admin** | Silent redirect to `/` (test user is not admin) |

**Note:** If the test account tier changes (e.g., subscription expires), `/portfolio` and `/watchlists` will show paywalls instead of content. Check the sidebar badge (bottom-left) to confirm current tier after login.

### Production Testing (signalfinderpro.com)

**Base URL:** `https://signalfinderpro.com`

#### Workflow

```
1. Navigate to signalfinderpro.com
2. Screenshot the landing page
3. Sign in with test account (see login flow above)
4. Navigate through key pages, screenshot each:
   - /dashboard → verify signal cards load
   - /gaps → verify gap signals list with data
   - /squeeze → verify coil signals list with data
   - /market → verify market drill-down loads
   - /best-of-best → verify featured symbols display
   - /portfolio → verify paywall appears (Free user)
   - /watchlists → verify paywall appears (Free user)
5. Check console for errors after each navigation
6. Take final screenshot of any issues found
```

#### Example Prompts

```text
# Quick smoke test
Go to signalfinderpro.com, sign in with testuser@gmail.com / Lore2121#,
then navigate to the dashboard and check for console errors.

# Full page verification
Sign in to signalfinderpro.com with testuser@gmail.com / Lore2121#,
then visit /gaps, /squeeze, /market, and /dashboard. Screenshot each
page and report any console errors.

# Paywall verification
Sign in to signalfinderpro.com with testuser@gmail.com / Lore2121# (Free user),
navigate to /portfolio and /watchlists, and verify both show the Pro paywall.

# Signal data check
Go to signalfinderpro.com/gaps, sign in with testuser@gmail.com / Lore2121#,
click on any stock symbol, and screenshot the Fibonacci levels panel.

# Debug production issue
Navigate to signalfinderpro.com/dashboard, sign in with testuser@gmail.com / Lore2121#,
and check the console for any errors or failed network requests.
```

#### Production Warnings

- **LIVE Stripe keys** — Do NOT test payment flows with real cards. The pricing page checkout uses real Stripe. Use localhost for payment testing.
- **Rate limiting** — E2E endpoints have a 5-minute cooldown between smoke test runs.
- **Real data** — Production shows live market data. Signal counts and values change daily.

### Localhost Testing (localhost:3000)

**Base URL:** `http://localhost:3000`

#### Pre-Flight

Before testing localhost, ensure the dev server is running:

```bash
# Start the Next.js dev server
cd signal-hub && npm run dev

# Optional: Start the backend API locally (port 7190)
cd azureApi/InvestipsHubApi && func start --port 7190
```

**Note:** If the local backend isn't running, the frontend uses Vercel rewrites to proxy `/api/backend/*` to the production Azure Functions API. Most pages will still work without a local backend.

#### Workflow

```
1. Verify localhost:3000 is running (navigate and screenshot)
2. Sign in with test account (same login flow as prod)
3. Navigate through key pages, screenshot each
4. Check console for errors — dev mode shows more warnings than prod
5. Test any new features or recent code changes
```

#### Example Prompts

```text
# Test after code changes
Open localhost:3000, sign in with testuser@gmail.com / Lore2121#,
navigate to /gaps and verify the signal list loads correctly.
Check the console for any errors.

# Test new feature
Go to localhost:3000/dashboard, sign in with testuser@gmail.com / Lore2121#,
and test the new filter I just added. Screenshot the results.

# Stripe payment testing (localhost only)
Go to localhost:3000/pricing, click "Start Pro Plan", and verify
the Stripe checkout opens. Use test card 4242 4242 4242 4242
with any future expiry and any CVC.

# Full localhost smoke test
Sign in to localhost:3000 with testuser@gmail.com / Lore2121#,
visit every page in the sidebar, screenshot each one, and report
any console errors or broken layouts.
```

#### Localhost Advantages

- **Stripe test mode** — Use test cards (4242 4242 4242 4242) for payment flows
- **Hot reload** — Fix code and re-test without restarting
- **Verbose logging** — Dev mode shows React warnings, hydration issues, slow renders
- **No rate limits** — Test as many times as needed

### Side-by-Side Comparison (Prod vs Dev)

Compare production and localhost to catch deployment drift:

```text
Open signalfinderpro.com/gaps in one tab and localhost:3000/gaps in another.
Sign in with testuser@gmail.com / Lore2121# on both. Screenshot both tabs
and tell me if there are any visual differences.
```

This is useful for:
- Verifying a feature works the same in dev and prod
- Catching environment-specific bugs (API differences, missing env vars)
- Comparing data between production and development databases

## Chrome Sidebar vs CLI Mode

The extension works in two modes:

| Feature | Chrome Sidebar | CLI (`claude --chrome`) |
|---------|---------------|------------------------|
| **How to access** | Click extension icon in Chrome | Run `claude --chrome` in terminal |
| **Best for** | Quick tasks while browsing | Development workflows (code + browser) |
| **Contextual suggestions** | Yes (based on current page) | No |
| **Shortcuts** | Yes (`/` in chat for saved prompts) | No (use Claude Code skills instead) |
| **Scheduled tasks** | Yes (clock icon, daily/weekly/monthly) | No |
| **Code editing** | No | Yes (full Claude Code capabilities) |
| **File system access** | Limited | Full |
| **Model selection** | Haiku (Pro), Opus/Sonnet/Haiku (Max+) | Uses your Claude Code model |

**For developers:** Use the CLI mode (`claude --chrome`) when you need both code editing and browser interaction. Use the sidebar for quick browser-only tasks.

## Scheduling Recurring Tasks

The Chrome extension sidebar supports scheduled tasks:

1. Click the **clock icon** in the extension panel
2. Set the schedule: daily, weekly, monthly, or annually
3. Describe the task (e.g., "Check my dashboard for alerts and send me a summary")
4. Chrome must remain open for scheduled tasks to run

**Note:** Scheduling is only available in the Chrome sidebar mode, not via CLI.

## Saved Shortcuts

Save frequently used prompts as shortcuts in the extension:

1. Write a prompt that works well (e.g., "Summarize this page in 3 bullet points")
2. Save it as a shortcut in extension settings
3. Access via `/` in the sidebar chat

## Security Considerations

### Prompt Injection Risk

Malicious actors can hide instructions in web pages, emails, and documents to trick Claude into taking harmful actions. The extension mitigates this with:

- **Per-domain permissions** — Claude asks before interacting with each new domain
- **"Ask Before Acting" mode** — Claude shows a plan and waits for approval before executing
- **High-risk site detection** — The extension identifies and warns about potentially dangerous sites

### Best Practices

1. **Approve only trusted domains** — Don't auto-approve domains you don't recognize
2. **Watch Claude's actions** — Actions run in a visible Chrome window in real time
3. **Use "Ask Before Acting"** for sensitive workflows involving financial or personal data
4. **Review before sending** — If Claude is drafting emails or messages, review before sending
5. **Handle login/CAPTCHA manually** — Claude pauses and asks you when it encounters these

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|---------|
| **"Multiple Chrome extensions connected"** | **Multiple Claude Code processes running, or extension installed in multiple browsers/profiles** | **This is the #1 issue.** Run `tasklist \| findstr -i "claude"` — if you see more than ~3 processes, close extra Claude Code sessions (other terminals, VS Code). Also close Edge or other browsers with the extension. Then click "Connect" in the Chrome extension popup. |
| "Chrome extension not detected" | Extension not installed or disabled | Install/enable at `chrome://extensions`, restart Chrome |
| "Extension not detected" after install | Native messaging host not picked up | Restart Chrome (reads config on startup) |
| "Browser extension is not connected" | Native messaging host can't reach extension | Restart Chrome and Claude Code, run `/chrome` |
| "Receiving end does not exist" | Extension service worker went idle | Run `/chrome` → "Reconnect extension" |
| "No tab available" | Claude acted before tab was ready | Call `tabs_context_mcp` then `tabs_create_mcp` to create a fresh tab |
| Browser stops responding | Modal dialog (alert/confirm) blocking page | Dismiss the dialog manually in Chrome, then continue |
| Connection drops during long session | Service worker idle timeout | Run `/chrome` → "Reconnect extension" |
| Named pipe conflicts (EADDRINUSE) | Another Claude Code session using Chrome | Close other Claude Code sessions, restart |
| Native messaging host crash (Windows) | Corrupted host config | Reinstall Claude Code to regenerate config |
| Page_Down / keyboard scroll doesn't work | GSAP ScrollTrigger pinned sections on landing page | Use `scroll` action with scroll wheel ticks instead of `key` Page_Down |

## Edge Cases

- **Login pages / CAPTCHA:** Claude pauses and asks you to handle these manually. Complete the login, then tell Claude to continue.
- **Browser not Chrome/Edge:** Only Google Chrome and Microsoft Edge are supported. Brave, Arc, and other Chromium browsers are not supported.
- **WSL:** Chrome integration does not work under Windows Subsystem for Linux.
- **Third-party API providers:** Chrome integration requires a direct Anthropic plan (Pro/Max/Teams/Enterprise). Not available through Bedrock, Vertex AI, or Foundry.
- **Context usage:** When Chrome is enabled by default, browser tools are always loaded, increasing context consumption. Use `--chrome` flag only when needed to conserve context.
- **Real-time visibility:** All browser actions happen in a visible Chrome window. The user can watch and intervene at any time.

## References

- For detailed MCP tool listings, see `references/mcp-tools-reference.md`
- For choosing between Chrome extension vs headless browser vs app-verifier, see `references/chrome-vs-headless.md`
- For headless browser automation, see `agent-browser` skill
- For structured QA verification, see `app-verifier` skill
- Official docs: https://code.claude.com/docs/en/chrome
