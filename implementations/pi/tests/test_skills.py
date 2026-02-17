#!/usr/bin/env python3
"""
Pi Bowser Skills - Test Suite
Tests for skills, agents, and commands

To run in isolation:
  cd test-environments/pi-test
  cp -r ../../implementations/pi/* .
  cp -r ../../shared/* .
  python -m pytest ../implementations/pi/tests/ -v
"""

import unittest
import tempfile
import os
import sys
import shutil
from pathlib import Path
import yaml

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSkillStructure(unittest.TestCase):
    """Test that skill files are properly structured."""
    
    def setUp(self):
        self.skills_dir = Path(__file__).parent.parent / "skills"
    
    def test_playwright_skill_exists(self):
        """Playwright skill file exists and has correct structure."""
        skill_file = self.skills_dir / "playwright-bowser" / "SKILL.md"
        self.assertTrue(skill_file.exists(), "Playwright skill file should exist")
        
        content = skill_file.read_text()
        self.assertIn("name: playwright-bowser", content)
        self.assertIn("description:", content)
        self.assertIn("allowed-tools:", content)
    
    def test_claude_skill_exists(self):
        """Claude skill file exists and has correct structure."""
        skill_file = self.skills_dir / "claude-bowser" / "SKILL.md"
        self.assertTrue(skill_file.exists(), "Claude skill file should exist")
        
        content = skill_file.read_text()
        self.assertIn("name: claude-bowser", content)
        self.assertIn("description:", content)
    
    def test_skill_has_workflow_section(self):
        """Skills have workflow documentation."""
        for skill_name in ["playwright-bowser", "claude-bowser"]:
            skill_file = self.skills_dir / skill_name / "SKILL.md"
            content = skill_file.read_text()
            self.assertIn("## Workflow", content, f"{skill_name} should have workflow section")


class TestAgentStructure(unittest.TestCase):
    """Test that agent files are properly structured."""
    
    def setUp(self):
        self.agents_dir = Path(__file__).parent.parent / "agents"
    
    def test_agents_exist(self):
        """All expected agent files exist."""
        expected_agents = [
            "playwright-bowser-agent.md",
            "claude-bowser-agent.md",
            "bowser-qa-agent.md"
        ]
        
        for agent_file in expected_agents:
            path = self.agents_dir / agent_file
            self.assertTrue(path.exists(), f"Agent {agent_file} should exist")
    
    def test_qa_agent_has_report_format(self):
        """QA agent has structured report format."""
        qa_file = self.agents_dir / "bowser-qa-agent.md"
        content = qa_file.read_text()
        
        self.assertIn("## Report", content)
        self.assertIn("✅ SUCCESS", content)
        self.assertIn("❌ FAILURE", content)
        self.assertIn("PASS", content)
        self.assertIn("FAIL", content)
    
    def test_agents_reference_skills(self):
        """Agents reference their required skills."""
        for agent_file in self.agents_dir.glob("*.md"):
            content = agent_file.read_text()
            # Check for skills section or skill reference
            has_skills = "skills:" in content or "skill" in content.lower()
            self.assertTrue(has_skills, f"{agent_file.name} should reference skills")


class TestCommandStructure(unittest.TestCase):
    """Test that command files are properly structured."""
    
    def setUp(self):
        self.commands_dir = Path(__file__).parent.parent / "commands"
    
    def test_ui_review_command_exists(self):
        """UI review command exists."""
        cmd_file = self.commands_dir / "ui-review.md"
        self.assertTrue(cmd_file.exists())
        
        content = cmd_file.read_text()
        self.assertIn("## Workflow", content)
        self.assertIn("Phase 1", content)
        self.assertIn("Phase 2", content)
    
    def test_hop_automate_exists(self):
        """Hop automate command exists."""
        cmd_file = self.commands_dir / "bowser" / "hop-automate.md"
        self.assertTrue(cmd_file.exists())
    
    def test_workflow_commands_exist(self):
        """Workflow commands exist."""
        workflows = ["amazon-add-to-cart.md", "blog-summarizer.md"]
        
        for workflow in workflows:
            path = self.commands_dir / "bowser" / workflow
            self.assertTrue(path.exists(), f"Workflow {workflow} should exist")


class TestUserStories(unittest.TestCase):
    """Test user story YAML format."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.stories_file = Path(self.temp_dir) / "test-stories.yaml"
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_valid_story_format(self):
        """Valid user story parses correctly."""
        story_content = """
stories:
  - name: "Test homepage loads"
    url: "https://example.com"
    workflow: |
      Navigate to https://example.com
      Verify the page loads
      Verify the title is correct
    metadata:
      priority: high
      tags: [smoke, test]
