# Phase 2E-R1 Shadbala Rule Inventory

## Sthana Bala (Positional Strength)
1. **Uccha Bala**: Exaltation strength derived directly from exact degree distance to the planet's specific BPHS debilitation point (`(dist / 180.0) * 60.0`). Range: 0 to 60 shashtiamsas.
2. **Sapta Vargaja Bala**: Strength evaluated across 7 divisional charts (D1, D2, D3, D7, D9, D12, D30) based on Panchadha Maitri (Compound Friendship = Naisargika + Tatkalika). Max points: 30 per own sign, 22.5 Adhi Mitra, 15 Mitra, 7.5 Sama, 3.75 Satru, 1.875 Adhi Satru.
3. **Ojha-Yugma Bala**: Rashi & Navamsa gender-sign alignment. Female planets (Moon, Venus) get 15 points for even signs in D1/D9. Male/Neutral planets get 15 points for odd signs in D1/D9. Range: 0 to 30 shashtiamsas.
4. **Kendradi Bala**: House placement strength relative to Lagna. Kendra (1, 4, 7, 10) = 60 points; Panaphara (2, 5, 8, 11) = 30 points; Apoklima (3, 6, 9, 12) = 15 points.
5. **Drekkana Bala**: Drekkana partition strength. Male planets get 15 points in 1st drekkana (0-10°); Hermaphrodite planets in 2nd (10-20°); Female planets in 3rd (20-30°).

## Dig Bala (Directional Strength)
6. **Dig Bala**: Angle from cardinal powerless point. Max (60 shashtiamsas) at power house (Sun/Mars in 10th MC, Jup/Merc in 1st Asc, Sat in 7th Desc, Moon/Ven in 4th IC). Min (0 shashtiamsas) at opposite house. Interpolated linearly with exact angular distance.

## Kala Bala (Temporal Strength)
7. **Nathonnatha Bala**: Diurnal/Nocturnal strength calculated from solar distance to Nadir (IC).
8. **Paksha Bala**: Lunar phase strength derived from Sun-Moon angular separation.
9. **Ayana Bala**: Declination-based strength (`(24 + Kranti) * 1.25`) calculated from tropical longitude.

## Cheshta Bala (Motional Strength)
10. **Cheshta Bala**: Retrograde planets receive 60 shashtiamsas, direct receive 30. Luminaries receive Ayana Bala (Sun) and Paksha Bala (Moon).

## Naisargika Bala (Natural Strength)
11. **Naisargika Bala**: Fixed classical constants (Sun=60.0, Moon=51.43, Venus=42.85, Jupiter=34.28, Mercury=25.70, Mars=17.14, Saturn=8.57).

## Drik Bala (Aspectual Strength)
12. **Drik Bala**: Aspect strength dynamically derived from aspectual angles with benefics (adding +1/4th of aspect power) and malefics (subtracting -1/4th of aspect power).
