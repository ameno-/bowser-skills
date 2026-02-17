#!/bin/bash
# Simple verification that bowser skills work
# This creates a screenshot you can actually see

set -e

echo "============================================"
echo "Bowser Skills Verification"
echo "============================================"
echo ""

# Check if playwright-cli exists
if ! command -v playwright-cli > /dev/null 2>&1; then
    echo "❌ playwright-cli not found!"
    echo ""
    echo "Install it with:"
    echo "  npm install -g @playwright/cli@latest"
    exit 1
fi

echo "✓ playwright-cli found"
echo ""

# Set up paths
SESSION="verify-test"
# Use absolute path for screenshots
SCREENSHOTS_DIR="$(pwd)/screenshots"
mkdir -p "$SCREENSHOTS_DIR"

echo "Screenshots will be saved to: $SCREENSHOTS_DIR"
echo ""

# Clean up any existing session
echo "Cleaning up any existing sessions..."
playwright-cli -s="$SESSION" close 2>/dev/null || true
playwright-cli close-all 2>/dev/null || true

echo ""
echo "Step 1: Opening Google..."
playwright-cli -s="$SESSION" open https://google.com --persistent

echo "Step 2: Taking screenshot of homepage..."
HOMEPAGE_SHOT="$SCREENSHOTS_DIR/01-homepage.png"
playwright-cli -s="$SESSION" screenshot --filename="$HOMEPAGE_SHOT"

if [ -f "$HOMEPAGE_SHOT" ]; then
    echo "  ✓ Homepage screenshot saved: $HOMEPAGE_SHOT"
    ls -lh "$HOMEPAGE_SHOT"
else
    echo "  ⚠ Homepage screenshot not found at expected location"
fi

echo ""
echo "Step 3: Typing 'nike shoes'..."
# Try to click/fill the search box - use 'e' which is usually the first input
playwright-cli -s="$SESSION" fill e "nike shoes" 2>/dev/null || \
    playwright-cli -s="$SESSION" type "nike shoes"

echo "Step 4: Submitting search..."
playwright-cli -s="$SESSION" press Enter

echo "Step 5: Waiting for results..."
sleep 3

echo "Step 6: Taking screenshot of results..."
RESULTS_SHOT="$SCREENSHOTS_DIR/02-nike-results.png"
playwright-cli -s="$SESSION" screenshot --filename="$RESULTS_SHOT"

if [ -f "$RESULTS_SHOT" ]; then
    echo "  ✓ Results screenshot saved: $RESULTS_SHOT"
    ls -lh "$RESULTS_SHOT"
else
    echo "  ⚠ Results screenshot not found"
fi

echo ""
echo "Step 7: Closing browser..."
playwright-cli -s="$SESSION" close

echo ""
echo "============================================"
echo "Verification Complete!"
echo "============================================"
echo ""
echo "Check these files:"
echo "  1. $HOMEPAGE_SHOT"
echo "  2. $RESULTS_SHOT"
echo ""

# List all screenshots
echo "All screenshots in $SCREENSHOTS_DIR:"
ls -lh "$SCREENSHOTS_DIR/"*.png 2>/dev/null || echo "  (no png files found)"
echo ""

# Check if screenshots exist
if [ -f "$RESULTS_SHOT" ]; then
    echo "✅ SUCCESS! Screenshot created."
    echo ""
    echo "To view it, run:"
    echo "  open '$RESULTS_SHOT'"
else
    echo "❌ Screenshot was not created"
    exit 1
fi
