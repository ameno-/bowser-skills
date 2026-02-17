#!/usr/bin/env python3
"""
Codex Bowser Skills - Test Suite
Tests for agent configurations and prompt patterns

To run in isolation:
  cd test-environments/codex-test
  cp -r ../../implementations/codex/* .
  cp -r ../../shared/* .
  python -m pytest ../implementations/codex/tests/ -v
"""

import unittest
import json
import tempfile
import os
import sys
from pathlib import Path
import yaml

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAgentConfigurations(unittest.TestCase):
    """Test Codex agent configurations."""
    
    def setUp(self):
        self.agents_md = Path(__file__).parent.parent / "AGENTS.md"
    
    def test_agents_md_exists(self):
        """AGENTS.md file exists."""
        self.assertTrue(self.agents_md.exists(), "AGENTS.md should exist")
    
    def test_playwright_agent_defined(self):
        """Playwright agent is defined."""
        content = self.agents_md.read_text()
        self.assertIn("playwright-bowser-agent", content)
        self.assertIn("system_prompt", content.lower())
    
    def test_qa_agent_defined(self):
        """QA agent is defined."""
        content = self.agents_md.read_text()
        self.assertIn("bowser-qa-agent", content)
        self.assertIn("QA validation", content)
    
    def test_agent_has_variables(self):
        """Agents have variable definitions."""
        content = self.agents_md.read_text()
        self.assertIn("HEADED", content)
        self.assertIn("VISION", content)


class TestPromptPatterns(unittest.TestCase):
    """Test Codex prompt patterns."""
    
    def test_skill_invocation_pattern(self):
        """Skill invocation pattern is documented."""
        agents_md = Path(__file__).parent.parent / "AGENTS.md"
        content = agents_md.read_text()
        
        # Should have examples of calling skills
        self.assertIn("browser-skill", content.lower())
        self.assertIn("playwright-bowser", content)
    
    def test_agent_spawning_pattern(self):
        """Agent spawning pattern is documented."""
        agents_md = Path(__file__).parent.parent / "AGENTS.md"
        content = agents_md.read_text()
        
        # Should have examples of spawning agents
        self.assertIn("spawn", content.lower())
        self.assertIn("agent", content.lower())
    
    def test_qa_validation_pattern(self):
        """QA validation pattern is documented."""
        agents_md = Path(__file__).parent.parent / "AGENTS.md"
        content = agents_md.read_text()
        
        self.assertIn("user story", content.lower())
        self.assertIn("PASS", content)
        self.assertIn("FAIL", content)


class TestToolSpecifications(unittest.TestCase):
    """Test tool specification format."""
    
    def test_tool_spec_structure(self):
        """Tool specs have correct structure."""
        # Codex uses JSON tool specifications
        spec = {
            "name": "playwright_cli",
            "description": "Run playwright-cli browser automation commands",
            "input_schema": {
                "type": "object",
                "properties": {
                    "session": {"type": "string"},
                    "command": {"type": "string"},
                    "args": {"type": "array"}
                },
                "required": ["command"]
            }
        }
        
        self.assertIn("name", spec)
        self.assertIn("description", spec)
        self.assertIn("input_schema", spec)
        self.assertIn("required", spec["input_schema"])


class TestConfigurationSchema(unittest.TestCase):
    """Test configuration schema."""
    
    def test_agent_config_schema(self):
        """Agent config has required fields."""
        config = {
            "name": "playwright-bowser-agent",
            "description": "Headless browser automation",
            "system_prompt": "You are a browser automation agent...",
            "model": "gpt-4",
            "tools": ["playwright-cli"],
            "variables": {
                "HEADED": False,
                "VISION": False
            }
        }
        
        required_fields = ["name", "description", "system_prompt", "tools"]
        for field in required_fields:
            self.assertIn(field, config, f"Config missing required field: {field}")


