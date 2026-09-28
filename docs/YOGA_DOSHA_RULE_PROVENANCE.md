# Vedic Yoga & Dosha Rule Provenance & Specifications — Astrovision (Phase 2D)

## 1. Executive Summary

This document specifies the rule provenance, traditional literature sources, trigger conditions, cancellation exceptions, orb conventions, and Whole Sign aspect rules for all supported Yogas and Doshas in **Astrovision**.

### Canonical Selection Rule
- **CANONICAL CONVENTIONS**: Maharishi Parashara (*Brihat Parasara Hora Sastra* - BPHS), Vaidyanatha Dikshita (*Jataka Parijata*), Mantreswara (*Phaladeepika*), and Kalyanavarman (*Saravali*).
- **HOUSE CONVENTION**: Whole Sign House System derived from Phase 2A Canonical Sidereal Ascendant.
- **ASPECT CONVENTION**: Parashari House Aspect Engine (`apps/api/engines/yogas/aspects.py`).

---

## 2. Canonical Aspect Rules

All planetary aspects are evaluated on Whole Sign house distances:
1. **7th House Aspect (All Planets)**: Every planet aspects the 7th house from its placement ($180^\circ$ Whole Sign distance).
2. **Mars Special Aspects**: Aspects 4th ($90^\circ$), 7th ($180^\circ$), and 8th ($210^\circ$) houses.
3. **Jupiter Special Aspects**: Aspects 5th ($120^\circ$), 7th ($180^\circ$), and 9th ($240^\circ$) houses.
4. **Saturn Special Aspects**: Aspects 3rd ($60^\circ$), 7th ($180^\circ$), and 10th ($270^\circ$) houses.
5. **Rahu / Ketu Special Aspects**: Aspect 5th ($120^\circ$), 7th ($180^\circ$), and 9th ($240^\circ$) houses.

---

## 3. Supported Yogas Provenance & Trigger Specifications

### A. Pancha Mahapurusha Yogas (*BPHS* Ch. 75, *Phaladeepika* Ch. 6)
Requires a non-luminary classical planet (Mars, Mercury, Jupiter, Venus, Saturn) to be placed in a **Kendra House (1, 4, 7, 10)** from the Ascendant AND in its **Own Sign** or **Exaltation Sign**.
1. **Ruchaka Yoga** (Mars in Aries, Scorpio, or Capricorn in Kendra).
2. **Bhadra Yoga** (Mercury in Gemini or Virgo in Kendra).
3. **Hamsa Yoga** (Jupiter in Sagittarius, Pisces, or Cancer in Kendra).
4. **Malavya Yoga** (Venus in Taurus, Libra, or Pisces in Kendra).
5. **Shasha Yoga** (Saturn in Capricorn, Aquarius, or Libra in Kendra).

### B. Gaja Kesari Yoga (*BPHS* Ch. 36, *Phaladeepika* Ch. 6)
- **Trigger**: Jupiter positioned in a **Kendra House (1, 4, 7, 10)** from the Moon.
- **Qualifiers**: Jupiter must not be debilitated or combust by Sun ($< 11^\circ$).

### C. Budha Aditya Yoga (*BPHS* Ch. 36)
- **Trigger**: Sun and Mercury conjunct in the same Rashi sign.
- **Orb Convention**: Longitudinal distance between Sun and Mercury $\le 12.0^\circ$.
- **Cancellation**: Mercury is combust if longitudinal distance to Sun $< 3.0^\circ$.

### D. Dharma-Karma Adhipati Yoga (*BPHS* Ch. 36)
- **Trigger**: Relationship between the **9th Lord** (Dharma) and **10th Lord** (Karma).
- **Qualifying Relationships**: Conjunction in same sign, Mutual Aspect (7th house aspect), or Parivartana (Sign Exchange).

### E. Parivartana Yogas (*Phaladeepika* Ch. 6)
- **Trigger**: Mutual sign exchange where Lord of House A occupies House B, and Lord of House B occupies House A.
- **Classifications**:
  - **Maha Parivartana**: Exchange between Kendras (1, 4, 7, 10), Trikonas (5, 9), 2nd, or 11th houses.
  - **Kahala Parivartana**: Exchange involving the 3rd house.
  - **Dainya Parivartana**: Exchange involving Dusthanas (6th, 8th, or 12th houses).

### F. Viparita Raja Yogas (*Phaladeepika* Ch. 6)
- **Trigger**: Dusthana lords placed in Dusthana houses without involvement of benefic house lords.
  - **Harsha Yoga**: 6th Lord placed in 6th, 8th, or 12th house.
  - **Sarala Yoga**: 8th Lord placed in 6th, 8th, or 12th house.
  - **Vimala Yoga**: 12th Lord placed in 6th, 8th, or 12th house.

### G. Neecha Bhanga Raja Yoga (*BPHS* Ch. 42, *Phaladeepika* Ch. 6)
- **Trigger**: Debilitated planet receiving cancellation via dispositor or exaltation lord:
  1. The lord of the sign occupied by the debilitated planet is in a Kendra (1, 4, 7, 10) from Ascendant or Moon.
  2. The lord of the exaltation sign of the debilitated planet is in a Kendra from Ascendant or Moon.

### H. Chandra Yogas (*BPHS* Ch. 37, *Phaladeepika* Ch. 6)
- **Sunapha Yoga**: Non-luminary planet (Mars, Mercury, Jupiter, Venus, Saturn) in 2nd house from Moon.
- **Anapha Yoga**: Non-luminary planet in 12th house from Moon.
- **Durudhara Yoga**: Non-luminary planets in both 2nd and 12th houses from Moon.

### I. Surya Yogas (*BPHS* Ch. 37, *Phaladeepika* Ch. 6)
- **Veshi Yoga**: Non-luminary planet in 2nd house from Sun.
- **Vashi Yoga**: Non-luminary planet in 12th house from Sun.
- **Obhayachari Yoga**: Non-luminary planets in both 2nd and 12th houses from Sun.

---

## 4. Supported Doshas Provenance & Trigger Specifications

### A. Manglik / Kuja Dosha (*BPHS*, *Jataka Parijata*)
- **Trigger**: Mars placed in **1st, 2nd, 4th, 7th, 8th, or 12th house** from Ascendant OR Moon.
- **Exceptions & Cancellation Rules**:
  1. Mars in own sign (Aries, Scorpio) or exaltation sign (Capricorn).
  2. Mars in Cancer (debilitation) or in 2nd house in Gemini/Virgo.
  3. Mars conjunct or aspected by Jupiter.

### B. Kemadruma Dosha (*BPHS* Ch. 37, *Phaladeepika* Ch. 6)
- **Trigger**: No planets (excluding Sun, Rahu, Ketu) in 2nd or 12th house from Moon.
- **Cancellation Exception**: Planets present in Kendra houses (1, 4, 7, 10) from Moon or Ascendant.

### C. Kala Sarpa-Type Condition (*Modern Classical Synthesis*)
- **Trigger**: All 7 classical planets (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn) contained within one $180^\circ$ hemisphere bounded by Rahu and Ketu.
- **Convention Note**: Outer planets (Uranus, Neptune, Pluto) are excluded by classical traditional rules.
