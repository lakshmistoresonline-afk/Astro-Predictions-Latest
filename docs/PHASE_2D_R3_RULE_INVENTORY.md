# Phase 2D-R3 Rule Inventory — Astrovision

## 1. Yogas
The following 15 base Yogas are implemented in `apps/api/engines/yogas/rules.py` and evaluated via `YogaEvaluator`:

1. **YOGA_RUCHAKA**: Ruchaka Mahapurusha Yoga (Mars in Kendra in Own/Exaltation)
2. **YOGA_BHADRA**: Bhadra Mahapurusha Yoga (Mercury in Kendra in Own/Exaltation)
3. **YOGA_HAMSA**: Hamsa Mahapurusha Yoga (Jupiter in Kendra in Own/Exaltation)
4. **YOGA_MALAVYA**: Malavya Mahapurusha Yoga (Venus in Kendra in Own/Exaltation)
5. **YOGA_SHASHA**: Shasha Mahapurusha Yoga (Saturn in Kendra in Own/Exaltation)
6. **YOGA_GAJA_KESARI**: Gaja Kesari Yoga (Jupiter in Kendra from Moon, not debilitated)
7. **YOGA_BUDHA_ADITYA**: Budha Aditya Yoga (Sun and Mercury conjunct within 12° orb)
8. **YOGA_DHARMA_KARMA**: Dharma-Karma Adhipati Yoga (9th & 10th lords conjunct, mutual aspect, or parivartana)
9. **YOGA_PARIVARTANA_{h1}_{h2}**: Parivartana Yogas (Maha, Kahala, Dainya based on exchanging houses)
10. **YOGA_HARSHA_VIPARITA**: Harsha Viparita Yoga (6th lord in 6th, 8th, or 12th)
11. **YOGA_SARALA_VIPARITA**: Sarala Viparita Yoga (8th lord in 6th, 8th, or 12th)
12. **YOGA_VIMALA_VIPARITA**: Vimala Viparita Yoga (12th lord in 6th, 8th, or 12th)
13. **YOGA_NEECHA_BHANGA_{PLANET}**: Neecha Bhanga Raja Yoga (Debilitated planet cancelled by dispositor/exalt-lord in Kendra)
14. **YOGA_SUNAPHA**: Sunapha Chandra Yoga (Planets in 2nd from Moon)
15. **YOGA_ANAPHA**: Anapha Chandra Yoga (Planets in 12th from Moon)
16. **YOGA_DURUDHARA**: Durudhara Chandra Yoga (Planets in 2nd and 12th from Moon)
17. **YOGA_VESHI**: Veshi Surya Yoga (Planets in 2nd from Sun)
18. **YOGA_VASHI**: Vashi Surya Yoga (Planets in 12th from Sun)
19. **YOGA_OBHAYACHARI**: Obhayachari Surya Yoga (Planets in 2nd and 12th from Sun)

## 2. Doshas
The following 3 base Doshas are implemented in `apps/api/engines/doshas/rules.py` and evaluated via `DoshaEvaluator`:

1. **DOSHA_MANGLIK**: Manglik / Kuja Dosha (Mars in 1/2/4/7/8/12 from Ascendant/Moon)
2. **DOSHA_KEMADRUMA**: Kemadruma Dosha (Moon isolated, no planets in 2/12)
3. **DOSHA_KALA_SARPA**: Kala Sarpa Condition (All 7 classical planets on one side of Rahu-Ketu axis)

## 3. Astronomy Boundary Analysis
The Yoga and Dosha engines strictly consume the `CanonicalVedicChart` state and do not invoke any astronomical calculations (`Skyfield`, `DE440s`, Julian day, etc.). No `Skyfield` dependencies exist in these folders.
