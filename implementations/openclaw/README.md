# OpenClaw Implementation — Bowser Skills

> Browser automation tools and plugins for OpenClaw.

<p align="center">
  <img src="https://raw.githubusercontent.com/disler/bowser/main/images/bowser_11.jpg" width="500" />
</p>

---

## Overview

This is the OpenClaw integration for Bowser Skills, adapted from the original [bowser](https://github.com/disler/bowser) project by [@disler](https://github.com/disler).

OpenClaw uses a **tool-first architecture** where agents call Python-decorated functions. This implementation provides browser automation as OpenClaw tools.

## Original Reference

- **Original Repository:** [github.com/disler/bowser](https://github.com/disler/bowser)
- **Original Author:** IndyDevDan ([@disler](https://github.com/disler))
- **License:** MIT

---

## Installation

### Prerequisites

```bash
# Install OpenClaw
pip install openclaw

# Install Playwright CLI
npm install -g @playwright/cli@latest
```

### Install Bowser Tools

```bash
cd implementations/openclaw

# Install as OpenClaw plugin
openclaw plugin install ./

# Or use directly
export OPENCLAW_TOOLS_PATH="$(pwd)/tools:$OPENCLAW_TOOLS_PATH"
```

---

## Architecture

OpenClaw implementation uses:

| Layer | OpenClaw Pattern |
|-------|------------------|
| **Skill** | `@tool` decorated Python functions |
| **Agent** | `@agent` decorated state machines |
| **Command** | `@workflow` orchestrators |
| **Runner** | OpenClaw CLI |

### Four-Layer Mapping

```
User Prompt
    ↓
Layer 4: openclaw run <workflow>
    ↓
Layer 3: @workflow orchestrator
    ↓ (spawns)
Layer 2: @agent execution
    ↓ (calls)
Layer 1: @tool browser automation
    ↓
playwright-cli → Browser
```

---

## Quick Start

### Using Tools Directly

```python
# In your OpenClaw environment
from openclaw.tools.bowser import browser_open, browser_screenshot

# Open a page
result = browser_open(url="https://example.com", session="demo")

# Take screenshot
browser_screenshot(session="demo", filename="home.png")

# Close
browser_close(session="demo")
```

### Using the Agent

```bash
# Run QA agent on a user story
openclaw agent bowser-qa \
  --story "shared/examples/hackernews.yaml" \
  --headed \
  --screenshots ./screenshots
```

### Using Workflows

```bash
# UI review across all stories
openclaw workflow ui-review \
  --stories "shared/examples/*.yaml" \
  --parallel 5

# Single workflow
openclaw workflow amazon-add-to-cart \
  --prompt "mechanical keyboard"
```

---

## Tool Reference

### Core Browser Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `browser_open` | Open URL in session | `url`, `session`, `headless`, `persistent` |
| `browser_goto` | Navigate to URL | `session`, `url` |
| `browser_click` | Click element | `session`, `ref` |
| `browser_fill` | Fill form input | `session`, `ref`, `text` |
| `browser_type` | Type text | `session`, `text` |
| `browser_press` | Press key | `session`, `key` |
| `browser_snapshot` | Get page snapshot | `session` |
| `browser_screenshot` | Capture screenshot | `session`, `filename` |
| `browser_console` | Get console messages | `session` |
| `browser_close` | Close session | `session` |

### Session Management

| Tool | Description |
|------|-------------|
| `session_list` | List all sessions |
| `session_close_all` | Close all sessions |

---

## Configuration

### `openclaw.yaml`

```yaml
# ~/.openclaw/openclaw.yaml
plugins:
  - path: /path/to/bowser-skills/implementations/openclaw
    
tools:
  bowser:
    config:
      screenshots_dir: ./screenshots
      default_viewport: "1440x900"
      playwright_timeout: 30000

agents:
  bowser-qa:
    class: agents.qa.BrowserQAAgent
    config:
      headed: false
      vision: false
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `PLAYWRIGHT_MCP_VIEWPORT_SIZE` | Default viewport (e.g., `1440x900`) |
| `BOWSER_SCREENSHOTS_DIR` | Screenshot output directory |
| `OPENCLAW_LOG_LEVEL` | Logging level (DEBUG, INFO, WARN) |

---

## Two Browser Approaches

### Playwright-Bowser (Default)

```python
from openclaw.tools.bowser import browser_open, browser_click

# Headless, parallel sessions
browser_open(
    url="https://example.com",
    session="my-test",
    headless=True,
    persistent=True
)
```

### Chrome-Bowser (If Available)

```python
from openclaw.tools.bowser_chrome import chrome_navigate, chrome_click

# Uses Chrome MCP (requires Chrome extension)
chrome_navigate(url="https://example.com")
chrome_click(ref="button-submit")
```

---

## Examples

### Example 1: Simple Browser Task

```python
# examples/simple_check.py
from openclaw.tools.bowser import *

@tool
def check_homepage(url: str) -> dict:
    """Check if a homepage loads correctly."""
    session = "check-homepage"
    
    browser_open(url=url, session=session)
    snapshot = browser_snapshot(session=session)
    browser_screenshot(session=session, filename="homepage.png")
    browser_close(session=session)
    
    return {
        "url": url,
        "loaded": len(snapshot) > 0,
        "screenshot": "homepage.png"
    }
```

### Example 2: QA Validation

See `examples/qa_validation.py` for full user story validation.

### Example 3: Parallel Stories

See `examples/parallel_stories.py` for running multiple stories concurrently.

---

## Project Structure

```
implementations/openclaw/
├── README.md                    # This file
├── AGENTS.md                    # Agent definitions
├── openclaw.yaml               # Configuration
│
├── tools/                       # Layer 1: Tools (Skills)
│   ├── __init__.py
│   ├── bowser.py               # Playwright tools
│   └── browser_chrome.py       # Chrome MCP tools (optional)
│
├── agents/                      # Layer 2: Agents
│   ├── __init__.py
│   └── qa.py                   # QA validation agent
│
├── commands/                    # Layer 3: Commands
│   └── ui_review.py            # UI review orchestrator
│
├── workflows/                   # Layer 3: Workflows
│   ├── amazon_add_to_cart.py
│   └── blog_summarizer.py
│
└── examples/                    # Usage examples
    ├── simple_check.py
    ├── qa_validation.py
    └── parallel_stories.py
```

---

## API Reference

See [AGENTS.md](./AGENTS.md) for complete tool and agent documentation.

---

## Contributing

To add a new tool:

1. Create function in `tools/` with `@tool` decorator
2. Add type hints and docstrings
3. Include example usage
4. Update this README

---

## Resources

- **OpenClaw Docs:** https://docs.openclaw.ai
- **OpenClaw Tools:** https://docs.openclaw.ai/tools
- **Original Bowser:** https://github.com/disler/bowser
- **Playwright CLI:** https://github.com/microsoft/playwright-cli

---

*Built for agentic browser automation with OpenClaw.*
