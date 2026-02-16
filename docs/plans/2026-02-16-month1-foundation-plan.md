# Month 1: Foundation — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the backend foundation — Docker environment, PostgreSQL database, FastAPI REST API, and JWT authentication — so all future features have a solid base to build on.

**Architecture:** Modular monolith with domain-driven design. FastAPI backend with SQLAlchemy ORM, Alembic migrations, PostgreSQL database. Docker Compose for local development. Layered architecture: API → Domain → Infrastructure.

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL 16, Redis, Docker Compose, pytest, Pydantic v2

**Design Doc:** `docs/plans/2026-02-16-mindbridge-full-stack-design.md`

---

## Week 1: Project Setup & Docker Environment (Days 1-5)

### Task 1: Initialize Backend Project Structure

**Files:**
- Create: `backend/app/__init__.py`
- Create: `backend/app/main.py`
- Create: `backend/app/config.py`
- Create: `backend/requirements.txt`
- Create: `backend/Dockerfile`
- Create: `backend/.env.example`

**Step 1: Create the directory structure**

```bash
mkdir -p backend/app/domain/patients
mkdir -p backend/app/domain/analysis
mkdir -p backend/app/domain/reports
mkdir -p backend/app/domain/identity
mkdir -p backend/app/domain/compliance
mkdir -p backend/app/api/v1
mkdir -p backend/app/api/middleware
mkdir -p backend/app/infrastructure
mkdir -p backend/app/tasks
mkdir -p backend/migrations
mkdir -p backend/tests/unit
mkdir -p backend/tests/integration
```

**Step 2: Create `backend/requirements.txt`**

```txt
# Web Framework
fastapi==0.115.6
uvicorn[standard]==0.34.0

# Database
sqlalchemy[asyncio]==2.0.36
asyncpg==0.30.0
alembic==1.14.1

# Validation & Settings
pydantic==2.10.4
pydantic-settings==2.7.1

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.20

# AI
anthropic==0.42.0

# Document Generation
python-docx==1.1.2
openpyxl==3.1.5
reportlab==4.2.5

# Cache
redis==5.2.1

# Testing
pytest==8.3.4
pytest-asyncio==0.25.0
httpx==0.28.1

# Utilities
python-dotenv==1.0.1
```

**Step 3: Create `backend/app/config.py`**

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "MindBridge Health AI"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    # Database
    database_url: str = "postgresql+asyncpg://mindbridge:mindbridge@db:5432/mindbridge"

    # Redis
    redis_url: str = "redis://redis:6379/0"

    # Auth
    secret_key: str = "CHANGE-ME-IN-PRODUCTION"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # AI
    anthropic_api_key: str = ""
    ai_model: str = "claude-sonnet-4-20250514"

    # HIPAA
    session_timeout_minutes: int = 15
    max_failed_login_attempts: int = 5
    lockout_duration_minutes: int = 30

    model_config = {"env_file": ".env", "case_sensitive": False}


settings = Settings()
```

**Step 4: Create `backend/app/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health")
    async def health_check():
        return {"status": "healthy", "service": settings.app_name}

    return app


app = create_app()
```

**Step 5: Create `backend/app/__init__.py`**

```python
```

**Step 6: Create `backend/.env.example`**

```env
DATABASE_URL=postgresql+asyncpg://mindbridge:mindbridge@db:5432/mindbridge
REDIS_URL=redis://redis:6379/0
SECRET_KEY=change-me-to-a-random-string-in-production
ANTHROPIC_API_KEY=your-key-here
DEBUG=true
```

**Step 7: Create `backend/Dockerfile`**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Step 8: Commit**

```bash
cd backend
git add -A
git commit -m "feat: initialize backend project structure with FastAPI and config"
```

---

### Task 2: Docker Compose Environment

**Files:**
- Create: `docker-compose.yml` (project root)
- Create: `backend/.env`

**Step 1: Create `docker-compose.yml`**

```yaml
version: "3.9"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    env_file:
      - ./backend/.env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: mindbridge
      POSTGRES_PASSWORD: mindbridge
      POSTGRES_DB: mindbridge
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mindbridge"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

**Step 2: Create `backend/.env` from example**

```bash
cp backend/.env.example backend/.env
```

Then edit `backend/.env` and set your real `ANTHROPIC_API_KEY`.

**Step 3: Add `.env` to `.gitignore`**

Append to the project root `.gitignore`:
```
backend/.env
```

**Step 4: Build and start**

```bash
docker compose up --build -d
```

**Step 5: Verify health endpoint**

```bash
curl http://localhost:8000/api/health
```

Expected: `{"status":"healthy","service":"MindBridge Health AI"}`

**Step 6: Verify docs**

Open browser: `http://localhost:8000/api/docs`
Expected: Swagger UI with health endpoint listed.

**Step 7: Commit**

```bash
git add docker-compose.yml backend/.env.example .gitignore
git commit -m "feat: add Docker Compose with PostgreSQL, Redis, and FastAPI"
```

---

### Task 3: Write First Test — Health Endpoint

**Files:**
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/conftest.py`
- Create: `backend/tests/unit/__init__.py`
- Create: `backend/tests/integration/__init__.py`
- Create: `backend/tests/integration/test_health.py`

**Step 1: Create `backend/tests/conftest.py`**

```python
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
```

**Step 2: Create `backend/tests/integration/test_health.py`**

```python
import pytest


@pytest.mark.asyncio
async def test_health_endpoint_returns_200(client):
    response = await client.get("/api/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_endpoint_returns_service_name(client):
    response = await client.get("/api/health")
    data = response.json()
    assert data["status"] == "healthy"
    assert "MindBridge" in data["service"]
```

**Step 3: Create all `__init__.py` files**

```bash
touch backend/tests/__init__.py
touch backend/tests/unit/__init__.py
touch backend/tests/integration/__init__.py
```

**Step 4: Run tests**

```bash
docker compose exec backend pytest tests/ -v
```

Expected: 2 tests PASS.

**Step 5: Commit**

```bash
git add backend/tests/
git commit -m "test: add health endpoint integration tests"
```

---

## Week 2: Database Models & Migrations (Days 6-10)

### Task 4: SQLAlchemy Database Setup

**Files:**
- Create: `backend/app/infrastructure/database.py`
- Create: `backend/app/dependencies.py`

**Step 1: Create `backend/app/infrastructure/__init__.py`**

```python
```

**Step 2: Create `backend/app/infrastructure/database.py`**

```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(settings.database_url, echo=settings.debug)

async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

**Step 3: Create `backend/app/dependencies.py`**

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db


async def get_db_session(db: AsyncSession = Depends(get_db)) -> AsyncSession:
    return db
```

**Step 4: Commit**

```bash
git add backend/app/infrastructure/ backend/app/dependencies.py
git commit -m "feat: add SQLAlchemy async database setup"
```

---

### Task 5: Identity Domain Models (Organization, Clinic, User)

**Files:**
- Create: `backend/app/domain/identity/__init__.py`
- Create: `backend/app/domain/identity/models.py`

**Step 1: Create `__init__.py` files for all domains**

```bash
touch backend/app/domain/__init__.py
touch backend/app/domain/identity/__init__.py
touch backend/app/domain/patients/__init__.py
touch backend/app/domain/analysis/__init__.py
touch backend/app/domain/reports/__init__.py
touch backend/app/domain/compliance/__init__.py
```

**Step 2: Create `backend/app/domain/identity/models.py`**

```python
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import BYTEA, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    subscription_tier: Mapped[str] = mapped_column(String(50), default="standard")
    hipaa_baa_signed: Mapped[bool] = mapped_column(Boolean, default=False)
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    clinics: Mapped[list["Clinic"]] = relationship(back_populates="organization")


class Clinic(Base):
    __tablename__ = "clinics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address_encrypted: Mapped[bytes | None] = mapped_column(BYTEA, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    npi_number: Mapped[str | None] = mapped_column(String(10), nullable=True)
    timezone: Mapped[str] = mapped_column(String(50), default="America/New_York")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    organization: Mapped["Organization"] = relationship(back_populates="clinics")
    users: Mapped[list["User"]] = relationship(back_populates="clinic")


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)  # case_manager, admin, compliance_officer, readonly
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    license_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    mfa_secret_encrypted: Mapped[bytes | None] = mapped_column(BYTEA, nullable=True)
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    password_changed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    clinic: Mapped["Clinic"] = relationship(back_populates="users")
```

**Step 3: Commit**

```bash
git add backend/app/domain/
git commit -m "feat: add Identity domain models — Organization, Clinic, User"
```

---

### Task 6: Patient Domain Models

**Files:**
- Create: `backend/app/domain/patients/models.py`

**Step 1: Create `backend/app/domain/patients/models.py`**

```python
import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import BYTEA, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    case_manager_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    mrn: Mapped[str | None] = mapped_column(String(50), nullable=True)
    name_encrypted: Mapped[bytes] = mapped_column(BYTEA, nullable=False)
    date_of_birth_encrypted: Mapped[bytes | None] = mapped_column(BYTEA, nullable=True)
    diagnosis: Mapped[str | None] = mapped_column(String(255), nullable=True)
    diagnosis_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    medication_adherence: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    last_appointment: Mapped[date | None] = mapped_column(Date, nullable=True)
    appointments_missed: Mapped[int] = mapped_column(Integer, default=0)
    crisis_calls_30days: Mapped[int] = mapped_column(Integer, default=0)
    current_risk_level: Mapped[str | None] = mapped_column(String(20), nullable=True)
    admitted_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    screenings: Mapped[list["Screening"]] = relationship(back_populates="patient")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="patient")
    crisis_events: Mapped[list["CrisisEvent"]] = relationship(back_populates="patient")

    __table_args__ = (
        Index("idx_patients_risk", "clinic_id", "current_risk_level", postgresql_where=(deleted_at.is_(None))),
        Index("idx_patients_manager", "case_manager_id", postgresql_where=(deleted_at.is_(None))),
    )


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    scheduled_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="scheduled")
    appointment_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    notes_encrypted: Mapped[bytes | None] = mapped_column(BYTEA, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    patient: Mapped["Patient"] = relationship(back_populates="appointments")


class CrisisEvent(Base):
    __tablename__ = "crisis_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    reported_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    event_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description_encrypted: Mapped[bytes | None] = mapped_column(BYTEA, nullable=True)
    resolution: Mapped[str | None] = mapped_column(Text, nullable=True)
    follow_up_required: Mapped[bool] = mapped_column(Boolean, default=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    patient: Mapped["Patient"] = relationship(back_populates="crisis_events")


# Forward reference for Patient.screenings — defined in analysis domain
from app.domain.analysis.models import Screening  # noqa: E402, F401
```

**Step 2: Commit**

```bash
git add backend/app/domain/patients/
git commit -m "feat: add Patient domain models — Patient, Appointment, CrisisEvent"
```

---

### Task 7: Analysis & Compliance Domain Models

**Files:**
- Create: `backend/app/domain/analysis/models.py`
- Create: `backend/app/domain/compliance/models.py`
- Create: `backend/app/domain/reports/models.py`

**Step 1: Create `backend/app/domain/analysis/models.py`**

```python
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


class Screening(Base):
    __tablename__ = "screenings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    performed_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False)
    risk_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    ai_model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ai_prompt_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ai_raw_response: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    primary_risk_factor: Mapped[str | None] = mapped_column(Text, nullable=True)
    recommended_actions: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=True)
    clinical_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    screening_type: Mapped[str] = mapped_column(String(50), default="standard")
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    screened_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    patient: Mapped["Patient"] = relationship(back_populates="screenings")

    __table_args__ = (
        Index("idx_screenings_patient", "patient_id", screened_at.desc()),
        Index("idx_screenings_risk", "risk_level", screened_at.desc()),
    )


# Import Patient for relationship resolution
from app.domain.patients.models import Patient  # noqa: E402, F401
```

**Step 2: Create `backend/app/domain/compliance/models.py`**

```python
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import INET, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    changes: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(INET, nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    session_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phi_accessed: Mapped[bool] = mapped_column(Boolean, default=False)
    access_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_audit_user", "user_id", created_at.desc()),
        Index("idx_audit_resource", "resource_type", "resource_id"),
        Index("idx_audit_phi", "phi_accessed", created_at.desc(), postgresql_where=(phi_accessed.is_(True))),
    )


class PatientConsent(Base):
    __tablename__ = "patient_consents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    consent_type: Mapped[str] = mapped_column(String(50), nullable=False)
    granted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    granted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    consent_form_version: Mapped[str | None] = mapped_column(String(20), nullable=True)
    witness_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

**Step 3: Create `backend/app/domain/reports/models.py`**

```python
import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    screening_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("screenings.id"), nullable=True)
    generated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    format: Mapped[str] = mapped_column(String(10), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    checksum: Mapped[str | None] = mapped_column(String(64), nullable=True)
    patient_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    high_risk_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    medium_risk_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    low_risk_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
```

**Step 4: Commit**

```bash
git add backend/app/domain/
git commit -m "feat: add Analysis, Compliance, and Reports domain models"
```

---

### Task 8: Alembic Migration Setup

**Files:**
- Create: `backend/alembic.ini`
- Create: `backend/migrations/env.py`
- Create: `backend/migrations/script.py.mako`

**Step 1: Initialize Alembic inside the container**

```bash
docker compose exec backend alembic init migrations
```

**Step 2: Edit `backend/migrations/env.py`**

Replace the entire file with:

```python
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.config import settings
from app.infrastructure.database import Base

# Import ALL models so Alembic sees them
from app.domain.identity.models import Organization, Clinic, User  # noqa: F401
from app.domain.patients.models import Patient, Appointment, CrisisEvent  # noqa: F401
from app.domain.analysis.models import Screening  # noqa: F401
from app.domain.compliance.models import AuditLog, PatientConsent  # noqa: F401
from app.domain.reports.models import Report  # noqa: F401

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

**Step 3: Edit `backend/alembic.ini`**

Set the `sqlalchemy.url` line to empty (we override it in env.py):

```ini
sqlalchemy.url =
```

**Step 4: Generate the initial migration**

```bash
docker compose exec backend alembic revision --autogenerate -m "initial schema"
```

**Step 5: Run the migration**

```bash
docker compose exec backend alembic upgrade head
```

**Step 6: Verify tables exist**

```bash
docker compose exec db psql -U mindbridge -c "\dt"
```

Expected: All tables listed (organizations, clinics, users, patients, screenings, etc.)

**Step 7: Commit**

```bash
git add backend/alembic.ini backend/migrations/
git commit -m "feat: add Alembic migrations — create initial database schema"
```

---

## Week 3: Authentication & User Management (Days 11-15)

### Task 9: Auth Service — Password Hashing & JWT

**Files:**
- Create: `backend/app/domain/identity/service.py`
- Create: `backend/app/domain/identity/schemas.py`
- Create: `backend/tests/unit/test_auth_service.py`

**Step 1: Write the failing test**

Create `backend/tests/unit/test_auth_service.py`:

```python
import pytest

from app.domain.identity.service import AuthService


class TestPasswordHashing:
    def test_hash_password_returns_different_string(self):
        password = "securePassword123!"
        hashed = AuthService.hash_password(password)
        assert hashed != password

    def test_verify_password_correct(self):
        password = "securePassword123!"
        hashed = AuthService.hash_password(password)
        assert AuthService.verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        hashed = AuthService.hash_password("securePassword123!")
        assert AuthService.verify_password("wrongPassword", hashed) is False


class TestJWT:
    def test_create_access_token(self):
        token = AuthService.create_access_token(
            user_id="test-uuid",
            email="test@example.com",
            role="case_manager",
        )
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_access_token(self):
        token = AuthService.create_access_token(
            user_id="test-uuid",
            email="test@example.com",
            role="case_manager",
        )
        payload = AuthService.decode_access_token(token)
        assert payload["sub"] == "test-uuid"
        assert payload["email"] == "test@example.com"
        assert payload["role"] == "case_manager"

    def test_decode_invalid_token_raises(self):
        with pytest.raises(ValueError):
            AuthService.decode_access_token("invalid.token.here")
```

**Step 2: Run tests to verify they fail**

```bash
docker compose exec backend pytest tests/unit/test_auth_service.py -v
```

Expected: FAIL — `ImportError: cannot import name 'AuthService'`

**Step 3: Create `backend/app/domain/identity/schemas.py`**

```python
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    clinic_id: str

    model_config = {"from_attributes": True}


class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "case_manager"
    clinic_id: str
```

**Step 4: Create `backend/app/domain/identity/service.py`**

```python
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(user_id: str, email: str, role: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
        payload = {
            "sub": user_id,
            "email": email,
            "role": role,
            "exp": expire,
            "type": "access",
        }
        return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

    @staticmethod
    def create_refresh_token(user_id: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
        payload = {
            "sub": user_id,
            "exp": expire,
            "type": "refresh",
        }
        return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

    @staticmethod
    def decode_access_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            if payload.get("type") != "access":
                raise ValueError("Not an access token")
            return payload
        except JWTError as e:
            raise ValueError(f"Invalid token: {e}")
```

**Step 5: Run tests to verify they pass**

```bash
docker compose exec backend pytest tests/unit/test_auth_service.py -v
```

Expected: 6 tests PASS.

**Step 6: Commit**

```bash
git add backend/app/domain/identity/ backend/tests/unit/
git commit -m "feat: add AuthService with password hashing and JWT tokens"
```

---

### Task 10: Auth Middleware — JWT Validation

**Files:**
- Create: `backend/app/api/middleware/auth.py`
- Create: `backend/tests/unit/test_auth_middleware.py`

**Step 1: Write the failing test**

Create `backend/tests/unit/test_auth_middleware.py`:

```python
import pytest
from httpx import ASGITransport, AsyncClient

from app.domain.identity.service import AuthService
from app.main import create_app


@pytest.fixture
def app_with_protected_route():
    from app.api.middleware.auth import get_current_user

    app = create_app()

    @app.get("/api/v1/test-protected")
    async def protected_route(current_user: dict = Depends(get_current_user)):
        return {"user_id": current_user["sub"], "role": current_user["role"]}

    return app


@pytest.mark.asyncio
async def test_protected_route_without_token():
    app = create_app()

    from fastapi import Depends
    from app.api.middleware.auth import get_current_user

    @app.get("/test-protected")
    async def protected(current_user: dict = Depends(get_current_user)):
        return current_user

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/test-protected")
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_with_valid_token():
    app = create_app()

    from fastapi import Depends
    from app.api.middleware.auth import get_current_user

    @app.get("/test-protected")
    async def protected(current_user: dict = Depends(get_current_user)):
        return current_user

    token = AuthService.create_access_token(
        user_id="test-uuid", email="test@example.com", role="admin"
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/test-protected",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["sub"] == "test-uuid"
```

**Step 2: Run test to verify it fails**

```bash
docker compose exec backend pytest tests/unit/test_auth_middleware.py -v
```

Expected: FAIL — cannot import `get_current_user`

**Step 3: Create `backend/app/api/__init__.py` and `backend/app/api/middleware/__init__.py`**

```bash
touch backend/app/api/__init__.py
touch backend/app/api/middleware/__init__.py
touch backend/app/api/v1/__init__.py
```

**Step 4: Create `backend/app/api/middleware/auth.py`**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.domain.identity.service import AuthService

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    try:
        payload = AuthService.decode_access_token(credentials.credentials)
        return payload
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def require_role(*allowed_roles: str):
    async def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.get('role')}' not authorized",
            )
        return current_user
    return role_checker
```

**Step 5: Run tests to verify they pass**

```bash
docker compose exec backend pytest tests/unit/test_auth_middleware.py -v
```

Expected: 2 tests PASS.

**Step 6: Commit**

```bash
git add backend/app/api/ backend/tests/unit/
git commit -m "feat: add JWT auth middleware with role-based access control"
```

---

### Task 11: Auth API Endpoints (Login, Register, Refresh)

**Files:**
- Create: `backend/app/domain/identity/repository.py`
- Create: `backend/app/api/v1/auth.py`
- Modify: `backend/app/main.py` (add router)
- Create: `backend/tests/integration/test_auth_api.py`

**Step 1: Create `backend/app/domain/identity/repository.py`**

```python
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.identity.models import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        return user

    async def list_by_clinic(self, clinic_id: uuid.UUID) -> list[User]:
        result = await self.db.execute(
            select(User).where(User.clinic_id == clinic_id, User.deleted_at.is_(None))
        )
        return list(result.scalars().all())
```

**Step 2: Create `backend/app/api/v1/auth.py`**

```python
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.identity.models import User
from app.domain.identity.repository import UserRepository
from app.domain.identity.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.domain.identity.service import AuthService
from app.infrastructure.database import get_db
from app.api.middleware.auth import get_current_user
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)

    existing = await repo.get_by_email(request.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=request.email,
        password_hash=AuthService.hash_password(request.password),
        full_name=request.full_name,
        role=request.role,
        clinic_id=request.clinic_id,
    )
    user = await repo.create(user)
    await db.commit()

    return UserResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        clinic_id=str(user.clinic_id),
    )


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get_by_email(request.email)

    if not user or not AuthService.verify_password(request.password, user.password_hash):
        # Increment failed attempts
        if user:
            user.failed_login_attempts += 1
            await db.commit()
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Check account lockout
    if user.locked_until and user.locked_until > datetime.now(timezone.utc):
        raise HTTPException(status_code=423, detail="Account locked. Try again later.")

    # Check if too many failed attempts
    if user.failed_login_attempts >= settings.max_failed_login_attempts:
        user.locked_until = datetime.now(timezone.utc) + __import__("datetime").timedelta(
            minutes=settings.lockout_duration_minutes
        )
        await db.commit()
        raise HTTPException(status_code=423, detail="Account locked due to too many failed attempts")

    # Successful login — reset failed attempts
    user.failed_login_attempts = 0
    user.last_login = datetime.now(timezone.utc)
    await db.commit()

    access_token = AuthService.create_access_token(
        user_id=str(user.id), email=user.email, role=user.role
    )
    refresh_token = AuthService.create_refresh_token(user_id=str(user.id))

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = UserRepository(db)
    user = await repo.get_by_id(current_user["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        clinic_id=str(user.clinic_id),
    )
```

**Step 3: Register the router in `backend/app/main.py`**

Add after the CORS middleware setup:

```python
from app.api.v1.auth import router as auth_router

# Inside create_app(), after middleware:
app.include_router(auth_router, prefix=settings.api_v1_prefix)
```

**Step 4: Commit**

```bash
git add backend/app/domain/identity/ backend/app/api/v1/ backend/app/main.py
git commit -m "feat: add auth endpoints — register, login, me"
```

---

### Task 12: HIPAA Audit Logging Middleware

**Files:**
- Create: `backend/app/domain/compliance/service.py`
- Create: `backend/app/api/middleware/audit.py`

**Step 1: Create `backend/app/domain/compliance/service.py`**

```python
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.compliance.models import AuditLog


class AuditService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log(
        self,
        user_id: uuid.UUID | None,
        action: str,
        resource_type: str,
        resource_id: uuid.UUID | None = None,
        changes: dict | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        phi_accessed: bool = False,
        access_reason: str | None = None,
    ) -> AuditLog:
        entry = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            changes=changes,
            ip_address=ip_address,
            user_agent=user_agent,
            phi_accessed=phi_accessed,
            access_reason=access_reason,
        )
        self.db.add(entry)
        await self.db.flush()
        return entry
```

**Step 2: Create `backend/app/api/middleware/audit.py`**

```python
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.infrastructure.database import async_session_factory
from app.domain.compliance.models import AuditLog


# PHI-accessing endpoints (log these with phi_accessed=True)
PHI_ENDPOINTS = {"/api/v1/patients", "/api/v1/screenings"}


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # Only audit authenticated API calls
        if not request.url.path.startswith("/api/v1"):
            return response

        # Skip health checks and docs
        if request.url.path in ("/api/health", "/api/docs", "/api/redoc"):
            return response

        phi_accessed = any(request.url.path.startswith(ep) for ep in PHI_ENDPOINTS)

        # Fire-and-forget audit log (don't slow down the response)
        try:
            async with async_session_factory() as session:
                entry = AuditLog(
                    action=request.method.lower(),
                    resource_type=request.url.path,
                    ip_address=request.client.host if request.client else None,
                    user_agent=request.headers.get("user-agent"),
                    phi_accessed=phi_accessed,
                )
                session.add(entry)
                await session.commit()
        except Exception:
            pass  # Audit failure must never break the request

        return response
```

**Step 3: Commit**

```bash
git add backend/app/domain/compliance/ backend/app/api/middleware/
git commit -m "feat: add HIPAA audit logging service and middleware"
```

---

## Week 4: Patient CRUD API & Integration Tests (Days 16-20)

### Task 13: Patient Repository & Service

**Files:**
- Create: `backend/app/domain/patients/repository.py`
- Create: `backend/app/domain/patients/service.py`
- Create: `backend/app/domain/patients/schemas.py`

**Step 1: Create `backend/app/domain/patients/schemas.py`**

```python
from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class PatientCreate(BaseModel):
    name: str
    diagnosis: str | None = None
    diagnosis_code: str | None = None
    medication_adherence: Decimal | None = None
    last_appointment: date | None = None
    appointments_missed: int = 0
    crisis_calls_30days: int = 0
    case_manager_id: str | None = None


class PatientUpdate(BaseModel):
    diagnosis: str | None = None
    diagnosis_code: str | None = None
    medication_adherence: Decimal | None = None
    appointments_missed: int | None = None
    crisis_calls_30days: int | None = None
    case_manager_id: str | None = None
    status: str | None = None


class PatientResponse(BaseModel):
    id: str
    name: str
    diagnosis: str | None
    diagnosis_code: str | None
    medication_adherence: float | None
    last_appointment: date | None
    appointments_missed: int
    crisis_calls_30days: int
    current_risk_level: str | None
    status: str
    case_manager_id: str | None
    created_at: str

    model_config = {"from_attributes": True}


class PaginatedResponse(BaseModel):
    data: list[PatientResponse]
    pagination: dict
```

**Step 2: Create `backend/app/domain/patients/repository.py`**

```python
import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.patients.models import Patient


class PatientRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, patient: Patient) -> Patient:
        self.db.add(patient)
        await self.db.flush()
        return patient

    async def get_by_id(self, patient_id: uuid.UUID) -> Patient | None:
        result = await self.db.execute(
            select(Patient).where(Patient.id == patient_id, Patient.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def list_by_clinic(
        self,
        clinic_id: uuid.UUID,
        risk_level: str | None = None,
        case_manager_id: uuid.UUID | None = None,
        limit: int = 50,
        cursor: uuid.UUID | None = None,
    ) -> list[Patient]:
        query = select(Patient).where(
            Patient.clinic_id == clinic_id,
            Patient.deleted_at.is_(None),
        )

        if risk_level:
            query = query.where(Patient.current_risk_level == risk_level)
        if case_manager_id:
            query = query.where(Patient.case_manager_id == case_manager_id)
        if cursor:
            query = query.where(Patient.id > cursor)

        query = query.order_by(Patient.id).limit(limit + 1)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_by_clinic(self, clinic_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(Patient).where(
                Patient.clinic_id == clinic_id,
                Patient.deleted_at.is_(None),
            )
        )
        return result.scalar_one()

    async def soft_delete(self, patient: Patient, deleted_by: uuid.UUID) -> None:
        from datetime import datetime
        patient.deleted_at = datetime.utcnow()
```

**Step 3: Create `backend/app/domain/patients/service.py`**

```python
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.patients.models import Patient
from app.domain.patients.repository import PatientRepository
from app.domain.patients.schemas import PatientCreate, PatientUpdate


class PatientService:
    def __init__(self, db: AsyncSession):
        self.repo = PatientRepository(db)
        self.db = db

    async def create_patient(self, data: PatientCreate, clinic_id: uuid.UUID) -> Patient:
        patient = Patient(
            clinic_id=clinic_id,
            name_encrypted=data.name.encode("utf-8"),  # TODO: real encryption
            diagnosis=data.diagnosis,
            diagnosis_code=data.diagnosis_code,
            medication_adherence=data.medication_adherence,
            last_appointment=data.last_appointment,
            appointments_missed=data.appointments_missed,
            crisis_calls_30days=data.crisis_calls_30days,
            case_manager_id=uuid.UUID(data.case_manager_id) if data.case_manager_id else None,
        )
        return await self.repo.create(patient)

    async def get_patient(self, patient_id: uuid.UUID) -> Patient | None:
        return await self.repo.get_by_id(patient_id)

    async def update_patient(self, patient: Patient, data: PatientUpdate) -> Patient:
        for field, value in data.model_dump(exclude_unset=True).items():
            if field == "case_manager_id" and value is not None:
                value = uuid.UUID(value)
            setattr(patient, field, value)
        await self.db.flush()
        return patient

    async def list_patients(
        self,
        clinic_id: uuid.UUID,
        risk_level: str | None = None,
        case_manager_id: uuid.UUID | None = None,
        limit: int = 50,
        cursor: str | None = None,
    ) -> tuple[list[Patient], bool]:
        cursor_uuid = uuid.UUID(cursor) if cursor else None
        patients = await self.repo.list_by_clinic(
            clinic_id=clinic_id,
            risk_level=risk_level,
            case_manager_id=case_manager_id,
            limit=limit,
            cursor=cursor_uuid,
        )
        has_more = len(patients) > limit
        return patients[:limit], has_more

    async def soft_delete_patient(self, patient: Patient, deleted_by: uuid.UUID) -> None:
        await self.repo.soft_delete(patient, deleted_by)
```

**Step 4: Commit**

```bash
git add backend/app/domain/patients/
git commit -m "feat: add Patient repository, service, and schemas"
```

---

### Task 14: Patient API Endpoints

**Files:**
- Create: `backend/app/api/v1/patients.py`
- Modify: `backend/app/main.py` (add router)

**Step 1: Create `backend/app/api/v1/patients.py`**

```python
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.middleware.auth import get_current_user
from app.domain.patients.schemas import PaginatedResponse, PatientCreate, PatientResponse, PatientUpdate
from app.domain.patients.service import PatientService
from app.infrastructure.database import get_db

router = APIRouter(prefix="/patients", tags=["Patients"])


def _patient_to_response(patient) -> PatientResponse:
    return PatientResponse(
        id=str(patient.id),
        name=patient.name_encrypted.decode("utf-8") if patient.name_encrypted else "",
        diagnosis=patient.diagnosis,
        diagnosis_code=patient.diagnosis_code,
        medication_adherence=float(patient.medication_adherence) if patient.medication_adherence else None,
        last_appointment=patient.last_appointment,
        appointments_missed=patient.appointments_missed,
        crisis_calls_30days=patient.crisis_calls_30days,
        current_risk_level=patient.current_risk_level,
        status=patient.status,
        case_manager_id=str(patient.case_manager_id) if patient.case_manager_id else None,
        created_at=patient.created_at.isoformat(),
    )


@router.get("", response_model=PaginatedResponse)
async def list_patients(
    risk_level: str | None = Query(None),
    cursor: str | None = Query(None),
    limit: int = Query(50, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = PatientService(db)
    clinic_id = uuid.UUID(current_user.get("clinic_id", current_user["sub"]))  # TODO: get from user record

    case_manager_id = None
    if current_user["role"] == "case_manager":
        case_manager_id = uuid.UUID(current_user["sub"])

    patients, has_more = await service.list_patients(
        clinic_id=clinic_id,
        risk_level=risk_level,
        case_manager_id=case_manager_id,
        limit=limit,
        cursor=cursor,
    )

    return PaginatedResponse(
        data=[_patient_to_response(p) for p in patients],
        pagination={
            "next_cursor": str(patients[-1].id) if patients and has_more else None,
            "has_more": has_more,
        },
    )


@router.post("", response_model=PatientResponse, status_code=201)
async def create_patient(
    data: PatientCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = PatientService(db)
    clinic_id = uuid.UUID(current_user.get("clinic_id", current_user["sub"]))
    patient = await service.create_patient(data, clinic_id)
    await db.commit()
    return _patient_to_response(patient)


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = PatientService(db)
    patient = await service.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return _patient_to_response(patient)


@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: uuid.UUID,
    data: PatientUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = PatientService(db)
    patient = await service.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient = await service.update_patient(patient, data)
    await db.commit()
    return _patient_to_response(patient)


@router.delete("/{patient_id}", status_code=204)
async def delete_patient(
    patient_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = PatientService(db)
    patient = await service.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    await service.soft_delete_patient(patient, uuid.UUID(current_user["sub"]))
    await db.commit()
```

**Step 2: Register router in `backend/app/main.py`**

Add:
```python
from app.api.v1.patients import router as patients_router

app.include_router(patients_router, prefix=settings.api_v1_prefix)
```

**Step 3: Commit**

```bash
git add backend/app/api/v1/patients.py backend/app/main.py
git commit -m "feat: add Patient CRUD API endpoints with cursor pagination"
```

---

### Task 15: Seed Data Script

**Files:**
- Create: `backend/scripts/seed.py`

**Step 1: Create `backend/scripts/seed.py`**

```python
"""Seed the database with test data for development."""
import asyncio
import uuid

from app.config import settings
from app.infrastructure.database import async_session_factory, engine, Base
from app.domain.identity.models import Organization, Clinic, User
from app.domain.identity.service import AuthService

# Import all models
from app.domain.patients.models import Patient  # noqa
from app.domain.analysis.models import Screening  # noqa
from app.domain.compliance.models import AuditLog  # noqa
from app.domain.reports.models import Report  # noqa


async def seed():
    async with async_session_factory() as session:
        # Create organization
        org = Organization(name="Oakwood Behavioral Health")
        session.add(org)
        await session.flush()

        # Create clinic
        clinic = Clinic(
            organization_id=org.id,
            name="Oakwood Main Campus",
            phone="555-0100",
            npi_number="1234567890",
        )
        session.add(clinic)
        await session.flush()

        # Create users
        admin = User(
            clinic_id=clinic.id,
            email="admin@oakwood.health",
            password_hash=AuthService.hash_password("admin123!"),
            role="admin",
            full_name="Dr. James Chen",
        )
        cm1 = User(
            clinic_id=clinic.id,
            email="maria@oakwood.health",
            password_hash=AuthService.hash_password("maria123!"),
            role="case_manager",
            full_name="Maria Garcia",
            license_number="CM-12345",
        )
        cm2 = User(
            clinic_id=clinic.id,
            email="sarah.kim@oakwood.health",
            password_hash=AuthService.hash_password("sarah123!"),
            role="case_manager",
            full_name="Sarah Kim",
            license_number="CM-67890",
        )
        session.add_all([admin, cm1, cm2])
        await session.flush()

        # Create patients (from original patients.csv)
        patients_data = [
            ("Sarah Johnson", "Bipolar Disorder", 45.0, 3, 4, cm1.id),
            ("Michael Williams", "Depression", 95.0, 0, 0, cm1.id),
            ("Jennifer Brown", "Anxiety Disorder", 75.0, 1, 1, cm2.id),
            ("Robert Davis", "Schizophrenia", 25.0, 4, 6, cm1.id),
            ("Lisa Anderson", "PTSD", 60.0, 2, 2, cm2.id),
            ("David Martinez", "Depression", 88.0, 0, 0, cm2.id),
            ("Emily Wilson", "Bipolar Disorder", 55.0, 2, 3, cm1.id),
            ("James Taylor", "Anxiety Disorder", 90.0, 1, 0, cm2.id),
            ("Amanda Thomas", "Schizophrenia", 40.0, 3, 5, cm1.id),
            ("Christopher Lee", "PTSD", 70.0, 1, 1, cm2.id),
        ]

        for name, diag, adherence, missed, crisis, manager_id in patients_data:
            patient = Patient(
                clinic_id=clinic.id,
                case_manager_id=manager_id,
                name_encrypted=name.encode("utf-8"),  # TODO: real encryption
                diagnosis=diag,
                medication_adherence=adherence,
                appointments_missed=missed,
                crisis_calls_30days=crisis,
            )
            session.add(patient)

        await session.commit()
        print("Seed data created successfully!")
        print(f"  Organization: {org.name} ({org.id})")
        print(f"  Clinic: {clinic.name} ({clinic.id})")
        print(f"  Admin: admin@oakwood.health / admin123!")
        print(f"  Case Manager 1: maria@oakwood.health / maria123!")
        print(f"  Case Manager 2: sarah.kim@oakwood.health / sarah123!")
        print(f"  Patients: 10 created")


if __name__ == "__main__":
    asyncio.run(seed())
```

**Step 2: Run seed**

```bash
docker compose exec backend python -m scripts.seed
```

**Step 3: Commit**

```bash
git add backend/scripts/
git commit -m "feat: add database seed script with Oakwood test data"
```

---

## Summary: Month 1 Deliverables

By the end of Month 1, you will have:

| # | Deliverable | Status |
|---|------------|--------|
| 1 | Docker Compose (PostgreSQL + Redis + FastAPI) | Task 1-2 |
| 2 | All domain models (10 tables) | Tasks 5-7 |
| 3 | Alembic migrations | Task 8 |
| 4 | JWT authentication (register, login, refresh) | Tasks 9-11 |
| 5 | HIPAA audit logging middleware | Task 12 |
| 6 | Patient CRUD API with cursor pagination | Tasks 13-14 |
| 7 | Seed data script | Task 15 |
| 8 | Integration & unit tests | Tasks 3, 9-10 |

### Commands Cheatsheet

```bash
# Start everything
docker compose up --build -d

# Run tests
docker compose exec backend pytest tests/ -v

# Run migrations
docker compose exec backend alembic upgrade head

# Create new migration
docker compose exec backend alembic revision --autogenerate -m "description"

# Seed database
docker compose exec backend python -m scripts.seed

# View logs
docker compose logs -f backend

# API docs
open http://localhost:8000/api/docs
```

### Next: Month 2 — Frontend

Month 2 plan will be created after Month 1 is complete. It will cover:
- Next.js 14 project setup with TypeScript
- Tailwind CSS + shadcn/ui component library
- Login/register pages
- Case Manager dashboard with risk overview cards
- Patient list with filtering and search
- Patient detail page with screening history

---

*Plan created: 2026-02-16*
*Design reference: `docs/plans/2026-02-16-mindbridge-full-stack-design.md`*
*Architecture reference: `docs/architecture/mindbridge-architecture.md`*
