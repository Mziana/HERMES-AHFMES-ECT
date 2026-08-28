"""
Physical File Scanner for AHFMES-ARE Repository
Enforces Epistemic Boundary: Model Hypothesis -> Tool Inspection -> Observed Evidence -> Verification.
Prevents hallucinated filenames by inspecting real filesystem contents.
"""

import os
from pathlib import Path

TARGET_REPO_PATH = r"D:\Hermes\AHFMES-ARE"


def get_repo_tree(sub_path=""):
    base_path = Path(TARGET_REPO_PATH) / sub_path
    if not base_path.exists():
        return {"error": f"Path '{sub_path}' does not exist in repo"}

    items = []
    for entry in sorted(base_path.iterdir()):
        if entry.name in ('.git', '__pycache__', '.pytest_cache'):
            continue
        is_dir = entry.is_dir()
        items.append({
            "name": entry.name,
            "path": str(entry.relative_to(TARGET_REPO_PATH)).replace('\\', '/'),
            "is_directory": is_dir,
            "size_bytes": entry.stat().st_size if not is_dir else 0,
        })

    return {
        "repo_root": TARGET_REPO_PATH,
        "current_rel_path": sub_path,
        "items": items
    }


def read_repo_file(rel_path):
    target_file = Path(TARGET_REPO_PATH) / rel_path
    if not target_file.exists() or not target_file.is_file():
        return {
            "error": f"FILE NOT FOUND: Physical inspection confirms '{rel_path}' does not exist in {TARGET_REPO_PATH}."
        }

    try:
        content = target_file.read_text(encoding='utf-8', errors='replace')
        lines = content.splitlines()
        return {
            "rel_path": rel_path.replace('\\', '/'),
            "filename": target_file.name,
            "total_lines": len(lines),
            "size_bytes": target_file.stat().st_size,
            "content": content,
            "snippet": "\n".join(lines[:150])  # Cap preview at 150 lines for inspection
        }
    except Exception as e:
        return {"error": f"Failed to read file '{rel_path}': {str(e)}"}
