# Phase 2E-R4.1 Ephemeris License & Compliance Audit

## 1. Ephemeris Engines Analyzed

### A. Swiss Ephemeris (`libswe` / `pyswisseph`)
- **Developer**: Astrodienst AG (Dieter Koch, Alois Treindl).
- **License Dual Model**:
  1. **GNU AGPLv3 (Affero General Public License v3)**: Free for open-source AGPL software. If integrated into a network-accessible web service (SaaS), AGPLv3 requires making the entire backend source code available under AGPLv3.
  2. **Commercial License**: Astrodienst offers paid commercial licenses for closed-source SaaS applications and proprietary mobile/desktop software.
- **Project Status**: Not compiled/linked in production backend due to build constraints on Python 3.13 Windows environment.

### B. PyEphem (`ephem` v4.2.1)
- **Engine Core**: XEphem C astronomical library (Elwood Downey).
- **License**: **MIT License**.
- **Compliance Status**: Fully permissive open-source license. Permitted for both commercial SaaS and testing without AGPL viral copyleft requirements.

### C. Skyfield v1.55 + NASA JPL DE440s
- **Developer**: Brandon Rhodes (Skyfield) / NASA Jet Propulsion Laboratory (JPL).
- **License**:
  - **Skyfield**: **MIT License**.
  - **NASA JPL DE440s BSP Kernel**: **Public Domain / US Government Work**. Unrestricted for commercial, non-commercial, and academic use.
- **Compliance Status**: Primary production ephemeris kernel for Astrovision Phase 2A/2B/2C/2D/2E. 100% compliant for production SaaS deployment.

## 2. Conclusion
Astrovision's production path utilizes Skyfield with NASA JPL DE440s (MIT / Public Domain). Reference cross-checks utilize PyEphem 4.2.1 (MIT License). Both libraries satisfy production commercial SaaS compliance without triggering AGPL open-source copyleft obligations.
