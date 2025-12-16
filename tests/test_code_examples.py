"""
Tests for validating code examples embedded in markdown documentation.

This module extracts code blocks from the skill documentation and validates
that they are syntactically correct for their respective languages.
"""
import ast
import re
from pathlib import Path
from typing import List, Dict, Any

import pytest


class TestCodeExamples:
    """Test suite for code example validation."""

    def test_main_skill_has_code_blocks(self, main_skill_path: Path, code_block_extractor):
        """Verify main skill.md contains code blocks."""
        content = main_skill_path.read_text(encoding='utf-8')
        code_blocks = code_block_extractor(content)

        assert len(code_blocks) > 0, "Main skill.md should contain code examples"

    def test_cskill_has_code_blocks(self, cskill_path: Path, code_block_extractor):
        """Verify cskill skill.md contains code blocks."""
        content = cskill_path.read_text(encoding='utf-8')
        code_blocks = code_block_extractor(content)

        assert len(code_blocks) > 0, "cskill skill.md should contain code examples"

    def test_markdown_code_blocks_well_formed(self, all_markdown_files: List[Path], code_block_extractor):
        """Verify all code blocks are properly closed."""
        for md_file in all_markdown_files:
            content = md_file.read_text(encoding='utf-8')

            # Count all code fences (opening have optional language, closing are bare)
            # A code fence is a line starting with ``` (optionally followed by language)
            all_fences = re.findall(r'^```', content, re.MULTILINE)

            # Total fences should be even (each block has open + close)
            assert len(all_fences) % 2 == 0, (
                f"Odd number of code fences in {md_file.name}: "
                f"{len(all_fences)} fences found (should be even)"
            )

    def test_markdown_template_blocks_valid(self, main_skill_path: Path, code_block_extractor):
        """Verify markdown template blocks are valid markdown structure."""
        content = main_skill_path.read_text(encoding='utf-8')
        code_blocks = code_block_extractor(content)

        markdown_blocks = [b for b in code_blocks if b['language'] == 'markdown']

        assert len(markdown_blocks) > 0, "Should have markdown template examples"

        for block in markdown_blocks:
            # Check that markdown templates have valid structure
            code = block['code']
            # Templates should contain headers or list items
            has_structure = (
                '##' in code or
                '- ' in code or
                '1.' in code or
                '[' in code
            )
            assert has_structure, (
                f"Markdown template at line {block['line_number']} "
                "should contain structural elements"
            )

    def test_bash_examples_valid_syntax(self, all_markdown_files: List[Path], code_block_extractor):
        """Verify bash code examples have valid syntax patterns."""
        for md_file in all_markdown_files:
            content = md_file.read_text(encoding='utf-8')
            code_blocks = code_block_extractor(content)

            bash_blocks = [b for b in code_blocks if b['language'] in ('bash', 'sh', 'shell')]

            for block in bash_blocks:
                code = block['code']
                # Check for common bash syntax errors
                # Unmatched quotes
                single_quotes = code.count("'") - code.count("\\'")
                double_quotes = code.count('"') - code.count('\\"')

                # Basic validation - quotes should be balanced
                # (This is a heuristic, not perfect)
                assert single_quotes % 2 == 0, (
                    f"Unbalanced single quotes in bash block at line {block['line_number']} "
                    f"in {md_file.name}"
                )
                assert double_quotes % 2 == 0, (
                    f"Unbalanced double quotes in bash block at line {block['line_number']} "
                    f"in {md_file.name}"
                )

    def test_code_blocks_have_language_hints(self, main_skill_path: Path, code_block_extractor):
        """Check that code blocks specify a language for syntax highlighting."""
        content = main_skill_path.read_text(encoding='utf-8')
        code_blocks = code_block_extractor(content)

        blocks_without_language = [
            b for b in code_blocks
            if not b['language']
        ]

        # Allow many blocks without language specification
        # since this documentation uses ASCII art diagrams and templates
        # that don't need language hints
        total_blocks = len(code_blocks)
        unlabeled_ratio = len(blocks_without_language) / total_blocks if total_blocks > 0 else 0

        # Only warn, don't fail - many blocks are intentionally unlabeled (diagrams, templates)
        if unlabeled_ratio > 0.3:
            print(
                f"\nNote: {len(blocks_without_language)}/{total_blocks} "
                f"({unlabeled_ratio:.0%}) blocks without language specification"
            )

        # Very lenient check - only fail if almost all are unlabeled
        assert unlabeled_ratio < 0.8, (
            f"Most code blocks lack language specification: "
            f"{len(blocks_without_language)}/{total_blocks} ({unlabeled_ratio:.0%})"
        )

    def test_ascii_diagrams_preserved(self, main_skill_path: Path, code_block_extractor):
        """Verify ASCII art diagrams are preserved in code blocks."""
        content = main_skill_path.read_text(encoding='utf-8')
        code_blocks = code_block_extractor(content)

        # Look for blocks containing ASCII art characters
        ascii_art_chars = ['┌', '┐', '└', '┘', '│', '├', '┤', '─', '►', '▼']

        diagram_blocks = []
        for block in code_blocks:
            if any(char in block['code'] for char in ascii_art_chars):
                diagram_blocks.append(block)

        # The main skill should have diagram blocks (5-phase model, etc.)
        assert len(diagram_blocks) > 0, "Expected ASCII art diagrams in skill documentation"

        # Verify diagrams have proper box structure
        for block in diagram_blocks:
            code = block['code']
            # Check for balanced box corners
            top_left = code.count('┌')
            bottom_right = code.count('┘')

            assert top_left == bottom_right, (
                f"Unbalanced box corners in diagram at line {block['line_number']}"
            )


