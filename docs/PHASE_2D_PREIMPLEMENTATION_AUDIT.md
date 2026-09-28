# Phase 2D Pre-Implementation Audit — Vedic Yoga & Dosha Engine

## 1. Executive Summary

This pre-implementation audit inspects all existing Yoga and Dosha implementations, assumptions, rule limitations, consumers, and dependencies across the repository prior to implementing **Phase 2D (Authoritative Vedic Yoga & Dosha Engine)**.

---

## 2. Audit of Existing Yoga & Dosha Implementations

### A. `apps/api/engines/yoga_engine.py`
- **Current Signature**: `YogaEngine.detect_yogas(planetary_positions: dict) -> list`
- **Current Methodology & Critical Flaws**:
  1. **Only 2 Naive Rules**: Evaluates only `Budha Aditya` and `Gaja Kesari` based on crude string comparison of sign names.
  2. **No Degree Orbs or Combustion**: Budha Aditya triggers whenever Sun and Mercury share a sign name, ignoring degree orb (e.g., $12^\circ$) and Mercury combustion ($< 3^\circ$).
  3. **No Ascendant or House Reference**: Gaja Kesari triggers on simple sign index modulo arithmetic without evaluating Kendra from Ascendant or Moon house placements.
  4. **Zero Coverage for Major Classical Yogas & Doshas**: Missing Pancha Mahapurusha (Ruchaka, Bhadra, Hamsa, Malavya, Shasha), Dharma-Karma Adhipati, Parivartana, Viparita, Neecha Bhanga, Dhana Yogas, Raja Yogas, Manglik / Kuja Dosha, Kemadruma, and Kala Sarpa.
  5. **No Evidence or Provenance**: Returns simple dicts (`{"id": "...", "name": "...", "description": "..."}`) without condition breakdown, exception checks, or SHA-256 calculation hash.

---

## 3. Dependency Graph & Repository Consumers

```
[Phase 2A Canonical Astronomy State]
[Phase 2B 16-Varga Suite (D9, etc.)]
[Phase 2C Authoritative Dasha Timeline]
                 │
                 ▼
[Phase 2D Authoritative Yoga & Dosha Engine]
  (`apps/api/engines/yogas/` & `doshas/`)
                 │
   ┌─────────────┼──────────────────────────┐
   ▼             ▼                          ▼
[Report Engine] [Evidence Aggregator] [Prediction Engine]
   │             │                          │
   └─────────────┴──────────┬───────────────┘
                            ▼
               [API Routers & AI Context]
```

### Active Consumer Locations
1. `apps/api/engines/report_engine.py`: Invokes `YogaEngine.detect_yogas(...)` for Chapter 7 report generation (`chapter_7_yogas`).
2. `apps/api/engines/evidence_aggregator.py`: Consumes detected Yogas for domain prediction evidence.
3. `apps/api/engines/prediction_engine.py`: Passes Yogas to evidence aggregator.
4. `apps/api/main.py`: Serializes `yogas` in `/api/v1/birth-profile` response.
5. `apps/api/services/ai_service.py`: Passes Yogas in prompt context.

---

## 4. Replacement & Migration Strategy

1. **New Authoritative Packages**:
   - `apps/api/engines/yogas/` (Models, Aspect System, Evaluator, Rules, Provenance)
   - `apps/api/engines/doshas/` (Models, Evaluator, Rules, Provenance)
2. **Single Source of Truth**: Consume `CanonicalVedicChart` (Phase 2A), `Full16VargaSuite` (Phase 2B), and `FullVimshottariDashaResult` (Phase 2C).
3. **Machine-Readable Evidence**: Return structured `YogaResult` and `DoshaResult` carrying status (`DETECTED`, `NOT_DETECTED`, `INDETERMINATE`), satisfied/failed conditions, exception checks, and SHA-256 calculation hashes.
4. **Adapter for Legacy API**: Adapt `apps/api/engines/yoga_engine.py` to delegate directly to the authoritative Yoga & Dosha engines, ensuring 100% backward compatibility for API responses while consuming authoritative rule evaluation.
