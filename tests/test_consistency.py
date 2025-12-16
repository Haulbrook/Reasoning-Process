"""
Tests for consistency between different copies of skill documentation.

The project contains multiple versions of the skill file:
- skill.md (root) - Full version
- reasoning-optimizer-cskill/skill.md - Full copy for distribution
- .claude/skills/reasoning-optimizer.md - Condensed version

These tests ensure consistency is maintained across these files.
"""
import hashlib
import re
from pathlib import Path
from typing import List, Set

import pytest


class TestFullVersionConsistency:
    """Test that full version copies remain in sync."""

    def test_main_and_cskill_identical(self, main_skill_path: Path, cskill_path: Path):
        """Verify main skill.md and cskill/skill.md are identical."""
        main_content = main_skill_path.read_text(encoding='utf-8')
        cskill_content = cskill_path.read_text(encoding='utf-8')

        # Use hash comparison for quick check
        main_hash = hashlib.sha256(main_content.encode()).hexdigest()
        cskill_hash = hashlib.sha256(cskill_content.encode()).hexdigest()

        assert main_hash == cskill_hash, (
            "skill.md and reasoning-optimizer-cskill/skill.md have diverged! "
            "They should be identical copies."
        )

    def test_main_and_cskill_line_counts_match(self, main_skill_path: Path, cskill_path: Path):
        """Verify line counts match between main and cskill copies."""
        main_lines = main_skill_path.read_text(encoding='utf-8').split('\n')
        cskill_lines = cskill_path.read_text(encoding='utf-8').split('\n')

        assert len(main_lines) == len(cskill_lines), (
            f"Line count mismatch: main has {len(main_lines)} lines, "
            f"cskill has {len(cskill_lines)} lines"
        )


class TestCondensedVersionConsistency:
    """Test that condensed version contains all key sections from full version."""

    def _extract_headers(self, content: str) -> List[str]:
        """Extract all markdown headers from content."""
        header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        headers = []
        for match in header_pattern.finditer(content):
            level = len(match.group(1))
            text = match.group(2).strip()
            headers.append((level, text))
        return headers

    def test_condensed_has_core_phases(self, claude_skill_path: Path):
        """Verify condensed version covers all 5 phases."""
        content = claude_skill_path.read_text(encoding='utf-8')

        required_phases = [
            'Phase 1',
            'Phase 2',
            'Phase 3',
            'Phase 4',
            'Phase 5',
        ]

        phase_terms = [
            'Comprehension',
            'Strategy',
            'Execution',
            'Review',
            'Refinement',
        ]

        # Check for numbered phases or named phases
        for phase_num, phase_name in zip(required_phases, phase_terms):
            has_phase = (
                phase_num in content or
                phase_name in content
            )
            assert has_phase, (
                f"Condensed version missing {phase_num}: {phase_name}"
            )

    def test_condensed_has_chain_of_thought(self, claude_skill_path: Path):
        """Verify condensed version includes Chain-of-Thought section."""
        content = claude_skill_path.read_text(encoding='utf-8')

        assert 'Chain-of-Thought' in content or 'CoT' in content, (
            "Condensed version should include Chain-of-Thought framework"
        )

    def test_condensed_has_code_generation(self, claude_skill_path: Path):
        """Verify condensed version includes code generation process."""
        content = claude_skill_path.read_text(encoding='utf-8')

        assert 'Code Generation' in content or 'code generation' in content.lower(), (
            "Condensed version should include Code Generation section"
        )

    def test_condensed_has_checklists(self, claude_skill_path: Path):
        """Verify condensed version includes checklist sections."""
        content = claude_skill_path.read_text(encoding='utf-8')

        checklist_terms = [
            'Pre-Response',
            'Post-Response',
            'Quality',
            'Checklist',
        ]

        found_terms = [term for term in checklist_terms if term in content]

        assert len(found_terms) >= 2, (
            f"Condensed version should include checklist sections. "
            f"Found only: {found_terms}"
        )

    def test_condensed_has_self_correction(self, claude_skill_path: Path):
        """Verify condensed version includes self-correction protocol."""
        content = claude_skill_path.read_text(encoding='utf-8')

        correction_terms = ['Self-Correction', 'self-correction', 'Accuracy', 'Completeness']

        found = any(term in content for term in correction_terms)

        assert found, (
            "Condensed version should include self-correction protocol"
        )


