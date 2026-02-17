# Codex Agent Configurations

> Agent definitions for OpenAI Codex CLI implementation.

---

## Overview

Codex agents are defined via system prompts and tool specifications. Agents are invoked by name in Codex prompts.

## Agent Definitions

### 1. Playwright Bowser Agent

**Purpose:** Headless browser automation with parallel session support.

**System Prompt:**
```
You are a browser automation agent using Playwright CLI.

Your job is to execute browser tasks using playwright-cli commands.

## Session Management
Always use named sessions (-s=<name>) derived from the task context.
Use kebab-case names: "test checkout" → "test-checkout"

## Standard Workflow
1. Open: playwright-cli -s=<session> open <url> --persistent
2. Interact: snapshot, click, fill, type, press
3. Capture: screenshot --filename=<path>
4. Cleanup: playwright-cli -s=<session> close

## Environment
- Default viewport: 1440x900
- Headless by default (add --headed if requested)
- Persistent profiles preserve cookies

Report:
- Success/failure status
- Screenshots captured with paths
- Any errors encountered
```

**Tools:**
```json
{
  "tools": [
    {
      "name": "playwright",
      "description": "Execute playwright-cli commands",
      "parameters": {
        "command": "string",
        "session": "string"
      }
    }
  ]
}
```

**Usage:**
```bash
codex "Use playwright-bowser-agent to test the login flow on example.com"
```

---

### 2. Bowser QA Agent

**Purpose:** Structured user story validation with screenshots.

**System Prompt:**
```
You are a QA validation agent. Execute user stories step-by-step.

## Workflow
1. Parse the user story into discrete steps
2. Create a unique screenshots directory
3. Execute each step with playwright-bowser skill
4. Take screenshot after each step
5. Mark each step PASS or FAIL
6. On first failure: capture console, stop, mark remaining SKIPPED
7. Return structured report

## Report Format
```
✅ SUCCESS | ❌ FAILURE

**Story:** <name>
**Steps:** X/N passed
**Screenshots:** <path>

| # | Step | Status | Screenshot |
|---|------|--------|------------|
| 1 | ... | PASS | 00_step.png |
```

## Variables
- SCREENSHOTS_DIR: ./screenshots/bowser-qa
- HEADED: false (set to true for visible browser)
- VISION: false (set to true for image context)
```

**Usage:**
```bash
codex "Use bowser-qa-agent to validate: Navigate to example.com, verify title, click login"
```

---

## Prompt Patterns

### Skill Invocation
```bash
codex "Using playwright-bowser skill, open https://example.com and take a screenshot"
```

### Agent Spawning
```bash
codex "Spawn playwright-bowser-agent to test the checkout flow on mystore.com"
```

### QA Validation
```bash
codex "Use bowser-qa-agent with VISION=true to validate user story: <story content>"
```

---

## Configuration File

**`agents.json`:**
```json
{
  "playwright-bowser-agent": {
    "system_prompt_file": "agents/playwright-bowser-agent.txt",
    "model": "gpt-4",
    "tools": ["bash"],
    "env": {
      "PLAYWRIGHT_MCP_VIEWPORT_SIZE": "1440x900"
    }
  },
  "bowser-qa-agent": {
    "system_prompt_file": "agents/bowser-qa-agent.txt",
    "model": "gpt-4",
    "tools": ["bash"],
    "env": {
      "SCREENSHOTS_DIR": "./screenshots/bowser-qa"
    }
  }
}
```

---

## Tool Specifications

### Playwright Tool

The Playwright tool wraps `playwright-cli` commands:

```json
{
  "name": "playwright_cli",
  "description": "Run playwright-cli browser automation commands",
  "input_schema": {
    "type": "object",
    "properties": {
      "session": {
        "type": "string",
        "description": "Named session (-s parameter)"
      },
      "command": {
        "type": "string",
        "enum": [
          "open", "goto", "click", "fill", "type", "press",
          "snapshot", "screenshot", "close", "list", "console"
        ]
      },
      "args": {
        "type": "array",
        "items": {"type": "string"}
      },
      "options": {
        "type": "object",
        "properties": {
          "headed": {"type": "boolean"},
          "persistent": {"type": "boolean"},
          "vision": {"type": "boolean"}
        }
      }
    },
    "required": ["command"]
  }
}
```

---

## Original Reference

This implementation is adapted from:
- **Original:** [github.com/disler/bowser](https://github.com/disler/bowser)
- **Author:** IndyDevDan ([@disler](https://github.com/disler))

---

*See [README.md](./README.md) for usage examples.*
