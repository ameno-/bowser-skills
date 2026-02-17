# Bowser Skills — Cross-Platform Browser Automation

> **A reusable, portable skillset for agentic browser automation across Pi, Codex, and OpenClaw.**

<p align="center">
  <img src="https://raw.githubusercontent.com/disler/bowser/main/images/bowser_11.jpg" width="600" />
</p>

---

## Overview

**Bowser Skills** is a cross-platform migration of the original [bowser](https://github.com/disler/bowser) project by [@disler](https://github.com/disler). It provides a consistent, four-layer architecture for browser automation that works across multiple AI agent platforms.

### Original Reference

- **Original Repository:** [github.com/disler/bowser](https://github.com/disler/bowser)
- **Original Author:** IndyDevDan ([@disler](https://github.com/disler))
- **License:** MIT (see [LICENSE](./LICENSE))
- **Video Walkthrough:** [YouTube Breakdown](https://youtu.be/efctPj6bjCY)

---

## The Four-Layer Architecture

Every Bowser implementation follows the same composable pattern:

```
┌──────────────────────────────────────────────────────────────────┐
│  LAYER 4 — REUSABILITY                                           │
│  Task runners, justfile recipes, one-command execution           │
│  just ui-review | make test | npm run e2e                        │
├──────────────────────────────────────────────────────────────────┤
│  LAYER 3 — ORCHESTRATION                                         │
│  Commands that discover, fan out, and aggregate                  │
│  /ui-review, /hop-automate, workflow runners                     │
├──────────────────────────────────────────────────────────────────┤
│  LAYER 2 — SCALE                                                 │
│  Subagents for parallel, isolated execution                      │
│  playwright-bowser-agent, bowser-qa-agent                        │
├──────────────────────────────────────────────────────────────────┤
│  LAYER 1 — CAPABILITY                                            │
│  Core browser automation skills                                  │
│  playwright-bowser, claude-bowser                                │
└──────────────────────────────────────────────────────────────────┘
```

| Layer | Purpose | Test In Isolation |
|-------|---------|-------------------|
| **Skill** | Browser capability | Run the skill directly |
| **Subagent** | Parallel execution | Spawn single agent |
| **Command** | Orchestration | Run one command |
| **Runner** | Reusability | One terminal command |

---

## Platform Implementations

Each platform has its own implementation directory with platform-specific adaptations:

### 🥧 [Pi Implementation](./implementations/pi/)
For the Pi agent harness. Uses Pi's skill/agent/command system.

### 🤖 [Codex Implementation](./implementations/codex/)
For OpenAI's Codex CLI. Uses Codex's prompt-based agent system.

### 🦞 [OpenClaw Implementation](./implementations/openclaw/)
For OpenClaw integration. Uses OpenClaw's `@tool` decorator pattern and plugin system.

---

## Two Browser Approaches

### Playwright-Bowser (Headless/Parallel)
- **Best for:** UI testing, CI/CD, parallel execution
- **Browser:** Isolated Chromium instances
- **Parallel:** Yes (named sessions)
- **Auth:** Persistent per-session profiles

### Claude-Bowser (Observable/Personal)
- **Best for:** Personal automation, existing sessions
- **Browser:** Your real Chrome profile
- **Parallel:** No (single instance)
- **Auth:** Uses your existing cookies

---

## Quick Start

### Choose Your Platform

```bash
# Pi users
cd implementations/pi
# Follow Pi-specific setup in Pi README

# Codex users
cd implementations/codex
# Follow Codex-specific setup in Codex README

# OpenClaw users
cd implementations/openclaw
# Follow OpenClaw-specific setup
```

### Common Workflow (All Platforms)

```bash
# Test a skill directly (Layer 1)
browser-skill open https://example.com

# Spawn an agent (Layer 2)
browser-agent "test the login flow"

# Run orchestration (Layer 3)
browser-orchestrate ui-review

# One command (Layer 4)
make browser-test
```

---

## Shared Resources

The [`shared/`](./shared/) directory contains platform-agnostic resources:

- **`shared/schemas/`** — YAML/JSON schemas for user stories, skills, and reports
- **`shared/examples/`** — Sample user stories and test cases
- **`shared/docs/`** — Architecture documentation and patterns

---

## Pre-Built Workflows

The [`workflows/`](./workflows/) directory contains reusable workflow templates:

| Category | Workflows |
|----------|-----------|
| **e-commerce** | Add to cart, checkout flows, price monitoring |
| **testing** | Login tests, form validation, navigation tests |
| **research** | Blog summarization, data extraction, archiving |

---

## Directory Structure

```
bowser-skills/
├── README.md                    # This file
├── AGENTS.md                    # Agent configuration reference
├── LICENSE                      # MIT license
├── ORIGINAL_REFERENCE.md        # Original bowser documentation
│
├── implementations/
│   ├── pi/                      # Pi agent harness
│   ├── codex/                   # OpenAI Codex CLI
│   └── openclaw/                # OpenClaw tools & plugins
│
├── shared/
│   ├── schemas/                 # Validation schemas
│   ├── examples/                # Sample stories/tests
│   └── docs/                    # Architecture docs
│
└── workflows/                   # Pre-built workflows
    ├── e-commerce/
    ├── testing/
    └── research/
```

---

## Contributing

When adding a new platform implementation:

1. Create `implementations/<platform>/`
2. Adapt each layer for the platform's paradigm
3. Include README.md and AGENTS.md
4. Reference original bowser implementation
5. Test all four layers independently

---

## Resources

- **Original Bowser:** [github.com/disler/bowser](https://github.com/disler/bowser)
- **Playwright CLI:** [github.com/microsoft/playwright-cli](https://github.com/microsoft/playwright-cli)
- **Pi Documentation:** See [Pi docs](https://github.com/mario pi docs)
- **Codex Documentation:** See OpenAI Codex CLI docs

---

## Acknowledgments

This project is a **cross-platform adaptation** of the original [**bowser**](https://github.com/disler/bowser) project by [**IndyDevDan**](https://github.com/disler) ([@disler](https://github.com/disler)).

All credit for the original four-layer architecture, skill patterns, agent concepts, and workflow ideas goes to the original author. This repository simply makes those excellent patterns available across multiple AI agent platforms.

- 🌟 **Original Repository:** [github.com/disler/bowser](https://github.com/disler/bowser)
- 📺 **Video Walkthrough:** [YouTube Breakdown](https://youtu.be/efctPj6bjCY)
- 🎓 **Learn More:** [Tactical Agentic Coding](https://agenticengineer.com/)

---

*Built for the age of agentic software engineering.*