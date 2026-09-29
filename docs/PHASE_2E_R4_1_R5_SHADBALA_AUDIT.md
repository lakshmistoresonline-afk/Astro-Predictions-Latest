# Phase 2E-R4.1-R5 Shadbala 17-Subcomponent Audit

## 1. Discovered Granular Components (17 Subcomponents)

| # | Subcomponent Name | Traditional BPHS Definition | Independent Oracle Location | Production Engine Location | Tolerance | Status |
|---|---|---|---|---|---|---|
| 1 | **Uccha Bala** | Exaltation distance | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |
| 2 | **Sapta Vargaja Bala** | Panchadha Maitri across 7 Vargas | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |
| 3 | **Ojha-Yugma Bala** | Odd/Even Rashi & Navamsa gender match | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |
| 4 | **Kendradi Bala** | House placement from Lagna (60/30/15) | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |
| 5 | **Drekkana Bala** | Gender-drekkana partition match | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |
| 6 | **Dig Bala** | Distance from cardinal power house | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |
| 7 | **Nathonnatha Bala** | Distance of Sun to Nadir | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |
| 8 | **Paksha Bala** | Sun-Moon phase separation | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |
| 9 | **Ayana Bala** | Declination (Kranti) from tropical lon | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |
| 10 | **Tribhaga Bala** | 1/3rd day/night partition lord | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |
| 11 | **Vara Bala** | Day Lord (+45) | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |
| 12 | **Hora Bala** | Hour Lord (+60) | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |
| 13 | **Masa Bala** | Month Lord (+30) | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |
| 14 | **Varsha Bala** | Year Lord (+15) | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |
| 15 | **Cheshta Bala** | Motion-speed classification | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |
| 16 | **Naisargika Bala** | BPHS fixed natural strength | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |
| 17 | **Drik Bala** | Aspectual Drishti Pinda | `independent_shadbala.py` | `shadbala.py` | $\le 0.03$ | **PASS** |

## 2. Summary
- All 17 subcomponents independently verified across 20 fixtures (15 real + 5 synthetic).
- Total Shashtiamsas, Rupas (`Shashtiamsas / 60.0`), and Minimum Required Strength % pass 100%.
