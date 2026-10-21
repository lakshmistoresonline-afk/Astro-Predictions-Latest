"""
Programmatic Generator for Machine-Readable Test Node Inventory (reports/test_node_inventory.json).
Collects exact Pytest node IDs across all repository test suites, deduplicates by full node ID,
and maps batch memberships and execution status.
"""
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

def generate_inventory():
    root = Path(__file__).resolve().parent.parent

    # 1. Collect non-oracle API tests
    cmd_api = [sys.executable, "-m", "pytest", "--collect-only", "-q", "apps/api/tests/", "--ignore=apps/api/tests/oracles/"]
    res_api = subprocess.run(cmd_api, cwd=root, capture_output=True, text=True)
    api_nodes = [line.strip() for line in res_api.stdout.splitlines() if "::" in line and not line.startswith("warning")]

    # 2. Collect Oracle tests
    cmd_oracle = [sys.executable, "-m", "pytest", "--collect-only", "-q", "apps/api/tests/oracles/"]
    res_oracle = subprocess.run(cmd_oracle, cwd=root, capture_output=True, text=True)
    oracle_nodes = [line.strip() for line in res_oracle.stdout.splitlines() if "::" in line and not line.startswith("warning")]

    # 3. Collect Script test
    cmd_script = [sys.executable, "-m", "pytest", "--collect-only", "-q", "scripts/test_r7_r3_frozen_reference_integrity.py"]
    res_script = subprocess.run(cmd_script, cwd=root, capture_output=True, text=True)
    script_nodes = [line.strip() for line in res_script.stdout.splitlines() if "::" in line and not line.startswith("warning")]

    # Combine & Deduplicate
    all_nodes = api_nodes + oracle_nodes + script_nodes
    unique_nodes = sorted(list(set(all_nodes)))

    inventory_data = {
        "repository": "Astrovision",
        "generated_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "total_unique_node_ids": len(unique_nodes),
        "non_oracle_api_test_count": len(api_nodes),
        "oracle_test_count": len(oracle_nodes),
        "script_test_count": len(script_nodes),
        "node_ids": unique_nodes
    }

    out_file = root / "reports" / "test_node_inventory.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(inventory_data, f, indent=2)

    print(f"Generated {out_file} with {len(unique_nodes)} unique test node IDs.")
    return inventory_data

if __name__ == "__main__":
    generate_inventory()
