"""
Programmatic Mandatory Clean-Source Fail-Closed Generator for Test Node Inventory (reports/test_node_inventory.json).
Collects exact Pytest node IDs across all repository test suites via pytest --collect-only,
verifies collection exit codes and stdout integrity, computes deterministic inventory SHA-256 hash,
and enforces mandatory clean-source working-tree certification for production mode.
"""
import json
import hashlib
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

def get_git_commit_sha(root: Path) -> str:
    res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Git rev-parse HEAD failed with exit code {res.returncode}: {res.stderr}")
    sha = res.stdout.strip()
    if not sha or len(sha) != 40:
        raise RuntimeError(f"Invalid Git commit SHA retrieved: '{sha}'")
    return sha

def is_working_tree_clean(root: Path) -> bool:
    res = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Git status check failed with exit code {res.returncode}: {res.stderr}")
    return len(res.stdout.strip()) == 0

def compute_inventory_hash(node_ids: list) -> str:
    content = "\n".join(sorted(node_ids)).encode("utf-8")
    return hashlib.sha256(content).hexdigest()

def generate_inventory(root: Path = None, enforce_clean_tree: bool = True):
    if root is None:
        root = Path(__file__).resolve().parent.parent
    else:
        root = Path(root).resolve()

    source_sha = get_git_commit_sha(root)
    clean_tree = is_working_tree_clean(root)

    # Mandatory clean-source enforcement for production certification mode
    if enforce_clean_tree and not clean_tree:
        raise RuntimeError(
            f"Production inventory certification refused for commit '{source_sha[:8]}': "
            f"Git working tree contains uncommitted changes. "
            f"Production inventory requires a clean committed source revision."
        )

    collection_targets = [
        ("non_oracle_api", [sys.executable, "-m", "pytest", "--collect-only", "-q", "apps/api/tests/", "--ignore=apps/api/tests/oracles/"]),
        ("oracles", [sys.executable, "-m", "pytest", "--collect-only", "-q", "apps/api/tests/oracles/"]),
        ("script_frozen_reference", [sys.executable, "-m", "pytest", "--collect-only", "-q", "scripts/test_r7_r3_frozen_reference_integrity.py"])
    ]

    all_collected_nodes = []
    category_counts = {}

    for cat_name, cmd in collection_targets:
        res = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Pytest collection failed for target '{cat_name}' with exit code {res.returncode}:\nStderr: {res.stderr}\nStdout: {res.stdout}")

        nodes = [line.strip().replace("\\", "/") for line in res.stdout.splitlines() if "::" in line and not line.startswith("warning")]
        if not nodes:
            raise RuntimeError(f"Pytest collection for target '{cat_name}' returned zero test node IDs. Output:\n{res.stdout}")

        category_counts[cat_name] = len(nodes)
        all_collected_nodes.extend(nodes)

    unique_nodes = sorted(list(set(all_collected_nodes)))
    if not unique_nodes:
        raise RuntimeError("Inventory generation collected zero unique test node IDs across all targets.")

    inventory_hash = compute_inventory_hash(unique_nodes)

    inventory_data = {
        "repository": "Astrovision",
        "source_sha": source_sha,
        "working_tree_clean": clean_tree,
        "inventory_sha256": inventory_hash,
        "generated_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "total_unique_node_ids": len(unique_nodes),
        "category_counts": category_counts,
        "node_ids": unique_nodes
    }

    out_file = root / "reports" / "test_node_inventory.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(inventory_data, f, indent=2)

    print(f"Generated {out_file} with {len(unique_nodes)} unique test node IDs (SHA-256: {inventory_hash[:16]}..., Git SHA: {source_sha}, Clean: {clean_tree}).")
    return inventory_data

if __name__ == "__main__":
    enforce = "--allow-dirty" not in sys.argv
    generate_inventory(enforce_clean_tree=enforce)
