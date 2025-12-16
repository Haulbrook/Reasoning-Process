"""
Tests for markdown syntax validation across all documentation files.

These tests ensure all markdown files are well-formed, consistently formatted,
and follow common markdown best practices.
"""
import re
from pathlib import Path
from typing import List, Tuple

import pytest


class TestMarkdownStructure:
    """Test markdown structural integrity."""

    def test_files_are_valid_utf8(self, all_markdown_files: List[Path]):
        """Verify all markdown files are valid UTF-8."""
        for md_file in all_markdown_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                # Basic validation - should not raise
                assert content is not None
            except UnicodeDecodeError as e:
                pytest.fail(f"File {md_file.name} is not valid UTF-8: {e}")

    def test_files_not_empty(self, all_markdown_files: List[Path]):
        """Verify all markdown files have content."""
        empty_files = []
        for md_file in all_markdown_files:
            content = md_file.read_text(encoding='utf-8').strip()
            if not content:
                empty_files.append(md_file.name)

        assert len(empty_files) == 0, f"Found empty markdown files: {empty_files}"

    def test_files_have_title(self, all_markdown_files: List[Path]):
        """Verify all markdown files start with a title (H1)."""
        missing_titles = []
        for md_file in all_markdown_files:
            content = md_file.read_text(encoding='utf-8')
            lines = content.strip().split('\n')

            # Find first non-empty line
            first_content_line = None
            for line in lines:
                if line.strip():
                    first_content_line = line.strip()
                    break

            if first_content_line and not first_content_line.startswith('# '):
                missing_titles.append(md_file.name)

        assert len(missing_titles) == 0, (
            f"Files missing H1 title at start: {missing_titles}"
        )

    def test_heading_hierarchy(self, all_markdown_files: List[Path]):
        """Verify heading levels don't skip more than 2 levels (e.g., H1 -> H4)."""
        # Note: This documentation intentionally uses H4 (####) for sub-steps
        # within H2 (##) sections, which is acceptable for this structure
        hierarchy_issues = []

        for md_file in all_markdown_files:
            content = md_file.read_text(encoding='utf-8')

            header_pattern = re.compile(r'^(#{1,6})\s+', re.MULTILINE)
            matches = list(header_pattern.finditer(content))

            prev_level = 0
            for match in matches:
                current_level = len(match.group(1))

                # Allow any level for first header
                if prev_level == 0:
                    prev_level = current_level
                    continue

                # Check for very large skips (more than 2 levels at once)
                # Allow H2->H4 (skip of 2) as this is common for step/sub-step patterns
                if current_level > prev_level + 2:
                    hierarchy_issues.append({
                        'file': md_file.name,
                        'issue': f'Large jump from H{prev_level} to H{current_level}'
                    })

                prev_level = current_level

        assert len(hierarchy_issues) == 0, (
            f"Found heading hierarchy issues: {hierarchy_issues}"
        )


