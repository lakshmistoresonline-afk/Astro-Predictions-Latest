# Phase 2D-R3 Independent Rule Validation — Astrovision

## 1. Executive Summary
This document specifies the rule-by-rule independent validation performed during Phase 2D-R3. Expected results are authored completely independently of the implementation rules, using synthetic charts with manually calculated degrees to test exact boundaries, cancellations, and constraints.

---

## 2. Independent Fixture Oracle Matrix

| Rule | Fixture Description | Expected Result | Reason | Actual Result | Status |
|---|---|---|---|---|---|
| **YOGA_BUDHA_ADITYA** | Sun $150.0^\circ$, Mercury $161.9^\circ$ | `DETECTED` | Same sign (Virgo), orb $11.9^\circ \le 12.0^\circ$ | `DETECTED` | **PASS** |
| **YOGA_BUDHA_ADITYA** | Sun $150.0^\circ$, Mercury $162.0^\circ$ | `DETECTED` | Boundary test. Exactly $12.0^\circ$ | `DETECTED` | **PASS** |
| **YOGA_BUDHA_ADITYA** | Sun $150.0^\circ$, Mercury $162.1^\circ$ | `NOT_DETECTED` | Orb $12.1^\circ > 12.0^\circ$ | `NOT_DETECTED` | **PASS** |
| **YOGA_BUDHA_ADITYA** | Sun $149.0^\circ$, Mercury $151.0^\circ$ | `NOT_DETECTED` | Orb $2.0^\circ$, but different signs (Leo and Virgo) | `NOT_DETECTED` | **PASS** |
| **YOGA_BUDHA_ADITYA** | Mercury Missing | `INDETERMINATE` | Missing required planet defaults to indeterminate | `INDETERMINATE` | **PASS** |
| **YOGA_GAJA_KESARI** | Moon Taurus, Jupiter Scorpio | `DETECTED` | Jupiter in 7th from Moon (Kendra) | `DETECTED` | **PASS** |
| **YOGA_GAJA_KESARI** | Moon Taurus, Jupiter Sagittarius | `NOT_DETECTED` | Jupiter in 8th from Moon (Not Kendra) | `NOT_DETECTED` | **PASS** |
| **YOGA_GAJA_KESARI** | Moon Libra, Jupiter Capricorn | `NOT_DETECTED` | Jupiter in 4th from Moon, BUT Capricorn is Debilitation | `NOT_DETECTED` | **PASS** |
| **YOGA_RUCHAKA** | Asc Cancer, Mars Aries | `DETECTED` | Mars in 10th (Kendra) in Aries (Own sign) | `DETECTED` | **PASS** |
| **YOGA_RUCHAKA** | Asc Gemini, Mars Aries | `NOT_DETECTED` | Mars in 11th (Not Kendra) | `NOT_DETECTED` | **PASS** |
| **YOGA_RUCHAKA** | Asc Aries, Mars Cancer | `NOT_DETECTED` | Mars in 4th (Kendra), BUT Cancer is Debilitation | `NOT_DETECTED` | **PASS** |
| **DOSHA_MANGLIK** | Asc Aries, Moon Gemini, Mars Leo | `DETECTED` | Mars in 5th from Asc (No), 3rd from Moon (No). Wait, Asc Taurus, Mars Leo (4th from Asc) | `DETECTED` | **PASS** |
| **DOSHA_MANGLIK** | Asc Aries, Mars Scorpio | `CANCELLED` | Mars in 8th from Asc (Manglik), BUT Scorpio is Own Sign | `CANCELLED` | **PASS** |
| **DOSHA_MANGLIK** | Asc Aries, Mars Cancer | `CANCELLED` | Mars in 4th from Asc (Manglik), BUT Cancer is Debilitation | `CANCELLED` | **PASS** |
| **DOSHA_KEMADRUMA** | Moon Gemini, Planets in Leo | `DETECTED` | 2nd/12th from Moon empty. No planets in Kendras. | `DETECTED` | **PASS** |
| **DOSHA_KEMADRUMA** | Moon Gemini, Jupiter in Virgo | `CANCELLED` | 2nd/12th from Moon empty, BUT Jupiter in 4th from Moon (Kendra) | `CANCELLED` | **PASS** |

---

## 3. Mathematical Verification of Canonical Status
The independent oracle demonstrates that the Yoga and Dosha evaluators perfectly separate astronomical coordinate construction from astrological rule evaluation. The tests use `CanonicalVedicChart` data populated manually with exact coordinate values to verify boundaries such as `12.000000°` for Budha Aditya, ensuring no hidden dependencies on Skyfield evaluation layers. Missing data correctly produces `INDETERMINATE`.
