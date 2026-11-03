"""
Astrovision Version 6.0.0 Detached Publication Attestation Generator (Phase 2BM Strict Implementation).
Generates an independent, non-circular publication attestation file in
reports/publication_attestation.json AFTER the actual publication commit is created in Git.
Cryptographically binds:
- publication_commit_sha (the exact Git commit where release evidence is committed)
- source_commit_sha (the exact tested source code revision from release_certificate.json)
- certificate_sha256 (the exact SHA-256 byte digest of release_certificate.json stored in publication commit)
- timestamp_utc (ISO-8601 UTC timestamp of attestation creation)

Strict Fail-Closed Enforcement:
- Unconditionally rejects uncommitted / dirty working trees.
- Unconditionally requires certificate verdict 'PASS - PRODUCTION READY'.
- Enforces strict descendant lineage (source_commit_sha != publication_commit_sha and source is ancestor of pub).
- Verifies Git object database existence (git cat-file) and Git DAG ancestry (--is-ancestor).
- Reads reports/release_certificate.json directly from publication commit via 'git show' and fails closed if missing.
- Computes SHA-256 from exact raw certificate bytes and asserts byte equality with disk.
- Enforces atomic file replacement and overwrite protection without --force.
"""
import os
import sys
import json
import hashlib
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any

def get_git_object_format(root: Path) -> Optional[str]:
    try:
        res = subprocess.run(["git", "rev-parse", "--show-object-format"], cwd=root, capture_output=True, text=True)
        if res.returncode == 0:
            fmt = res.stdout.strip().lower()
            if fmt in ["sha1", "sha256"]:
                return fmt
    except Exception:
        pass
    return None

def is_valid_git_commit_sha(val: Any, object_format: str = "sha1") -> bool:
    expected_len = 64 if object_format == "sha256" else 40
    if not isinstance(val, str) or len(val) != expected_len:
        return False
    try:
        int(val, 16)
        return True
    except ValueError:
        return False

def get_git_commit_sha(root: Path) -> str:
    try:
        res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True)
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return ""

def is_git_working_tree_clean(root: Path) -> bool:
    try:
        res = subprocess.run(["git", "status", "--porcelain=v1"], cwd=root, capture_output=True, text=True)
        if res.returncode == 0:
            return len(res.stdout.strip()) == 0
    except Exception:
        pass
    return False

def is_git_commit_in_repo(root: Path, commit_sha: str) -> bool:
    try:
        res = subprocess.run(
            ["git", "cat-file", "-e", f"{commit_sha}^{{commit}}"],
            cwd=root,
            capture_output=True,
            text=True
        )
        return res.returncode == 0
    except Exception:
        return False

def is_git_ancestor(root: Path, ancestor_sha: str, descendant_sha: str) -> bool:
    try:
        res = subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor_sha, descendant_sha],
            cwd=root,
            capture_output=True,
            text=True
        )
        return res.returncode == 0
    except Exception:
        return False

def get_file_bytes_from_commit(root: Path, commit_sha: str, rel_path: str) -> Optional[bytes]:
    try:
        res = subprocess.run(
            ["git", "show", f"{commit_sha}:{rel_path}"],
            cwd=root,
            capture_output=True
        )
        if res.returncode == 0:
            return res.stdout
    except Exception:
        pass
    return None

