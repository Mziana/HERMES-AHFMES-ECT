"""
Physical File Scanner for AHFMES-ARE Repository
Enforces Epistemic Boundary & Path Containment Policy:
- Model Hypothesis -> Tool Inspection -> Observed Evidence -> Verification.
- Strict containment checks preventing path traversal attacks (../ escapes).
- Environment-configurable repository root path.
"""

import os
from pathlib import Path

TARGET_REPO_PATH = os.getenv("AHFMES_REPO_ROOT", r"D:\Hermes\AHFMES-ARE")


def resolve_safe_path(rel_path=""):
    """Resolves target path and strictly enforces repository boundary containment."""
    repo_root = Path(TARGET_REPO_PATH).resolve()
    target = (repo_root / rel_path).resolve()
    
    # Check if resolved target path is contained within repository root
    try:
        if not target.is_relative_to(repo_root):
            raise PermissionError(f"PATH TRAVERSAL DENIED: '{rel_path}' escapes repository boundary {repo_root}")
    except ValueError:
        raise PermissionError(f"PATH TRAVERSAL DENIED: '{rel_path}' is outside repository root {repo_root}")

    return target, repo_root


def get_repo_tree(sub_path=""):
    try:
        base_path, repo_root = resolve_safe_path(sub_path)
    except PermissionError as pe:
        return {"error": str(pe)}

    if not base_path.exists():
        return {"error": f"Path '{sub_path}' does not exist in repo"}

    if not base_path.is_dir():
        return {"error": f"Path '{sub_path}' is a file, not a directory"}

    items = []
    for entry in sorted(base_path.iterdir()):
        if entry.name in ('.git', '__pycache__', '.pytest_cache', 'venv', '.venv'):
            continue
        is_dir = entry.is_dir()
        rel_to_root = str(entry.relative_to(repo_root)).replace('\\', '/')
        items.append({
            "name": entry.name,
            "path": rel_to_root,
            "is_directory": is_dir,
            "size_bytes": entry.stat().st_size if not is_dir else 0,
        })

    return {
        "repo_root": str(repo_root).replace('\\', '/'),
        "current_rel_path": sub_path,
        "items": items
    }


def read_repo_file(rel_path):
    try:
        target_file, repo_root = resolve_safe_path(rel_path)
    except PermissionError as pe:
        return {"error": str(pe)}

    if not target_file.exists() or not target_file.is_file():
        return {
            "error": f"FILE NOT FOUND: Physical inspection confirms '{rel_path}' does not exist in {repo_root}."
        }

    try:
        content = target_file.read_text(encoding='utf-8', errors='replace')
        lines = content.splitlines()
        rel_str = str(target_file.relative_to(repo_root)).replace('\\', '/')
        return {
            "rel_path": rel_str,
            "filename": target_file.name,
            "total_lines": len(lines),
            "size_bytes": target_file.stat().st_size,
            "content": content,
            "snippet": "\n".join(lines[:150])  # Cap preview at 150 lines for inspection
        }
    except Exception as e:
        return {"error": f"Failed to read file '{rel_path}': {str(e)}"}
