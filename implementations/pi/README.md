# Pi Implementation — Bowser Skills

> Browser automation skillset for the Pi agent harness.

---

## Overview

This is the Pi-native implementation of Bowser Skills, adapted from the original [bowser](https://github.com/disler/bowser) project. It uses Pi's skill/agent/command architecture.

## Installation

### Prerequisites

1. **Pi** — The Pi agent harness
2. **playwright-cli** — For headless browser automation:
   ```bash
   npm install -g @playwright/cli@latest
   ```
3. **just** (optional) — For one-command recipes:
   ```bash
   brew install just
   ```

### Setup

1. Copy this directory to your project's `.pi/` folder:
   ```bash
   cp -r implementations/pi/* /path/to/your/project/.pi/
   ```

2. Or use as a standalone project:
   ```bash
   cd implementations/pi
   pi
   ```

---

## Quick Start

### Layer 1: Skills (Capability)

```bash
# Playwright skill — headless browser
pi "Use the /playwright-bowser skill to open https://example.com"

# Claude-bowser skill — observable Chrome (requires --chrome)
pi --chrome "Use the /claude-bowser skill to check my email"
```

### Layer 2: Agents (Scale)

```bash
# Spawn a playwright agent
pi "Spawn a @playwright-bowser-agent to test the login flow"

# Spawn a QA agent
pi "Spawn a @bowser-qa-agent to validate the user story"
```

### Layer 3: Commands (Orchestration)

```bash
# UI review across all YAML stories
pi "/ui-review"

# Run a saved workflow
pi "/bowser:hop-automate amazon-add-to-cart 'mechanical keyboard'"
```

### Layer 4: Just (Reusability)

```bash
# List all recipes
just

# Test skill directly
just test-playwright-skill

# Run UI review
just ui-review

# Amazon automation demo
just automate-amazon
```

---

## Directory Structure

```
.pi/
├── skills/
│   ├── playwright-bowser/
│   │   ├── SKILL.md          # Headless browser skill
│   │   └── examples/
│   │       └── basic-usage.md
│   └── claude-bowser/
│       ├── SKILL.md          # Chrome MCP skill
│       └── examples/
│           └── basic-usage.md
├── agents/
│   ├── playwright-bowser-agent.md
│   ├── claude-bowser-agent.md
│   └── bowser-qa-agent.md
└── commands/
    ├── ui-review.md
    └── bowser/
        ├── hop-automate.md
        ├── amazon-add-to-cart.md
        └── blog-summarizer.md
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PLAYWRIGHT_MCP_VIEWPORT_SIZE` | `1440x900` | Browser viewport |
| `PLAYWRIGHT_MCP_CAPS` | `null` | Set to `vision` for vision mode |
| `SCREENSHOTS_DIR` | `./screenshots` | Screenshot save path |

### User Stories

Place YAML story files in `ai_review/user_stories/`:

```yaml
stories:
  - name: "Homepage loads correctly"
    url: "https://example.com"
    workflow: |
      Navigate to https://example.com
      Verify the page loads
      Verify the title contains "Example"
```

---

## Two Approaches

### Playwright-Bowser (Recommended for Testing)

- Headless by default
- Parallel sessions via named instances
- Token-efficient CLI
- CI/CD friendly

### Claude-Bowser (Recommended for Personal Use)

- Uses your real Chrome
- Observable (you can watch)
- Access to your cookies/extensions
- Single instance only

---

## Platform-Specific Notes

### Pi Differences from Original

- Uses Pi's skill system (same structure as original Claude Code)
- Agents use Pi's `subagent_type` system
- Commands use Pi's slash-command format
- Justfile recipes work identically

---

## Original Reference

This implementation is adapted from:
- **Original:** [github.com/disler/bowser](https://github.com/disler/bowser)
- **Author:** IndyDevDan ([@disler](https://github.com/disler))
- **Video:** [YouTube Breakdown](https://youtu.be/efctPj6bjCY)

---

*See [AGENTS.md](./AGENTS.md) for complete agent configuration reference.*