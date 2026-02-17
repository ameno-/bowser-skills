"""
OpenClaw Bowser Skills
Browser automation tools for OpenClaw.
Adapted from https://github.com/disler/bowser
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="openclaw-bowser",
    version="1.0.0",
    author="Bowser Skills Contributors",
    description="Browser automation tools for OpenClaw",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/disler/bowser",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "openclaw.plugins": [
            "bowser=tools.bowser",
        ],
        "openclaw.agents": [
            "bowser-qa=agents.qa:BrowserQAAgent",
        ],
    },
)

# Original implementation reference:
# Repository: https://github.com/disler/bowser
# Author: IndyDevDan (@disler)
