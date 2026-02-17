# Bowser Skills - Test Environments

> Isolated test environments for Pi and Codex implementations.

## Overview

This directory contains isolated test environments for validating Bowser Skills implementations.

## Quick Start

### Run All Tests

```bash
./run-all-tests.sh
```

### Run Individual Tests

**Pi Implementation:**
```bash
cd pi-test
./run-tests.sh
```

**Codex Implementation:**
```bash
cd codex-test
./run-tests.sh
```

## Test Structure

### Pi Tests (`pi-test/`)

Tests the Pi agent harness implementation:
- Skill file structure validation
- Agent configuration validation
- Command workflow validation
- User story YAML parsing
- Justfile recipe validation
- Documentation completeness

**Test File:** `implementations/pi/tests/test_skills.py`

### Codex Tests (`codex-test/`)

Tests the Codex CLI implementation:
- Agent configuration schema
- Prompt pattern validation
- Tool specification format
- Documentation completeness
- Codex-specific integration patterns

**Test File:** `implementations/codex/tests/test_codex_bowser.py`

## Test Output

Results are saved to:
- `pi-test/test-output/results.txt`
- `codex-test/test-output/results.txt`

## Prerequisites

- Python 3.8+
- pytest (`pip install pytest`)
- pyyaml (`pip install pyyaml`)

## What Each Test Validates

### Pi Implementation

1. **Skill Structure**
   - Playwright and Claude skill files exist
   - Correct frontmatter format
   - Workflow sections present

2. **Agent Structure**
   - All agent files exist
   - QA agent has report format
   - Agents reference skills

3. **Command Structure**
   - UI review command exists
   - Hop automate exists
   - Workflow commands exist

4. **User Stories**
   - YAML parsing
   - Required fields
   - Format validation

5. **Justfile**
   - All layer recipes present
   - Layer 1-4 coverage

### Codex Implementation

1. **Agent Configurations**
   - AGENTS.md exists
   - Playwright and QA agents defined
   - Variable definitions present

2. **Prompt Patterns**
   - Skill invocation documented
   - Agent spawning documented
   - QA validation documented

3. **Tool Specifications**
   - JSON schema format
   - Required fields present

4. **Documentation**
   - README complete
   - AGENTS.md complete
   - Layer mapping documented

## Running in Isolation

Each test environment is self-contained and can be run independently:

```bash
# Pi tests only
cd pi-test
python3 -m pytest ../implementations/pi/tests/ -v

# Codex tests only
cd codex-test
python3 -m pytest ../implementations/codex/tests/ -v
```

## Manual Validation

To manually verify an implementation:

**Pi:**
```bash
cd implementations/pi
# Check files exist
ls skills/*/SKILL.md
ls agents/*.md
ls commands/*.md
```

**Codex:**
```bash
cd implementations/codex
# Check documentation
cat README.md | grep -A5 "Quick Start"
cat AGENTS.md | grep -A5 "Agent Definitions"
```

## Original Reference

- **Original:** [github.com/disler/bowser](https://github.com/disler/bowser)
- **Author:** IndyDevDan ([@disler](https://github.com/disler))
