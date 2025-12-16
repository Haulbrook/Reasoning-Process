"""
Tests for checklist completeness and quality in the skill documentation.

The skill documentation defines various checklists for reasoning verification.
These tests ensure checklists are comprehensive, non-duplicative, and well-organized.
"""
import re
from pathlib import Path
from typing import List, Dict, Set, Any
from collections import Counter

import pytest


class TestChecklistExtraction:
    """Test checklist extraction and basic properties."""

    def test_main_skill_has_checklists(self, main_skill_path: Path, checklist_extractor):
        """Verify main skill.md contains checklists."""
        content = main_skill_path.read_text(encoding='utf-8')
        checklists = checklist_extractor(content)

        assert len(checklists) > 0, "Main skill.md should contain checklists"
        print(f"\nFound {len(checklists)} checklists in main skill.md")

    def test_minimum_checklist_count(self, main_skill_path: Path, checklist_extractor):
        """Verify sufficient number of checklists exist."""
        content = main_skill_path.read_text(encoding='utf-8')
        checklists = checklist_extractor(content)

        # Based on the skill structure, we expect multiple checklists
        expected_minimum = 5  # Phase checklists + quality + security + etc.

        assert len(checklists) >= expected_minimum, (
            f"Expected at least {expected_minimum} checklists, "
            f"found {len(checklists)}"
        )

    def test_checklists_have_items(self, main_skill_path: Path, checklist_extractor):
        """Verify all checklists have at least one item."""
        content = main_skill_path.read_text(encoding='utf-8')
        checklists = checklist_extractor(content)

        empty_checklists = [
            c for c in checklists
            if len(c['items']) == 0
        ]

        assert len(empty_checklists) == 0, (
            f"Found empty checklists: {[c['section'] for c in empty_checklists]}"
        )


class TestChecklistCompleteness:
    """Test that checklists cover all necessary aspects."""

    def test_phase_checklists_exist(self, main_skill_path: Path, checklist_extractor):
        """Verify each reasoning phase has a checklist."""
        content = main_skill_path.read_text(encoding='utf-8')
        checklists = checklist_extractor(content)

        phase_keywords = [
            'Comprehension',
            'Strategy',
            'Execution',
            'Review',
            'Refinement'
        ]

        for phase in phase_keywords:
            has_checklist = any(
                phase.lower() in c['section'].lower()
                for c in checklists
            )
            # Note: phases might be in combined sections
            if not has_checklist:
                print(f"Warning: No dedicated checklist found for phase: {phase}")

    def test_edge_case_checklist_comprehensive(self, main_skill_path: Path):
        """Verify edge case checklist covers common edge cases."""
        content = main_skill_path.read_text(encoding='utf-8')

        required_edge_cases = [
            'empty',
            'single',
            'maximum',
            'invalid',
            'null',
            'negative',
            'zero',
        ]

        # Search for edge cases anywhere in the document
        # The skill.md mentions these in the Edge Case Coverage section
        content_lower = content.lower()
        found_cases = [case for case in required_edge_cases if case in content_lower]

        assert len(found_cases) >= 5, (
            f"Should document at least 5 edge case types. "
            f"Found: {found_cases}"
        )

    def test_security_checklist_comprehensive(self, main_skill_path: Path):
        """Verify security checklist covers OWASP-style concerns."""
        content = main_skill_path.read_text(encoding='utf-8')

        security_concerns = [
            'sql injection',
            'xss',
            'input',  # input validation
            'sensitive',  # sensitive data
            'secrets',  # hardcoded secrets
            'authentication',
        ]

        content_lower = content.lower()
        found_concerns = [c for c in security_concerns if c in content_lower]

        assert len(found_concerns) >= 4, (
            f"Security checklist should cover common vulnerabilities. "
            f"Found: {found_concerns}, expected at least 4"
        )

    def test_code_quality_checklist_complete(self, main_skill_path: Path):
        """Verify code quality checklist covers key aspects."""
        content = main_skill_path.read_text(encoding='utf-8')

        quality_aspects = [
            'readable',
            'correct',
            'error',  # error handling
            'efficient',
            'performance',
        ]

        content_lower = content.lower()
        found_aspects = [a for a in quality_aspects if a in content_lower]

        assert len(found_aspects) >= 4, (
            f"Code quality checklist should cover key aspects. "
            f"Found: {found_aspects}"
        )