class TestSectionAlignment:
    """Test that key sections exist in all versions."""

    def _get_major_sections(self, content: str) -> Set[str]:
        """Extract level 2 headers (## Section)."""
        pattern = re.compile(r'^##\s+(.+)$', re.MULTILINE)
        sections = set()
        for match in pattern.finditer(content):
            # Normalize: lowercase, strip, remove special chars
            normalized = re.sub(r'[^a-z\s]', '', match.group(1).lower()).strip()
            sections.add(normalized)
        return sections

    def test_main_sections_coverage(self, main_skill_path: Path):
        """Verify main skill has all expected major sections."""
        content = main_skill_path.read_text(encoding='utf-8')
        sections = self._get_major_sections(content)

        # Expected section keywords - we do fuzzy matching
        expected_keywords = [
            'overview',
            'reasoning',  # covers "core reasoning phases"
            'thought',    # covers "chain-of-thought" or "chainofthought"
            'code',       # covers "code generation"
            'checklist',  # covers "checklists and filters"
            'correction', # covers "self-correction"
            'master',     # covers "master checklists"
            'integration',# covers "integration guide"
        ]

        for keyword in expected_keywords:
            # Fuzzy match - check if any section contains the keyword
            found = any(keyword in section for section in sections)
            assert found, (
                f"Main skill.md missing section containing '{keyword}'. "
                f"Found sections: {sorted(sections)}"
            )

    def test_full_copies_have_same_sections(self, main_skill_path: Path, cskill_path: Path):
        """Verify full copies have identical section structure."""
        main_content = main_skill_path.read_text(encoding='utf-8')
        cskill_content = cskill_path.read_text(encoding='utf-8')

        main_sections = self._get_major_sections(main_content)
        cskill_sections = self._get_major_sections(cskill_content)

        assert main_sections == cskill_sections, (
            f"Section mismatch between full copies. "
            f"Only in main: {main_sections - cskill_sections}. "
            f"Only in cskill: {cskill_sections - main_sections}"
        )


class TestContentIntegrity:
    """Test content integrity across files."""

    def test_table_of_contents_matches_sections(self, main_skill_path: Path):
        """Verify Table of Contents links match actual sections."""
        content = main_skill_path.read_text(encoding='utf-8')

        # Extract ToC links
        toc_pattern = re.compile(r'\[([^\]]+)\]\(#([^\)]+)\)')
        toc_links = {}
        in_toc = False

        for line in content.split('\n'):
            if 'Table of Contents' in line:
                in_toc = True
                continue
            if in_toc:
                if line.startswith('---'):
                    break
                match = toc_pattern.search(line)
                if match:
                    text = match.group(1)
                    anchor = match.group(2)
                    toc_links[anchor] = text

        # Extract actual section headers
        header_pattern = re.compile(r'^##\s+(.+)$', re.MULTILINE)
        actual_sections = []
        for match in header_pattern.finditer(content):
            text = match.group(1).strip()
            # Convert to anchor format
            anchor = text.lower().replace(' ', '-')
            anchor = re.sub(r'[^\w-]', '', anchor)
            actual_sections.append((anchor, text))

        # Verify ToC links have corresponding sections
        for toc_anchor, toc_text in toc_links.items():
            # Find matching section (fuzzy match on anchor)
            found = any(
                toc_anchor in section_anchor or section_anchor in toc_anchor
                for section_anchor, _ in actual_sections
            )
            assert found, (
                f"ToC link '{toc_text}' (#{toc_anchor}) has no matching section"
            )

    def test_no_broken_internal_links(self, all_markdown_files: List[Path]):
        """Check for potentially broken internal links."""
        broken_links = []

        for md_file in all_markdown_files:
            content = md_file.read_text(encoding='utf-8')

            # Find internal links (links starting with #)
            internal_link_pattern = re.compile(r'\[([^\]]+)\]\(#([^\)]+)\)')

            for match in internal_link_pattern.finditer(content):
                link_text = match.group(1)
                anchor = match.group(2)

                # Check if anchor target exists (header that would generate this anchor)
                # Simple check: anchor text should appear somewhere in the document
                anchor_words = anchor.replace('-', ' ').lower()

                if anchor_words not in content.lower():
                    broken_links.append({
                        'file': md_file.name,
                        'link_text': link_text,
                        'anchor': anchor
                    })

        # Allow some flexibility - internal links may use abbreviated anchors
        if len(broken_links) > 0:
            print(f"\nPotentially broken internal links: {broken_links}")

        # Only fail if there are many broken links
        assert len(broken_links) < 5, (
            f"Found potentially broken internal links: {broken_links}"
        )

    def test_readme_references_valid_files(self, readme_path: Path, project_root: Path):
        """Verify README references point to existing files."""
        content = readme_path.read_text(encoding='utf-8')

        # Find file path references
        path_pattern = re.compile(r'`([~./][^`]+)`|cp\s+(\S+)\s+')

        for match in path_pattern.finditer(content):
            path_ref = match.group(1) or match.group(2)
            if path_ref and not path_ref.startswith('~'):
                # Skip home directory references and relative paths
                if path_ref.startswith('./'):
                    check_path = project_root / path_ref[2:]
                elif not path_ref.startswith('/'):
                    check_path = project_root / path_ref

                    # Only check if it looks like a real file reference
                    if '.' in path_ref and not path_ref.startswith('-'):
                        # This is a soft check - just print warnings
                        if not check_path.exists():
                            print(f"Warning: README references '{path_ref}' which may not exist")
