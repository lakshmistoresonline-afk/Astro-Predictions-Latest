# Phase 2E-R4.1 Provenance Matrix

| Component | Source Text & Verse | Formula / Rule | Implementation Location | Oracle Location |
|---|---|---|---|---|
| **Uccha Bala** | *BPHS* Ch. 27 v. 2-3 | `(180 - min_dist(p_lon, deb_lon)) / 180 * 60` | `shadbala.py` | `independent_shadbala.py` |
| **Sapta Vargaja** | *BPHS* Ch. 27 v. 4-7 | Panchadha Maitri score across D1..D30 | `shadbala.py` | `independent_shadbala.py` |
| **Ojha Yugma** | *BPHS* Ch. 27 v. 8 | Gender sign alignment in D1/D9 | `shadbala.py` | `independent_shadbala.py` |
| **Kendradi** | *BPHS* Ch. 27 v. 9 | Kendra=60, Panaphara=30, Apoklima=15 | `shadbala.py` | `independent_shadbala.py` |
| **Drekkana** | *BPHS* Ch. 27 v. 10 | Gender alignment in 1st/2nd/3rd drekkana | `shadbala.py` | `independent_shadbala.py` |
| **Dig Bala** | *BPHS* Ch. 27 v. 11-13 | `(180 - dist(p_lon, powerless_lon)) / 180 * 60` | `shadbala.py` | `independent_shadbala.py` |
| **Nathonnatha** | *BPHS* Ch. 27 v. 14-15 | Distance of Sun from Nadir (IC) | `shadbala.py` | `independent_shadbala.py` |
| **Paksha Bala** | *BPHS* Ch. 27 v. 16-17 | Sun-Moon phase separation angle | `shadbala.py` | `independent_shadbala.py` |
| **Ayana Bala** | *BPHS* Ch. 27 v. 18-20 | Declination (Kranti) from tropical longitude | `shadbala.py` | `independent_shadbala.py` |
| **Tribhaga Bala** | *BPHS* Ch. 27 v. 21 | Day/Night 1/3rd partition lord | `shadbala.py` | `independent_shadbala.py` |
| **Vara/Hora/Masa/Varsha** | *BPHS* Ch. 27 v. 22-23 | Time period lords | `shadbala.py` | `independent_shadbala.py` |
| **Cheshta Bala** | *BPHS* Ch. 27 v. 24-27 | Apparent daily velocity | `shadbala.py` | `independent_shadbala.py` |
| **Naisargika** | *BPHS* Ch. 27 v. 28 | Natural fixed strength constants | `shadbala.py` | `independent_shadbala.py` |
| **Drik Bala** | *BPHS* Ch. 27 v. 29-33 | Aspectual Drishti Pinda | `shadbala.py` | `independent_shadbala.py` |
| **Ashtakavarga** | *BPHS* Ch. 66 v. 6-61 | BAV matrices for 7 planets + Lagna | `ashtakavarga.py` | `independent_ashtakavarga.py` |
