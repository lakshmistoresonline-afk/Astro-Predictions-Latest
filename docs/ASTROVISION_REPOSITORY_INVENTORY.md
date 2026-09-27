# Astrovision Repository Inventory

## Backend (`apps/api/`)
- `main.py`: FastAPI application entrypoint and REST endpoints.
- `config.py`: Application settings and environment configuration.
- `engines/`:
  - `astronomical_engine.py`: Meeus astronomical calculation engine.
  - `birth_engine.py`: Birth coordinate and timezone processing.
  - `vedic_engine.py`: Sidereal rashi, house, and nakshatra analysis.
  - `western_engine.py`: Tropical aspect and house calculations.
  - `dasha_engine.py`: Vimshottari dasha hierarchy with birth balance.
  - `varga_engine.py` & `masterwork_engine.py`: Divisional vargas D1 to D60.
  - `yoga_engine.py`: Planetary combination rule engine.
  - `strength_engine.py`: Shadbala and Ashtakavarga calculators.
  - `prediction_engine.py`: Life domain evidence aggregator.
  - `report_engine.py`: Comprehensive astrological treatise compiler.
- `routers/`: Admin export and export utilities.
- `services/`: AI interpretation and validation service (Ollama).
- `tests/`: Unit and differential personalization tests.

## Frontend (`apps/web/`)
- `app/layout.tsx`: Root layout with celestial background.
- `app/page.tsx`: Full-width Astrovision command center and tab router.
- `tailwind.config.js` & `globals.css`: Celestial design system tokens.
