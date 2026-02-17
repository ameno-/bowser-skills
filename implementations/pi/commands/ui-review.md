---
model: opus
description: Parallel user story validation — discovers YAML stories, fans out bowser-qa-agents, aggregates results
argument-hint: [headed] [filename-filter] [vision]
---

# UI Review Command

## Purpose

Discover user stories from YAML files, fan out parallel `bowser-qa-agent` instances to validate each story, then aggregate and report pass/fail results with screenshots.

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HEADED` | `"false"` | Set to `"true"` for visible browser |
| `VISION` | `false` | Enable if `vision` keyword present |
| `FILENAME_FILTER` | `""` | Filter stories by filename substring |
| `STORIES_DIR` | `"ai_review/user_stories"` | YAML stories location |
| `AGENT_TIMEOUT` | `300000` | Agent timeout (ms) |

## Workflow

### Phase 1: Discover

1. Find all `.yaml` files in `STORIES_DIR`
2. Apply `FILENAME_FILTER` if provided
3. Parse each file's `stories` array
4. Generate unique `RUN_DIR`: `screenshots/bowser-qa/YYYYMMDD_HHMMSS_shortuuid/`

### Phase 2: Spawn

1. Create team via `TeamCreate`
2. Create `TaskCreate` entry per story
3. Spawn `bowser-qa-agent` per story (all in parallel)
4. Pass `SCREENSHOT_PATH` to each agent

### Phase 3: Collect

1. Wait for agent messages
2. Parse each report (look for `RESULT:` line)
3. Mark tasks complete via `TaskUpdate`

### Phase 4: Cleanup

1. Send `shutdown_request` to all agents
2. Call `TeamDelete`
3. Generate aggregated report

## Report Format

```markdown
# UI Review Summary

**Run:** {datetime}
**Stories:** {total} total | {passed} passed | {failed} failed
**Status:** ✅ ALL PASSED | ❌ PARTIAL FAILURE | ❌ ALL FAILED

## Results

| #   | Story        | Source File | Status | Steps            |
| --- | ------------ | ----------- | ------ | ---------------- |
| 1   | {story name} | {filename}  | ✅ PASS | {passed}/{total} |

## Failures
(Only if failures exist)

## Screenshots
All screenshots saved to: `{RUN_DIR}/`
```

## Usage

```bash
# Run all stories
pi "/ui-review"

# Run with visible browser
pi "/ui-review headed"

# Filter by filename
pi "/ui-review hackernews"

# Enable vision mode
pi "/ui-review vision"

# Combined
pi "/ui-review headed hackernews vision"
```

---

*Original implementation: [github.com/disler/bowser](https://github.com/disler/bowser)*
