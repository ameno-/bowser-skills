---
name: claude-bowser
description: Observable browser automation using Chrome MCP tools. Use when you need to browse websites, take screenshots, interact with web pages, or perform browser tasks in your current Chrome. Keywords - browse, screenshot, browser, chrome, bowser, ui testing, observable.
---

# Claude Bowser

## Purpose

Automate browsing using Chrome MCP tools (`mcp__claude_in_chrome__*`) available when Pi is started with `--chrome`. This uses your real Chrome browser — observable, with your existing profile, cookies, and extensions.

## Prerequisites

Start Pi with the `--chrome` flag:
```bash
pi --chrome
```

## Pre-flight Check

**Before doing anything**, verify Chrome MCP tools are available. Look for tools matching `mcp__claude_in_chrome__*`.

- If available: proceed with the workflow
- If NOT available: stop and reply: _"Chrome tools are not available. Please restart Pi with the `--chrome` flag"_

## Standard Workflow

1. **Resize browser** to 1440x900 (optional but recommended):
   - Get tab context: `mcp__claude_in_chrome__tabs_context_mcp`
   - Resize: `mcp__claude_in_chrome__resize_window`

2. **Navigate** to the target URL:
   - `mcp__claude_in_chrome__navigate`

3. **Interact** with the page:
   - Read page: `mcp__claude_in_chrome__read_page`
   - Find elements: `mcp__claude_in_chrome__find`
   - Click: `mcp__claude_in_chrome__computer` with `action: "left_click"`
   - Type: `mcp__claude_in_chrome__computer` with `action: "type"`
   - Fill forms: `mcp__claude_in_chrome__form_input`

4. **Capture results**:
   - Screenshot: `mcp__claude_in_chrome__computer` with `action: "screenshot"`

5. **Report** results back to the user

## Available Tools

### Page Interaction
- `mcp__claude_in_chrome__javascript_tool` — Execute JavaScript
- `mcp__claude_in_chrome__computer` — Mouse, keyboard, screenshot
- `mcp__claude_in_chrome__form_input` — Set form values
- `mcp__claude_in_chrome__upload_image` — Upload files/images

### Page Reading
- `mcp__claude_in_chrome__read_page` — Accessibility tree
- `mcp__claude_in_chrome__find` — Natural language element finding
- `mcp__claude_in_chrome__get_page_text` — Raw text extraction

### Navigation & Tabs
- `mcp__claude_in_chrome__navigate` — Navigate to URL
- `mcp__claude_in_chrome__resize_window` — Resize browser
- `mcp__claude_in_chrome__tabs_context_mcp` — Get tab context
- `mcp__claude_in_chrome__tabs_create_mcp` — Create new tab

### Debugging
- `mcp__claude_in_chrome__read_console_messages` — Console messages
- `mcp__claude_in_chrome__read_network_requests` — Network requests

### Recording
- `mcp__claude_in_chrome__gif_creator` — Record actions as GIF
- `mcp__claude_in_chrome__shortcuts_list` — List shortcuts
- `mcp__claude_in_chrome__shortcuts_execute` — Execute shortcuts

## Key Features

- **Observable** — Watch the browser as it works
- **Your Profile** — Uses your real Chrome with cookies, extensions, logins
- **Accessibility Tree** — Navigate using semantic page structure
- **Screenshots** — Capture visual state
- **GIF Recording** — Record animated workflows

## Limitations

| Limitation | Details |
|------------|---------|
| **No parallel instances** | All Chrome MCP connections share a single controller |
| **Observable only** | Uses your real Chrome — no headless mode |
| **Requires --chrome flag** | Must start Pi with `pi --chrome` |
| **Single tab group** | All work happens in one Chrome extension tab group |

## When to Use

Use Claude-Bowser when:
- You need your real browser session (logins, cookies, extensions)
- You want to watch the automation happen
- You're doing one-off personal tasks
- The site requires browser extensions (password managers, etc.)

Use Playwright-Bowser when:
- You need parallel execution
- You're running CI/CD tests
- You need headless operation
- You want token efficiency

## Example Workflow

User: "Check my order status on amazon.com"

Your workflow:
1. Verify Chrome MCP tools are available
2. Resize window to 1440x900
3. Navigate to https://amazon.com
4. Find and click "Returns & Orders"
5. Read the orders list
6. Report status back

## Best Practices

1. **Always resize first** — Consistent viewport size for reproducibility
2. **Use find before click** — Get coordinates from `find` tool
3. **Read page after navigation** — Verify state before interacting
4. **Take screenshots** — Document the journey
5. **Check for errors** — Read console if something fails

---

*Original implementation: [github.com/disler/bowser](https://github.com/disler/bowser)*
