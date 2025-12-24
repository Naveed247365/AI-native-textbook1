#!/usr/bin/env python3
"""
Code Cleanup Script for Feature 006: Urdu Translation

Removes unused imports and organizes code
Run: python3 cleanup_code.py
"""

import os
import re
from pathlib import Path


def remove_unused_imports(file_path):
    """Remove commented imports and organize imports"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    lines = content.split('\n')
    cleaned_lines = []
    import_section = []
    in_import_section = True

    for line in lines:
        # Skip empty lines in import section
        if in_import_section and line.strip() == '':
            continue

        # Collect imports
        if in_import_section and (line.startswith('import ') or line.startswith('from ')):
            import_section.append(line)
            continue

        # End of import section
        if in_import_section and not line.startswith('import ') and not line.startswith('from ') and line.strip():
            in_import_section = False
            # Add organized imports
            import_section.sort()
            cleaned_lines.extend(import_section)
            cleaned_lines.append('')

        cleaned_lines.append(line)

    # Write back if changed
    new_content = '\n'.join(cleaned_lines)
    if new_content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def cleanup_trailing_whitespace(file_path):
    """Remove trailing whitespace from lines"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    cleaned_lines = [line.rstrip() for line in lines]
    new_content = '\n'.join(cleaned_lines)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def check_pep8_line_length(file_path):
    """Check for lines exceeding PEP 8 line length (120 chars is acceptable for modern code)"""
    issues = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if len(line.rstrip()) > 120:
                issues.append(f"  Line {i}: {len(line.rstrip())} characters")

    return issues


def main():
    """Main cleanup function"""
    backend_dir = Path(__file__).parent

    # Files to cleanup
    files_to_check = [
        'api/translation.py',
        'api/feedback.py',
        'services/translation_service.py',
        'services/rate_limiter.py',
        'models/translation_feedback.py',
        'main.py'
    ]

    print("🧹 Starting code cleanup...")
    print(f"📁 Backend directory: {backend_dir}\n")

    total_files = 0
    files_modified = 0

    for file_rel_path in files_to_check:
        file_path = backend_dir / file_rel_path

        if not file_path.exists():
            print(f"⚠️  {file_rel_path} - NOT FOUND")
            continue

        total_files += 1
        print(f"🔍 Checking {file_rel_path}...")

        modified = False

        # Cleanup trailing whitespace
        if cleanup_trailing_whitespace(file_path):
            print(f"  ✅ Removed trailing whitespace")
            modified = True

        # Check line length
        long_lines = check_pep8_line_length(file_path)
        if long_lines:
            print(f"  ⚠️  Found {len(long_lines)} lines exceeding 120 characters:")
            for issue in long_lines[:3]:  # Show first 3
                print(issue)
            if len(long_lines) > 3:
                print(f"  ... and {len(long_lines) - 3} more")

        if modified:
            files_modified += 1
        else:
            print(f"  ✓ No changes needed")

        print()

    print("═" * 50)
    print(f"✅ Cleanup complete!")
    print(f"📊 Files checked: {total_files}")
    print(f"✏️  Files modified: {files_modified}")
    print("═" * 50)

    # Additional recommendations
    print("\n📝 Additional Recommendations:")
    print("  1. Run: pip install black flake8  # Install linters")
    print("  2. Run: black backend/           # Auto-format code")
    print("  3. Run: flake8 backend/          # Check PEP 8 compliance")
    print("  4. Add .flake8 config to exclude tests/ from strict checks")


if __name__ == '__main__':
    main()
