# Astrovision Production Deployment Architecture & Specification

## 1. Production Topology
Astrovision consists of three containerized / cloud services:

```
[ Frontend: Cloudflare Pages / Next.js 14 ] ── (HTTPS API Calls) ──► [ Backend: FastAPI Container on Render / Railway ]
                                                                                │
                                                                                ├─► [ NASA JPL DE440s Kernel ]
                                                                                ├─► [ Persistent Database (SQLite / Postgres) ]
                                                                                └─► [ AI Service (Ollama / OpenAI API) ]
```

## 2. Service Specifications

### A. Frontend Deployment (Next.js 14 / Cloudflare Pages)
- **Directory**: `apps/web/`
- **Build Command**: `npm run build`
- **Output Directory**: `apps/web/.next` / `out`
- **Environment Variables**:
  - `NEXT_PUBLIC_API_URL`: Base URL of live FastAPI backend (e.g. `https://api.astrovision.io`).

### B. Backend API Deployment (FastAPI Container on Render / Railway)
- **Directory**: `apps/api/`
- **Container Definition**: `Dockerfile`
- **Build Command**: `pip install -r apps/api/requirements.txt`
- **Start Command**: `uvicorn apps.api.main:app --host 0.0.0.0 --port $PORT`
- **Resource Requirements**:
  - RAM: Minimum 1GB RAM (2GB recommended) for NASA JPL DE440s kernel in memory and Skyfield almanac calculations.
  - Disk: Minimum 500MB disk space (for `de440s.bsp` kernel file [32MB] and Python dependencies).
- **Environment Variables**:
  - `ENVIRONMENT`: `production`
  - `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed frontend origins (e.g. `https://astrovision.io,http://localhost:3000`).
  - `ADMIN_API_KEY`: Secret administrative API key for protected routes.
  - `DATABASE_URL`: Relational database connection string (e.g. `sqlite:////app/data/astrovision.db` or `postgresql://user:pass@host:5432/dbname`).
  - `AI_PROVIDER`: `ollama` or `openai`.
  - `OLLAMA_BASE_URL`: Base URL for local Ollama container (`http://ollama:11434`).

### C. AI Provider Deployment (Ollama / OpenAI)
- **Ollama Container**: Runs `ollama/ollama:latest` with volume mount `ollama-data:/root/.ollama` serving models `gemma4` and `qwen3.5`.
- **OpenAI Option**: Set `AI_PROVIDER=openai`, `OPENAI_API_KEY=your_key`, `OPENAI_MODEL=gpt-4o-mini`.

## 3. Health & Readiness Verification Endpoints
- **Health Check**: `GET /health` -> Returns `200 OK` with `"status": "healthy"`, `"database_status": "sqlite_persistent"`, `"ephemeris_status": "NASA JPL DE440s Verified"`.
- **Readiness Check**: `GET /ready` -> Returns `200 OK` with `{"ready": true}` when DE440s kernel is loaded.

## 4. Local Production Stack Launch (Docker Compose)
Launch the complete production containerized stack locally using Docker Compose:
```bash
docker-compose up -d --build
```
Verify status:
```bash
curl http://localhost:8000/health
```
