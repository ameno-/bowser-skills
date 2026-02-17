#!/usr/bin/env python3
"""
Minimal screenshot test - verifies playwright-cli works
"""

import subprocess
import os
from pathlib import Path

print("=" * 50)
print("Minimal Screenshot Test")
print("=" * 50)
print()

# Setup
session = "minimal-test"
screenshots_dir = Path("screenshots")
screenshots_dir.mkdir(exist_ok=True)

screenshot_path = screenshots_dir / "minimal-test.png"

# Clean up existing session
print("Cleaning up...")
subprocess.run(["playwright-cli", "-s", session, "close"], 
               capture_output=True)

try:
    # Open page
    print("Opening example.com...")
    result = subprocess.run(
        ["playwright-cli", f"-s={session}", "open", "https://example.com", "--persistent"],
        capture_output=True,
        text=True,
        check=True
    )
    print("✓ Page opened")
    
    # Take screenshot
    print(f"Taking screenshot...")
    result = subprocess.run(
        ["playwright-cli", f"-s={session}", "screenshot", "--filename", str(screenshot_path)],
        capture_output=True,
        text=True,
        check=True
    )
    print("✓ Screenshot command executed")
    
    # Close
    print("Closing browser...")
    subprocess.run(["playwright-cli", f"-s={session}", "close"], 
                   capture_output=True)
    
    # Check if file exists
    print()
    print("=" * 50)
    print("Results")
    print("=" * 50)
    print()
    
    if screenshot_path.exists():
        size = screenshot_path.stat().st_size
        print(f"✅ Screenshot created!")
        print(f"   Path: {screenshot_path.absolute()}")
        print(f"   Size: {size / 1024:.1f} KB")
        print()
        print(f"To view: open {screenshot_path}")
    else:
        print("❌ Screenshot file not found!")
        print(f"   Expected: {screenshot_path.absolute()}")
        print()
        print("Directory contents:")
        for f in screenshots_dir.iterdir():
            print(f"   {f.name}")
            
except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
    print(f"stdout: {e.stdout}")
    print(f"stderr: {e.stderr}")
except FileNotFoundError:
    print("❌ playwright-cli not found!")
    print("Install: npm install -g @playwright/cli@latest")
