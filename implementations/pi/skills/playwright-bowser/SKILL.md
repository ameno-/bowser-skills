---
name: playwright-bowser
description: Headless browser automation using Playwright CLI. Use when you need headless browsing, parallel browser sessions, UI testing, screenshots, web scraping, or browser automation that can run in the background. Keywords - playwright, headless, browser, test, screenshot, scrape, parallel.
allowed-tools: Bash
---

# Playwright Bowser

## Purpose

Automate browsers using `playwright-cli` — a token-efficient CLI for Playwright. Runs headless by default, supports parallel sessions via named sessions (`-s=`), and doesn't load tool schemas into context.

## Prerequisites

```bash
npm install -g @playwright/cli@latest
```

Verify installation:
```bash
playwright-cli --help
```

## Key Details

- **Headless by default** — pass `--headed` to `open` to see the browser
- **Parallel sessions** — use `-s=<name>` to run multiple independent browser instances
- **Persistent profiles** — cookies and storage state preserved between calls
- **Token-efficient** — CLI-based, no accessibility trees or tool schemas in context
- **Vision mode** (opt-in) — set `PLAYWRIGHT_MCP_CAPS=vision` to receive screenshots as image responses

## Sessions

**Always use a named session.** Derive a short, descriptive kebab-case name from the user's prompt.

```bash
# Examples:
# "test the checkout flow on mystore.com" → -s=mystore-checkout
# "scrape pricing from competitor.com"    → -s=competitor-pricing
# "UI test the login page"                → -s=login-ui-test

playwright-cli -s=mystore-checkout open https://mystore.com --persistent
playwright-cli -s=mystore-checkout snapshot
playwright-cli -s=mystore-checkout click e12
```

Managing sessions:
```bash
playwright-cli list                 # list all sessions
playwright-cli close-all            # close all sessions
playwright-cli -s=<name> close      # close specific session
playwright-cli -s=<name> delete-data # wipe session profile
```

## Quick Reference

```
Core:       open [url], goto <url>, click <ref>, fill <ref> <text>, 
            type <text>, snapshot, screenshot [ref], close
Navigate:   go-back, go-forward, reload
Keyboard:   press <key>, keydown <key>, keyup <key>
Mouse:      mousemove <x> <y>, mousedown, mouseup, mousewheel <dx> <dy>
Tabs:       tab-list, tab-new [url], tab-close [index], tab-select <index>
Save:       screenshot [ref], pdf, screenshot --filename=f
Storage:    state-save, state-load, cookie-*, localstorage-*, sessionstorage-*
Network:    route <pattern>, route-list, unroute, network
DevTools:   console, run-code <code>, tracing-start/stop, video-start/stop
Sessions:   -s=<name> <cmd>, list, close-all, kill-all
Config:     open --headed, open --browser=chrome, resize <w> <h>
```

## Standard Workflow

1. **Derive a session name** from the user's prompt and open with `--persistent`:
```bash
PLAYWRIGHT_MCP_VIEWPORT_SIZE=1440x900 playwright-cli -s=<session-name> open <url> --persistent
```

2. **Get element references** via snapshot:
```bash
playwright-cli snapshot
```

3. **Interact** using refs from snapshot:
```bash
playwright-cli click <ref>
playwright-cli fill <ref> "text"
playwright-cli type "text"
playwright-cli press Enter
```

4. **Capture results**:
```bash
playwright-cli screenshot
playwright-cli screenshot --filename=output.png
```

5. **Always close the session** when done:
```bash
playwright-cli -s=<session-name> close
```

## Configuration

If a `playwright-cli.json` exists in the working directory, use it automatically:

```json
{
  "browser": {
    "browserName": "chromium",
    "launchOptions": { "headless": true },
    "contextOptions": { 
      "viewport": { "width": 1440, "height": 900 } 
    }
  },
  "outputDir": "./screenshots"
}
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `PLAYWRIGHT_MCP_VIEWPORT_SIZE` | Set viewport (e.g., `1440x900`) |
| `PLAYWRIGHT_MCP_CAPS` | Set to `vision` for image responses |

## Modes

### Headless (Default)
```bash
playwright-cli -s=session open https://example.com --persistent
```

### Headed (Visible)
```bash
playwright-cli -s=session open https://example.com --persistent --headed
```

### Vision Mode
Screenshots returned as image responses in context:
```bash
PLAYWRIGHT_MCP_CAPS=vision playwright-cli -s=session open https://example.com --persistent
```

## Full Help

```bash
playwright-cli --help
playwright-cli --help <command>
```

See [docs/playwright-cli.md](./docs/playwright-cli.md) for full documentation.

## Examples

### Basic Navigation
```bash
playwright-cli -s=demo open https://example.com --persistent
playwright-cli -s=demo snapshot
playwright-cli -s=demo click link-about
playwright-cli -s=demo screenshot --filename=about.png
playwright-cli -s=demo close
```

### Form Interaction
```bash
playwright-cli -s=form open https://example.com/login --persistent
playwright-cli -s=form fill input-email "user@example.com"
playwright-cli -s=form fill input-password "secret"
playwright-cli -s=form click button-submit
playwright-cli -s=form screenshot --filename=logged-in.png
playwright-cli -s=form close
```

### Scraping
```bash
playwright-cli -s=scrape open https://example.com/products --persistent
playwright-cli -s=scrape snapshot
# Extract data from snapshot output
playwright-cli -s=scrape close
```

---

*Original implementation: [github.com/disler/bowser](https://github.com/disler/bowser)*