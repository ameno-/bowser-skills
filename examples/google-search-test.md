# Google Search Test - Skill Verification

This document demonstrates how to test the Google search workflow to verify the skills are working correctly.

## Test: Search for "Nike Shoes" on Google

### Using Pi Implementation

#### Method 1: Direct Skill Usage

```bash
# Start Pi in the bowser-skills directory
pi

# Then use the skill directly:
/playwright-bowser
Navigate to https://www.google.com, search for "nike shoes", and take a screenshot of the results.
```

#### Method 2: Using the Hop Automate Command

```bash
# Add the workflow to the commands directory first:
mkdir -p .pi/commands/bowser
cp workflows/e-commerce/google-search.yaml .pi/commands/bowser/google-search.md

# Then in Pi:
/bowser:hop-automate google-search "nike shoes"

# Or with visible browser:
/bowser:hop-automate google-search "nike shoes" headed
```

#### Method 3: Using Justfile

```bash
# Add to justfile:
cat >> justfile << 'EOF'

# Google search demo
google-search query="nike shoes":
    pi --dangerously-skip-permissions --model opus "/bowser:hop-automate google-search '{{query}}'"
EOF

# Run it:
just google-search "nike shoes"
```

### Using Codex Implementation

```bash
# With Codex CLI:
codex "Use playwright-bowser-agent to go to google.com and search for nike shoes"

# Or using the workflow pattern:
codex "Execute the google-search workflow with query 'nike shoes'"
```

### Using OpenClaw Implementation

```python
# Test script for OpenClaw
from openclaw.tools.bowser import browser_open, browser_fill, browser_press, browser_screenshot, browser_close

def test_google_search():
    session = "google-test"
    
    try:
        # Open Google
        browser_open(url="https://google.com", session=session, headless=False)
        
        # Get snapshot to find search box
        snapshot = browser_snapshot(session=session)
        print("Page snapshot:", snapshot)
        
        # Fill search box (reference 'e' for search input)
        browser_fill(session=session, ref="e", text="nike shoes")
        
        # Press Enter
        browser_press(session=session, key="Enter")
        
        # Take screenshot
        result = browser_screenshot(session=session, filename="nike-search.png")
        print(f"Screenshot saved: {result['path']}")
        
    finally:
        browser_close(session=session)

if __name__ == "__main__":
    test_google_search()
```

## Expected Results

When the test runs successfully, you should see:

1. Browser opens https://www.google.com
2. "nike shoes" is typed into the search box
3. Search results page loads
4. Screenshot is saved to `./screenshots/` or current directory

## Verification Checklist

- [ ] Browser opens without errors
- [ ] Page loads successfully
- [ ] Search input is found and filled
- [ ] Search executes (Enter key works)
- [ ] Results page loads
- [ ] Screenshot is captured
- [ ] Browser session closes cleanly

## Troubleshooting

### If search box not found:
- Check the snapshot output for the correct element reference
- Google may have different refs (e.g., "e4", "e8", "input-search")

### If headless mode fails:
- Try with `--headed` flag to see what's happening
- Check that playwright-cli is installed: `npm install -g @playwright/cli`

### If screenshot fails:
- Ensure the screenshots directory exists: `mkdir -p screenshots`
- Check write permissions in the directory

## Original Reference

- **Original:** [github.com/disler/bowser](https://github.com/disler/bowser)
- **Author:** IndyDevDan ([@disler](https://github.com/disler))
