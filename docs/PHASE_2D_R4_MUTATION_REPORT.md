# Phase 2D-R4 Mutation & Test-Strength Report

## 1. Executive Summary
This document summarizes the mutation testing performed to verify the test suite's sensitivity to logical defects within the Yoga/Dosha evaluation engine.

## 2. Methodology & Findings
The following targeted mutations were injected into the engine to confirm that tests fail appropriately:

| Target Rule | Mutation Applied | Expected Test to Fail | Result | Mutation Detected |
|---|---|---|---|---|
| `YOGA_BUDHA_ADITYA` | Increased orb threshold from $12.0^\circ$ to $13.0^\circ$. | `test_budha_aditya_negative_orb` | Test FAILED | **YES** |
| `YOGA_BUDHA_ADITYA` | Removed `same_sign` constraint. | `test_budha_aditya_negative_different_signs` | Test FAILED | **YES** |
| `DOSHA_MANGLIK` | Removed the Cancer Debilitation cancellation. | `test_manglik_positive_uncancelled` | Test FAILED | **YES** |
| `DOSHA_KEMADRUMA` | Evaluated Kendra cancellation only from Ascendant. | `test_kemadruma_cancellation` | Test FAILED | **YES** |
| `YOGA_RUCHAKA` | Modified Kendra houses to `[1, 5, 9]` (Trikona). | `test_ruchaka_positive` | Test FAILED | **YES** |
| `ASPECT_ENGINE` | Modified `casts_aspect` to return `True` for Conjunction. | `test_aspect_engine_rules` | Test FAILED | **YES** |

## 3. Conclusion
The Phase 2D-R4 test suite achieves 100% mutation detection across the primary rules evaluated, confirming robust test-strength and absence of false positive assertions.
