# Bowser Skills — Agent Configuration Reference

> Agent definitions and configuration patterns for cross-platform browser automation.

---

## Overview

This document defines the standard agent types used across all Bowser implementations. Each platform adapts these patterns to its specific agent system.

---

## Core Agent Types

### 1. Playwright Bowser Agent

**Purpose:** Headless browser automation with parallel session support.

| Attribute | Value |
|-----------|-------|
| **Name** | `playwright-bowser-agent` |
| **Description** | Headless browser automation using Playwright CLI |
| **Skill** | `playwright-bowser` |
| **Parallel** | Yes |
| **Use When** | UI testing, scraping, parallel validation |

**Configuration Pattern:**
```yaml
name: playwright-bowser-agent
description: Headless browser automation agent
model: large  # Platform-specific model selection
skills:
  - playwright-bowser
variables:
  SESSION_NAME: null  # Derived from task
  HEADED: false
  VISION: false
```

**Workflow:**
1. Derive session name from task context
2. Execute playwright-bowser skill commands
3. Report results with session artifacts

---

### 2. Claude Bowser Agent

**Purpose:** Observable browser automation using real Chrome profile.

| Attribute | Value |
|-----------|-------|
| **Name** | `claude-bowser-agent` |
| **Description** | Observable browser automation using Chrome MCP |
| **Skill** | `claude-bowser` |
| **Parallel** | No (single instance) |
| **Use When** | Personal automation, sites needing real profile |

**Configuration Pattern:**
```yaml
name: claude-bowser-agent
description: Observable browser automation agent
model: large
skills:
  - claude-bowser
constraints:
  max_parallel: 1  # Cannot run multiple instances
requirements:
  - chrome_mcp_available
```

**Workflow:**
1. Verify Chrome MCP tools are available
2. Execute claude-bowser skill commands
3. Report results

---

### 3. Bowser QA Agent

**Purpose:** Structured user story validation with screenshot reporting.

| Attribute | Value |
|-----------|-------|
| **Name** | `bowser-qa-agent` |
| **Description** | UI validation agent for user story testing |
| **Skill** | `playwright-bowser` |
| **Parallel** | Yes |
| **Use When** | QA validation, acceptance testing, story verification |

**Configuration Pattern:**
```yaml
name: bowser-qa-agent
description: UI validation and user story testing agent
model: large
skills:
  - playwright-bowser
variables:
  SCREENSHOTS_DIR: ./screenshots/bowser-qa
  VISION: false
  HEADED: false
```

**Workflow:**
1. Parse user story into steps
2. Create screenshots directory
3. Execute each step with screenshot
4. Report PASS/FAIL for each step
5. Return structured report

**Report Format:**
```
✅ SUCCESS | ❌ FAILURE

**Story:** <story name>
**Steps:** N/N passed
**Screenshots:** ./screenshots/bowser-qa/<story-name>_<uuid>/

| #   | Step             | Status | Screenshot       |
| --- | ---------------- | ------ | ---------------- |
| 1   | Step description | PASS   | 00_step-name.png |
```

---

## Agent Variables Reference

### Common Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `HEADED` | boolean | `false` | Show browser window |
| `VISION` | boolean | `false` | Return screenshots as images |
| `TIMEOUT` | number | `300000` | Task timeout in ms |
| `SCREENSHOTS_DIR` | string | `./screenshots` | Screenshot save path |

### Playwright-Specific

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `SESSION_NAME` | string | derived | Named browser session |
| `PERSISTENT` | boolean | `true` | Persist cookies/storage |
| `VIEWPORT_WIDTH` | number | `1440` | Browser viewport width |
| `VIEWPORT_HEIGHT` | number | `900` | Browser viewport height |

### Chrome-Specific

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CHROME_TAB_ID` | number | auto | Target Chrome tab |
| `RESIZE_WIDTH` | number | `1440` | Window width |
| `RESIZE_HEIGHT` | number | `900` | Window height |

---

## Agent Selection Guide

```
┌─────────────────────────────────────────────────────────────────┐
│  Do you need your real browser (cookies, extensions, logins)?   │
├─────────────────────────────────────────────────────────────────┤
│  YES ──> claude-bowser-agent                                     │
│  NO ────> Continue                                               │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  Do you need to run multiple browser tasks in parallel?         │
├─────────────────────────────────────────────────────────────────┤
│  YES ──> playwright-bowser-agent                                │
│  NO ────> Continue                                               │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  Is this a structured test with validation steps?               │
├─────────────────────────────────────────────────────────────────┤
│  YES ──> bowser-qa-agent                                        │
│  NO ────> playwright-bowser-agent (default)                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Platform-Specific Adaptations

### Pi
- Agents defined as `.md` files in `.pi/agents/`
- Use `---` frontmatter for metadata
- Skills referenced by name
- Colors for terminal display

### Codex
- Agents defined in `codex-agents.json`
- Use Codex's agent registry
- Prompt-based skill invocation

### OpenClaw
- Agents as tool collections
- Function-calling interface
- State machine orchestration

### CloudHub
- Agents as serverless functions
- Event-driven execution
- Cloud storage for artifacts

---

## Example Agent Definitions

### Pi Format
```markdown
---
name: playwright-bowser-agent
description: Headless browser automation
model: opus
color: orange
skills:
  - playwright-bowser
---

# Playwright Bowser Agent

Execute browser tasks using the playwright-bowser skill.

## Workflow
1. Derive session name from task
2. Run skill commands
3. Report results
```

### Codex Format
```json
{
  "name": "playwright-bowser-agent",
  "description": "Headless browser automation",
  "model": "gpt-4",
  "system_prompt": "You are a browser automation agent...",
  "tools": ["playwright-cli"],
  "variables": {
    "HEADED": false,
    "VISION": false
  }
}
```

### OpenClaw Format
```yaml
agent:
  name: playwright-bowser-agent
  type: tool_executor
  tools:
    - playwright.open
    - playwright.click
    - playwright.screenshot
  state:
    session_name: null
    headed: false
```

---

*Refer to each platform's AGENTS.md for complete, platform-specific configurations.*