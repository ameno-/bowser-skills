#!/usr/bin/env python3
"""
Example: Simple Homepage Check

This example demonstrates basic browser tool usage.
Adapted from https://github.com/disler/bowser
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tools.bowser import (
    browser_open,
    browser_snapshot,
    browser_screenshot,
    browser_close,
    session_close_all
)


def check_homepage(url: str) -> dict:
    """
    Check if a homepage loads correctly.
    
    Args:
        url: URL to check
    
    Returns:
        Check results with snapshot and screenshot
    """
    session = "homepage-check"
    
    try:
        print(f"Opening {url}...")
        browser_open(
            url=url,
            session=session,
            headless=True,
            persistent=False
        )
        
        print("Getting page snapshot...")
        snapshot = browser_snapshot(session=session)
        
        print("Taking screenshot...")
        screenshot_result = browser_screenshot(
            session=session,
            filename="homepage.png"
        )
        
        # Check if page loaded (snapshot has content)
        loaded = len(snapshot) > 100  # Arbitrary threshold
        
        return {
            "url": url,
            "loaded": loaded,
            "snapshot_length": len(snapshot),
            "screenshot": screenshot_result["path"]
        }
        
    finally:
        print("Closing browser...")
        browser_close(session=session)


def main():
    """Run example."""
    # Clean up any existing sessions
    session_close_all()
    
    # Check example.com
    result = check_homepage("https://example.com")
    
    print("\n" + "="*50)
    print("RESULT:")
    print(f"  URL: {result['url']}")
    print(f"  Loaded: {result['loaded']}")
    print(f"  Snapshot: {result['snapshot_length']} chars")
    print(f"  Screenshot: {result['screenshot']}")
    print("="*50)


if __name__ == "__main__":
    main()