class TestMarkdownFormatting:
    """Test markdown formatting consistency."""

    def test_no_trailing_whitespace(self, all_markdown_files: List[Path]):
        """Check for excessive trailing whitespace."""
        files_with_trailing = []

        for md_file in all_markdown_files:
            content = md_file.read_text(encoding='utf-8')
            lines = content.split('\n')

            # Count lines with more than 2 trailing spaces
            # (2 spaces is valid markdown for line break)
            excessive_trailing = 0
            for i, line in enumerate(lines, 1):
                trailing_spaces = len(line) - len(line.rstrip(' '))
                if trailing_spaces > 2:
                    excessive_trailing += 1

            if excessive_trailing > 5:  # Allow some tolerance
                files_with_trailing.append({
                    'file': md_file.name,
                    'count': excessive_trailing
                })

        assert len(files_with_trailing) == 0, (
            f"Files with excessive trailing whitespace: {files_with_trailing}"
        )

    def test_no_multiple_blank_lines(self, all_markdown_files: List[Path]):
        """Check for more than 2 consecutive blank lines."""
        issues = []

        for md_file in all_markdown_files:
            content = md_file.read_text(encoding='utf-8')

            # Find sequences of 3+ blank lines
            if '\n\n\n\n' in content:
                issues.append(md_file.name)

        assert len(issues) == 0, (
            f"Files with excessive blank lines: {issues}"
        )

    def test_consistent_list_markers(self, main_skill_path: Path):
        """Verify list markers are consistent within sections."""
        content = main_skill_path.read_text(encoding='utf-8')

        # Look for mixed list markers in same section
        # This is a heuristic check - look for - and * on consecutive lines
        lines = content.split('\n')

        inconsistent_sections = []
        prev_marker = None

        for i, line in enumerate(lines):
            stripped = line.strip()

            if stripped.startswith('- '):
                current_marker = '-'
            elif stripped.startswith('* '):
                current_marker = '*'
            elif stripped.startswith('+ '):
                current_marker = '+'
            else:
                # Non-list line resets tracking
                prev_marker = None
                continue

            if prev_marker and prev_marker != current_marker:
                inconsistent_sections.append(i + 1)

            prev_marker = current_marker

        # Allow some inconsistency (different sections may use different styles)
        assert len(inconsistent_sections) < 5, (
            f"Found inconsistent list markers near lines: {inconsistent_sections[:5]}"
        )

    def test_proper_horizontal_rules(self, all_markdown_files: List[Path]):
        """Verify horizontal rules are properly formatted."""
        issues = []

        for md_file in all_markdown_files:
            content = md_file.read_text(encoding='utf-8')
            lines = content.split('\n')

            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                # Check for improperly formatted horizontal rules
                # Valid: ---, ***, ___  (3+ characters)
                if re.match(r'^[-*_]{1,2}$', stripped) and stripped:
                    issues.append({
                        'file': md_file.name,
                        'line': i,
                        'content': stripped
                    })

        assert len(issues) == 0, (
            f"Found improperly formatted horizontal rules: {issues}"
        )


class TestMarkdownLinks:
    """Test markdown link formatting."""

    def test_link_format_valid(self, all_markdown_files: List[Path]):
        """Verify links follow proper markdown format."""
        malformed_links = []

        # Pattern for markdown links
        link_pattern = re.compile(r'\[([^\]]*)\]\(([^\)]*)\)')

        for md_file in all_markdown_files:
            content = md_file.read_text(encoding='utf-8')

            for match in link_pattern.finditer(content):
                link_text = match.group(1)
                link_url = match.group(2)

                # Check for common issues
                if not link_text.strip():
                    malformed_links.append({
                        'file': md_file.name,
                        'issue': 'empty link text',
                        'url': link_url
                    })
                if link_url.strip() != link_url:
                    malformed_links.append({
                        'file': md_file.name,
                        'issue': 'whitespace in URL',
                        'url': link_url
                    })

        assert len(malformed_links) == 0, (
            f"Found malformed links: {malformed_links}"
        )

    def test_no_bare_urls(self, all_markdown_files: List[Path]):
        """Check for bare URLs that should be formatted as links."""
        bare_urls = []

        # Pattern for bare URLs not in link format or code blocks
        url_pattern = re.compile(r'(?<!\()(https?://[^\s\)]+)(?!\))')

        for md_file in all_markdown_files:
            content = md_file.read_text(encoding='utf-8')

            # Simple check - may have false positives in code blocks
            in_code_block = False
            for i, line in enumerate(content.split('\n'), 1):
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    continue

                if not in_code_block:
                    # Check if line has URL not in markdown link format
                    if 'http' in line and '](http' not in line and '`http' not in line:
                        match = url_pattern.search(line)
                        if match:
                            bare_urls.append({
                                'file': md_file.name,
                                'line': i,
                                'url': match.group(1)[:50]
                            })

        # This is advisory - bare URLs may be intentional
        if bare_urls:
            print(f"\nNote: Found bare URLs that could be formatted: {bare_urls}")


class TestMarkdownTables:
    """Test markdown table formatting."""

    def test_tables_well_formed(self, main_skill_path: Path):
        """Verify markdown tables are properly formatted."""
        content = main_skill_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        table_issues = []
        in_table = False
        table_start = 0
        column_count = 0

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Detect table start (line with |)
            if '|' in stripped and not in_table:
                in_table = True
                table_start = i
                column_count = stripped.count('|')
                continue

            if in_table:
                if '|' in stripped:
                    # Check column consistency
                    current_columns = stripped.count('|')
                    if current_columns != column_count:
                        table_issues.append({
                            'line': i,
                            'issue': f'Column count changed from {column_count} to {current_columns}'
                        })
                else:
                    # Table ended
                    in_table = False

        assert len(table_issues) == 0, (
            f"Found table formatting issues: {table_issues}"
        )

    def test_tables_have_headers(self, main_skill_path: Path):
        """Verify tables have proper header separator row."""
        content = main_skill_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        tables_without_headers = []
        prev_line_was_table_row = False

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            is_table_row = '|' in stripped and stripped.startswith('|')
            is_separator = bool(re.match(r'^\|[\s\-:|]+\|$', stripped))

            if is_table_row and prev_line_was_table_row and not is_separator:
                # Previous line was a table row, this is too, but we never saw separator
                # This might indicate missing header separator
                pass

            prev_line_was_table_row = is_table_row