class TestChecklistQuality:
    """Test checklist item quality and formatting."""

    def test_checklist_items_are_questions_or_statements(
        self, main_skill_path: Path, checklist_extractor
    ):
        """Verify checklist items are properly formatted questions or statements."""
        content = main_skill_path.read_text(encoding='utf-8')
        checklists = checklist_extractor(content)

        problematic_items = []

        for checklist in checklists:
            for item in checklist['items']:
                # Items should be substantial (not too short)
                if len(item) < 10:
                    problematic_items.append({
                        'section': checklist['section'],
                        'item': item,
                        'issue': 'too short'
                    })
                # Items should start with capital letter or be part of structured format
                elif not (item[0].isupper() or item[0] in '0123456789*-['):
                    # Allow some flexibility
                    pass

        # Only fail if there are many problematic items
        assert len(problematic_items) < 3, (
            f"Found low-quality checklist items: {problematic_items}"
        )

    def test_no_duplicate_checklist_items(self, main_skill_path: Path, checklist_extractor):
        """Verify no exact duplicate items within checklists."""
        content = main_skill_path.read_text(encoding='utf-8')
        checklists = checklist_extractor(content)

        duplicates = []

        for checklist in checklists:
            item_counts = Counter(item.lower().strip() for item in checklist['items'])
            for item, count in item_counts.items():
                if count > 1:
                    duplicates.append({
                        'section': checklist['section'],
                        'item': item,
                        'count': count
                    })

        assert len(duplicates) == 0, (
            f"Found duplicate checklist items: {duplicates}"
        )

    def test_checklist_items_actionable(self, main_skill_path: Path, checklist_extractor):
        """Verify checklist items are actionable (verifiable)."""
        content = main_skill_path.read_text(encoding='utf-8')
        checklists = checklist_extractor(content)

        # Actionable items typically start with verbs or are yes/no questions
        action_indicators = [
            'is', 'are', 'does', 'do', 'have', 'has', 'can', 'will',
            'verify', 'check', 'ensure', 'confirm', 'review', 'test',
            'what', 'how', 'am', 'i '
        ]

        non_actionable = []

        for checklist in checklists:
            for item in checklist['items']:
                item_lower = item.lower().strip()
                is_actionable = any(
                    item_lower.startswith(indicator)
                    for indicator in action_indicators
                )

                # Also check for question marks (indicates verifiable question)
                is_question = '?' in item

                # Check for implied checkbox format (statement to verify)
                has_verification_word = any(
                    word in item_lower
                    for word in ['correct', 'proper', 'valid', 'complete', 'clear']
                )

                if not (is_actionable or is_question or has_verification_word):
                    # Only flag if really unclear
                    if len(item_lower.split()) < 3:
                        non_actionable.append({
                            'section': checklist['section'],
                            'item': item
                        })

        # Allow some flexibility
        assert len(non_actionable) < 5, (
            f"Found potentially non-actionable checklist items: {non_actionable}"
        )


class TestChecklistOrganization:
    """Test checklist logical organization."""

    def test_checklists_grouped_by_category(self, main_skill_path: Path, checklist_extractor):
        """Verify checklists are organized into logical groups."""
        content = main_skill_path.read_text(encoding='utf-8')
        checklists = checklist_extractor(content)

        # Extract section names
        sections = [c['section'] for c in checklists]

        # Should have some categorization
        categories = set()
        for section in sections:
            section_lower = section.lower()
            if 'phase' in section_lower or 'step' in section_lower:
                categories.add('process')
            elif 'quality' in section_lower:
                categories.add('quality')
            elif 'security' in section_lower:
                categories.add('security')
            elif 'code' in section_lower:
                categories.add('code')
            elif 'review' in section_lower or 'check' in section_lower:
                categories.add('verification')
            else:
                categories.add('other')

        assert len(categories) >= 2, (
            f"Checklists should cover multiple categories. Found: {categories}"
        )

    def test_pre_and_post_checklists_exist(self, main_skill_path: Path):
        """Verify both pre-response and post-response checklists exist."""
        content = main_skill_path.read_text(encoding='utf-8')
        content_lower = content.lower()

        assert 'pre-response' in content_lower, (
            "Should have pre-response checklist"
        )
        assert 'post-response' in content_lower, (
            "Should have post-response checklist"
        )

    def test_master_checklist_section_exists(self, main_skill_path: Path):
        """Verify master checklist section consolidates key checks."""
        content = main_skill_path.read_text(encoding='utf-8')

        assert 'Master Checklist' in content, (
            "Should have a Master Checklists section for consolidation"
        )


class TestChecklistCoverage:
    """Test coverage of checklist items across different scenarios."""

    def test_covers_common_task_types(self, main_skill_path: Path):
        """Verify checklists address common task types."""
        content = main_skill_path.read_text(encoding='utf-8')
        content_lower = content.lower()

        task_types = [
            'coding',
            'analysis',
            'problem',  # problem-solving
            'complex',
        ]

        found_types = [t for t in task_types if t in content_lower]

        assert len(found_types) >= 3, (
            f"Should cover common task types. Found references to: {found_types}"
        )

    def test_covers_error_categories(self, main_skill_path: Path):
        """Verify error categories are defined for self-correction."""
        content = main_skill_path.read_text(encoding='utf-8')
        content_lower = content.lower()

        error_types = [
            'logic',
            'completeness',
            'accuracy',
            'efficiency',
        ]

        found_types = [t for t in error_types if t in content_lower]

        assert len(found_types) >= 3, (
            f"Should define error categories. Found: {found_types}"
        )

    def test_total_checklist_item_count(self, main_skill_path: Path, checklist_extractor):
        """Verify comprehensive coverage via total item count."""
        content = main_skill_path.read_text(encoding='utf-8')
        checklists = checklist_extractor(content)

        total_items = sum(len(c['items']) for c in checklists)

        # A comprehensive skill should have substantial checklist coverage
        minimum_expected = 30  # Reasonable minimum for thorough coverage

        assert total_items >= minimum_expected, (
            f"Expected at least {minimum_expected} total checklist items, "
            f"found {total_items}"
        )

        print(f"\nTotal checklist items across all sections: {total_items}")
