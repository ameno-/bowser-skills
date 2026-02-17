# OpenClaw Agent & Tool Reference

> Complete tool and agent documentation for OpenClaw Bowser Skills.

---

## Tools (Layer 1)

Tools are Python functions decorated with `@tool`. They provide browser automation capabilities.

### Browser Tools

#### `browser_open`

```python
from openclaw import tool

@tool
def browser_open(
    url: str,
    session: str = None,
    headless: bool = True,
    persistent: bool = True,
    viewport: str = "1440x900"
) -> dict:
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
    """
```

**Usage:**
```python
result = browser_open(
    url="https://example.com",
    session="my-test",
    headless=True
)
```

---

#### `browser_goto`

```python
@tool
def browser_goto(session: str, url: str) -> dict:
    """Navigate to a URL in an existing session."""
```

---

#### `browser_click`

```python
@tool
def browser_click(session: str, ref: str) -> dict:
    """
    Click an element by reference.
    
    Args:
        session: Session name
        ref: Element reference from snapshot
    """
```

---

#### `browser_fill`

```python
@tool
def browser_fill(session: str, ref: str, text: str) -> dict:
    """Fill a form input with text."""
```

---

#### `browser_type`

```python
@tool
def browser_type(session: str, text: str) -> dict:
    """Type text (not specific to a field)."""
```

---

#### `browser_press`

```python
@tool
def browser_press(session: str, key: str) -> dict:
    """
    Press a key.
    
    Args:
        key: Key name (Enter, Tab, Escape, etc.)
    """
```

---

#### `browser_snapshot`

```python
@tool
def browser_snapshot(session: str) -> str:
    """
    Get a snapshot of the current page with element references.
    
    Returns:
        Accessibility tree with element refs (e12, e13, etc.)
    """
```

---

#### `browser_screenshot`

```python
@tool
def browser_screenshot(session: str, filename: str = None) -> dict:
    """
    Capture a screenshot.
    
    Args:
        filename: Output filename (auto-generated if None)
    
    Returns:
        {"path": "screenshot.png", "url": "artifact-url"}
    """
```

---

#### `browser_console`

```python
@tool
def browser_console(session: str) -> list:
    """Get browser console messages."""
```

---

#### `browser_close`

```python
@tool
def browser_close(session: str) -> dict:
    """Close a browser session."""
```

---

### Session Management Tools

#### `session_list`

```python
@tool
def session_list() -> list:
    """List all active browser sessions."""
```

#### `session_close_all`

```python
@tool
def session_close_all() -> dict:
    """Close all browser sessions."""
```

---

## Agents (Layer 2)

Agents are Python classes decorated with `@agent`. They orchestrate tool calls for complex tasks.

### Browser QA Agent

```python
from openclaw import agent, tool
from typing import List
import uuid
import os

@agent
class BrowserQAAgent:
    """
    QA validation agent for browser user stories.
    
    Executes user stories step-by-step with screenshot reporting.
    """
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.screenshots_dir = self.config.get(
            "screenshots_dir", 
            "./screenshots/bowser-qa"
        )
        self.headed = self.config.get("headed", False)
        self.vision = self.config.get("vision", False)
    
    def run(self, story: dict) -> dict:
        """
        Execute a user story.
        
        Args:
            story: {
                "name": "Story name",
                "url": "https://example.com",
                "workflow": "Step 1\nStep 2\nStep 3"
            }
        
        Returns:
            {
                "story": "name",
                "status": "PASS|FAIL",
                "steps": [{"step": 1, "name": "...", "status": "PASS"}],
                "screenshots": ["path1.png", "path2.png"]
            }
        """
        # Implementation in agents/qa.py
        pass
```

**Usage:**
```bash
openclaw agent bowser-qa --story story.yaml --headed
```

Or programmatically:
```python
from openclaw.agents.bowser import BrowserQAAgent

agent = BrowserQAAgent(config={"headed": True})
result = agent.run({
    "name": "Homepage loads",
    "url": "https://example.com",
    "workflow": "Navigate to URL\nVerify page loads"
})
```

---

### Playwright Bowser Agent

```python
@agent
class PlaywrightBowserAgent:
    """
    General-purpose browser automation agent.
    
    Executes arbitrary browser tasks.
    """
    
    def run(self, task: str) -> dict:
        """
        Execute a browser task.
        
        Args:
            task: Natural language task description
        
        Returns:
            {"result": "...", "screenshots": []}
        """
        pass
```

---

## Workflows (Layer 3)

Workflows orchestrate multiple agents for complex operations.

### UI Review Workflow

```python
from openclaw import workflow
import glob
import yaml

@workflow
def ui_review(
    stories_glob: str = "shared/examples/*.yaml",
    parallel: int = 5,
    headed: bool = False,
    vision: bool = False
) -> dict:
    """
    Run UI review across multiple user stories.
    
    Args:
        stories_glob: Pattern to find story files
        parallel: Number of parallel agents
        headed: Run with visible browser
        vision: Return screenshots in context
    
    Returns:
        {
            "total": 10,
            "passed": 8,
            "failed": 2,
            "results": [...],
            "report_path": "report.md"
        }
    """
    # Find all story files
    story_files = glob.glob(stories_glob)
    
    # Parse stories
    stories = []
    for f in story_files:
        with open(f) as file:
            data = yaml.safe_load(file)
            stories.extend(data.get("stories", []))
    
    # Spawn agents in parallel
    # ... implementation in commands/ui_review.py
```