def generate_publication_attestation(
    project_root: Optional[Path] = None,
    publication_commit_sha: Optional[str] = None,
    force: bool = False
) -> Dict[str, Any]:
    if project_root is None:
        project_root = Path(__file__).resolve().parent.parent
    else:
        project_root = Path(project_root).resolve()

    # 1. Object format detection
    obj_fmt = get_git_object_format(project_root)
    if not obj_fmt:
        raise RuntimeError("Failed to detect supported Git repository object format (expected sha1 or sha256)")

    # 2. Strict Unconditional Clean Working Tree Check
    if not is_git_working_tree_clean(project_root):
        raise RuntimeError("Cannot generate publication attestation: Git working tree contains uncommitted changes")

    reports_dir = project_root / "reports"
    cert_path = reports_dir / "release_certificate.json"
    att_path = reports_dir / "publication_attestation.json"

    # 3. Overwrite protection without --force
    if att_path.exists() and not force:
        raise RuntimeError(f"Publication attestation already exists at {att_path}. Use force=True to overwrite.")

    # 4. Read and parse release certificate from disk
    if not cert_path.exists() or cert_path.stat().st_size == 0:
        raise RuntimeError(f"Release certificate missing or empty at {cert_path}")

    cert_bytes = cert_path.read_bytes()
    try:
        cert_data = json.loads(cert_bytes.decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"Failed to parse release certificate at {cert_path}: {e}")

    # 5. Strict Unconditional Certificate Verdict Check
    cert_verdict = cert_data.get("verdict", "")
    if cert_verdict != "PASS - PRODUCTION READY":
        raise RuntimeError(f"Cannot generate publication attestation: Certificate verdict is '{cert_verdict}', expected 'PASS - PRODUCTION READY'")

    # 6. Source commit SHA validation
    source_commit_sha = cert_data.get("commit_sha", "")
    if not source_commit_sha or not is_valid_git_commit_sha(source_commit_sha, obj_fmt):
        raise RuntimeError(f"Release certificate contains missing or malformed commit_sha for object format '{obj_fmt}': '{source_commit_sha}'")

    if not is_git_commit_in_repo(project_root, source_commit_sha):
        raise RuntimeError(f"Source commit SHA ({source_commit_sha}) does not exist in Git object database")

    # 7. Publication commit SHA validation
    pub_sha = publication_commit_sha or get_git_commit_sha(project_root)
    if not pub_sha or not is_valid_git_commit_sha(pub_sha, obj_fmt):
        raise RuntimeError(f"Publication commit SHA is missing or malformed for object format '{obj_fmt}': '{pub_sha}'")

    if not is_git_commit_in_repo(project_root, pub_sha):
        raise RuntimeError(f"Publication commit SHA ({pub_sha}) does not exist in Git object database")

    # 8. Strict Descendant Lineage Verification
    if source_commit_sha == pub_sha:
        raise RuntimeError(f"Publication commit SHA ({pub_sha}) must be a strict descendant of source commit SHA ({source_commit_sha}); identical commits are not permitted for publication attestation")

    if not is_git_ancestor(project_root, source_commit_sha, pub_sha):
        raise RuntimeError(f"Source commit SHA ({source_commit_sha}) is not a verified Git ancestor of publication commit SHA ({pub_sha})")

    # 9. Verify certificate bytes stored in publication commit exist and match disk bytes exactly
    commit_cert_bytes = get_file_bytes_from_commit(project_root, pub_sha, "reports/release_certificate.json")
    if commit_cert_bytes is None or len(commit_cert_bytes) == 0:
        raise RuntimeError(f"Release certificate 'reports/release_certificate.json' missing or unavailable in publication commit {pub_sha}")

    commit_cert_sha256 = hashlib.sha256(commit_cert_bytes).hexdigest()
    disk_cert_sha256 = hashlib.sha256(cert_bytes).hexdigest()
    if commit_cert_sha256 != disk_cert_sha256:
        raise RuntimeError(f"Certificate bytes on disk (SHA256: {disk_cert_sha256}) differ from certificate bytes stored in publication commit {pub_sha} (SHA256: {commit_cert_sha256})")

    # 10. Compute certificate SHA-256
    cert_sha256 = disk_cert_sha256

    ts_now = datetime.now(timezone.utc).isoformat()
    try:
        datetime.fromisoformat(ts_now)
    except Exception as ts_exc:
        raise RuntimeError(f"Invalid timestamp generated: {ts_exc}")

    att_data = {
        "publication_commit_sha": pub_sha,
        "source_commit_sha": source_commit_sha,
        "certificate_sha256": cert_sha256,
        "timestamp_utc": ts_now
    }

    # 11. Atomic File Write via tempfile + os.replace
    reports_dir.mkdir(parents=True, exist_ok=True)
    fd, tmp_att_path = tempfile.mkstemp(dir=str(reports_dir), prefix="tmp_att_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(json.dumps(att_data, indent=2))
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_att_path, str(att_path))
    except Exception as write_exc:
        if os.path.exists(tmp_att_path):
            try: os.unlink(tmp_att_path)
            except Exception: pass
        raise RuntimeError(f"Failed to atomically write publication attestation: {write_exc}") from write_exc

    print(f"SUCCESS: Generated publication attestation at {att_path}")
    print(f"  Publication Commit: {pub_sha}")
    print(f"  Source Commit: {source_commit_sha}")
    print(f"  Certificate SHA-256: {cert_sha256}")

    return att_data

if __name__ == "__main__":
    force_flag = "--force" in sys.argv
    try:
        generate_publication_attestation(force=force_flag)
    except Exception as ex:
        print(f"ERROR: Failed to generate publication attestation: {ex}", file=sys.stderr)
        sys.exit(1)
