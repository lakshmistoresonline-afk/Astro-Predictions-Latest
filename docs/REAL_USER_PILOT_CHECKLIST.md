# Astrovision Version 6.0.0 Real-User Pilot Checklist

## 1. Host Environment Setup (Windows Primary Host)
- [ ] **Python 3.13 Environment**: Verify virtual environment with required dependencies installed (`pip install -r apps/api/requirements.txt`).
- [ ] **NASA JPL DE440s Ephemeris Kernel**: Verify 32.7MB BSP kernel file exists at `apps/api/engines/astronomy/de440s.bsp` (SHA-256: `c1c7feeab882263fc493a9d5a5b2ddd71b54826cdf65d8d17a76126b260a49f2`).
- [ ] **PostgreSQL Database Container**: Start PostgreSQL container via `docker-compose up -d postgres`.
- [ ] **Alembic Schema Migrations**: Execute `alembic upgrade head` to bring PostgreSQL schema to latest revision.
- [ ] **Ollama Local AI Service**: Start Ollama service (`ollama serve`) and verify `gemma4` and `qwen3.5` models are downloaded (`ollama list`).

## 2. Server & Client Launch Sequence
- [ ] **Start API Server**: Run `uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 --env-file .env.local-pilot`.
- [ ] **Verify Readiness**: Query `curl http://localhost:8000/ready` and confirm `{"ready": true}`.
- [ ] **Start Web Frontend**: Navigate to `apps/web`, run `npm run build && npm run start`. Verify web server running at `http://localhost:3000`.
- [ ] **LAN IP Verification**: Discover host IPv4 address (`ipconfig`) and verify LAN API accessibility from mobile/second device (`http://<HOST-LAN-IP>:8000/health`).

## 3. Real Tester Experience Checklist
- [ ] **Web Registration & Login**: Real user signs up via `AuthModal`, receives JWT, and verifies `/auth/me` profile bootstrap.
- [ ] **Birth Profile Creation**: User enters birth date, civil time, and location to calculate canonical Vedic birth chart.
- [ ] **Chart & Predictions Display**: User views North Indian / South Indian Rashi chart, Vargas, Dashas, Yogas, Doshas, Shadbala, and 14 prediction domain evidence.
- [ ] **AI Interpretation Synthesis**: User requests AI interpretation and verifies structured LLM validation and trust badge.
- [ ] **PDF Treatise Export**: User exports 12-chapter PDF treatise report starting with `%PDF-1.4`.
- [ ] **User Feedback Submission**: User submits feedback or calculation discrepancy report via `/api/v1/feedback`.
- [ ] **Account Deletion & Data Privacy**: User deletes account via `DELETE /api/v1/auth/me` and confirms complete data cascade cleanup.
