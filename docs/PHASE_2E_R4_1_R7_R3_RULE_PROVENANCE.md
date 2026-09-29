# Phase 2E-R4.1-R7-R3 Traditional Rule Provenance Matrix

| # | Rule / Component Name | Traditional Definition & Verse | Formula / Algorithm | Independent Oracle File | Production File |
|---|---|---|---|---|---|
| 1 | **Uccha Bala** | *BPHS* Ch. 27 v. 2-3 | `(180 - min_dist(p_lon, deb_lon)) / 180 * 60` | `independent_shadbala.py` | `shadbala.py` |
| 2 | **Sapta Vargaja Bala** | *BPHS* Ch. 27 v. 4-7 | Panchadha Maitri score across D1, D2, D3, D7, D9, D12, D30 | `independent_shadbala.py` | `shadbala.py` |
| 3 | **Ojha-Yugma Bala** | *BPHS* Ch. 27 v. 8 | Gender sign match in D1 and D9 | `independent_shadbala.py` | `shadbala.py` |
| 4 | **Kendradi Bala** | *BPHS* Ch. 27 v. 9 | Kendra=60, Panaphara=30, Apoklima=15 | `independent_shadbala.py` | `shadbala.py` |
| 5 | **Drekkana Bala** | *BPHS* Ch. 27 v. 10 | Gender alignment in 1st/2nd/3rd drekkana | `independent_shadbala.py` | `shadbala.py` |
| 6 | **Dig Bala** | *BPHS* Ch. 27 v. 11-13 | Linear distance from cardinal power houses | `independent_shadbala.py` | `shadbala.py` |
| 7 | **Nathonnatha Bala** | *BPHS* Ch. 27 v. 14-15 | Distance of Sun from Nadir (IC) | `independent_shadbala.py` | `shadbala.py` |
| 8 | **Paksha Bala** | *BPHS* Ch. 27 v. 16-17 | Sun-Moon phase separation angle | `independent_shadbala.py` | `shadbala.py` |
| 9 | **Ayana Bala** | *BPHS* Ch. 27 v. 18-20 | Declination (Kranti) from tropical longitude | `independent_shadbala.py` | `shadbala.py` |
| 10 | **Tribhaga Bala** | *BPHS* Ch. 27 v. 21 | Day/Night 1/3rd partition lord | `independent_shadbala.py` | `shadbala.py` |
| 11 | **Vara Bala** | *BPHS* Ch. 27 v. 22 | Day Lord (+45) | `independent_shadbala.py` | `shadbala.py` |
| 12 | **Hora Bala** | *BPHS* Ch. 27 v. 22 | Hour Lord (+60) | `independent_shadbala.py` | `shadbala.py` |
| 13 | **Masa Bala** | *BPHS* Ch. 27 v. 23 | Month Lord (+30) | `independent_shadbala.py` | `shadbala.py` |
| 14 | **Varsha Bala** | *BPHS* Ch. 27 v. 23 | Year Lord (+15) | `independent_shadbala.py` | `shadbala.py` |
| 15 | **Cheshta Bala** | *BPHS* Ch. 27 v. 24-27 | Daily apparent velocity classification | `independent_shadbala.py` | `shadbala.py` |
| 16 | **Naisargika Bala** | *BPHS* Ch. 27 v. 28 | Fixed natural strength constants | `independent_shadbala.py` | `shadbala.py` |
| 17 | **Drik Bala** | *BPHS* Ch. 27 v. 29-33 | Aspectual Drishti Pinda | `independent_shadbala.py` | `shadbala.py` |
| 18 | **BAV Contributor Rules** | *BPHS* Ch. 66 v. 6-61 | 56 contributor vectors across 8 sources | `independent_ashtakavarga.py` | `ashtakavarga.py` |
