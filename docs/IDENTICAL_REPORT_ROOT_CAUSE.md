# Root Cause Analysis: Identical Astrology Reports Defect

## 1. Observed Symptom
Users opening the application or generating reports were sometimes presented with sample or hardcoded default birth profiles (`Aswathy J K`, 1990-05-15, New Delhi) on initial load, leading to the perception that different users received identical reports.

## 2. Root Cause
- **Frontend Initial Load Fallback**: The frontend `page.tsx` component automatically executed a `useEffect` on mount fetching a default birth profile without requiring explicit user submission or distinct session scoping, causing first-time visitors to see pre-cached default data.
- **Lack of Differential Validation**: The test suite lacked explicit multi-user comparative tests proving that distinct birth data (e.g., User A vs User B) yielded divergent planetary longitudes, nakshatras, ascendants, and reports.

## 3. Fix Plan
1. Ensure the calculation engine strictly derives planetary positions, Nakshatras, Ascendant, and Dashas from input coordinates and Julian Day.
2. Implement automated differential tests (`apps/api/tests/test_personalization.py`) verifying that User A (`1990-01-15`, Kochi) and User B (`1985-07-22`, London) produce demonstrably different calculations and reports.
3. Update frontend to clearly distinguish between user-inputted birth profiles and default previews.
