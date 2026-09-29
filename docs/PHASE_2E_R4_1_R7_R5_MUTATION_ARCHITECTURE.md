# Phase 2E-R4.1-R7-R5 Physical File Source Mutation Architecture

## 1. Physical File Source Mutation Protocol
```
              [Original Production File] (SHA-256: Original)
                           │
             Fresh Process Execution -> PASS
                           │
                           ▼
          [Physically Modify File Bytes on Disk]
                           │
             (SHA-256: Mutated != Original)
                           │
                           ▼
          [Fresh Python Subprocess Execution]
                           │
             Independent Oracle Validation -> FAIL
                           │
                           ▼
          [Exact Byte-for-Byte File Restoration]
                           │
             (SHA-256: Restored == Original)
                           │
                           ▼
          [Fresh Python Subprocess Execution]
                           │
             Independent Oracle Validation -> PASS
```

## 2. Invariants
- **No Monkey-Patching / No `setattr`**: Every mutation edits the physical Python source file on disk (`shadbala.py` or `ashtakavarga.py`).
- **Fresh Process Subprocess**: Every execution runs via `subprocess.run([sys.executable, "scripts/run_single_mutation_case.py", mutation_id])` in a separate Python process to eliminate module caching or in-memory state leakage.
- **Cryptographic Hash Proof**: `original_sha256`, `mutated_sha256`, and `restored_sha256` are calculated from actual physical file bytes on disk for every mutation.
