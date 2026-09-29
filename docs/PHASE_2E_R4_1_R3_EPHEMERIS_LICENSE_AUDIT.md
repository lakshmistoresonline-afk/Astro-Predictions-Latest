# Phase 2E-R4.1-R3 Ephemeris License & Commercial Use Audit

## 1. PyEphem 4.2.1
- **Core Engine**: XEphem C Astronomical Ephemeris Library (Elwood Downey).
- **License**: **MIT License**.
- **Commercial SaaS & Distribution Use**: Fully permissible without copyleft restrictions.
- **Role**: Reference data extraction engine for Phase 2E-R4.1-R3 independent oracle.

## 2. Skyfield 1.55 + NASA JPL DE440s
- **Skyfield License**: **MIT License** (Brandon Rhodes).
- **DE440s Kernel**: **NASA / JPL Public Domain Work**. Unrestricted for commercial, non-commercial, and academic use.
- **Role**: Primary production astronomy kernel for Astrovision backend.

## 3. Swiss Ephemeris (`libswe`)
- **License**: AGPLv3 (open-source) / Commercial License (paid Astrodienst license required for closed-source commercial SaaS).
- **Role**: Not linked or compiled in production code, eliminating AGPL viral copyleft requirements.
