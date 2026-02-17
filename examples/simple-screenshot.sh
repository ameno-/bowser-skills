#!/bin/bash
# Minimal screenshot test - just open a page and save screenshot

echo "Taking a simple screenshot..."

SESSION="simple-test"
mkdir -p screenshots

# Clean up
playwright-cli -s="$SESSION" close 2>/dev/null || true

# Open page and take screenshot
echo "Opening example.com..."
playwright-cli -s="$SESSION" open https://example.com --persistent

echo "Taking screenshot..."
playwright-cli -s="$SESSION" screenshot --filename="screenshots/test.png"

# Close
playwright-cli -s="$SESSION" close

# Check if screenshot exists
if [ -f "screenshots/test.png" ]; then
    echo "✅ Screenshot created: screenshots/test.png"
    ls -lh screenshots/test.png
    
    # Try to open it (macOS)
    if command -v open >/dev/null; then
        echo ""
        echo "Opening screenshot..."
        open screenshots/test.png
    fi
else
    echo "❌ Screenshot not found!"
    echo "Looking in: $(pwd)/screenshots/"
    ls -la screenshots/ 2>/dev/null || echo "Directory doesn't exist"
fi
