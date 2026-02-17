#!/usr/bin/env python3
"""
Test Google Search - OpenClaw Implementation
Verifies bowser skills work by searching for "nike shoes" on Google

Usage:
    python test_google_search.py [headless|headed]

Requirements:
    - playwright-cli installed: npm install -g @playwright/cli
    - OpenClaw tools in PYTHONPATH
"""

import sys
import os
import time
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from implementations.openclaw.tools.bowser import (
        browser_open,
        browser_fill,
        browser_press,
        browser_snapshot,
        browser_screenshot,
        browser_close,
    )
except ImportError as e:
    print(f"Error importing tools: {e}")
    print("Make sure you're running from the bowser-skills directory")
    sys.exit(1)


def test_google_search(headless: bool = True) -> dict:
    """
    Test Google search for "nike shoes".
    
    Args:
        headless: Run browser without visible window
    
    Returns:
        Test results dictionary
    """
    session = "google-search-test"
    screenshots_dir = Path("./screenshots")
    screenshots_dir.mkdir(exist_ok=True)
    
    results = {
        "success": False,
        "steps": [],
        "screenshot": None,
        "errors": []
    }
    
    try:
        print("=" * 50)
        print("Step 1: Open Google")
        print("=" * 50)
        
        result = browser_open(
            url="https://www.google.com",
            session=session,
            headless=headless,
            persistent=True
        )
        print(f"✓ Browser opened: {result}")
        results["steps"].append("open_google")
        
        print()
        print("=" * 50)
        print("Step 2: Get Page Snapshot")
        print("=" * 50)
        
        snapshot = browser_snapshot(session=session)
        print(f"✓ Page snapshot captured ({len(snapshot)} chars)")
        print("First 500 chars of snapshot:")
        print(snapshot[:500])
        results["steps"].append("get_snapshot")
        
        print()
        print("=" * 50)
        print("Step 3: Fill Search Box")
        print("=" * 50)
        
        # Try to find the search input reference
        # On Google, it's often the first input element
        search_ref = "e"  # Common ref for Google search
        
        try:
            browser_fill(session=session, ref=search_ref, text="nike shoes")
            print(f"✓ Search text entered in ref '{search_ref}'")
            results["steps"].append("fill_search")
        except Exception as e:
            print(f"⚠ Could not fill search box: {e}")
            print("Trying alternative: type directly...")
            from implementations.openclaw.tools.bowser import browser_type
            browser_type(session=session, text="nike shoes")
            print("✓ Text typed directly")
            results["steps"].append("type_search")
        
        print()
        print("=" * 50)
        print("Step 4: Submit Search")
        print("=" * 50)
        
        browser_press(session=session, key="Enter")
        print("✓ Search submitted")
        results["steps"].append("submit_search")
        
        print()
        print("Waiting for results to load...")
        time.sleep(2)
        
        print()
        print("=" * 50)
        print("Step 5: Take Screenshot")
        print("=" * 50)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_file = screenshots_dir / f"nike-search-{timestamp}.png"
        
        result = browser_screenshot(
            session=session,
            filename=str(screenshot_file)
        )
        
        if Path(result["path"]).exists():
            print(f"✓ Screenshot saved: {result['path']}")
            file_size = Path(result["path"]).stat().st_size
            print(f"  Size: {file_size / 1024:.1f} KB")
            results["screenshot"] = result["path"]
            results["success"] = True
        else:
            results["errors"].append("Screenshot file not created")
        
        results["steps"].append("screenshot")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        results["errors"].append(str(e))
    
    finally:
        print()
        print("=" * 50)
        print("Step 6: Cleanup")
        print("=" * 50)
        
        try:
            browser_close(session=session)
            print("✓ Browser session closed")
            results["steps"].append("cleanup")
        except Exception as e:
            print(f"⚠ Cleanup error: {e}")
    
    return results


def main():
    """Main entry point."""
    print("=" * 50)
    print("Google Search Test - Bowser Skills")
    print("=" * 50)
    print()
    
    # Parse arguments
    mode = sys.argv[1] if len(sys.argv) > 1 else "headless"
    headless = mode != "headed"
    
    print(f"Mode: {'headless' if headless else 'headed (visible)'}")
    print()
    
    # Run test
    results = test_google_search(headless=headless)
    
    # Print summary
    print()
    print("=" * 50)
    print("Test Summary")
    print("=" * 50)
    print()
    
    if results["success"]:
        print("✓ All steps completed successfully!")
        print(f"  Screenshot: {results['screenshot']}")
        print()
        print(f"Steps executed ({len(results['steps'])}):")
        for step in results["steps"]:
            print(f"  ✓ {step}")
        return 0
    else:
        print("✗ Test encountered errors")
        print()
        if results["errors"]:
            print("Errors:")
            for error in results["errors"]:
                print(f"  ✗ {error}")
        print()
        print(f"Steps completed ({len(results['steps'])}):")
        for step in results["steps"]:
            print(f"  ✓ {step}")
        return 1


if __name__ == "__main__":
    sys.exit(main())


# Original implementation reference:
# Repository: https://github.com/disler/bowser
# Author: IndyDevDan (@disler)
