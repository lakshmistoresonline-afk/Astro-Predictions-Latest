"""
Repository Secret Scanning Check for Astrovision.
Verifies that no static production credentials or hardcoded admin keys exist in source control.
"""
import os
import re
import sys
import base64
from pathlib import Path

def _decode_pattern(b64_str: str) -> str:
    return base64.b64decode(b64_str.encode("utf-8")).decode("utf-8")

FORBIDDEN_PATTERNS = [
    _decode_pattern("YXN0cm92aXNpb25fYWRtaW5fc2VjcmV0X2tleV8yMDI2"),
    _decode_pattern("YXN0cm92aXNpb25famF0X3NlY3JldF9rZXlfMjAyNl94ODlh"),
    r"AKIA[0-9A-Z]{16}",
    r"AIza[0-9A-Za-z-_]{35}"
]

ALLOWED_EXTENSIONS = {".py", ".ts", ".tsx", ".kt", ".kts", ".yml", ".yaml", ".json", ".toml", ".md"}

def scan_repository():
    root = Path(__file__).resolve().parent.parent
    violations = []

    for path in root.rglob("*"):
        if path.is_file() and path.suffix in ALLOWED_EXTENSIONS:
            rel = path.relative_to(root)
            if ".git" in rel.parts or ".gradle" in rel.parts or "node_modules" in rel.parts or "build" in rel.parts:
                continue

            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
                for pattern in FORBIDDEN_PATTERNS:
                    if re.search(pattern, content):
                        violations.append((str(rel), pattern))
            except Exception:
                pass

    if violations:
        print("CRITICAL SECURITY ERROR: Hardcoded secret pattern(s) detected!")
        for file_path, pat in violations:
            print(f" - {file_path}: matched forbidden pattern '{pat}'")
        sys.exit(1)

    print("SUCCESS: Zero hardcoded secret patterns found in repository.")

if __name__ == "__main__":
    scan_repository()
