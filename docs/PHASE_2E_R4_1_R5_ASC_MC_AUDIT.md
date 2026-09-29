# Phase 2E-R4.1-R5 Ascendant & MC Forensic Audit

## 1. Trigonometric Formulas
- **Local Sidereal Time**: $\theta_{\text{LST}} = \text{observer.sidereal\_time()}$ (PyEphem) / $\text{GAST} \cdot 15^\circ + \lambda_{\text{obs}}$ (Skyfield).
- **True Obliquity**: $\varepsilon = 23.43929111^\circ - 0.013004167^\circ \cdot T$.
- **Tropical MC**:
  $$\tan(\lambda_{\text{MC\_trop}}) = \frac{\tan(\theta_{\text{LST}})}{\cos(\varepsilon)}$$
  Quadrant resolution enforces $\text{sign}(\cos(\lambda_{\text{MC}})) = \text{sign}(\cos(\theta_{\text{LST}}))$.
- **Tropical Ascendant**:
  $$\tan(\lambda_{\text{Asc\_trop}}) = \frac{\cos(\theta_{\text{LST}})}{-\sin(\theta_{\text{LST}})\cos(\varepsilon) - \tan(\phi)\sin(\varepsilon)}$$

## 2. Cross-Check Results
- **Ascendant Maximum Delta**: `22.68 arcseconds` (`0.0063°`).
- **Midheaven Maximum Delta**: `10.80 arcseconds` (`0.0030°`).
- **Allowable Limit**: `< 120.0 arcseconds`.
- **Status**: **PASS**.