**Usage:**
```bash
openclaw workflow ui-review --stories "*.yaml" --parallel 5
```

---

### Amazon Add to Cart Workflow

```python
@workflow
def amazon_add_to_cart(
    prompt: str,
    skill: str = "playwright",
    headed: bool = False
) -> dict:
    """
    Search Amazon and add item to cart.
    
    Args:
        prompt: Item to search for
        skill: "playwright" or "chrome"
        headed: Run with visible browser
    """
    pass
```

---

## Tool Implementation Details

### Tool Decorator

The `@tool` decorator registers a function as an OpenClaw tool:

```python
from openclaw import tool
import subprocess
import os

@tool
def browser_open(
    url: str,
    session: str = None,
    headless: bool = True,
    persistent: bool = True
) -> dict:
    """
    Open a URL in a browser session.
    """
    # Auto-generate session name if not provided
    if session is None:
        session = generate_session_name(url)
    
    # Build command
    cmd = ["playwright-cli", f"-s={session}", "open", url]
    
    if persistent:
        cmd.append("--persistent")
    if headless:
        cmd.append("--headless")
    
    # Set viewport
    env = os.environ.copy()
    env["PLAYWRIGHT_MCP_VIEWPORT_SIZE"] = "1440x900"
    
    # Execute
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env
    )
    
    if result.returncode != 0:
        raise ToolError(f"Failed to open browser: {result.stderr}")
    
    return {
        "session": session,
        "url": url,
        "status": "success"
    }
```

---

## Agent Implementation Details

### Agent Base Class

```python
from openclaw import agent
from typing import List, Dict
import uuid
import os

@agent
class BowserAgentBase:
    """Base class for browser automation agents."""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.session = None
    
    def _derive_session_name(self, context: str) -> str:
        """Generate kebab-case session name from context."""
        import re
        name = re.sub(r'[^\w]+', '-', context.lower())
        return name[:30]
    
    def _create_screenshot_dir(self, story_name: str) -> str:
        """Create unique screenshot directory."""
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        short_id = uuid.uuid4().hex[:6]
        slug = self._slugify(story_name)
        
        path = os.path.join(
            self.config.get("screenshots_dir", "./screenshots"),
            f"{timestamp}_{short_id}",
            slug
        )
        os.makedirs(path, exist_ok=True)
        return path
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug."""
        import re
        return re.sub(r'[^\w]+', '-', text.lower())[:30]
```

---

## Configuration Schema

### `openclaw.yaml`

```yaml
# ~/.openclaw/openclaw.yaml
version: "1.0"

# Tool configuration
tools:
  bowser:
    # Default settings for all browser tools
    defaults:
      viewport: "1440x900"
      headless: true
      persistent: true
    
    # Paths
    screenshots_dir: "./screenshots"
    
    # Timeouts (milliseconds)
    timeouts:
      navigation: 30000
      screenshot: 10000

# Agent configuration
agents:
  bowser-qa:
    class: "openclaw.agents.bowser.qa.BrowserQAAgent"
    config:
      headed: false
      vision: false
      screenshots_dir: "./screenshots/bowser-qa"

# Workflow configuration
workflows:
  ui-review:
    class: "openclaw.workflows.ui_review.UIReviewWorkflow"
    config:
      max_parallel: 10
      default_agent: "bowser-qa"
```

---

## Error Handling

### Tool Errors

```python
from openclaw.exceptions import ToolError

@tool
def browser_click(session: str, ref: str) -> dict:
    try:
        # ... execute command
    except subprocess.CalledProcessError as e:
        raise ToolError(
            f"Failed to click element {ref}: {e.stderr}",
            tool="browser_click",
            context={"session": session, "ref": ref}
        )
```

### Agent Errors

```python
from openclaw.exceptions import AgentError

@agent
class BrowserQAAgent:
    def run(self, story: dict) -> dict:
        try:
            # ... execute steps
        except Exception as e:
            raise AgentError(
                f"Failed to execute story: {e}",
                agent="bowser-qa",
                story=story["name"]
            )
```

---

## Testing Tools

```python
# tests/test_browser_tools.py
from openclaw.tools.bowser import browser_open, browser_close

def test_browser_open():
    result = browser_open(
        url="https://example.com",
        session="test-open",
        headless=True
    )
    assert result["status"] == "success"
    assert result["session"] == "test-open"
    
    browser_close(session="test-open")
```

---

## Original Reference

This implementation is adapted from:
- **Original:** [github.com/disler/bowser](https://github.com/disler/bowser)
- **Author:** IndyDevDan ([@disler](https://github.com/disler))

---

*See [README.md](./README.md) for installation and usage.*
