"""
Pytest configuration and shared fixtures for Reasoning Optimizer tests.
"""
import os
from pathlib import Path
from typing import List, Dict, Any

import pytest


# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture
def project_root() -> Path:
    """Return the project root directory."""
    return PROJECT_ROOT


@pytest.fixture
def main_skill_path() -> Path:
    """Return path to the main skill.md file."""
    return PROJECT_ROOT / "skill.md"


@pytest.fixture
def cskill_path() -> Path:
    """Return path to the cskill skill.md file."""
    return PROJECT_ROOT / "reasoning-optimizer-cskill" / "skill.md"


@pytest.fixture
def claude_skill_path() -> Path:
    """Return path to the .claude/skills skill file."""
    return PROJECT_ROOT / ".claude" / "skills" / "reasoning-optimizer.md"


@pytest.fixture
def readme_path() -> Path:
    """Return path to the README file."""
    return PROJECT_ROOT / "reasoning-optimizer-cskill" / "README.md"


@pytest.fixture
def all_markdown_files(project_root: Path) -> List[Path]:
    """Return all markdown files in the project."""
    md_files = []
    for pattern in ["*.md", "**/*.md"]:
        md_files.extend(project_root.glob(pattern))
    # Deduplicate and filter out node_modules, .git, etc.
    excluded_dirs = {".git", "node_modules", "__pycache__", ".pytest_cache"}
    filtered = []
    for f in set(md_files):
        if not any(excluded in f.parts for excluded in excluded_dirs):
            filtered.append(f)
    return sorted(filtered)


@pytest.fixture
def skill_files(main_skill_path: Path, cskill_path: Path, claude_skill_path: Path) -> Dict[str, Path]:
    """Return dictionary of all skill files."""
    return {
        "main": main_skill_path,
        "cskill": cskill_path,
        "claude": claude_skill_path,
    }


def extract_code_blocks(content: str) -> List[Dict[str, Any]]:
    """
    Extract code blocks from markdown content.

    Returns list of dicts with:
    - language: The language identifier (or empty string)
    - code: The code content
    - line_number: Starting line number in the file
    """
    import re

    code_blocks = []
    lines = content.split('\n')
    in_code_block = False
    current_block = None
    start_line = 0

    code_fence_pattern = re.compile(r'^```(\w*)')

    for i, line in enumerate(lines, 1):
        if not in_code_block:
            match = code_fence_pattern.match(line)
            if match:
                in_code_block = True
                current_block = {
                    'language': match.group(1) or '',
                    'code': [],
                    'line_number': i
                }
                start_line = i
        else:
            if line.startswith('```'):
                in_code_block = False
                current_block['code'] = '\n'.join(current_block['code'])
                code_blocks.append(current_block)
                current_block = None
            else:
                current_block['code'].append(line)

    return code_blocks


def extract_checklists(content: str) -> List[Dict[str, Any]]:
    """
    Extract checklist items from markdown content.

    Returns list of dicts with:
    - section: The section name where checklist appears
    - items: List of checklist item texts
    - line_number: Starting line number
    """
    import re

    checklists = []
    lines = content.split('\n')
    current_section = "Unknown"
    current_checklist = None

    section_pattern = re.compile(r'^#{1,6}\s+(.+)')
    checklist_pattern = re.compile(r'^-\s*\[[ x]\]\s*(.+)', re.IGNORECASE)

    for i, line in enumerate(lines, 1):
        # Track section headers
        section_match = section_pattern.match(line)
        if section_match:
            # Save previous checklist if exists
            if current_checklist and current_checklist['items']:
                checklists.append(current_checklist)
            current_section = section_match.group(1).strip()
            current_checklist = None
            continue

        # Check for checklist items
        checklist_match = checklist_pattern.match(line)
        if checklist_match:
            if current_checklist is None:
                current_checklist = {
                    'section': current_section,
                    'items': [],
                    'line_number': i
                }
            current_checklist['items'].append(checklist_match.group(1).strip())
        elif current_checklist and line.strip() and not line.startswith('-'):
            # End of checklist (non-empty, non-list line)
            if current_checklist['items']:
                checklists.append(current_checklist)
            current_checklist = None

    # Don't forget the last checklist
    if current_checklist and current_checklist['items']:
        checklists.append(current_checklist)

    return checklists


# Make helpers available as fixtures
@pytest.fixture
def code_block_extractor():
    """Return the code block extraction function."""
    return extract_code_blocks


@pytest.fixture
def checklist_extractor():
    """Return the checklist extraction function."""
    return extract_checklists
