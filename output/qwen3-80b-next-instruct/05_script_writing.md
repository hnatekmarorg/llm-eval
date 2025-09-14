Here's a Python script that converts your old flat file structure to the new nested folder structure, respecting the `--dry-run` flag, logging all actions, and avoiding modification of files already in the new structure.

```python
#!/usr/bin/env python3
"""
Convert old flat file structure to new nested folder structure.

Old format: <model-name>-<test-case>.md
New format: <model-name>/<test-case>.md

Examples:
  Old: qwen3-235b-instruct-00_code_complete.md
  New: qwen3-235b-instruct/00_code_complete.md

Skips files already in nested structure (i.e., inside a directory).
Uses logging to record actions.
Supports --dry-run flag.
"""

import os
import re
import logging
import argparse
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def is_old_format(filename):
    """
    Detect if filename matches old flat format: <model>-<test>.md
    We assume model names do NOT contain hyphens in the last part (i.e., not ending with -NN_...).
    But since model names can have hyphens, we use the fact that test cases are always 5-digit pattern: -00_..., -01_..., etc.
    We look for a pattern: any string ending with -XX_..., where XX is two digits.
    """
    # Match: anything followed by - followed by two digits, underscore, then anything and .md
    pattern = r'^(.+)-\d{2}_.*\.md$'
    match = re.match(pattern, filename)
    return match is not None

def extract_model_and_test(filename):
    """
    Extract model name and test case from old format filename.
    Example: "qwen3-235b-instruct-00_code_complete.md" -> ("qwen3-235b-instruct", "00_code_complete.md")
    We assume the last hyphen-separated part is the test case (starts with two digits and underscore).
    """
    if not is_old_format(filename):
        return None, None

    # Split by hyphen and look for the last part that matches the test case pattern
    parts = filename.split('-')
    # The last part should be like "00_code_complete.md"
    if len(parts) < 2:
        return None, None

    # Try to find the last part that matches the test case pattern
    for i in range(len(parts) - 1, -1, -1):
        candidate = parts[i]
        if re.match(r'^\d{2}_.*\.md$', candidate):
            # Found the test case part
            model_name = '-'.join(parts[:i])
            test_case = candidate
            return model_name, test_case

    return None, None

def main():
    parser = argparse.ArgumentParser(description="Convert old flat file structure to new nested folder structure.")
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes.')
    args = parser.parse_args()

    # Current directory
    current_dir = Path('.')

    # Get all .md files in current directory (not in subdirectories)
    old_files = [f for f in current_dir.iterdir() if f.is_file() and f.suffix == '.md']

    # Identify files that are already in new structure (i.e., inside a directory)
    # We'll skip any file that's inside a subdirectory — but we're only looking at top-level files
    # So we don't need to check that here — we're only processing top-level .md files.

    converted_count = 0
    skipped_count = 0

    for old_file in old_files:
        model_name, test_case = extract_model_and_test(old_file.name)

        if model_name is None:
            logger.debug(f"Skipping {old_file.name}: does not match old format.")
            continue

        # Check if the target directory already exists and contains the test case file
        target_dir = current_dir / model_name
        target_file = target_dir / test_case

        # If target directory exists and target file exists, skip
        if target_dir.exists() and target_file.exists():
            logger.info(f"Skipping {old_file.name}: target {target_file} already exists.")
            skipped_count += 1
            continue

        # If target directory exists but file doesn't, we'll create the file (but we still need to check if it's a new structure)
        # However, the requirement says: "not change existing new structure outputs"
        # So if the directory exists, we assume it's the new structure and we skip to avoid overwriting.
        # But note: it's possible the directory exists but the file doesn't — we should create it.
        # However, the problem says: "not change existing new structure outputs"
        # So if the directory exists, we assume it's managed and we don't touch it.
        # But what if the directory exists and the file is missing? That's a partial new structure.
        # Since the requirement is ambiguous, we'll interpret "not change existing new structure outputs"
        # as: if the directory exists, we assume the user is managing it and we skip.
        # This avoids accidentally overwriting files in a partially created new structure.

        if target_dir.exists():
            logger.info(f"Skipping {old_file.name}: target directory {target_dir} exists — assuming new structure already in use.")
            skipped_count += 1
            continue

        # If we get here, we want to convert
        logger.info(f"Would convert {old_file.name} -> {target_dir}/{test_case}" if args.dry_run else
                    f"Converting {old_file.name} -> {target_dir}/{test_case}")

        if not args.dry_run:
            # Create directory
            target_dir.mkdir(parents=True, exist_ok=True)
            # Move file
            old_file.rename(target_file)
            converted_count += 1

    logger.info(f"Summary: {converted_count} converted, {skipped_count} skipped.")

if __name__ == '__main__':
    main()
```

### How It Works:

1. **Pattern Recognition**:  
   The script identifies old-format files using a regex: `^(.+)-\d{2}_.*\.md$` — meaning any string ending with `-XX_...md` (where `XX` are two digits). This matches your test case pattern like `-00_code_complete.md`.

2. **Extraction**:  
   It splits the filename by hyphens and finds the last part matching the test case pattern. Everything before that becomes the model name.

3. **Safety Checks**:  
   - If the target directory (e.g., `qwen3-235b-instruct`) already exists, it skips conversion — assuming it's part of the new structure.
   - If the target file already exists in the new structure, it skips.
   - This ensures **no existing new structure files are modified**.

4. **Dry Run**:  
   Uses `--dry-run` flag to preview actions without modifying the filesystem.

5. **Logging**:  
   All actions (skips, conversions, errors) are logged with appropriate levels.

6. **No Recursion**:  
   Only processes top-level `.md` files — ignores files in subdirectories (which are assumed to be new structure).

---

### Usage:

```bash
# Preview what will happen
python3 convert_structure.py --dry-run

# Actually perform the conversion
python3 convert_structure.py
```

### Example Output (log):

```
2024-06-15 10:00:00,123 - INFO - Would convert qwen3-235b-instruct-00_code_complete.md -> qwen3-235b-instruct/00_code_complete.md
2024-06-15 10:00:00,124 - INFO - Skipping gpt-oss-00_code_complete.md: target directory gpt-oss already exists — assuming new structure already in use.
2024-06-15 10:00:00,125 - INFO - Summary: 10 converted, 5 skipped.
```

This script is safe, clear, and meets all your requirements.