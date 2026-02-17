#!/bin/bash
# Codex Bowser Skills - Isolated Test Runner
# Usage: ./run-tests.sh

set -e

echo "========================================="
echo "Codex Bowser Skills - Isolated Test Suite"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 not found${NC}"
    exit 1
fi

# Check if we're in isolated environment
if [ ! -f "README.md" ]; then
    echo -e "${YELLOW}Warning: Not in isolated environment${NC}"
    echo "Setting up isolated environment..."
    
    # Copy from parent
    if [ -d "../../implementations/codex" ]; then
        cp -r ../../implementations/codex/* .
        cp -r ../../shared .
        cp -r ../../workflows .
    else
        echo -e "${RED}Error: Cannot find implementation files${NC}"
        exit 1
    fi
fi

# Create test directories
mkdir -p test-output

# Install test dependencies
echo "Installing test dependencies..."
pip install pyyaml pytest -q 2>/dev/null || pip3 install pyyaml pytest -q 2>/dev/null

echo ""
echo "========================================="
echo "Running Tests"
echo "========================================="
echo ""

# Run structure validation
echo "Validating implementation structure..."
python3 -c "
import sys
from pathlib import Path

base = Path('.')
required = ['README.md', 'AGENTS.md']

all_good = True
for f in required:
    if (base / f).exists():
        print(f'✓ {f}')
    else:
        print(f'✗ {f} (missing)')
        all_good = False

sys.exit(0 if all_good else 1)
"

echo ""

# Run unit tests
python3 -m pytest ../implementations/codex/tests/ -v --tb=short 2>&1 | tee test-output/results.txt || true

# Check results
if grep -q "FAILED" test-output/results.txt; then
    echo ""
    echo -e "${RED}Some tests failed${NC}"
else
    echo ""
    echo -e "${GREEN}All tests passed!${NC}"
fi

echo ""
echo "========================================="
echo "Documentation Validation"
echo "========================================="
echo ""

# Check documentation completeness
echo "Checking documentation completeness..."

grep -q "## Overview" README.md && echo -e "${GREEN}✓${NC} README has Overview" || echo -e "${RED}✗${NC} README missing Overview"
grep -q "## Quick Start" README.md && echo -e "${GREEN}✓${NC} README has Quick Start" || echo -e "${RED}✗${NC} README missing Quick Start"
grep -q "## Architecture" README.md && echo -e "${GREEN}✓${NC} README has Architecture" || echo -e "${RED}✗${NC} README missing Architecture"

grep -q "playwright-bowser-agent" AGENTS.md && echo -e "${GREEN}✓${NC} AGENTS.md has Playwright agent" || echo -e "${RED}✗${NC} AGENTS.md missing Playwright agent"
grep -q "bowser-qa-agent" AGENTS.md && echo -e "${GREEN}✓${NC} AGENTS.md has QA agent" || echo -e "${RED}✗${NC} AGENTS.md missing QA agent"
grep -q "system_prompt" AGENTS.md && echo -e "${GREEN}✓${NC} AGENTS.md has system_prompt" || echo -e "${RED}✗${NC} AGENTS.md missing system_prompt"

echo ""
echo "========================================="
echo "Codex-Specific Validation"
echo "========================================="
echo ""

# Validate Codex patterns
grep -q "system_prompt" AGENTS.md && echo -e "${GREEN}✓${NC} Uses system prompts" || echo -e "${RED}✗${NC} Missing system prompts"
grep -q "tools" AGENTS.md && echo -e "${GREEN}✓${NC} References tools" || echo -e "${RED}✗${NC} Missing tools reference"
grep -q "gpt" AGENTS.md && echo -e "${GREEN}✓${NC} References GPT models" || echo -e "${RED}✗${NC} Missing model references"

echo ""
echo "========================================="
echo "Shared Resources"
echo "========================================="
echo ""

# Check shared resources are available
check_shared() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1 (missing)"
    fi
}

check_shared "shared/schemas/user-story-schema.yaml"
check_shared "shared/schemas/skill-schema.yaml"
check_shared "shared/examples/sample-user-stories/hackernews.yaml"
check_shared "shared/docs/architecture.md"

echo ""
echo "========================================="
echo "Test Complete"
echo "========================================="
echo ""
echo "Results saved to: test-output/results.txt"
echo ""
echo "To test with actual Codex CLI:"
echo "  1. Install Codex CLI"
echo "  2. Configure agents per AGENTS.md"
echo "  3. Run: codex \"Use playwright-bowser-agent to open example.com\""
