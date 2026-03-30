# Claude in Chrome MCP Tools Reference

The `claude-in-chrome` MCP server provides browser control tools when Chrome integration is active.
View available tools at any time with `/mcp` → select `claude-in-chrome`.

## Discovering Tools

```text
# In Claude Code, run:
/mcp

# Select "claude-in-chrome" to see all available tools
```

## Tool Categories

### Navigation

| Tool | Description |
|------|-------------|
| Navigate | Open a URL in a new or existing tab |
| Go back | Navigate back in browser history |
| Go forward | Navigate forward in browser history |
| Create tab | Open a new tab (optionally with a URL) |
| Switch tab | Switch to a specific tab by index or title |

### Reading Page Content

| Tool | Description |
|------|-------------|
| Get page text | Extract text content from the current page |
| Get tab context | Get information about all tabs in the Claude group |
| Screenshot | Capture a screenshot of the current tab |

### Interaction

| Tool | Description |
|------|-------------|
| Click | Click on an element (by position, selector, or description) |
| Type | Type text into an input field |
| Upload image | Upload an image file to a web form |
| Download | Download a file from the current page |

### Developer Tools

| Tool | Description |
|------|-------------|
| Console logs | Read browser console output (errors, warnings, info) |
| Network requests | View network requests and responses |
| Execute JavaScript | Run arbitrary JavaScript on the current page |

### Visual & Recording

| Tool | Description |
|------|-------------|
| Screenshot | Capture current tab as an image |
| Resize window | Change browser window dimensions |
| Record GIF | Start/stop recording browser interactions as a GIF |

### Tab Management

| Tool | Description |
|------|-------------|
| List tabs | View all tabs in the Claude group |
| Create tab | Open a new tab |
| Switch tab | Activate a different tab |
| Close tab | Close a tab |

## Key Differences from Playwright/agent-browser

| Feature | Claude Chrome | agent-browser (Playwright) |
|---------|--------------|---------------------------|
| **Browser context** | Real browser, real sessions | Isolated headless browser |
| **Authentication** | Uses existing cookies/logins | Must authenticate each time |
| **Element targeting** | Position, description, or selector | CSS selectors and `@ref` from snapshots |
| **JavaScript execution** | Yes | Yes |
| **Console reading** | Yes | Yes (via `agent-browser console`) |
| **Network inspection** | Yes | Yes (via `agent-browser network`) |
| **GIF recording** | Yes (built-in) | Video recording (`.webm`) |
| **Tab management** | Multi-tab with tab groups | Multi-session parallel browsers |
| **File system access** | Via Claude Code (download → move) | Direct file save |
| **Cookie management** | Shared with user's browser | Isolated per context |

## Usage Tips

### Targeting Elements

Claude Chrome uses visual understanding and page context to identify elements. You can guide it with:

- **Natural language:** "Click the Submit button"
- **Position:** "Click in the search box at the top of the page"
- **Specific text:** "Click the link that says 'View Details'"
- **CSS selectors:** When other methods fail, Claude can use JavaScript with `document.querySelector()`

### Working with Multiple Tabs

Claude manages tabs within a "Claude" tab group visible in Chrome. It can:

1. Open multiple tabs to different sites
2. Switch between them to gather or transfer data
3. Parallelize actions across tabs
4. Download files from one tab and reference them in another

### Console Log Filtering

When reading console logs, be specific about what you're looking for:

```text
# Good — targeted request
"Check the console for any errors related to API calls"
"Look for React hydration warnings in the console"
"Are there any CORS errors when the page loads?"

# Less effective — too broad
"Show me all console output"
"What's in the console?"
```

### Screenshot Best Practices

- Take screenshots after each navigation or state change
- Use screenshots to verify form fills before submitting
- Screenshots serve as evidence in verification workflows
- Claude can read and interpret screenshot content for follow-up actions
