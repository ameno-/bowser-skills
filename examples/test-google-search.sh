#!/bin/bash
# Test Google Search Automation
# Verifies bowser skills work by searching for "nike shoes" on Google
# Usage: ./test-google-search.sh [headless|headed]

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "============================================"
echo "Google Search Test - Bowser Skills"
echo "============================================"
echo ""

# Check playwright-cli
if ! command -v playwright-cli &> /dev/null; then
    echo -e "${RED}Error: playwright-cli not found${NC}"
    echo "Install with: npm install -g @playwright/cli@latest"
    exit 1
fi

echo -e "${GREEN}✓ playwright-cli found${NC}"

# Parse arguments
MODE="${1:-headless}"
SESSION="google-search-test"
SCREENSHOTS_DIR="./screenshots"

echo "Mode: $MODE"
echo "Session: $SESSION"
echo ""

# Create screenshots directory
mkdir -p "$SCREENSHOTS_DIR"

# Set viewport
export PLAYWRIGHT_MCP_VIEWPORT_SIZE="1440x900"

echo "============================================"
echo "Step 1: Open Google"
echo "============================================"
echo ""

if [ "$MODE" = "headed" ]; then
    echo "Opening browser (visible mode)..."
    playwright-cli -s="$SESSION" open https://google.com --persistent --headed
else
    echo "Opening browser (headless mode)..."
    playwright-cli -s="$SESSION" open https://google.com --persistent
fi

echo -e "${GREEN}✓ Google opened${NC}"
echo ""

echo "============================================"
echo "Step 2: Get Page Snapshot"
echo "============================================"
echo ""

SNAPSHOT=$(playwright-cli -s="$SESSION" snapshot)
echo "Page elements found:"
echo "$SNAPSHOT" | head -20
echo ""

# Find search input (usually 'e' or similar)
SEARCH_REF="e"
if echo "$SNAPSHOT" | grep -q "search"; then
    echo -e "${GREEN}✓ Found search input${NC}"
else
    echo -e "${YELLOW}⚠ Search input not clearly identified, will try 'e'${NC}"
fi
echo ""

echo "============================================"
echo "Step 3: Type 'nike shoes'"
echo "============================================"
echo ""

# Try to fill the search box
# Note: The ref 'e' is typically the search input on Google
if playwright-cli -s="$SESSION" fill "$SEARCH_REF" "nike shoes" 2>/dev/null; then
    echo -e "${GREEN}✓ Text entered successfully${NC}"
else
    echo -e "${YELLOW}⚠ Could not fill search box, trying alternative...${NC}"
    # Try typing directly
    playwright-cli -s="$SESSION" type "nike shoes"
fi
echo ""

echo "============================================"
echo "Step 4: Submit Search"
echo "============================================"
echo ""

playwright-cli -s="$SESSION" press Enter
echo -e "${GREEN}✓ Search submitted${NC}"
echo ""

# Wait for results
echo "Waiting for results to load..."
sleep 2

echo "============================================"
echo "Step 5: Take Screenshot"
echo "============================================"
echo ""

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SCREENSHOT_FILE="$SCREENSHOTS_DIR/nike-search-$TIMESTAMP.png"

playwright-cli -s="$SESSION" screenshot --filename="$SCREENSHOT_FILE"

if [ -f "$SCREENSHOT_FILE" ]; then
    echo -e "${GREEN}✓ Screenshot saved: $SCREENSHOT_FILE${NC}"
    ls -lh "$SCREENSHOT_FILE"
else
    echo -e "${RED}✗ Screenshot failed${NC}"
fi
echo ""

echo "============================================"
echo "Step 6: Cleanup"
echo "============================================"
echo ""

playwright-cli -s="$SESSION" close
echo -e "${GREEN}✓ Browser session closed${NC}"
echo ""

echo "============================================"
echo "Test Complete!"
echo "============================================"
echo ""
echo "Results:"
echo "  - Search term: nike shoes"
echo "  - Mode: $MODE"
echo "  - Screenshot: $SCREENSHOT_FILE"
echo ""

if [ -f "$SCREENSHOT_FILE" ]; then
    echo -e "${GREEN}✓ All steps completed successfully!${NC}"
    echo ""
    echo "To view the screenshot:"
    echo "  open $SCREENSHOT_FILE"
    exit 0
else
    echo -e "${RED}✗ Test completed but screenshot may have issues${NC}"
    exit 1
fi
