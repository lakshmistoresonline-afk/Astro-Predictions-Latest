# Phase 2E-R2 Shadbala Rule-Level Provenance & Traceability

| Component | Classical Source | Rule Description | Implemented Formula / Logic |
|---|---|---|---|
| **Uccha Bala** | BPHS Ch. 27 v. 2-3 | Distance from exact debilitation degree | `(180 - min_dist(p_lon, deb_lon)) / 180 * 60` |
| **Sapta Vargaja Bala** | BPHS Ch. 27 v. 4-7 | Panchadha Maitri across D1, D2, D3, D7, D9, D12, D30 | Sum of points: Own=30, Adhi Mitra=22.5, Mitra=15, Sama=7.5, Satru=3.75, Adhi Satru=1.875 |
| **Ojha Yugma Bala** | BPHS Ch. 27 v. 8 | Odd/Even sign gender alignment in D1 and D9 | +15 for Male in Odd, +15 for Female in Even |
| **Kendradi Bala** | BPHS Ch. 27 v. 9 | House placement from Ascendant | Kendra=60, Panaphara=30, Apoklima=15 |
| **Drekkana Bala** | BPHS Ch. 27 v. 10 | Gender alignment across 1st, 2nd, 3rd drekkana | Male in 1st=15, Hermaphrodite in 2nd=15, Female in 3rd=15 |
| **Dig Bala** | BPHS Ch. 27 v. 11-13 | Distance from cardinal powerless point | `(180 - dist(p_lon, powerless_lon)) / 180 * 60` |
| **Nathonnatha Bala** | BPHS Ch. 27 v. 14-15 | Distance of Sun from Nadir (Midnight IC) | Diurnal planets = `dist_mid / 180 * 60`, Nocturnal = `60 - diurnal` |
| **Paksha Bala** | BPHS Ch. 27 v. 16-17 | Sun-Moon phase separation | Benefics = `angle / 180 * 60`, Malefics = `60 - Paksha` |
| **Ayana Bala** | BPHS Ch. 27 v. 18-20 | Declination (Kranti) from tropical longitude | `(24 + Kranti) * 1.25` for North strong, `(24 - Kranti) * 1.25` for South strong |
| **Tribhaga Bala** | BPHS Ch. 27 v. 21 | Day/Night 1/3rd partition | Merc (1st day), Sun (2nd day), Sat (3rd day); Moon (1st night), Mars (2nd night), Ven (3rd night); Jup (60 always) |
| **Vara/Hora/Masa/Varsha** | BPHS Ch. 27 v. 22-23 | Time period lords | Vara=45, Hora=60, Masa=30, Varsha=15 |
| **Cheshta Bala** | BPHS Ch. 27 v. 24-27 | Apparent motion and speed velocity | Luminaries = Ayana/Paksha; Star planets = Vakra (60), Vikala (15), Atichara (45), Sama (30), Manda (15) |
| **Naisargika Bala** | BPHS Ch. 27 v. 28 | Natural fixed strength constants | Fixed constants: Sun=60, Moon=51.43, Ven=42.85, Jup=34.28, Merc=25.70, Mars=17.14, Sat=8.57 |
| **Drik Bala** | BPHS Ch. 27 v. 29-33 | Aspectual Drishti Pinda calculation | Drishti value (0-60) modified by +1/4th (benefic) or -1/4th (malefic) |