class TestCodeBlockLanguages:
    """Test suite for code block language identification."""

    def test_extract_all_languages(self, main_skill_path: Path, code_block_extractor):
        """Extract and report all languages used in code blocks."""
        content = main_skill_path.read_text(encoding='utf-8')
        code_blocks = code_block_extractor(content)

        languages = set(b['language'] for b in code_blocks)

        # Should have at least markdown for templates
        assert 'markdown' in languages, "Should have markdown template examples"

        # Log all found languages for visibility
        print(f"\nLanguages found in code blocks: {sorted(languages)}")

    def test_no_invalid_language_identifiers(self, all_markdown_files: List[Path], code_block_extractor):
        """Check for obviously invalid language identifiers."""
        invalid_identifiers = []
        valid_languages = {
            '', 'markdown', 'md', 'bash', 'sh', 'shell', 'python', 'py',
            'javascript', 'js', 'typescript', 'ts', 'json', 'yaml', 'yml',
            'html', 'css', 'sql', 'go', 'rust', 'java', 'c', 'cpp', 'ruby',
            'text', 'plaintext', 'txt', 'diff', 'xml', 'toml', 'ini'
        }

        for md_file in all_markdown_files:
            content = md_file.read_text(encoding='utf-8')
            code_blocks = code_block_extractor(content)

            for block in code_blocks:
                lang = block['language'].lower()
                if lang and lang not in valid_languages:
                    # Could be valid, just unusual - check it's alphanumeric
                    if not lang.isalnum():
                        invalid_identifiers.append({
                            'file': md_file.name,
                            'language': block['language'],
                            'line': block['line_number']
                        })

        assert len(invalid_identifiers) == 0, (
            f"Found invalid language identifiers: {invalid_identifiers}"
        )


class TestTemplateCompleteness:
    """Test suite for template completeness validation."""

    def test_cot_template_has_required_sections(self, main_skill_path: Path, code_block_extractor):
        """Verify Chain-of-Thought template has all required sections."""
        content = main_skill_path.read_text(encoding='utf-8')
        code_blocks = code_block_extractor(content)

        # Find CoT template
        cot_template = None
        for block in code_blocks:
            if block['language'] == 'markdown' and 'Problem Understanding' in block['code']:
                cot_template = block
                break

        assert cot_template is not None, "Should have CoT template"

        required_sections = [
            'Problem Understanding',
            'Known Information',
            'Reasoning Steps',
            'Conclusion'
        ]

        for section in required_sections:
            assert section in cot_template['code'], (
                f"CoT template missing required section: {section}"
            )

    def test_code_generation_template_complete(self, main_skill_path: Path, code_block_extractor):
        """Verify code generation template has required sections."""
        content = main_skill_path.read_text(encoding='utf-8')
        code_blocks = code_block_extractor(content)

        # Find Solution Plan template
        plan_template = None
        for block in code_blocks:
            if block['language'] == 'markdown' and 'Solution Plan' in block['code']:
                plan_template = block
                break

        assert plan_template is not None, "Should have Solution Plan template"

        required_fields = [
            'Approach',
            'Data Structures',
            'Architecture',
            'Edge Cases',
            'Error Handling'
        ]

        for field in required_fields:
            assert field in plan_template['code'], (
                f"Solution Plan template missing required field: {field}"
            )
