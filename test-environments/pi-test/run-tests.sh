#!/bin/bash
# Pi Bowser Skills - Isolated Test Runner
# Usage: ./run-tests.sh

set -e

echo "========================================="
echo "Pi Bowser Skills - Isolated Test Suite"
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
if [ ! -d ".pi" ]; then
    echo -e "${YELLOW}Warning: .pi directory not found${NC}"
    echo "Setting up isolated environment..."
    
    # Copy from parent
    if [ -d "../../implementations/pi" ]; then
        cp -r ../../implementations/pi/* .
        cp -r ../../shared .
        cp -r ../../workflows .
    else
        echo -e "${RED}Error: Cannot find implementation files${NC}"
        exit 1
    fi
fi

# Create test directories
mkdir -p test-output/screenshots

# Install test dependencies
echo "Installing test dependencies..."
pip install pyyaml pytest -q 2>/dev/null || pip3 install pyyaml pytest -q 2>/dev/null

echo ""
echo "========================================="
echo "Running Tests"
echo "========================================="
echo ""

# Run unit tests
python3 -m pytest ../implementations/pi/tests/ -v --tb=short 2>&1 | tee test-output/results.txt || true

# Check results
if grep -q "FAILED" test-output/results.txt; then
    echo ""
    echo -e "${RED}Some tests failed${NC}"
    exit 1
else
    echo ""
    echo -e "${GREEN}All tests passed!${NC}"
fi

echo ""
echo "========================================="
echo "Structure Validation"
echo "========================================="
echo ""

# Validate directory structure
echo "Validating directory structure..."

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1 (missing)"
    fi
}

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1 (missing)"
    fi
}

echo ""
echo "Skills:"
check_file ".pi/skills/playwright-bowser/SKILL.md"
check_file ".pi/skills/claude-bowser/SKILL.md"

echo ""
echo "Agents:"
check_file ".pi/agents/playwright-bowser-agent.md"
check_file ".pi/agents/claude-bowser-agent.md"
check_file ".pi/agents/bowser-qa-agent.md"

echo ""
echo "Commands:"
check_file ".pi/commands/ui-review.md"
check_file ".pi/commands/bowser/hop-automate.md"
check_file ".pi/commands/bowser/amazon-add-to-cart.md"

echo ""
echo "Documentation:"
check_file "README.md"
check_file "AGENTS.md"
check_file "justfile"

echo ""
echo "Shared Resources:"
check_file "shared/schemas/user-story-schema.yaml"
check_file "shared/examples/sample-user-stories/hackernews.yaml"

echo ""
echo "Workflows:"
check_file "workflows/e-commerce/amazon-add-to-cart.yaml"
check_file "workflows/testing/login-flow.yaml"

echo ""
echo "========================================="
echo "Test Complete"
echo "========================================="
echo ""
echo "Results saved to: test-output/results.txt"
