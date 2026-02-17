# Codex Implementation — Bowser Skills

> Browser automation skillset for OpenAI Codex CLI.

---

## Overview

This is the OpenAI Codex CLI implementation of Bowser Skills, adapted from the original [bowser](https://github.com/disler/bowser) project. It uses Codex's prompt-based agent system.

## Installation

### Prerequisites

1. **Codex CLI** — OpenAI's Codex command-line tool
2. **playwright-cli** — For headless browser automation:
   ```bash
   npm install -g @playwright/cli@latest
   ```

### Setup

```bash
cd implementations/codex
# Copy to your project or use standalone
codex
```

---

## Quick Start

### Using Codex Commands

```bash
# Direct skill usage
codex "Use browser-skill to open https://example.com"

# With Playwright (headless)
codex "Use playwright-bowser to test the login flow on localhost:3000"

# QA validation
codex "Use bowser-qa-agent to validate user story: 'Homepage loads correctly'"
```

### Using the Justfile

```bash
# List commands
just

# Test skill directly
just test-skill url="https://example.com"

# Run user story
just run-story story="homepage-loads"

# UI review
just ui-review
```

---

## Architecture

Codex implementation uses:

- **System Prompts** — Agent behavior definitions
- **Tool Specifications** — Playwright CLI as tools
- **Prompt Patterns** — Standardized prompt templates
- **JSON Output** — Structured agent responses

### Layer Mapping

| Layer | Codex Implementation |
|-------|---------------------|
| Skill | System prompt + tool specs |
| Agent | Agent system prompt + skill |
| Command | Orchestrator prompt pattern |
| Just | Makefile/justfile recipes |

---

## Configuration

### Agent Registry (`agents.json`)

```json
{
  "agents": {
    "playwright-bowser-agent": {
      "system_prompt": "...",
      "tools": ["playwright"],
      "model": "gpt-4"
    }
  }
}
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `PLAYWRIGHT_MCP_VIEWPORT_SIZE` | Viewport dimensions |
| `SCREENSHOTS_DIR` | Screenshot output path |
| `CODEX_BOWSER_HEADED` | Default headed mode |

---

## Two Approaches

### Playwright-Bowser
- **Codex Tools**: `playwright.open`, `playwright.click`, etc.
- **Use When**: Testing, parallel execution, CI/CD
- **Mode**: Headless default, `--headed` optional

### Chrome-Bowser (if available)
- **Codex Tools**: Chrome automation via MCP
- **Use When**: Personal automation, existing sessions
- **Mode**: Observable only

---

## Original Reference

- **Original:** [github.com/disler/bowser](https://github.com/disler/bowser)
- **Author:** IndyDevDan ([@disler](https://github.com/disler))
- **Video:** [YouTube Breakdown](https://youtu.be/efctPj6bjCY)

---

*See [AGENTS.md](./AGENTS.md) for Codex-specific agent configurations.*
