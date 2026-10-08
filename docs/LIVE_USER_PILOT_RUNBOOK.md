# Astrovision Version 6.0.0 Live Real-User Local Pilot Runbook

## Overview
This runbook provides complete operational procedures for executing the **Controlled Real-User Local Pilot Environment** for Astrovision on a Windows host system.

---

## 1. Prerequisites & Environment Setup

### Environment Configuration
1. Copy `.env.local-pilot.example` to `.env.local-pilot` (or `.env`).
2. Replace default secret keys with strong 32-character random strings:
   - `ADMIN_API_KEY`: e.g. `pilot_admin_9a8b7c6d5e4f3a2b1c0d_prod`
   - `JWT_SECRET_KEY`: e.g. `pilot_jwt_1f2e3d4c5b6a7b8c9d0e_prod`
   - `DATABASE_URL`: `postgresql://astro_user:pilot_db_pass_99@localhost:5432/astrovision_db`

---

## 2. Windows Service Startup Sequence

### Step 1: Start PostgreSQL Container
```powershell
docker-compose up -d postgres
```

### Step 2: Start Ollama & Verify Models
```powershell
# Start Ollama service
ollama serve

# Verify required models are pulled
ollama list
# Ensure 'gemma4' and 'qwen3.5' are installed
```

### Step 3: Run Database Migrations
```powershell
alembic upgrade head
```

### Step 4: Start FastAPI Backend Server
```powershell
uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 --env-file .env.local-pilot
```

### Step 5: Start Web Frontend
```powershell
cd apps/web
npm run build
npm run start
```

---

## 3. Health & Readiness Verification

### Check Readiness Endpoint
```powershell
curl http://localhost:8000/ready
# Response: {"ready": true, "ephemeris_kernel": "NASA JPL DE440s"}
```

### Check Subsystem Breakdown
```powershell
curl http://localhost:8000/health
```

---

## 4. Database Backup & Restoration Procedure

### Create Database Backup
```powershell
docker exec -t astrovision-postgres pg_dump -U astro_user astrovision_db > backups/pilot_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.sql
```

### Restore Database Backup
```powershell
docker exec -i astrovision-postgres psql -U astro_user astrovision_db < backups/pilot_backup_20261008.sql
```

---

## 5. Emergency Shutdown Procedure

In the event of a security incident, data anomaly, or resource abuse:

1. **Disable Public API Binding**: Stop the API process or block port 8000 in Windows Firewall:
   ```powershell
   netsh advfirewall firewall add rule name="Block_Astrovision_Pilot" dir=in action=block protocol=TCP localport=8000
   ```
2. **Revoke Active Sessions**: Restart the API process to clear in-memory sessions or execute token revocation sweep.
3. **Stop PostgreSQL Container**:
   ```powershell
   docker-compose stop postgres
   ```
