# Phase 2D-R1 Independent Rule Validation & Test Fixtures — Astrovision

## 1. Executive Summary

This document specifies the rule-by-rule independent validation test matrix, expected results, classical literature references, and evidence rationale for all supported Yogas and Doshas in **Astrovision**.

---

## 2. Independent Rule-by-Rule Validation Matrix

| Rule ID | Rule Name | Positive Case Fixture | Negative Case Fixture | Cancellation / Exception Case Fixture | Rationale & Classical Literature Source | Validation Status |
|---|---|---|---|---|---|---|
| **YOGA_BUDHA_ADITYA** | Budha Aditya Yoga | Subramanian T S (1986): Sun & Mercury in Virgo ($1.79^\circ$ orb $\le 12^\circ$) | London Native (1985): Sun in Cancer, Mercury in Leo (different signs) | New York Native (2026): Sun & Mercury conjunct in Virgo ($1.5^\circ$ orb). *Parashari Rule: Mercury is immune to combustion cancellation for Budha Aditya Yoga*. | *BPHS* Ch. 36. Sun and Mercury co-location within $12^\circ$ orb. | **PASS** |
| **YOGA_GAJA_KESARI** | Gaja Kesari Yoga | Paris Historical (1950): Jupiter in Aquarius (1st house from Moon in Aquarius) | Subramanian T S (1986): Jupiter in 8th house from Moon | Tokyo Native (2050): Jupiter in Capricorn (debilitated) | *BPHS* Ch. 36. Jupiter in Kendra from Moon and not in debilitation. | **PASS** |
| **YOGA_RUCHAKA** | Ruchaka Mahapurusha | Sydney Native (1995): Mars in Capricorn in 1st Kendra | Subramanian T S (1986): Mars in 12th house | Berlin Native (1968): Mars in Taurus (not own/exalt sign) | *BPHS* Ch. 75. Mars in own/exaltation sign in Kendra. | **PASS** |
| **YOGA_HAMSA** | Hamsa Mahapurusha | Greenwich (2000): Jupiter in Cancer in 10th Kendra | London Native (1985): Jupiter in Capricorn | Rome Native (1988): Jupiter in Gemini | *BPHS* Ch. 75. Jupiter in own/exaltation sign in Kendra. | **PASS** |
| **YOGA_MALAVYA** | Malavya Mahapurusha | Paris Historical (1950): Venus in Pisces in 1st Kendra | Subramanian T S (1986): Venus in 9th house | Delhi Native (1980): Venus in Virgo (debilitated) | *BPHS* Ch. 75. Venus in own/exaltation sign in Kendra. | **PASS** |
| **YOGA_DHARMA_KARMA** | Dharma-Karma Adhipati | New York Native (2026): 9th Lord and 10th Lord conjunct | Subramanian T S (1986): 9th Lord & 10th Lord disconnected | London Native (1985): 9th Lord in 12th house without aspect | *BPHS* Ch. 36. Conjunction, mutual aspect, or exchange between 9th and 10th lords. | **PASS** |
| **YOGA_HARSHA_VIPARITA** | Harsha Viparita Yoga | New York Native (2026): 6th Lord placed in 8th house | London Native (1985): 6th Lord in 1st house | Sydney Native (1995): 6th Lord in 10th house | *Phaladeepika* Ch. 6. 6th Lord in 6th, 8th, or 12th house. | **PASS** |
| **YOGA_SUNAPHA** | Sunapha Chandra Yoga | Tokyo Native (2050): Venus in 2nd house from Moon | London Native (1985): Planets in both 2nd and 12th | Paris Native (1950): Moon isolated | *BPHS* Ch. 37. Non-luminary planet in 2nd from Moon. | **PASS** |
| **DOSHA_MANGLIK** | Manglik / Kuja Dosha | Mumbai Native (1975): Mars in 1st house from Ascendant | London Native (1985): Mars in 3rd house | Subramanian T S (1986): Mars in 12th house, but exalted in Capricorn (Cancelled) | *BPHS* Ch. 80. Mars in 1/2/4/7/8/12, cancelled by own/exaltation/debilitation dignity or Jupiter aspect. | **PASS** |
| **DOSHA_KEMADRUMA** | Kemadruma Dosha | Cairo Native (2005): Moon isolated without 2nd/12th planets | London Native (1985): Venus in 12th from Moon | Subramanian T S (1986): Isolated 2nd/12th, but Sun/Mercury in Kendra (Cancelled) | *BPHS* Ch. 37. Moon isolated from 2nd/12th planets, cancelled by Kendra planets. | **PASS** |
| **DOSHA_KALA_SARPA** | Kala Sarpa Condition | Auckland Native (2012): All 7 classical planets on one side of Rahu-Ketu axis | Subramanian T S (1986): Planets distributed across axis | San Francisco (1992): Moon outside axis hemisphere | Modern Classical Synthesis. 7 classical planets contained within $180^\circ$ Rahu-Ketu arc. | **PASS** |

---

## 3. Machine-Readable Evidence & Fail-Closed Semantics

1. **Partial Chart Input Handling (`INDETERMINATE`)**:
   - If required planets/points (e.g., Moon for Chandra Yogas/Kemadruma, Sun/Mercury for Budha Aditya, Mars for Kuja Dosha) are absent from the input chart, status = **`INDETERMINATE`** (not `NOT_DETECTED`).
2. **Cryptographic SHA-256 Calculation Hash**:
   - Every result is stamped with a SHA-256 calculation hash tying rule_id, status, conditions, and canonical astronomy state hash together.
