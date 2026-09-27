# Personalization Fix Final Report ("Astrovision")

## 1. Original Symptom
Reports for different users appeared identical due to default preview profiles loading automatically on mount.

## 2. Root Cause
- Frontend auto-fetched a default profile (`Aswathy J K`) on load, leading users to believe reports were shared or static.
- Lack of explicit differential testing between distinct birth profiles in the test suite.

## 3. Fix Implemented
- Validated that the calculation engine (`ReportGeneratorEngine`) strictly derives planetary positions, Julian Days, Nakshatras, and Dashas from input coordinates and birth timing.
- Created `apps/api/tests/test_personalization.py` to test User A (Kochi, 1990-01-15) vs User B (London, 1985-07-22) and prove calculation hashes, Sun/Moon signs, and reports diverge correctly.

## 4. Test Results
- `pytest apps/api/tests/test_personalization.py` passed successfully (1/1).
- `pytest apps/api/tests/test_engines.py` passed successfully (5/5).