class TestDocumentation(unittest.TestCase):
    """Test documentation completeness."""
    
    def test_readme_exists(self):
        """README.md exists with required sections."""
        readme = Path(__file__).parent.parent / "README.md"
        self.assertTrue(readme.exists())
        
        content = readme.read_text()
        self.assertIn("## Overview", content)
        self.assertIn("## Quick Start", content)
        self.assertIn("## Architecture", content)
    
    def test_agents_md_complete(self):
        """AGENTS.md has complete documentation."""
        agents_md = Path(__file__).parent.parent / "AGENTS.md"
        content = agents_md.read_text()
        
        # Should have agent types
        self.assertIn("## Agent", content)
        
        # Should have variable reference
        self.assertIn("## Variables", content.lower())
        
        # Should have examples
        self.assertIn("## Prompt Patterns", content)


class TestCodexIntegration(unittest.TestCase):
    """Test Codex-specific integration patterns."""
    
    def test_codex_tool_usage(self):
        """Codex tools are properly referenced."""
        agents_md = Path(__file__).parent.parent / "AGENTS.md"
        content = agents_md.read_text()
        
        # Codex uses tool calling
        self.assertIn("tools", content.lower())
        self.assertIn("system_prompt", content.lower())
    
    def test_model_selection(self):
        """Model selection is documented."""
        agents_md = Path(__file__).parent.parent / "AGENTS.md"
        content = agents_md.read_text()
        
        # Should reference GPT models
        self.assertIn("gpt", content.lower())
    
    def test_layer_mapping(self):
        """Layer mapping for Codex is documented."""
        readme = Path(__file__).parent.parent / "README.md"
        content = readme.read_text()
        
        # Should explain Codex architecture
        self.assertIn("Layer", content)
        self.assertIn("Codex", content)


class TestSessionManagement(unittest.TestCase):
    """Test session management concepts."""
    
    def test_session_naming(self):
        """Session naming is consistent."""
        # Session names should be kebab-case
        test_cases = [
            ("Test Checkout", "test-checkout"),
            ("Scrape Data", "scrape-data"),
        ]
        
        import re
        for input_name, expected in test_cases:
            result = re.sub(r'[^\w]+', '-', input_name.lower()).strip('-')
            self.assertEqual(result, expected)


class TestReportFormat(unittest.TestCase):
    """Test QA report format."""
    
    def test_pass_report_format(self):
        """PASS report has correct format."""
        report = """
✅ SUCCESS

**Story:** Homepage loads
**Steps:** 3/3 passed
**Screenshots:** ./screenshots/test/

| # | Step | Status | Screenshot |
|---|------|--------|------------|
| 1 | Navigate | PASS | 00_nav.png |
"""
        self.assertIn("✅ SUCCESS", report)
        self.assertIn("PASS", report)
        self.assertIn("Steps:", report)
    
    def test_fail_report_format(self):
        """FAIL report has correct format."""
        report = """
❌ FAILURE

**Story:** Login test
**Steps:** 1/3 passed
**Failed at:** Step 2

| # | Step | Status |
|---|------|--------|
| 1 | Enter email | PASS |
| 2 | Click login | FAIL |
| 3 | Verify | SKIPPED |

### Failure Detail
**Step 2:** Click login
**Expected:** Login button clickable
**Actual:** Element not found
"""
        self.assertIn("❌ FAILURE", report)
        self.assertIn("FAIL", report)
        self.assertIn("SKIPPED", report)


def validate_codex_structure():
    """Validate the complete Codex implementation structure."""
    base_dir = Path(__file__).parent.parent
    
    required_files = [
        "README.md",
        "AGENTS.md",
    ]
    
    results = []
    for file in required_files:
        path = base_dir / file
        results.append((file, path.exists()))
    
    return results


if __name__ == "__main__":
    # Run validation first
    print("\n" + "="*50)
    print("Codex Implementation Structure Validation")
    print("="*50 + "\n")
    
    results = validate_codex_structure()
    for file, exists in results:
        status = "✓" if exists else "✗"
        print(f"{status} {file}")
    
    print("\n" + "="*50)
    print("Running Unit Tests")
    print("="*50 + "\n")
    
    # Run tests
    unittest.main(verbosity=2, exit=False)
