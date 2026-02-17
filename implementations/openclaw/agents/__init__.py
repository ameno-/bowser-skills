"""
OpenClaw Browser Agents

Agent implementations for browser automation.
Adapted from https://github.com/disler/bowser
"""

try:
    from .qa import BrowserQAAgent
    __all__ = ["BrowserQAAgent"]
except ImportError:
    __all__ = []
