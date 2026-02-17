# Bowser Skills Architecture

> Cross-platform browser automation architecture based on the original [bowser](https://github.com/disler/bowser) project.

---

## The Four-Layer Architecture

Bowser Skills implements a consistent four-layer architecture across all platforms:

```
┌──────────────────────────────────────────────────────────────────┐
│  LAYER 4 — REUSABILITY                                           │
│  One-command execution, task runners, CI/CD integration          │
│  just, make, npm scripts, cloud functions                        │
├──────────────────────────────────────────────────────────────────┤
│  LAYER 3 — ORCHESTRATION                                         │
│  Discover, fan out, aggregate                                    │
│  /ui-review, hop-automate, workflow runners                      │
├──────────────────────────────────────────────────────────────────┤
│  LAYER 2 — SCALE                                                 │
│  Parallel, isolated execution                                    │
│  playwright-bowser-agent, bowser-qa-agent                        │
├──────────────────────────────────────────────────────────────────┤
│  LAYER 1 — CAPABILITY                                            │
│  Core browser automation                                         │
│  playwright-bowser, claude-bowser                                │
└──────────────────────────────────────────────────────────────────┘
```

### Why Four Layers?

Each layer has **one job** and delegates down:

1. **Layer 1 (Skill)** — Knows *how* to automate the browser
2. **Layer 2 (Agent)** — Knows *how to scale* that capability
3. **Layer 3 (Command)** — Knows *how to orchestrate* multiple agents
4. **Layer 4 (Runner)** — Knows *how to invoke* everything

**Key insight:** You can enter at any layer. Test a skill directly, spawn one agent, run a command, or fire a one-liner.

---

## Layer 1: Capability (Skills)

### Purpose

Provide raw browser automation capability through a consistent interface.

### Two Browser Approaches

#### Playwright-Bowser

| Aspect | Details |
|--------|---------|
| **Provider** | Playwright CLI (`playwright-cli`) |
| **Browser** | Headless Chromium |
| **Sessions** | Named, parallel, isolated |
| **Best For** | Testing, CI/CD, scraping |
| **Token Efficiency** | High (CLI-based) |

```bash
# Named session workflow
playwright-cli -s=my-test open https://example.com --persistent
playwright-cli -s=my-test snapshot
playwright-cli -s=my-test click e12
playwright-cli -s=my-test close
```

#### Claude-Bowser

| Aspect | Details |
|--------|---------|
| **Provider** | Chrome MCP (`mcp__claude_in_chrome__*`) |
| **Browser** | Your real Chrome |
| **Sessions** | Single, shared |
| **Best For** | Personal automation, existing logins |
| **Token Efficiency** | Lower (MCP tool schemas) |

```
# Chrome MCP workflow
mcp__claude_in_chrome__navigate
tabId: 1, url: "https://example.com"

mcp__claude_in_chrome__read_page
tabId: 1, depth: 10
```

### Skill Interface

All skills expose:

```typescript
interface BrowserSkill {
  // Navigation
  open(url: string): Promise<void>;
  goto(url: string): Promise<void>;
  
  // Interaction
  click(ref: string): Promise<void>;
  fill(ref: string, text: string): Promise<void>;
  type(text: string): Promise<void>;
  press(key: string): Promise<void>;
  
  // Information
  snapshot(): Promise<PageSnapshot>;
  
  // Capture
  screenshot(path?: string): Promise<string>;
  pdf(path?: string): Promise<string>;
  
  // Debug
  console(): Promise<ConsoleMessage[]>;
  network(): Promise<NetworkRequest[]>;
  
  // Lifecycle
  close(): Promise<void>;
}
```

---

## Layer 2: Scale (Agents)

### Purpose

Wrap skills for parallel, isolated execution with structured reporting.

### Agent Types

#### Playwright Bowser Agent

- Thin wrapper around playwright-bowser skill
- One task = one agent = one isolated session
- Can spawn N agents for N parallel tasks

#### Bowser QA Agent

- Specialized for user story validation
- Parses stories into steps
- Screenshots every step
- Structured PASS/FAIL reporting

### Agent Lifecycle

```
Spawn → Parse Task → Execute Steps → Capture Results → Report → Cleanup
```

### Parallel Execution Model

```
Orchestrator
├── Agent 1 (Session A) → Story 1
├── Agent 2 (Session B) → Story 2
├── Agent 3 (Session C) → Story 3
└── ...
```

Each agent:
- Runs in isolation
- Has its own browser session
- Produces independent results
- Reports back to orchestrator

---

## Layer 3: Orchestration (Commands)

### Purpose

Coordinate multiple agents to execute complex workflows.

### UI Review Orchestrator

**Workflow:**
1. Discover YAML story files
2. Parse all stories
3. Create execution team
4. Spawn QA agent per story (all parallel)
5. Collect results as agents complete
6. Aggregate into summary report
7. Cleanup team

**Parallelism:** N stories = N simultaneous agents

### Hop Automate

**Workflow:**
1. Parse workflow name and arguments
2. Load workflow definition
3. Resolve skill/mode/vision settings
4. Execute with resolved skill
5. Return results

### Story Discovery

Stories are YAML files with `stories` array:

```yaml
stories:
  - name: "Story name"
    url: "https://example.com"
    workflow: |
      Step 1
      Step 2
      Step 3
```

---

## Layer 4: Reusability (Runners)

### Purpose

Make everything callable with a single command.

### Implementations

| Platform | Runner | Example |
|----------|--------|---------|
| Pi | justfile | `just ui-review` |
| Codex | Makefile | `make test` |
| OpenClaw | CLI | `openclaw workflow run` |
| CloudHub | Function | `cloudhub workflows invoke` |

### Justfile Recipes (Example)

```makefile
# Layer 1: Skills
just test-playwright-skill

# Layer 2: Agents
just test-playwright-agent

# Layer 3: Commands
just ui-review

# Layer 4: Full workflows
just automate-amazon
```

---

## Cross-Platform Adaptation

### Platform Mapping

| Concept | Pi | Codex | OpenClaw | CloudHub |
|---------|-----|-------|----------|----------|
| **Skill** | `.pi/skills/SKILL.md` | System prompt + tools | Tool collection | Serverless function |
| **Agent** | `.pi/agents/AGENT.md` | Agent prompt | State machine | Stateful function |
| **Command** | `.pi/commands/CMD.md` | Command prompt | Workflow | Orchestrator function |
| **Runner** | `justfile` | `Makefile` | CLI + config | Cloud CLI |

### Shared Components

All platforms share:
- **User Story Schema** — YAML format for test stories
- **Skill Schema** — Skill definition structure
- **Sample Stories** — Example user stories
- **Architecture Patterns** — This document

---

## Data Flow

```
User Input
    ↓
Layer 4: Runner (just, make, CLI)
    ↓
Layer 3: Orchestrator
    ↓ (fans out)
Layer 2: Agents (N parallel)
    ↓ (each delegates to)
Layer 1: Skills
    ↓
Browser (Playwright / Chrome)
    ↓
Results flow back up → Aggregated Report
```

---

## Session Management

### Playwright Sessions

```bash
# Create named session
playwright-cli -s=session-name open https://example.com --persistent

# Use existing session
playwright-cli -s=session-name snapshot
playwright-cli -s=session-name click e12

# Close session
playwright-cli -s=session-name close
```

**Benefits:**
- Isolated cookie/storage state
- Parallel execution
- Persistent profiles

### Chrome MCP

```
# Single shared session via Chrome extension
mcp__claude_in_chrome__tabs_context_mcp
# Uses existing Chrome profile
```

**Limitations:**
- Single instance only
- No parallel execution
- Shares your real browser

---

## Screenshot & Artifact Management

### Directory Structure

```
screenshots/
└── bowser-qa/
    └── 20260210_143022_a1b2c3/     # Run directory
        ├── hackernews/              # Source file stem
        │   ├── front-page-loads/
        │   │   ├── 00_navigate.png
        │   │   ├── 01_verify-page.png
        │   │   └── 02_verify-posts.png
        │   └── navigate-to-page-two/
        └── example-app/
            └── ...
```

### Naming Convention

- **Run directory:** `YYYYMMDD_HHMMSS_shortuuid`
- **Story directory:** `source-file/story-name/`
- **Screenshots:** `##_step-name.png` (zero-padded)

---

## Testing the Architecture

### Test Each Layer

```bash
# Layer 1: Test skill directly
just test-playwright-skill

# Layer 2: Test single agent
just test-qa

# Layer 3: Test orchestration
just ui-review

# Layer 4: Test full workflow
just automate-amazon
```

### Test in Isolation

Each layer should be testable independently:
- Skills don't depend on agents
- Agents don't depend on orchestrators
- Orchestrators can use mock agents

---

## Best Practices

1. **Always use named sessions** (Playwright) — Derive from task context
2. **Always close sessions** — Don't leave browsers hanging
3. **Screenshot every step** (QA) — Full audit trail
4. **Parse stories defensively** — Handle various formats
5. **Report structured results** — Tables, not prose
6. **Handle failures gracefully** — Capture errors, continue where possible
7. **Test at every layer** — Verify each layer independently

---

## Original Reference

This architecture is derived from:

- **Original:** [github.com/disler/bowser](https://github.com/disler/bowser)
- **Author:** IndyDevDan ([@disler](https://github.com/disler))
- **Video:** [YouTube Breakdown](https://youtu.be/efctPj6bjCY)

---

*Built for the age of agentic software engineering.*
