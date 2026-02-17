# Examples - Verification Tests

This directory contains simple tests to verify the bowser skills work correctly.

## Quick Start

The easiest way to verify everything works:

```bash
cd bowser-skills/examples

# Run the minimal test (just opens example.com and takes screenshot)
./simple-screenshot.sh
```

This will:
1. Open https://example.com
2. Take a screenshot
3. Save it to `screenshots/test.png`
4. Try to open it (on macOS)

## Test Scripts

### 1. `simple-screenshot.sh` - Minimal Test

**What it does:** Opens example.com and takes a screenshot

**Usage:**
```bash
./simple-screenshot.sh
```

**Output:**
```
✅ Screenshot created: screenshots/test.png
-rw-r--  1 user  staff  12K Feb 17 00:45 screenshots/test.png
Opening screenshot...
```

### 2. `verify-skills.sh` - Full Google Search Test

**What it does:** Searches for "nike shoes" on Google

**Usage:**
```bash
./verify-skills.sh
```

**Creates:**
- `screenshots/01-homepage.png` - Google homepage
- `screenshots/02-nike-results.png` - Search results

### 3. `minimal_screenshot.py` - Python Version

**What it does:** Same as simple-screenshot.sh but in Python

**Usage:**
```bash
python3 minimal_screenshot.py
```

**Shows:**
- Absolute path to screenshot
- File size
- Open command

### 4. `test-google-search.sh` - Original Test

**What it does:** Full test with detailed output

**Usage:**
```bash
./test-google-search.sh [headless|headed]
```

## Where Are Screenshots Saved?

All screenshots are saved to: `bowser-skills/examples/screenshots/`

**To find your screenshots:**
```bash
# Show absolute path
pwd
ls -la screenshots/

# On macOS, open the folder
open screenshots/
```

## Troubleshooting

### "playwright-cli not found"

Install it:
```bash
npm install -g @playwright/cli@latest
```

### Screenshot not created

1. Check if playwright-cli works:
```bash
playwright-cli --version
```

2. Try running with visible browser:
```bash
./test-google-search.sh headed
```

3. Check the error output - the scripts show detailed error messages

### Can't find the screenshot file

The scripts print the **absolute path** to the screenshot. Look for:
```
Screenshots will be saved to: /Users/.../bowser-skills/examples/screenshots
✅ Screenshot created: /Users/.../bowser-skills/examples/screenshots/test.png
```

### Permission denied

Make scripts executable:
```bash
chmod +x *.sh
```

## Manual Test

If scripts don't work, test manually:

```bash
# Open browser
playwright-cli -s=test open https://example.com --persistent

# Take screenshot
playwright-cli -s=test screenshot --filename=myshot.png

# Close
playwright-cli -s=test close

# Check if file exists
ls -la myshot.png
```

## Original Reference

- **Original:** [github.com/disler/bowser](https://github.com/disler/bowser)
- **Author:** IndyDevDan ([@disler](https://github.com/disler))