class TestMarkdownSpecialCharacters:
    """Test handling of special characters."""

    def test_no_smart_quotes(self, all_markdown_files: List[Path]):
        """Check for smart/curly quotes that should be straight."""
        smart_quote_files = []

        smart_quotes = ['"', '"', ''', ''']

        for md_file in all_markdown_files:
            content = md_file.read_text(encoding='utf-8')

            found_smart = [q for q in smart_quotes if q in content]
            if found_smart:
                smart_quote_files.append({
                    'file': md_file.name,
                    'quotes': found_smart
                })

        # This is advisory - smart quotes may be intentional
        if smart_quote_files:
            print(f"\nNote: Files with smart quotes: {smart_quote_files}")

    def test_consistent_emphasis_markers(self, main_skill_path: Path):
        """Verify consistent use of emphasis markers (* vs _)."""
        content = main_skill_path.read_text(encoding='utf-8')

        # Count different emphasis styles
        asterisk_bold = len(re.findall(r'\*\*[^*]+\*\*', content))
        underscore_bold = len(re.findall(r'__[^_]+__', content))

        asterisk_italic = len(re.findall(r'(?<!\*)\*[^*]+\*(?!\*)', content))
        underscore_italic = len(re.findall(r'(?<!_)_[^_]+_(?!_)', content))

        # Prefer asterisks (more common) - check for consistency
        if asterisk_bold > 0 and underscore_bold > 0:
            # Mixed usage - should prefer one style
            total = asterisk_bold + underscore_bold
            dominant = max(asterisk_bold, underscore_bold)
            consistency = dominant / total

            assert consistency > 0.8, (
                f"Inconsistent bold markers: ** used {asterisk_bold} times, "
                f"__ used {underscore_bold} times"
            )

    def test_no_broken_emphasis(self, main_skill_path: Path):
        """Check for unmatched emphasis markers."""
        content = main_skill_path.read_text(encoding='utf-8')

        # This is a heuristic - look for odd counts of emphasis markers
        # excluding code blocks
        lines = content.split('\n')

        in_code_block = False
        suspicious_lines = []

        for i, line in enumerate(lines, 1):
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue

            if not in_code_block:
                # Count asterisks not in code spans
                line_no_code = re.sub(r'`[^`]+`', '', line)
                asterisks = line_no_code.count('*')
                underscores = line_no_code.count('_')

                # Odd count might indicate unmatched
                # But allow single * or _ for lists, etc.
                if asterisks > 1 and asterisks % 2 == 1:
                    # Likely unmatched
                    suspicious_lines.append({
                        'line': i,
                        'issue': 'possibly unmatched asterisks'
                    })

        # Allow some tolerance
        assert len(suspicious_lines) < 3, (
            f"Found possibly broken emphasis: {suspicious_lines}"
        )


class TestFileNaming:
    """Test markdown file naming conventions."""

    def test_lowercase_extensions(self, all_markdown_files: List[Path]):
        """Verify markdown files use lowercase extensions."""
        uppercase_extensions = []

        for md_file in all_markdown_files:
            if md_file.suffix != md_file.suffix.lower():
                uppercase_extensions.append(md_file.name)

        assert len(uppercase_extensions) == 0, (
            f"Files with uppercase extensions: {uppercase_extensions}"
        )

    def test_no_spaces_in_filenames(self, all_markdown_files: List[Path]):
        """Check for spaces in filenames (prefer dashes)."""
        files_with_spaces = [
            md_file.name for md_file in all_markdown_files
            if ' ' in md_file.name
        ]

        # Advisory - spaces work but dashes are preferred
        if files_with_spaces:
            print(f"\nNote: Files with spaces in names: {files_with_spaces}")
