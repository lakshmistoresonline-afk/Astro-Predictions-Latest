# Varga Rule Provenance & Canonical Conventions — Astrovision (Phase 2B)

## 1. Executive Summary

This document specifies the exact rule provenance, mathematical segment algorithms, sign mapping rules, and traditional sources for all 16 Shodashavargas (D1 through D60) in **Astrovision**.

### Canonical Selection Rule
- **CANONICAL CONVENTION**: Maharishi Parashara Traditional System (*Brihat Parasara Hora Sastra*, Chapters 6–7).
- **DOCUMENTED RATIONALE**: Parashari Varga rules form the authoritative classical foundation of Vedic astrology. All 16 divisional charts are calculated using exact full-precision sidereal longitudes produced by Phase 2A (Skyfield 1.55 + NASA JPL DE440s + Lahiri Ayanamsha) without pre-rounding.

---

## 2. Comprehensive 16-Varga Mathematical Specifications

| Varga | Division Name | Division Factor ($N$) | Segment Size | Canonical Starting Sign & Progression Rules | Classical Source Reference |
|---|---|---|---|---|---|
| **D1** | Rashi | 1 | $30^\circ$ | Reproduces canonical Rashi placement ($1:1$). Sign = $\lfloor \text{Lon} / 30 \rfloor + 1$. | *BPHS* Ch. 6, v. 2 |
| **D2** | Hora | 2 | $15^\circ$ | **Odd Signs**: $0^\circ-15^\circ \rightarrow$ Sun ($\text{Leo}=5$), $15^\circ-30^\circ \rightarrow$ Moon ($\text{Cancer}=4$).<br>**Even Signs**: $0^\circ-15^\circ \rightarrow$ Moon ($\text{Cancer}=4$), $15^\circ-30^\circ \rightarrow$ Sun ($\text{Leo}=5$). | *BPHS* Ch. 6, v. 5-6 |
| **D3** | Drekkana | 3 | $10^\circ$ | **Div 1** ($0^\circ-10^\circ$): Same sign $S$.<br>**Div 2** ($10^\circ-20^\circ$): 5th sign from $S$ ($S+4 \pmod{12}$).<br>**Div 3** ($20^\circ-30^\circ$): 9th sign from $S$ ($S+8 \pmod{12}$). | *BPHS* Ch. 6, v. 7-8 |
| **D4** | Chaturthamsa | 4 | $7^\circ 30'$ ($7.5^\circ$) | Divisions 1..4 start from $S$ and advance by 4 signs ($S, S+3, S+6, S+9 \pmod{12}$). | *BPHS* Ch. 6, v. 9 |
| **D7** | Saptamsa | 7 | $4^\circ 17' 08.57"$ ($4.2857^\circ$) | **Odd Signs**: Starts from $S$.<br>**Even Signs**: Starts from 7th sign from $S$ ($S+6 \pmod{12}$). Advance sequentially sign-by-sign. | *BPHS* Ch. 6, v. 10-11 |
| **D9** | Navamsa | 9 | $3^\circ 20'$ ($3.3333^\circ$) | **Movable Signs** ($1,4,7,10$): Starts from $S$.<br>**Fixed Signs** ($2,5,8,11$): Starts from 9th sign ($S+8 \pmod{12}$).<br>**Dual Signs** ($3,6,9,12$): Starts from 5th sign ($S+4 \pmod{12}$). Advance sequentially. | *BPHS* Ch. 6, v. 12-14 |
| **D10** | Dasamsa | 10 | $3^\circ 00'$ ($3.0^\circ$) | **Odd Signs**: Starts from $S$.<br>**Even Signs**: Starts from 9th sign ($S+8 \pmod{12}$). Advance sequentially sign-by-sign. | *BPHS* Ch. 6, v. 15-16 |
| **D12** | Dvadasamsa | 12 | $2^\circ 30'$ ($2.5^\circ$) | Starts from $S$ and advances sequentially sign-by-sign ($S, S+1, \dots, S+11 \pmod{12}$). | *BPHS* Ch. 6, v. 17 |
| **D16** | Shodasamsa | 16 | $1^\circ 52' 30"$ ($1.875^\circ$) | **Movable Signs**: Starts from Aries ($1$).<br>**Fixed Signs**: Starts from Leo ($5$).<br>**Dual Signs**: Starts from Sagittarius ($9$). Advance sequentially. | *BPHS* Ch. 6, v. 18-19 |
| **D20** | Vimsamsa | 20 | $1^\circ 30'$ ($1.5^\circ$) | **Movable Signs**: Starts from Aries ($1$).<br>**Fixed Signs**: Starts from Sagittarius ($9$).<br>**Dual Signs**: Starts from Leo ($5$). Advance sequentially. | *BPHS* Ch. 6, v. 20-21 |
| **D24** | Chaturvimsamsa | 24 | $1^\circ 15'$ ($1.25^\circ$) | **Odd Signs**: Starts from Leo ($5$).<br>**Even Signs**: Starts from Cancer ($4$). Advance sequentially sign-by-sign. | *BPHS* Ch. 6, v. 22-23 |
| **D27** | Saptavimsamsa | 27 | $1^\circ 06' 40"$ ($1.1111^\circ$) | **Fiery Signs** ($1,5,9$): Starts from Aries ($1$).<br>**Earthy** ($2,6,10$): Starts from Cancer ($4$).<br>**Airy** ($3,7,11$): Starts from Libra ($7$).<br>**Watery** ($4,8,12$): Starts from Capricorn ($10$). | *BPHS* Ch. 6, v. 24-26 |
| **D30** | Trimsamsa | 30 (Unequal) | Unequal ($5^\circ, 5^\circ, 8^\circ, 7^\circ, 5^\circ$) | **Odd Signs**: $0-5^\circ \rightarrow$ Mars (Aries), $5-10^\circ \rightarrow$ Saturn (Aquarius), $10-18^\circ \rightarrow$ Jupiter (Sagittarius), $18-25^\circ \rightarrow$ Mercury (Gemini), $25-30^\circ \rightarrow$ Venus (Libra).<br>**Even Signs**: $0-5^\circ \rightarrow$ Venus (Taurus), $5-12^\circ \rightarrow$ Mercury (Virgo), $12-20^\circ \rightarrow$ Jupiter (Pisces), $20-25^\circ \rightarrow$ Saturn (Capricorn), $25-30^\circ \rightarrow$ Mars (Scorpio). | *BPHS* Ch. 6, v. 27-28 |
| **D40** | Khavedamsa | 40 | $0^\circ 45'$ ($0.75^\circ$) | **Odd Signs**: Starts from Aries ($1$).<br>**Even Signs**: Starts from Libra ($7$). Advance sequentially sign-by-sign. | *BPHS* Ch. 6, v. 29-30 |
| **D45** | Akshavedamsa | 45 | $0^\circ 40'$ ($0.6667^\circ$) | **Movable Signs**: Starts from Aries ($1$).<br>**Fixed Signs**: Starts from Leo ($5$).<br>**Dual Signs**: Starts from Sagittarius ($9$). Advance sequentially. | *BPHS* Ch. 6, v. 31-32 |
| **D60** | Shashtiamsa | 60 | $0^\circ 30'$ ($0.5^\circ$) | Starts from $S$ and advances sequentially sign-by-sign ($S, S+1, \dots, S+59 \pmod{12}$). Associated with 60 Shashtiamsa deity names. | *BPHS* Ch. 6, v. 33-41 |

---

## 3. Strict Boundary Precision Rules

1. **Unrounded Calculation**: Varga division indices and signs are derived directly from 64-bit IEEE floating-point sidereal longitudes ($0.000000^\circ$ precision).
2. **Boundary Testing**: Fixture tests explicitly verify behavior at exact division boundaries (e.g. $0^\circ$, $3^\circ 20'$, $7.5^\circ$, $10^\circ$, $15^\circ$, $29^\circ 59' 59.999"$).
3. **No Silent Fallbacks**: Unsupported Varga division names or corrupted input longitudes fail closed immediately.
