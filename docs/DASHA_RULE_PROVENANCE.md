# Vimshottari Dasha Rule Provenance & Classical Specifications — Astrovision (Phase 2C)

## 1. Executive Summary

This document specifies the rule provenance, mathematical formulas, lord sequences, and classical literature references for the **Authoritative Vimshottari Dasha Engine** (Phase 2C) in **Astrovision**.

---

## 2. Classical Literature Provenance

- **Primary Source**: Maharishi Parashara, *Brihat Parasara Hora Sastra* (BPHS), Chapters 46–48 ("Vimshottari Dasha").
- **Canonical Cycle Length**: **120 Solar Years** ($43,830 \text{ Days}$ based on $365.25 \text{ days/year}$).

---

## 3. Planetary Mahadasha Cycle Durations

| Sequence | Planetary Lord | Vimshottari Duration (Years) | Fraction of 120 Years | Days ($365.25 \text{ d/yr}$) |
|---|---|---|---|---|
| 1 | **Ketu** | 7 Years | $7 / 120 = 0.058333$ | 2,556.75 Days |
| 2 | **Venus** | 20 Years | $20 / 120 = 0.166667$ | 7,305.00 Days |
| 3 | **Sun** | 6 Years | $6 / 120 = 0.050000$ | 2,191.50 Days |
| 4 | **Moon** | 10 Years | $10 / 120 = 0.083333$ | 3,652.50 Days |
| 5 | **Mars** | 7 Years | $7 / 120 = 0.058333$ | 2,556.75 Days |
| 6 | **Rahu** | 18 Years | $18 / 120 = 0.150000$ | 6,574.50 Days |
| 7 | **Jupiter** | 16 Years | $16 / 120 = 0.133333$ | 5,844.00 Days |
| 8 | **Saturn** | 19 Years | $19 / 120 = 0.158333$ | 6,939.75 Days |
| 9 | **Mercury** | 17 Years | $17 / 120 = 0.141667$ | 6,209.25 Days |
| **TOTAL** | **9 Lords** | **120 Years** | **1.000000** | **43,830.00 Days** |

---

## 4. Nakshatra to Planetary Lord Mapping

The 27 Nakshatras ($13^\circ 20'$ each) map to the 9 planetary lords in a repeating 3-cycle triad:

```
Cycle 1 (0° - 120°):     Ketu (Ashwini), Venus (Bharani), Sun (Krittika), Moon (Rohini), Mars (Mrigashira), Rahu (Ardra), Jupiter (Punarvasu), Saturn (Pushya), Mercury (Ashlesha)
Cycle 2 (120° - 240°):   Ketu (Magha), Venus (Purva Phalguni), Sun (Uttara Phalguni), Moon (Hasta), Mars (Chitra), Rahu (Swati), Jupiter (Vishakha), Saturn (Anuradha), Mercury (Jyeshtha)
Cycle 3 (240° - 360°):   Ketu (Mula), Venus (Purva Ashadha), Sun (Uttara Ashadha), Moon (Shravana), Mars (Dhanishta), Rahu (Shatabhisha), Jupiter (Purva Bhadrapada), Saturn (Uttara Bhadrapada), Mercury (Revati)
```

- **Lord Index Formula**: $\text{Lord Index} = (\text{Nakshatra Index} - 1) \pmod{9}$

---

## 5. Mathematical Hierarchy Formulas

### A. Birth Nakshatra Progress & Remaining Balance
Let $\lambda_{\text{Moon}}$ be the canonical sidereal longitude of the Moon in $[0^\circ, 360^\circ)$.
- Nakshatra Span: $\Delta_{\text{Nak}} = 13^\circ 20' = 13.3333333333^\circ$
- Nakshatra Index: $K = \lfloor \lambda_{\text{Moon}} / \Delta_{\text{Nak}} \rfloor + 1 \in [1, 27]$
- Nakshatra Start: $\lambda_{\text{start}} = (K - 1) \times \Delta_{\text{Nak}}$
- Elapsed Degrees: $\lambda_{\text{elapsed}} = \lambda_{\text{Moon}} - \lambda_{\text{start}}$
- Elapsed Fraction: $f_{\text{elapsed}} = \frac{\lambda_{\text{elapsed}}}{\Delta_{\text{Nak}}}$
- Remaining Fraction: $f_{\text{remaining}} = 1 - f_{\text{elapsed}}$
- Birth Mahadasha Balance (Years):
  $$MD_{\text{balance\_years}} = Y_{\text{lord}} \times f_{\text{remaining}}$$

### B. Nested Sub-Period Duration Formulas
For any parent period $P_{\text{parent}}$ (with duration $D_{\text{parent}}$ in days):
1. **Antardasha (AD)**:
   $$D_{\text{AD}} = D_{\text{MD}} \times \frac{Y_{\text{AD\_lord}}}{120}$$
2. **Pratyantardasha (PD)**:
   $$D_{\text{PD}} = D_{\text{AD}} \times \frac{Y_{\text{PD\_lord}}}{120}$$
3. **Sookshma (Sookshma)**:
   $$D_{\text{Sookshma}} = D_{\text{PD}} \times \frac{Y_{\text{Sookshma\_lord}}}{120}$$
4. **Prana (Prana)**:
   $$D_{\text{Prana}} = D_{\text{Sookshma}} \times \frac{Y_{\text{Prana\_lord}}}{120}$$

---

## 6. Sum-of-Subdivisions Invariant

For every period $P$ and its 9 nested child subdivisions $C_1, C_2, \dots, C_9$:
$$\sum_{i=1}^{9} \text{Duration}(C_i) \equiv \text{Duration}(P)$$
This invariant is tested mathematically at all 5 levels of the hierarchy.
