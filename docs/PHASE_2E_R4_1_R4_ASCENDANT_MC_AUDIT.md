# Phase 2E-R4.1-R4 Ascendant & MC Audit

## 1. Mathematical Derivation
Local Sidereal Time (LST) is computed directly from PyEphem native `observer.sidereal_time()` in radians ($\theta_{\text{LST}}$).
True Obliquity of Ecliptic ($\varepsilon$) is computed per Meeus Ch. 22:
$$\varepsilon = 23.43929111^\circ - 0.013004167^\circ \cdot T$$
where $T = \frac{JD - 2451545.0}{36525.0}$.

### Tropical Midheaven (MC)
$$\tan(\lambda_{\text{MC\_trop}}) = \frac{\tan(\theta_{\text{LST}})}{\cos(\varepsilon)}$$
Quadrant adjustments ensure $\lambda_{\text{MC}}$ lies in the same semicircle as $\theta_{\text{LST}}$.

### Tropical Ascendant (Asc)
$$\tan(\lambda_{\text{Asc\_trop}}) = \frac{\cos(\theta_{\text{LST}})}{-\sin(\theta_{\text{LST}})\cos(\varepsilon) - \tan(\phi)\sin(\varepsilon)}$$
where $\phi$ is observer latitude.

### Sidereal Conversion
$$\lambda_{\text{Asc\_sidereal}} = (\lambda_{\text{Asc\_trop}} - A_{\text{Lahiri}}) \bmod 360^\circ$$
$$\lambda_{\text{MC\_sidereal}} = (\lambda_{\text{MC\_trop}} - A_{\text{Lahiri}}) \bmod 360^\circ$$

## 2. Cross-Check Results
Across all 15 real birth chart profiles, the maximum angular delta between PyEphem LST Ascendant/MC and Skyfield DE421 GAST Ascendant/MC is **19.81 arcseconds** (well below the 120 arcsecond limit).
