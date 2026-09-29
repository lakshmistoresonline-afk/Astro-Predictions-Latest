# Phase 2E-R4.1-R3 PyEphem Execution Evidence

## 1. Execution Environment & Command
- **Command Executed**: `python reference_source/standalone_ephemeris_extractor.py`
- **PyEphem Version**: `4.2.1` (XEphem C Astronomical Ephemeris Core)
- **Python Version**: `3.13.0`
- **Platform**: `Windows 10`
- **Execution Timestamp**: `2026-09-29T03:13:04.606609+00:00`
- **Production Imports**: **ZERO** (0 imports from `apps.api.engines.*`)

## 2. Sample Extraction Output
```
=== PYEPHEM STANDALONE EXTRACTION RUNNER ===
PyEphem Version: 4.2.1
Python Version: 3.13.0
Platform: Windows-10-10.0.16299-SP0
Extraction Timestamp: 2026-09-29T03:13:04.606609+00:00
=============================================
Extracted REF_001 (Subramanian T S) -> Asc: 328.721219°, MC: 240.444875°, Sun: 161.552177°
Extracted REF_002 (User A Kochi) -> Asc: 79.899001°, MC: 347.788974°, Sun: 271.126883°
Extracted REF_003 (User B London) -> Asc: 177.672008°, MC: 94.542295°, Sun: 96.408495°
Extracted REF_004 (New York Native) -> Asc: 250.588674°, MC: 184.838728°, Sun: 256.74096°
Extracted REF_005 (Tokyo Native) -> Asc: 232.017725°, MC: 158.445222°, Sun: 20.33448°
...
Completed! Total raw reference datasets = 20. Written manifest to PHASE_2E_R4_1_R3_REFERENCE_MANIFEST.json
```

## 3. Cryptographic Manifest
All 20 extracted reference datasets were hashed with SHA-256 and committed to `PHASE_2E_R4_1_R3_REFERENCE_MANIFEST.json`.
