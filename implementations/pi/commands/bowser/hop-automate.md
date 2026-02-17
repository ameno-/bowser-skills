---
model: opus
description: Run a saved browser automation workflow with configurable skill, mode, and vision settings
argument-hint: <workflow-name> [prompt] [playwright|claude] [headed|headless] [vision]
---

# Hop Automate

Run a saved browser automation workflow from `.pi/commands/bowser/` with configurable defaults and overrides.

## Variables

| Variable | Detection | Default |
|----------|-----------|---------|
| `WORKFLOW` | `$1` (required) | — |
| `SKILL` | `claude`/`playwright` | `playwright-bowser` |
| `MODE` | `headed`/`headless` | `headless` |
| `VISION` | `vision` keyword | `false` |
| `PROMPT` | Remaining text | `""` |

## Workflow

### Phase 1: Parse and Validate

1. If no arguments, list available workflows
2. Extract `WORKFLOW` from first argument
3. Verify `.pi/commands/bowser/{WORKFLOW}.md` exists
4. Parse keywords and collect `PROMPT`

### Phase 2: Load Workflow

1. Read workflow file
2. Check frontmatter for `defaults:`
3. Keyword overrides take priority

### Phase 3: Execute

Execute resolved skill with combined prompt:
```
(headed: {MODE}) (vision: {VISION})

{workflow content with {PROMPT} replaced}
```

### Phase 4: Report

Report:
- Workflow name
- Skill and mode used
- Skill output/results

## Adding Workflows

1. Create `.md` file in `.pi/commands/bowser/`
2. Add frontmatter with optional `defaults:`
3. Include `{PROMPT}` placeholder in content
4. Available immediately via hop-automate

## Usage

```bash
# List workflows
pi "/bowser:hop-automate"

# Run workflow
pi "/bowser:hop-automate amazon-add-to-cart 'mechanical keyboard'"

# Override defaults
pi "/bowser:hop-automate amazon-add-to-cart 'keyboard' playwright headless"

# Use Chrome
pi "/bowser:hop-automate amazon-add-to-cart 'keyboard' claude headed"
```

---

*Original implementation: [github.com/disler/bowser](https://github.com/disler/bowser)*
