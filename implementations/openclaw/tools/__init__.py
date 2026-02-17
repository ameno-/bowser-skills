"""
OpenClaw Browser Tools

Browser automation tools using playwright-cli.
Adapted from https://github.com/disler/bowser
"""

from .bowser import (
    browser_open,
    browser_goto,
    browser_click,
    browser_fill,
    browser_type,
    browser_press,
    browser_snapshot,
    browser_screenshot,
    browser_console,
    browser_close,
    session_list,
    session_close_all,
    session_delete_data,
    browser_pdf,
    browser_evaluate,
)

__all__ = [
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
    "session_list",
    "session_close_all",
    "session_delete_data",
    "browser_pdf",
    "browser_evaluate",
]
