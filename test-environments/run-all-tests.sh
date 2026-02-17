#!/bin/bash
# Bowser Skills - Comprehensive Test Runner
# Runs all tests for Pi and Codex implementations

set -e

echo "============================================"
echo "Bowser Skills - Comprehensive Test Suite"
echo "============================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOWSER_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TOTAL_PASSED=0
TOTAL_FAILED=0

run_pi_tests() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Testing Pi Implementation${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    cd "$SCRIPT_DIR/pi-test"
    
    # Setup isolated environment
    if [ ! -d ".pi" ]; then
        echo "Setting up Pi test environment..."
        mkdir -p .pi agents skills commands shared workflows
        cp -r "$BOWSER_DIR/implementations/pi/"* .pi/ 2>/dev/null || true
        cp -r "$BOWSER_DIR/shared/"* shared/ 2>/dev/null || true
        cp -r "$BOWSER_DIR/workflows/"* workflows/ 2>/dev/null || true
    fi
    
    # Install dependencies
    pip install pyyaml pytest -q 2>/dev/null || pip3 install pyyaml pytest -q 2>/dev/null || true
    
    # Run tests
    if python3 -m pytest "$BOWSER_DIR/implementations/pi/tests/" -v --tb=short 2>&1 | tee test-output/pi-results.txt; then
        echo -e "${GREEN}✓ Pi tests passed${NC}"
        TOTAL_PASSED=$((TOTAL_PASSED + 1))
    else
        echo -e "${RED}✗ Pi tests failed${NC}"
        TOTAL_FAILED=$((TOTAL_FAILED + 1))
    fi
    
    echo ""
}

run_codex_tests() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Testing Codex Implementation${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    cd "$SCRIPT_DIR/codex-test"
    
    # Setup isolated environment
    if [ ! -f "README.md" ]; then
        echo "Setting up Codex test environment..."
        cp -r "$BOWSER_DIR/implementations/codex/"* . 2>/dev/null || true
        cp -r "$BOWSER_DIR/shared/"* shared/ 2>/dev/null || true
        cp -r "$BOWSER_DIR/workflows/"* workflows/ 2>/dev/null || true
    fi
    
    # Install dependencies
    pip install pyyaml pytest -q 2>/dev/null || pip3 install pyyaml pytest -q 2>/dev/null || true
    
    # Run tests
    if python3 -m pytest "$BOWSER_DIR/implementations/codex/tests/" -v --tb=short 2>&1 | tee test-output/codex-results.txt; then
        echo -e "${GREEN}✓ Codex tests passed${NC}"
        TOTAL_PASSED=$((TOTAL_PASSED + 1))
    else
        echo -e "${RED}✗ Codex tests failed${NC}"
        TOTAL_FAILED=$((TOTAL_FAILED + 1))
    fi
    
    echo ""
}

validate_structure() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Validating Project Structure${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    cd "$BOWSER_DIR"
    
    # Check main files
    echo "Checking main documentation..."
    [ -f "README.md" ] && echo -e "${GREEN}✓${NC} README.md" || echo -e "${RED}✗${NC} README.md"
    [ -f "AGENTS.md" ] && echo -e "${GREEN}✓${NC} AGENTS.md" || echo -e "${RED}✗${NC} AGENTS.md"
    [ -f "LICENSE" ] && echo -e "${GREEN}✓${NC} LICENSE" || echo -e "${RED}✗${NC} LICENSE"
    [ -f "ORIGINAL_REFERENCE.md" ] && echo -e "${GREEN}✓${NC} ORIGINAL_REFERENCE.md" || echo -e "${RED}✗${NC} ORIGINAL_REFERENCE.md"
    
    echo ""
    echo "Checking Pi implementation..."
    [ -d "implementations/pi/skills/playwright-bowser" ] && echo -e "${GREEN}✓${NC} Pi Playwright skill" || echo -e "${RED}✗${NC} Pi Playwright skill"
    [ -d "implementations/pi/skills/claude-bowser" ] && echo -e "${GREEN}✓${NC} Pi Claude skill" || echo -e "${RED}✗${NC} Pi Claude skill"
    [ -f "implementations/pi/agents/bowser-qa-agent.md" ] && echo -e "${GREEN}✓${NC} Pi QA agent" || echo -e "${RED}✗${NC} Pi QA agent"
    [ -f "implementations/pi/justfile" ] && echo -e "${GREEN}✓${NC} Pi justfile" || echo -e "${RED}✗${NC} Pi justfile"
    
    echo ""
    echo "Checking Codex implementation..."
    [ -f "implementations/codex/README.md" ] && echo -e "${GREEN}✓${NC} Codex README" || echo -e "${RED}✗${NC} Codex README"
    [ -f "implementations/codex/AGENTS.md" ] && echo -e "${GREEN}✓${NC} Codex AGENTS.md" || echo -e "${RED}✗${NC} Codex AGENTS.md"
    
    echo ""
    echo "Checking OpenClaw implementation..."
    [ -f "implementations/openclaw/tools/bowser.py" ] && echo -e "${GREEN}✓${NC} OpenClaw tools" || echo -e "${RED}✗${NC} OpenClaw tools"
    [ -f "implementations/openclaw/agents/qa.py" ] && echo -e "${GREEN}✓${NC} OpenClaw agents" || echo -e "${RED}✗${NC} OpenClaw agents"
    
    echo ""
    echo "Checking shared resources..."
    [ -f "shared/schemas/user-story-schema.yaml" ] && echo -e "${GREEN}✓${NC} User story schema" || echo -e "${RED}✗${NC} User story schema"
    [ -f "shared/docs/architecture.md" ] && echo -e "${GREEN}✓${NC} Architecture docs" || echo -e "${RED}✗${NC} Architecture docs"
    
    echo ""
    echo "Checking workflows..."
    [ -f "workflows/e-commerce/amazon-add-to-cart.yaml" ] && echo -e "${GREEN}✓${NC} E-commerce workflows" || echo -e "${RED}✗${NC} E-commerce workflows"
    [ -f "workflows/testing/login-flow.yaml" ] && echo -e "${GREEN}✓${NC} Testing workflows" || echo -e "${RED}✗${NC} Testing workflows"
    
    echo ""
}

# Main execution
echo "Starting comprehensive test suite..."
echo ""

# Validate structure first
validate_structure

# Run tests
run_pi_tests
run_codex_tests

# Summary
echo "============================================"
echo "Test Summary"
echo "============================================"
echo ""
echo -e "${GREEN}Passed: $TOTAL_PASSED${NC}"
echo -e "${RED}Failed: $TOTAL_FAILED${NC}"
echo ""

if [ $TOTAL_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi
