# Docker Setup Guide - MindBridge Health AI

## What You're Building Today

A containerized PostgreSQL database for MindBridge that:
- Runs in Docker (industry standard)
- Persists data between restarts
- Can be deployed anywhere
- Proves you understand production infrastructure

**Interview value:** "I containerized the database layer using Docker Compose with health checks and persistent volumes."

---

## Step-by-Step Setup (45 minutes)

### 1. Install Docker Desktop (10 min)

**Download:**
- Go to: https://www.docker.com/products/docker-desktop
- Download Docker Desktop for Windows
- Install (will require system restart)

**After restart, verify:**
```powershell
docker --version
docker compose version
```

Should see:
```
Docker version 24.x.x
Docker Compose version v2.x.x
```

---

### 2. Install Python PostgreSQL Driver (2 min)

```powershell
pip install psycopg2-binary --break-system-packages
```

---

### 3. Create Docker Files (5 min)

**Save these 3 files to: `E:\Mindbridge health care\`**

1. `docker-compose.yml` (download from outputs above)
2. `test_docker_db.py` (download from outputs above)
3. `.dockerignore` (create this):

```
__pycache__/
*.pyc
*.env
.git/
reports/
logs/
*.db
```

---

### 4. Start Docker Database (3 min)

```powershell
cd "E:\Mindbridge health care"

# Start PostgreSQL in background
docker compose up -d

# Check it's running
docker compose ps

# View logs
docker compose logs -f db
```

**Expected output:**
```
✓ Container mindbridge-db  Started
```

---

### 5. Test Connection & Generate Report (5 min)

```powershell
python test_docker_db.py
```

**You'll see:**
```
✅ Connection successful!
✅ Table created successfully!
✅ Report generated successfully!
📁 Location: reports/docker_test_report_20260218_*.txt
```

---

### 6. Verify Everything Works (2 min)

```powershell
# Check running containers
docker ps

# Connect to database directly (optional)
docker exec -it mindbridge-db psql -U mindbridge_user -d mindbridge

# Inside PostgreSQL shell:
\dt              # List tables
SELECT * FROM patients;
\q               # Quit
```

---

## Common Commands

```powershell
# Start services
docker compose up -d

# Stop services
docker compose down

# Restart services
docker compose restart

# View logs
docker compose logs -f db

# Fresh start (deletes all data!)
docker compose down -v
docker compose up -d
```

---

## What This Proves to Employers

✅ You understand containerization (Docker)
✅ You can set up PostgreSQL with proper config
✅ You know health checks and dependencies
✅ You use persistent volumes (data survives restarts)
✅ You can connect Python to containerized databases
✅ You follow production best practices

**This is Week 3-4 material in most bootcamps. You're doing it Week 2.**

---

## Troubleshooting

**Docker won't start:**
- Enable WSL 2 in Windows Features
- Restart computer
- Run Docker Desktop as Administrator

**Connection fails:**
- Make sure Docker is running: `docker ps`
- Check container status: `docker compose ps`
- View logs: `docker compose logs db`

**Port already in use:**
- Change port in docker-compose.yml:
  ```yaml
  ports:
    - "5433:5432"  # Use 5433 instead
  ```

---

## Next Steps (Week 3)

- [ ] Add Alembic migrations to Docker setup
- [ ] Create Dockerfile for FastAPI backend
- [ ] Deploy to Railway with Docker
- [ ] Add Redis for caching

---

**Portfolio piece complete:** ✅ Docker + PostgreSQL working locally

**Time invested:** 45 minutes

**Interview value:** HUGE (most candidates can't do this)
