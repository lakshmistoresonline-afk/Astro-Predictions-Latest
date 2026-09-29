# Phase 2E-R4.1-R7-R4 Source-Level Mutation Architecture

## 1. Zero-Trust Source-Level Mutation Lifecycle
```
                 [Original Source Code] (SHA-256: Original)
                            │
                     baseline calculation
                            │
               Independent Oracle Validation -> PASS
                            │
                            ▼
             [Mutate Source Code Rule/Constant] (SHA-256: Mutated)
                            │
                     production calculation
                            │
               Independent Oracle Validation -> FAIL (Detected)
                            │
                            ▼
               [Exact Source Code Restoration] (SHA-256: Restored)
                            │
                            ▼
               Assert Original Hash == Restored Hash
                            │
                     production calculation
                            │
               Independent Oracle Validation -> PASS
```

## 2. Invariants Enforced
- **Source-Level Modification**: Actual production code in `apps/api/engines/strength/shadbala.py` or `apps/api/engines/strength/ashtakavarga.py` is mutated. Output objects are NEVER tampered with.
- **Hash Verification**: `SHA256(original_file) == SHA256(restored_file)`.
- **Validation Failure**: The independent oracle validator MUST fail with `exit_code != 0` or `AssertionError` when evaluated against mutated production calculations.
- **73 Total Mutations**: Exactly 17 Shadbala subcomponents + 56 BAV contributor cells.
