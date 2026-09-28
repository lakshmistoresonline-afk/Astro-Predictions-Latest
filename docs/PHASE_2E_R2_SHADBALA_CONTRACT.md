# Phase 2E-R2 Shadbala Output Contract & Specification

## 1. Selected Convention
- **Convention ID**: `PARASHARI_CANONICAL_BPHS_SHADBALA_V1`
- **Source**: *Brihat Parasara Hora Sastra*, Ch. 27.
- **Unit**: Shashtiamsas (raw) and Rupas (1 Rupa = 60 Shashtiamsas).

## 2. Component Specification

### A. Sthana Bala (Positional Strength)
- **Uccha Bala**: `(180.0 - |p_lon - deb_lon|) / 180.0 * 60.0` shashtiamsas. Max 60.
- **Sapta Vargaja Bala**: Points in D1, D2, D3, D7, D9, D12, D30 based on Panchadha Maitri (Own=30, Adhi Mitra=22.5, Mitra=15, Sama=7.5, Satru=3.75, Adhi Satru=1.875). Max 210.
- **Ojha Yugma Bala**: Male planets (Sun, Mars, Jup, Merc, Sat) in odd signs in D1/D9 (+15 each). Female planets (Moon, Ven) in even signs in D1/D9 (+15 each). Max 30.
- **Kendradi Bala**: Kendra=60, Panaphara=30, Apoklima=15 shashtiamsas.
- **Drekkana Bala**: Male planets in 1st drekkana (+15), Hermaphrodite in 2nd (+15), Female in 3rd (+15). Max 15.

### B. Dig Bala (Directional Strength)
- Cardinal Power Points: Sun/Mars (10th/MC), Jup/Merc (1st/Asc), Sat (7th/Desc), Moon/Ven (4th/IC).
- Formula: `(180.0 - |p_lon - powerless_lon|) / 180.0 * 60.0`. Max 60.

### C. Kala Bala (Temporal Strength)
- **Nathonnatha Bala**: Diurnal (Sun, Jup, Ven) / Nocturnal (Moon, Mars, Sat) / Merc (60 always). Max 60.
- **Paksha Bala**: Lunar phase separation. Benefics = `(angle / 180.0) * 60.0`, Malefics = `60.0 - Paksha`. Max 60.
- **Ayana Bala**: `(24 + Kranti) * 1.25` clamped between 0 and 60.
- **Tribhaga Bala**: Day 1/3 (Merc), 2/3 (Sun), 3/3 (Sat). Night 1/3 (Moon), 2/3 (Mars), 3/3 (Ven). Jupiter gets 60 always.
- **Vara Bala**: Day Lord (+45).
- **Hora Bala**: Hour Lord (+60).
- **Masa Bala**: Month Lord (+30).
- **Varsha Bala**: Year Lord (+15).

### D. Cheshta Bala (Motional Strength)
- Sun: Ayana Bala
- Moon: Paksha Bala
- Star Planets (Mars, Merc, Jup, Ven, Sat): Derived from Phase 2A apparent daily velocity `velocity_deg_day`:
  - Retrograde (`velocity < 0`): 60 shashtiamsas
  - Stationary (`|velocity| < 0.005`): 15 shashtiamsas
  - Fast (`velocity > 1.15 * avg`): 45 shashtiamsas
  - Normal (`0.85 * avg <= velocity <= 1.15 * avg`): 30 shashtiamsas
  - Slow (`0 < velocity < 0.85 * avg`): 15 shashtiamsas

### E. Naisargika Bala (Natural Strength)
- Sun=60.0, Moon=51.43, Venus=42.85, Jupiter=34.28, Mercury=25.70, Mars=17.14, Saturn=8.57.

### F. Drik Bala (Aspectual Strength)
- BPHS Drishti Pinda calculation from all aspecting planets, including special aspects for Mars (4th/8th), Jupiter (5th/9th), Saturn (3rd/10th), modified by +1/4th (benefic) or -1/4th (malefic).
