# Phase 2E-R4.1-R7-R5 Forensic Baseline & Audit

## 1. Audited Baseline
- **Git Commit**: `c18153042689ceca82f6b3378bd1dc810b007647`
- **`apps/api/engines/strength/shadbala.py` SHA-256**: `1cf9f6f7da2c5d7e0bc78dcb70060eef1fc2743d9cc01002c7756a2ef895309f` (18,023 bytes)
- **`apps/api/engines/strength/ashtakavarga.py` SHA-256**: `d568a4697bd75f1a2e4d3c5f0e9d502728bbee3196ce998ff3ee9bba42d40635` (5,723 bytes)

## 2. Rejection of Previous R7-R4 Certification Claims
Forensic analysis of R7-R4 revealed that the Shadbala mutation suite utilized in-memory function replacement:
```python
setattr(shad_module.ShadbalaEngine, "calc_sapta_vargaja", staticmethod(lambda *a, **kw: 99.0))
```
and claimed `hash_restored = True` without executing physical file byte modifications on disk or launching fresh Python subprocesses for each mutation.

## 3. R7-R5 Mandatory Physical File Mutation Architecture
In Phase 2E-R4.1-R7-R5, all 73 mutations ($17 \text{ Shadbala subcomponents} + 56 \text{ BAV contributor cells}$) MUST:
1. Physically edit bytes in `apps/api/engines/strength/shadbala.py` or `apps/api/engines/strength/ashtakavarga.py` on disk or in an isolated temporary worktree.
2. Compute actual physical file SHA-256: `mutated_sha256 != original_sha256`.
3. Launch a fresh Python subprocess (`subprocess.run([sys.executable, ...])`) to execute production calculation and independent oracle validation.
4. Verify validator fails with `exit_code != 0`.
5. Restore physical file bytes to exact original state.
6. Compute actual physical file SHA-256: `restored_sha256 == original_sha256`.
7. Launch a fresh Python subprocess to execute production calculation and independent oracle validation.
8. Verify validator passes with `exit_code == 0`.
