"""
OpenClaw Browser Tools - Playwright CLI Integration
Adapted from https://github.com/disler/bowser

This module provides browser automation tools using playwright-cli.
"""

import subprocess
import os
import uuid
import re
from typing import Optional, Dict, Any, List
from datetime import datetime

try:
    from openclaw import tool, ToolError
except ImportError:
    # Fallback decorator for standalone use
    def tool(func):
        func._is_tool = True
        return func
    class ToolError(Exception):
        pass


# ============================================================================
# Session Management Helpers
# ============================================================================

def _generate_session_name(context: str = None) -> str:
    """Generate a kebab-case session name from context."""
    if context:
        name = re.sub(r'[^\w]+', '-', context.lower()).strip('-')
        return name[:30]
    return f"session-{uuid.uuid4().hex[:8]}"


def _build_env(viewport: str = "1440x900") -> Dict[str, str]:
    """Build environment variables for playwright-cli."""
    env = os.environ.copy()
    env["PLAYWRIGHT_MCP_VIEWPORT_SIZE"] = viewport
    return env


def _run_playwright(args: List[str], env: Dict[str, str] = None, timeout: int = 60) -> str:
    """Execute playwright-cli command."""
    cmd = ["playwright-cli"] + args
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env or os.environ.copy(),
            timeout=timeout
        )
        
        if result.returncode != 0:
            raise ToolError(f"playwright-cli failed: {result.stderr}")
        
        return result.stdout
    except subprocess.TimeoutExpired:
        raise ToolError(f"playwright-cli command timed out after {timeout}s")
    except FileNotFoundError:
        raise ToolError("playwright-cli not found. Install with: npm install -g @playwright/cli")


# ============================================================================
# Core Browser Tools
# ============================================================================

@tool
def browser_open(
    url: str,
    session: Optional[str] = None,
    headless: bool = True,
    persistent: bool = True,
    viewport: str = "1440x900"
) -> Dict[str, Any]:
    """
    Open a URL in a browser session.
    
    Args:
        url: The URL to open
        session: Named session (auto-generated if None)
        headless: Run without visible window
        persistent: Persist cookies/storage between calls
        viewport: Viewport size (e.g., "1440x900")
    
    Returns:
        {
            "session": "session-name",
            "url": "opened-url",
            "status": "success"
        }
    
    Example:
        >>> browser_open("https://example.com", session="my-test")
        {"session": "my-test", "url": "https://example.com", "status": "success"}
    """
    session = session or _generate_session_name(url)
    
    args = [f"-s={session}", "open", url]
    
    if persistent:
        args.append("--persistent")
    if not headless:
        args.append("--headed")
    
    env = _build_env(viewport)
    _run_playwright(args, env)
    
    return {
        "session": session,
        "url": url,
        "status": "success",
        "headless": headless,
        "persistent": persistent
    }


@tool
def browser_goto(session: str, url: str) -> Dict[str, Any]:
    """
    Navigate to a URL in an existing session.
    
    Args:
        session: Session name
        url: URL to navigate to
    
    Returns:
        {"session": "...", "url": "...", "status": "success"}
    """
    args = [f"-s={session}", "goto", url]
    _run_playwright(args)
    
    return {
        "session": session,
        "url": url,
        "status": "success"
    }


@tool
def browser_click(session: str, ref: str) -> Dict[str, Any]:
    """
    Click an element by reference.
    
    Args:
        session: Session name
        ref: Element reference from snapshot (e.g., "e12")
    
    Returns:
        {"session": "...", "ref": "...", "status": "success"}
    """
    args = [f"-s={session}", "click", ref]
    _run_playwright(args)
    
    return {
        "session": session,
        "ref": ref,
        "status": "success"
    }


@tool
def browser_fill(session: str, ref: str, text: str) -> Dict[str, Any]:
    """
    Fill a form input with text.
    
    Args:
        session: Session name
        ref: Element reference from snapshot
        text: Text to fill
    
    Returns:
        {"session": "...", "ref": "...", "text": "...", "status": "success"}
    """
    args = [f"-s={session}", "fill", ref, text]
    _run_playwright(args)
    
    return {
        "session": session,
        "ref": ref,
        "text": text,
        "status": "success"
    }


@tool
def browser_type(session: str, text: str) -> Dict[str, Any]:
    """
    Type text (not specific to a field).
    
    Args:
        session: Session name
        text: Text to type
    
    Returns:
        {"session": "...", "text": "...", "status": "success"}
    """
    args = [f"-s={session}", "type", text]
    _run_playwright(args)
    
    return {
        "session": session,
        "text": text,
        "status": "success"
    }


@tool
def browser_press(session: str, key: str) -> Dict[str, Any]:
    """
    Press a key.
    
    Args:
        session: Session name
        key: Key name (Enter, Tab, Escape, ArrowUp, etc.)
    
    Returns:
        {"session": "...", "key": "...", "status": "success"}
    """
    args = [f"-s={session}", "press", key]
    _run_playwright(args)
    
    return {
        "session": session,
        "key": key,
        "status": "success"
    }


