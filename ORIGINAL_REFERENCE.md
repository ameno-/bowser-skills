# Original Bowser Reference

> Complete reference to the original [bowser](https://github.com/disler/bowser) project by [@disler](https://github.com/disler).

---

## Original Repository

- **Repository:** [github.com/disler/bowser](https://github.com/disler/bowser)
- **Author:** IndyDevDan ([@disler](https://github.com/disler))
- **YouTube:** [Breakdown Video](https://youtu.be/efctPj6bjCY)
- **License:** MIT

---

## Original Project Overview

B_owser is an **agentic browser automation and UI testing system** built with:
- Composable skills
- Subagent parallelization
- Command orchestration
- Justfile recipe layer

### Original Problem Statement

> No consistent agentic tooling for running browser automation and UI testing across tools and applications — agents need both observable (your browser) and headless (background) modes, configurable per-run settings, and true validation workflows with full user-level tooling.

### Original Solution

A composable, dual-purpose system with a four-layer architecture:
1. **Skill** drives the browser
2. **Subagent** wraps it for parallel execution
3. **Slash Command** orchestrates stories at scale
4. **Justfile** makes everything callable with one command

---

## Original Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  REUSABILITY — justfile recipes                                  │
├──────────────────────────────────────────────────────────────────┤
│  ORCHESTRATE — /ui-review command                                │
│  Discover YAML stories, fan out agents, aggregate results        │
├──────────────────────────────────────────────────────────────────┤
│  SCALE — bowser-qa-agent                                         │
│  Parse story → execute steps → screenshot → report               │
├──────────────────────────────────────────────────────────────────┤
│  CAPABILITY — playwright-bowser skill                            │
│  playwright-cli open, snapshot, click, fill, screenshot, close   │
└──────────────────────────────────────────────────────────────────┘
```

| Layer | Original Location | Purpose |
|-------|-------------------|---------|
| Skill | `.claude/skills/` | Browser capability |
| Subagent | `.claude/agents/` | Parallel execution |
| Command | `.claude/commands/` | Orchestration |
| Just | `justfile` | Reusability |

---

## Original File Structure

```
bowser/
├── README.md                    # Main documentation
├── TOOLS.md                     # Chrome MCP tool reference
├── justfile                     # Layer 4 - Reusability
│
├── .claude/
│   ├── skills/
│   │   ├── playwright-bowser/   # Headless browser skill
│   │   │   ├── SKILL.md
│   │   │   └── docs/
│   │   │       └── playwright-cli.md
│   │   ├── claude-bowser/       # Chrome MCP skill
│   │   │   └── SKILL.md
│   │   └── just/                # Just command runner skill
│   │       └── SKILL.md
│   │
│   ├── agents/
│   │   ├── playwright-bowser-agent.md
│   │   ├── claude-bowser-agent.md
│   │   └── bowser-qa-agent.md
│   │
│   └── commands/
│       ├── ui-review.md
│       ├── build.md
│       ├── list-tools.md
│       ├── prime.md
│       └── bowser/
│           ├── hop-automate.md
│           ├── amazon-add-to-cart.md
│           └── blog-summarizer.md
│
├── ai_review/
│   └── user_stories/
│       ├── hackernews.yaml
│       └── example-app.yaml
│
└── specs/
    └── init-automation.md
```

---

## Original Two-Browser Comparison

### Claude-Bowser (Chrome MCP)

| Aspect | Details |
|--------|---------|
| **Built for** | Personal workflow automation |
| **Browser** | Your real Chrome (observable) |
| **Parallel** | No — single shared instance |
| **Auth** | Uses your existing Chrome profile |
| **Startup** | Requires `--chrome` flag |
| **Token efficiency** | Lower (MCP tool schemas) |
| **Best for** | Personal automation, existing sessions |

### Playwright-Bowser (CLI)

| Aspect | Details |
|--------|---------|
| **Built for** | UI testing at scale |
| **Browser** | Headless Chromium (isolated) |
| **Parallel** | Yes (named sessions) |
| **Auth** | Persistent per session |
| **Startup** | Standard Claude Code |
| **Token efficiency** | Higher (CLI-based) |
| **Best for** | Scale, CI, testing, automation |

---

## Original Key Concepts

### 1. Named Sessions (Playwright)

```bash
# Derive session name from task context
playwright-cli -s=mystore-checkout open https://mystore.com --persistent
playwright-cli -s=mystore-checkout snapshot
playwright-cli -s=mystore-checkout click e12
playwright-cli -s=mystore-checkout close
```

### 2. User Stories (YAML)

```yaml
stories:
  - name: "Front page loads with posts"
    url: "https://news.ycombinator.com/"
    workflow: |
      Navigate to https://news.ycombinator.com/
      Verify the front page loads successfully
      Verify at least 10 posts are visible
```

### 3. Four-Layer Testing

```bash
# Layer 1: Skill direct
just test-playwright-skill

# Layer 2: Subagent
just test-playwright-agent

# Layer 3: Command
just ui-review

# Layer 4: Just recipe
just automate-amazon
```

---

## Original Dependencies

- [Claude Code](https://code.claude.com/) — Agent harness
- [playwright-cli](https://github.com/microsoft/playwright-cli) — Token-efficient Playwright CLI
- [just](https://github.com/casey/just) — Command runner (optional)

---

## Original Usage Patterns

### Direct Skill Execution
```bash
/playwright-bowser test the login flow on localhost:3000
/claude-bowser check my gmail for unread messages
```

### Subagent Spawning
```bash
# Task tool → subagent_type: playwright-bowser-agent
# prompt: "Verify the checkout flow"
```

### Orchestration Command
```bash
/ui-review                    # Run all YAML stories
/bowser:hop-automate <workflow>  # Run saved workflow
```

### Justfile Recipe
```bash
just ui-review                # Parallel QA
just hop <workflow>          # Saved workflow
just automate-amazon          # Demo automation
```

---

## Migration Notes

This cross-platform adaptation preserves:
- ✅ Four-layer architecture
- ✅ Two-browser approaches
- ✅ User story YAML format
- ✅ Session management patterns
- ✅ QA reporting structure

Adapted for:
- 🔄 Pi agent harness
- 🔄 Codex CLI
- 🔄 OpenClaw integration
- 🔄 CloudHub deployment

---

## Attribution

All architectural concepts, patterns, and original implementations are credited to:

**IndyDevDan** ([@disler](https://github.com/disler))
- YouTube: [@indydevdan](https://www.youtube.com/@indydevdan)
- GitHub: [github.com/disler](https://github.com/disler)
- Course: [Tactical Agentic Coding](https://agenticengineer.com/)

This migration project aims to make these excellent patterns available across multiple AI agent platforms while maintaining full credit and reference to the original work.

---

## License

The original bowser project is licensed under MIT. This migration maintains compatibility with the original license terms.

---

*Bowser — Agentic browser automation for the age of AI.*