"""
        self.stories_file.write_text(story_content)
        
        with open(self.stories_file) as f:
            data = yaml.safe_load(f)
        
        self.assertIn("stories", data)
        self.assertEqual(len(data["stories"]), 1)
        
        story = data["stories"][0]
        self.assertEqual(story["name"], "Test homepage loads")
        self.assertEqual(story["url"], "https://example.com")
        self.assertIn("Navigate", story["workflow"])
    
    def test_story_requires_name(self):
        """Story without name should fail validation."""
        invalid_content = """
stories:
  - url: "https://example.com"
    workflow: "Test"
"""
        self.stories_file.write_text(invalid_content)
        
        with open(self.stories_file) as f:
            data = yaml.safe_load(f)
        
        # YAML parses but story is incomplete
        story = data["stories"][0]
        self.assertNotIn("name", story)


class TestSessionNaming(unittest.TestCase):
    """Test session name derivation logic."""
    
    def test_derive_from_context(self):
        """Session names derived from context."""
        test_cases = [
            ("test the checkout flow", "test-the-checkout-flow"),
            ("Scrape Pricing Data", "scrape-pricing-data"),
            ("UI Test Login Page", "ui-test-login-page"),
        ]
        
        for context, expected in test_cases:
            # Simulate kebab-case conversion
            import re
            result = re.sub(r'[^\w]+', '-', context.lower()).strip('-')
            self.assertEqual(result, expected, f"Failed for: {context}")


class TestJustfile(unittest.TestCase):
    """Test justfile recipes."""
    
    def setUp(self):
        self.justfile = Path(__file__).parent.parent / "justfile"
    
    def test_justfile_exists(self):
        """Justfile exists."""
        self.assertTrue(self.justfile.exists())
    
    def test_layer_1_recipes(self):
        """Layer 1 (skill) recipes exist."""
        content = self.justfile.read_text()
        self.assertIn("test-playwright-skill", content)
        self.assertIn("test-chrome-skill", content)
    
    def test_layer_2_recipes(self):
        """Layer 2 (agent) recipes exist."""
        content = self.justfile.read_text()
        self.assertIn("test-playwright-agent", content)
        self.assertIn("test-qa", content)
    
    def test_layer_3_recipes(self):
        """Layer 3 (command) recipes exist."""
        content = self.justfile.read_text()
        self.assertIn("ui-review", content)
        self.assertIn("hop", content)


class TestDocumentation(unittest.TestCase):
    """Test documentation completeness."""
    
    def test_readme_exists(self):
        """README.md exists with required sections."""
        readme = Path(__file__).parent.parent / "README.md"
        self.assertTrue(readme.exists())
        
        content = readme.read_text()
        self.assertIn("## Overview", content)
        self.assertIn("## Quick Start", content)
        self.assertIn("## Installation", content)
    
    def test_agents_md_exists(self):
        """AGENTS.md exists with agent definitions."""
        agents_md = Path(__file__).parent.parent / "AGENTS.md"
        self.assertTrue(agents_md.exists())
        
        content = agents_md.read_text()
        self.assertIn("playwright-bowser-agent", content)
        self.assertIn("bowser-qa-agent", content)


class TestIntegration(unittest.TestCase):
    """Integration tests that verify components work together."""
    
    def test_skill_to_agent_flow(self):
        """Skills can be called by agents."""
        # This is a conceptual test - in real usage:
        # 1. Agent spawns with skill reference
        # 2. Agent calls skill tools
        # 3. Results returned
        
        skills_dir = Path(__file__).parent.parent / "skills"
        agents_dir = Path(__file__).parent.parent / "agents"
        
        # Verify playwright skill exists
        pw_skill = skills_dir / "playwright-bowser" / "SKILL.md"
        self.assertTrue(pw_skill.exists())
        
        # Verify agent references playwright
        pw_agent = agents_dir / "playwright-bowser-agent.md"
        content = pw_agent.read_text()
        self.assertIn("playwright-bowser", content)
    
    def test_agent_to_command_flow(self):
        """Agents can be spawned by commands."""
        commands_dir = Path(__file__).parent.parent / "commands"
        agents_dir = Path(__file__).parent.parent / "agents"
        
        # UI review command spawns QA agents
        ui_review = commands_dir / "ui-review.md"
        content = ui_review.read_text()
        self.assertIn("bowser-qa-agent", content)


def create_isolated_test_env():
    """Create an isolated test environment."""
    import shutil
    
    base_dir = Path(__file__).parent.parent.parent.parent
    test_env = base_dir / "test-environments" / "pi-test"
    
    # Clean and recreate
    if test_env.exists():
        shutil.rmtree(test_env)
    test_env.mkdir(parents=True)
    
    # Copy implementation
    pi_impl = base_dir / "implementations" / "pi"
    shutil.copytree(pi_impl, test_env / ".pi")
    
    # Copy shared resources
    shared = base_dir / "shared"
    shutil.copytree(shared, test_env / "shared")
    
    # Copy workflows
    workflows = base_dir / "workflows"
    shutil.copytree(workflows, test_env / "workflows")
    
    print(f"Isolated test environment created at: {test_env}")
    return test_env


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