@tool
def browser_snapshot(session: str) -> str:
    """
    Get a snapshot of the current page with element references.
    
    Args:
        session: Session name
    
    Returns:
        Accessibility tree with element refs (e12, e13, etc.)
    
    Example:
        >>> browser_snapshot("my-session")
        "- main [ref=e8]:\n  - heading \"Welcome\" [ref=e9]\n  - button \"Submit\" [ref=e12]"
    """
    args = [f"-s={session}", "snapshot"]
    return _run_playwright(args)


@tool
def browser_screenshot(
    session: str,
    filename: Optional[str] = None,
    full_page: bool = False
) -> Dict[str, Any]:
    """
    Capture a screenshot.
    
    Args:
        session: Session name
        filename: Output filename (auto-generated if None)
        full_page: Capture full page or just viewport
    
    Returns:
        {"path": "screenshot.png", "filename": "...", "status": "success"}
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
    
    args = [f"-s={session}", "screenshot", "--filename", filename]
    
    if full_page:
        args.append("--full-page")
    
    _run_playwright(args)
    
    return {
        "path": os.path.abspath(filename),
        "filename": filename,
        "status": "success"
    }


@tool
def browser_console(session: str) -> List[Dict[str, Any]]:
    """
    Get browser console messages.
    
    Args:
        session: Session name
    
    Returns:
        List of console messages with level, text, and source
    """
    args = [f"-s={session}", "console"]
    output = _run_playwright(args)
    
    # Parse console output (format depends on playwright-cli)
    messages = []
    for line in output.strip().split('\n'):
        if line.strip():
            messages.append({
                "text": line,
                "level": "log",  # Parse actual level if available
                "source": "console"
            })
    
    return messages


@tool
def browser_close(session: str) -> Dict[str, Any]:
    """
    Close a browser session.
    
    Args:
        session: Session name
    
    Returns:
        {"session": "...", "status": "closed"}
    """
    args = [f"-s={session}", "close"]
    _run_playwright(args)
    
    return {
        "session": session,
        "status": "closed"
    }


# ============================================================================
# Session Management Tools
# ============================================================================

@tool
def session_list() -> List[Dict[str, Any]]:
    """
    List all active browser sessions.
    
    Returns:
        List of sessions with name, status, and URL
    """
    args = ["list"]
    output = _run_playwright(args)
    
    sessions = []
    for line in output.strip().split('\n'):
        if line.strip() and not line.startswith('-'):
            # Parse session info (format: "session-name [status] url")
            parts = line.split(None, 2)
            if len(parts) >= 1:
                sessions.append({
                    "name": parts[0],
                    "status": parts[1] if len(parts) > 1 else "unknown",
                    "url": parts[2] if len(parts) > 2 else None
                })
    
    return sessions


@tool
def session_close_all() -> Dict[str, Any]:
    """
    Close all browser sessions.
    
    Returns:
        {"closed": N, "status": "success"}
    """
    args = ["close-all"]
    _run_playwright(args)
    
    return {
        "closed": "all",
        "status": "success"
    }


@tool
def session_delete_data(session: str) -> Dict[str, Any]:
    """
    Delete session data (cookies, storage).
    
    Args:
        session: Session name
    
    Returns:
        {"session": "...", "status": "data-deleted"}
    """
    args = [f"-s={session}", "delete-data"]
    _run_playwright(args)
    
    return {
        "session": session,
        "status": "data-deleted"
    }


# ============================================================================
# Advanced Tools
# ============================================================================

@tool
def browser_pdf(session: str, filename: Optional[str] = None) -> Dict[str, Any]:
    """
    Save page as PDF.
    
    Args:
        session: Session name
        filename: Output filename (auto-generated if None)
    
    Returns:
        {"path": "...", "filename": "...", "status": "success"}
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"page_{timestamp}.pdf"
    
    args = [f"-s={session}", "pdf", "--filename", filename]
    _run_playwright(args)
    
    return {
        "path": os.path.abspath(filename),
        "filename": filename,
        "status": "success"
    }


@tool
def browser_evaluate(session: str, script: str) -> Any:
    """
    Execute JavaScript in the browser.
    
    Args:
        session: Session name
        script: JavaScript code to execute
    
    Returns:
        Result of the JavaScript execution
    """
    args = [f"-s={session}", "run-code", script]
    output = _run_playwright(args)
    return output


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Core browser tools
    "browser_open",
    "browser_goto",
    "browser_click",
    "browser_fill",
    "browser_type",
    "browser_press",
    "browser_snapshot",
    "browser_screenshot",
    "browser_console",
    "browser_close",
    
    # Session management
    "session_list",
    "session_close_all",
    "session_delete_data",
    
    # Advanced tools
    "browser_pdf",
    "browser_evaluate",
]


# Original implementation reference:
# Repository: https://github.com/disler/bowser
# Author: IndyDevDan (@disler)
