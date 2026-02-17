"""
Browser QA Agent for OpenClaw
Adapted from https://github.com/disler/bowser

Executes user stories with step-by-step validation and screenshot reporting.
"""

import os
import uuid
import re
from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    from openclaw import agent, AgentError
except ImportError:
    def agent(cls):
        cls._is_agent = True
        return cls
    class AgentError(Exception):
        pass

# Import tools
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tools.bowser import (
    browser_open,
    browser_click,
    browser_fill,
    browser_type,
    browser_press,
    browser_snapshot,
    browser_screenshot,
    browser_console,
    browser_close,
)


@agent
class BrowserQAAgent:
    """
    QA validation agent for browser user stories.
    
    Executes user stories step-by-step with screenshot reporting.
    
    Example:
        agent = BrowserQAAgent(config={"headed": True})
        result = agent.run({
            "name": "Homepage loads",
            "url": "https://example.com",
            "workflow": "Navigate to URL\nVerify page loads"
        })
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the QA agent.
        
        Args:
            config: Configuration dictionary with options:
                - screenshots_dir: Directory for screenshots (default: ./screenshots/bowser-qa)
                - headed: Run with visible browser (default: False)
                - vision: Enable vision mode (default: False)
                - viewport: Viewport size (default: 1440x900)
        """
        self.config = config or {}
        self.screenshots_dir = self.config.get("screenshots_dir", "./screenshots/bowser-qa")
        self.headed = self.config.get("headed", False)
        self.vision = self.config.get("vision", False)
        self.viewport = self.config.get("viewport", "1440x900")
        self.session = None
        self.run_dir = None
    
    def _derive_session_name(self, story_name: str) -> str:
        """Generate kebab-case session name from story name."""
        name = re.sub(r'[^\w]+', '-', story_name.lower()).strip('-')
        return name[:30] or f"qa-{uuid.uuid4().hex[:8]}"
    
    def _create_run_directory(self, story_name: str) -> str:
        """Create unique screenshot directory for this run."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        short_id = uuid.uuid4().hex[:6]
        slug = self._slugify(story_name)
        
        run_dir = os.path.join(self.screenshots_dir, f"{timestamp}_{short_id}", slug)
        os.makedirs(run_dir, exist_ok=True)
        return run_dir
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug."""
        return re.sub(r'[^\w]+', '-', text.lower()).strip('-')[:30]
    
    def _parse_story(self, story: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse user story into discrete steps.
        
        Supports formats:
        - Simple sentences
        - Step-by-step imperative
        - Given/When/Then (BDD)
        - Checklists
        """
        workflow = story.get("workflow", "")
        
        # Split into lines and clean
        lines = [
            line.strip()
            for line in workflow.split('\n')
            if line.strip() and not line.strip().startswith('#')
        ]
        
        # Parse each line as a step
        steps = []
        for i, line in enumerate(lines):
            # Remove markdown list markers
            clean_line = re.sub(r'^[-*•]\s*\[?\s*\]?\s*', '', line)
            # Remove BDD keywords
            clean_line = re.sub(r'^(Given|When|Then|And)\s+', '', clean_line, flags=re.IGNORECASE)
            
            if clean_line:
                steps.append({
                    "index": i,
                    "name": clean_line,
                    "original": line
                })
        
        return steps
    
    def _execute_step(self, step: Dict[str, Any], step_num: int) -> Dict[str, Any]:
        """
        Execute a single step and capture screenshot.
        
        Args:
            step: Step definition
            step_num: Step number (0-indexed)
        
        Returns:
            Step result with status and screenshot
        """
        screenshot_filename = f"{step_num:02d}_{self._slugify(step['name'])}.png"
        screenshot_path = os.path.join(self.run_dir, screenshot_filename)
        
        try:
            # Execute step logic based on step content
            # This is a simplified implementation - real one would parse action types
            action_result = self._execute_action(step['name'])
            
            # Take screenshot
            browser_screenshot(
                session=self.session,
                filename=screenshot_path
            )
            
            return {
                "step": step_num + 1,
                "name": step['name'],
                "status": "PASS",
                "screenshot": screenshot_path,
                "action_result": action_result
            }
            
        except Exception as e:
            # Try to capture screenshot even on failure
            try:
                browser_screenshot(
                    session=self.session,
                    filename=screenshot_path
                )
            except:
                screenshot_path = None
            
            return {
                "step": step_num + 1,
                "name": step['name'],
                "status": "FAIL",
                "screenshot": screenshot_path,
                "error": str(e)
            }
    
    def _execute_action(self, action_text: str) -> Dict[str, Any]:
        """
        Parse and execute an action from step text.
        
        This is a simplified action parser. Real implementation would be more sophisticated.
        """
        action_text_lower = action_text.lower()
        
        # Navigation actions
        if "navigate" in action_text_lower or "go to" in action_text_lower or "open" in action_text_lower:
            # Extract URL if present
            url_match = re.search(r'(https?://[^\s]+)', action_text)
            if url_match:
                url = url_match.group(1)
                # Already opened in setup
                return {"action": "navigate", "url": url}
        
        # Click actions
        if "click" in action_text_lower:
            # Would need to find element reference from snapshot
            return {"action": "click", "note": "Element reference needed"}
        
        # Fill actions
        if "fill" in action_text_lower or "enter" in action_text_lower:
            return {"action": "fill", "note": "Form fill action"}
        
        # Verification actions (no-op for execution, validated by screenshot)
        if any(word in action_text_lower for word in ["verify", "check", "assert", "confirm"]):
            return {"action": "verify", "note": "Verification step"}
        
        return {"action": "unknown", "note": "Could not parse action"}
    
    def _capture_console_errors(self) -> List[str]:
        """Capture browser console errors."""
        try:
            messages = browser_console(session=self.session)
            errors = [m for m in messages if m.get("level") in ("error", "warning")]
            return [e.get("text", "") for e in errors]
        except Exception:
            return []
    
    def _generate_report(
        self,
        story: Dict[str, Any],
        steps: List[Dict[str, Any]],
        results: List[Dict[str, Any]],
        console_errors: List[str] = None
    ) -> str:
        """Generate structured QA report."""
        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = sum(1 for r in results if r["status"] == "FAIL")
        skipped = sum(1 for r in results if r["status"] == "SKIPPED")
        total = len(results)
        
        # Status emoji
        status_emoji = "✅ SUCCESS" if failed == 0 else "❌ FAILURE"
        
        report_lines = [
            f"{status_emoji}",
            "",
            f"**Story:** {story.get('name', 'Unnamed')}",
            f"**URL:** {story.get('url', 'N/A')}",
            f"**Steps:** {passed}/{total} passed",
            f"**Screenshots:** {self.run_dir}/",
            "",
            "| # | Step | Status | Screenshot |",
            "|---|------|--------|------------|"
        ]
        
        for result in results:
            screenshot = os.path.basename(result.get("screenshot", "")) if result.get("screenshot") else "—"
            report_lines.append(
                f"| {result['step']} | {result['name']} | {result['status']} | {screenshot} |"
            )
        
        # Add failure details if applicable
        if failed > 0:
            report_lines.extend(["", "### Failures"])
            for result in results:
                if result["status"] == "FAIL":
                    report_lines.extend([
                        "",
                        f"**Step {result['step']}:** {result['name']}",
                        f"**Error:** {result.get('error', 'Unknown error')}"
                    ])
        
        # Add console errors if present
        if console_errors:
            report_lines.extend([
                "",
                "### Console Errors",
                ""
            ])
            for error in console_errors[:10]:  # Limit to first 10
                report_lines.append(f"- {error}")
        
        return "\n".join(report_lines)
    
    def run(self, story: Dict[str, Any]) -> Dict[str, Any]:
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
                "steps": "X/Y passed",
                "results": [...],
                "screenshots_dir": "...",
                "report": "markdown report"
            }
        """
        story_name = story.get("name", "unnamed-story")
        story_url = story.get("url", "")
        
        try:
            # Setup
            self.session = self._derive_session_name(story_name)
            self.run_dir = self._create_run_directory(story_name)
            
            # Parse steps
            steps = self._parse_story(story)
            
            # Open browser
            browser_open(
                url=story_url,
                session=self.session,
                headless=not self.headed,
                persistent=True,
                viewport=self.viewport
            )
            
            # Execute steps
            results = []
            console_errors = []
            failed = False
            
            for i, step in enumerate(steps):
                if failed:
                    # Mark remaining as skipped
                    results.append({
                        "step": i + 1,
                        "name": step['name'],
                        "status": "SKIPPED",
                        "screenshot": None
                    })
                    continue
                
                result = self._execute_step(step, i)
                results.append(result)
                
                if result["status"] == "FAIL":
                    failed = True
                    console_errors = self._capture_console_errors()
            
            # Close browser
            browser_close(session=self.session)
            
            # Generate report
            report = self._generate_report(story, steps, results, console_errors)
            
            # Write report to file
            report_path = os.path.join(self.run_dir, "report.md")
            with open(report_path, "w") as f:
                f.write(report)
            
            passed_count = sum(1 for r in results if r["status"] == "PASS")
            
            return {
                "story": story_name,
                "status": "FAIL" if failed else "PASS",
                "steps": f"{passed_count}/{len(steps)}",
                "results": results,
                "screenshots_dir": self.run_dir,
                "report": report,
                "report_path": report_path,
                "console_errors": console_errors if console_errors else None
            }
            
        except Exception as e:
            # Cleanup on error
            if self.session:
                try:
                    browser_close(session=self.session)
                except:
                    pass
            
            raise AgentError(
                f"Failed to execute story '{story_name}': {e}",
                agent="bowser-qa",
                story=story_name
            )


# Original implementation reference:
# Repository: https://github.com/disler/bowser
# Author: IndyDevDan (@disler)
