# MindBridge Health AI — Full-Stack Design Document

**Date:** 2026-02-16
**Author:** Fidelis Emmanuel
**Status:** Approved
**Version:** 1.0

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Architecture & Design Philosophy](#2-system-architecture--design-philosophy)
3. [Backend & API Design](#3-backend--api-design)
4. [Database Design & Healthcare Data Patterns](#4-database-design--healthcare-data-patterns)
5. [Frontend & Dashboard Design](#5-frontend--dashboard-design)
6. [AI Engine Design](#6-ai-engine-design)
7. [HIPAA Compliance Architecture](#7-hipaa-compliance-architecture)
8. [Testing Strategy](#8-testing-strategy)
9. [Deployment & DevOps](#9-deployment--devops)
10. [Interview Knowledge Base](#10-interview-knowledge-base)

---

## 1. Executive Summary

### Vision

Transform MindBridge from a collection of Python scripts into a full-stack, HIPAA-compliant, multi-tenant SaaS platform for behavioral health risk assessment — serving case managers, clinic administrators, patients, insurance payers, and regulatory bodies.

### Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, shadcn/ui, Recharts |
| Backend | Python 3.12, FastAPI, SQLAlchemy ORM, Celery, Pydantic |
| AI Engine | Claude API (Anthropic), structured prompts, clinical guardrails |
| Database | PostgreSQL 16, Redis (cache/sessions), Alembic (migrations) |
| Infrastructure | Docker Compose, GitHub Actions, Vercel, Railway, AWS (growth) |
| Security | HIPAA-compliant, AES-256 encryption, TLS 1.3, RBAC, MFA, audit logging |

### Target Users

- **Case Managers** — Daily risk dashboards, patient screening, actionable alerts
- **Clinic Administrators** — Operational oversight, staffing insights, compliance reporting
- **Patients** — Self-service portal, appointments, wellness check-ins, medication reminders
- **Insurance/Payers** — Outcome reporting, utilization data
- **Regulatory Bodies** — HIPAA audit trails, compliance documentation

### Timeline

6+ months, enterprise-grade, incremental delivery

### Budget

$50-200/month for infrastructure

---

## 2. System Architecture & Design Philosophy

### Architecture Pattern: Modular Monolith to Microservices

```
Phase 1 (Months 1-3): Modular Monolith
  - Single deployable unit, internally separated by domain modules
  - Faster to build, easier to debug, cheaper to run

Phase 2 (Months 4-6): Service Extraction
  - Extract AI Engine (most expensive compute, independent scaling)
  - Extract Notification Service (different scaling needs)
  - Keep Patient/User/Report in the monolith

Phase 3 (Post-6 months): Full Microservices
  - Each domain becomes its own service when scale demands it
```

### Domain-Driven Design (DDD) — Bounded Contexts

| Domain | Responsibility | Key Entities |
|--------|---------------|--------------|
| **Patient Management** | CRUD, demographics, history | Patient, Appointment, CrisisEvent |
| **Clinical Analysis** | AI risk assessment, scoring | Screening, RiskAssessment |
| **Document Generation** | Multi-format reports | Report, Template |
| **Identity & Access** | Auth, roles, permissions | User, Organization, Clinic |
| **Compliance** | HIPAA audit, data retention | AuditLog, ConsentRecord |

Each domain exposes a service interface. Other domains communicate through that interface, never by directly accessing another domain's database tables or internal models. This preserves encapsulation and allows future service extraction.

### CQRS (Command Query Responsibility Segregation)

- **Commands** (writes): `create_patient()`, `run_screening()`, `generate_report()`
- **Queries** (reads): `get_dashboard_stats()`, `list_high_risk_patients()`, `get_audit_trail()`

Healthcare apps are read-heavy. A case manager checks the dashboard constantly but runs a screening once a day. CQRS lets you optimize each path independently.

### Event-Driven Architecture

When a screening completes, multiple things need to happen:

```
ScreeningCompleted event triggers:
  ├── UpdateDashboardHandler
  ├── GenerateReportHandler
  ├── SendAlertHandler (if high risk)
  └── WriteAuditLogHandler
```

Downstream handlers subscribe independently — adding new reactions (like a new notification channel) requires zero changes to the screening code. Failed handlers don't block others.

---

## 3. Backend & API Design

### REST API Endpoints

```
Base URL: /api/v1

Patient Management:
  GET    /api/v1/patients                  → List patients (paginated, filtered)
  POST   /api/v1/patients                  → Create new patient
  GET    /api/v1/patients/{id}             → Get patient details
  PUT    /api/v1/patients/{id}             → Update patient
  DELETE /api/v1/patients/{id}             → Soft delete (HIPAA: never hard delete)
  GET    /api/v1/patients/{id}/history     → Patient screening history
  POST   /api/v1/patients/import           → Bulk CSV import

Clinical Analysis:
  POST   /api/v1/screenings                → Run screening for one patient
  POST   /api/v1/screenings/batch          → Run batch screening
  GET    /api/v1/screenings/{id}           → Get screening result
  GET    /api/v1/screenings/dashboard      → Dashboard aggregates

Reports:
  POST   /api/v1/reports/generate          → Generate report (word/excel/pdf)
  GET    /api/v1/reports                   → List generated reports
  GET    /api/v1/reports/{id}/download     → Download report file

Users & Auth:
  POST   /api/v1/auth/login               → Login
  POST   /api/v1/auth/logout              → Logout
  POST   /api/v1/auth/refresh             → Refresh JWT token
  GET    /api/v1/users/me                  → Current user profile
  GET    /api/v1/users                     → List users (admin only)

Compliance:
  GET    /api/v1/audit-logs                → Query audit trail
  GET    /api/v1/audit-logs/export         → Export audit log
```

### Why REST over GraphQL

For healthcare: REST endpoints map to specific resources/actions, making HIPAA audit logging straightforward. Each endpoint = one logged action. GraphQL queries can traverse multiple entities in one request, making granular audit logging significantly harder. Also, the HL7 FHIR healthcare integration ecosystem is REST-based.

### Pagination: Cursor-Based

Offset pagination breaks when records change between pages. Cursor-based pagination uses the last record's ID as the cursor, so results are stable.

```json
{
    "data": [...],
    "pagination": {
        "next_cursor": "patient_abc123",
        "has_more": true,
        "total_count": 847
    }
}
```

### Error Format: RFC 7807 Problem Details

```json
{
    "type": "https://api.mindbridge.health/errors/screening-failed",
    "title": "AI Analysis Unavailable",
    "status": 503,
    "detail": "Claude API timed out after 30s. Screening queued for retry.",
    "instance": "/api/v1/screenings/scr_789",
    "correlation_id": "req_abc123def456",
    "retry_after": 60
}
```

### Async Task Queue Pattern

Long-running operations (batch screenings, report generation) use an async pattern:

```
POST /api/v1/screenings/batch → 202 Accepted
{
    "task_id": "task_abc123",
    "status": "queued",
    "progress_url": "/api/v1/tasks/task_abc123",
    "websocket_url": "ws://api/v1/tasks/task_abc123/progress"
}
```

Case managers see a progress bar: "Analyzing patient 23 of 50..." instead of a loading spinner.

### Backend Project Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI app factory
│   ├── config.py                  # Settings (env vars, secrets)
│   ├── dependencies.py            # Dependency injection
│   │
│   ├── domain/                    # Business logic (framework-agnostic)
│   │   ├── patients/
│   │   │   ├── models.py          # Patient domain model
│   │   │   ├── service.py         # PatientService
│   │   │   └── repository.py      # PatientRepository (DB access)
│   │   ├── analysis/
│   │   │   ├── models.py          # Screening, RiskAssessment
│   │   │   ├── service.py         # AnalysisService (Claude integration)
│   │   │   ├── prompts.py         # Prompt templates (versioned)
│   │   │   └── repository.py
│   │   ├── reports/
│   │   │   ├── models.py
│   │   │   ├── service.py         # ReportService
│   │   │   ├── generators/        # Word, Excel, PDF generators
│   │   │   └── repository.py
│   │   ├── identity/
│   │   │   ├── models.py          # User, Organization
│   │   │   ├── service.py         # AuthService
│   │   │   └── repository.py
│   │   └── compliance/
│   │       ├── models.py          # AuditLog
│   │       ├── service.py         # AuditService
│   │       └── repository.py
│   │
│   ├── api/                       # HTTP layer (thin, delegates to domain)
│   │   ├── v1/
│   │   │   ├── patients.py
│   │   │   ├── screenings.py
│   │   │   ├── reports.py
│   │   │   ├── auth.py
│   │   │   └── audit.py
│   │   └── middleware/
│   │       ├── auth.py            # JWT validation
│   │       ├── audit.py           # HIPAA audit logging
│   │       ├── rate_limit.py
│   │       └── cors.py
│   │
│   ├── infrastructure/            # External service adapters
│   │   ├── database.py            # SQLAlchemy engine & sessions
│   │   ├── claude_client.py       # Anthropic API wrapper
│   │   ├── email_client.py
│   │   ├── storage.py             # File storage (local → S3)
│   │   └── cache.py               # Redis client
│   │
│   └── tasks/                     # Background jobs (Celery)
│       ├── screening.py
│       ├── reports.py
│       └── notifications.py
│
├── migrations/                    # Alembic database migrations
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── Dockerfile
└── requirements.txt
```

### Layered Architecture

- **API Layer** — Thin. Handles HTTP concerns (parsing, formatting, status codes), delegates to domain.
- **Domain Layer** — All business logic. Framework-agnostic (doesn't know about FastAPI, HTTP, or databases).
- **Infrastructure Layer** — Adapters for external services (database, Claude API, email).

This separation means you can test business logic without spinning up a server, swap databases without changing business rules, and new developers understand an endpoint in 30 seconds.

---

## 4. Database Design & Healthcare Data Patterns

### Why PostgreSQL

1. **ACID transactions** — When recording a screening + updating risk level + writing audit log, ALL succeed or NONE do. Partial writes in healthcare mean a patient could show "low risk" while their screening says "high risk."
2. **JSONB columns** — Structured relational data for patients/screenings, flexible JSON for semi-structured AI responses. No separate document store needed.
3. **Row-Level Security (RLS)** — Case managers only see their own patients at the DATABASE level, not just the application level. Defense-in-depth.

### Schema Design Principles

**1. Soft Deletes Only (HIPAA: Never Hard Delete PHI)**

```sql
ALTER TABLE patients ADD COLUMN deleted_at TIMESTAMP NULL;
ALTER TABLE patients ADD COLUMN deleted_by UUID REFERENCES users(id);

CREATE VIEW active_patients AS
  SELECT * FROM patients WHERE deleted_at IS NULL;
```

HIPAA requires minimum 6-year data retention. Some states require 10+ years. Hard delete = compliance violation.

**2. Temporal Data (Track Trends Over Time)**

```sql
CREATE TABLE patient_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id) NOT NULL,
    metric_type VARCHAR(50) NOT NULL,
    metric_value DECIMAL(10,2) NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT NOW(),
    recorded_by UUID REFERENCES users(id)
);
```

A single adherence number is a snapshot. A trend is a clinical insight. Temporal data transforms a screening tool into a clinical decision support system.

### Full Database Schema

```sql
-- ============================================
-- IDENTITY & MULTI-TENANCY
-- ============================================

CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    subscription_tier VARCHAR(50) DEFAULT 'standard',
    hipaa_baa_signed BOOLEAN DEFAULT FALSE,
    hipaa_baa_date DATE,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE clinics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id) NOT NULL,
    name VARCHAR(255) NOT NULL,
    address_encrypted BYTEA,
    phone VARCHAR(20),
    npi_number VARCHAR(10),
    timezone VARCHAR(50) DEFAULT 'America/New_York',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clinic_id UUID REFERENCES clinics(id) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    license_number VARCHAR(50),
    mfa_enabled BOOLEAN DEFAULT FALSE,
    mfa_secret_encrypted BYTEA,
    failed_login_attempts INT DEFAULT 0,
    locked_until TIMESTAMP,
    last_login TIMESTAMP,
    password_changed_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

-- ============================================
-- PATIENT MANAGEMENT
-- ============================================

CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clinic_id UUID REFERENCES clinics(id) NOT NULL,
    case_manager_id UUID REFERENCES users(id),
    mrn VARCHAR(50),
    name_encrypted BYTEA NOT NULL,
    date_of_birth_encrypted BYTEA,
    diagnosis VARCHAR(255),
    diagnosis_code VARCHAR(10),
    medication_adherence DECIMAL(5,2),
    last_appointment DATE,
    appointments_missed INT DEFAULT 0,
    crisis_calls_30days INT DEFAULT 0,
    current_risk_level VARCHAR(20),
    admitted_at DATE,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

CREATE INDEX idx_patients_risk ON patients(clinic_id, current_risk_level)
    WHERE deleted_at IS NULL;
CREATE INDEX idx_patients_manager ON patients(case_manager_id)
    WHERE deleted_at IS NULL;

-- ============================================
-- CLINICAL ANALYSIS
-- ============================================

CREATE TABLE screenings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id) NOT NULL,
    performed_by UUID REFERENCES users(id) NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    risk_score DECIMAL(5,2),
    ai_model VARCHAR(100),
    ai_prompt_hash VARCHAR(64),
    ai_raw_response JSONB,
    primary_risk_factor TEXT,
    recommended_actions TEXT[],
    clinical_notes TEXT,
    screening_type VARCHAR(50) DEFAULT 'standard',
    duration_ms INT,
    screened_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_screenings_patient ON screenings(patient_id, screened_at DESC);
CREATE INDEX idx_screenings_risk ON screenings(risk_level, screened_at DESC);

-- ============================================
-- REPORTS & DOCUMENTS
-- ============================================

CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    screening_id UUID REFERENCES screenings(id),
    generated_by UUID REFERENCES users(id) NOT NULL,
    format VARCHAR(10) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size_bytes BIGINT,
    checksum VARCHAR(64),
    patient_count INT,
    high_risk_count INT,
    medium_risk_count INT,
    low_risk_count INT,
    generated_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

-- ============================================
-- APPOINTMENTS & CRISIS TRACKING
-- ============================================

CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id) NOT NULL,
    scheduled_by UUID REFERENCES users(id),
    scheduled_at TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled',
    appointment_type VARCHAR(50),
    notes_encrypted BYTEA,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE crisis_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id) NOT NULL,
    reported_by UUID REFERENCES users(id),
    severity VARCHAR(20) NOT NULL,
    event_type VARCHAR(50),
    description_encrypted BYTEA,
    resolution TEXT,
    follow_up_required BOOLEAN DEFAULT TRUE,
    occurred_at TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- HIPAA COMPLIANCE
-- ============================================

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID,
    changes JSONB,
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(255),
    phi_accessed BOOLEAN DEFAULT FALSE,
    access_reason TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Audit logs are APPEND-ONLY. No UPDATE or DELETE.
CREATE INDEX idx_audit_user ON audit_logs(user_id, created_at DESC);
CREATE INDEX idx_audit_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_phi ON audit_logs(phi_accessed, created_at DESC)
    WHERE phi_accessed = TRUE;

-- ============================================
-- CONSENT MANAGEMENT
-- ============================================

CREATE TABLE patient_consents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id) NOT NULL,
    consent_type VARCHAR(50) NOT NULL,
    granted BOOLEAN NOT NULL,
    granted_at TIMESTAMP,
    revoked_at TIMESTAMP,
    consent_form_version VARCHAR(20),
    witness_user_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- PATIENT METRICS (TEMPORAL)
-- ============================================

CREATE TABLE patient_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id) NOT NULL,
    metric_type VARCHAR(50) NOT NULL,
    metric_value DECIMAL(10,2) NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT NOW(),
    recorded_by UUID REFERENCES users(id)
);

CREATE INDEX idx_metrics_patient ON patient_metrics(patient_id, metric_type, recorded_at DESC);
```

### Row-Level Security

```sql
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;

CREATE POLICY case_manager_patients ON patients
    FOR SELECT
    USING (
        case_manager_id = current_setting('app.current_user_id')::UUID
        OR current_setting('app.current_role') IN ('admin', 'compliance_officer')
    );
```

### Scaling Strategy

1. **Indexing & query optimization** — handles first 100K patients
2. **Read replicas** — dashboard is read-heavy, add replica for reads
3. **Table partitioning** — audit_logs partitioned by month, patients by clinic_id
4. **Sharding** — only past 10M patients (avoid distributed transaction complexity)

---

## 5. Frontend & Dashboard Design

### Technology Stack

- **Next.js 14 (App Router)** — SSR for instant dashboard loads
- **TypeScript** — Catches data shape errors at compile time
- **Tailwind CSS + shadcn/ui** — Accessible, healthcare-appropriate components (WCAG 2.1 AA)
- **Recharts** — Dashboard data visualization
- **SWR** — Server state management (stale-while-revalidate)

### Role-Based Dashboard Views

**Case Manager Dashboard:**
```
┌──────────────────────────────────────────────────────┐
│  MindBridge Health AI                    👤 Maria G. │
├──────────┬───────────────────────────────────────────┤
│          │                                           │
│ Dashboard│  MY PATIENTS TODAY           [Run Screen] │
│ Patients │  ┌─────┐ ┌─────┐ ┌─────┐                │
│ Screening│  │  5  │ │  3  │ │  2  │                │
│ Reports  │  │HIGH │ │ MED │ │ LOW │                │
│ Alerts   │  └─────┘ └─────┘ └─────┘                │
│          │                                           │
│          │  ⚠ IMMEDIATE ATTENTION                    │
│          │  ┌──────────────────────────────────┐     │
│          │  │ Robert Davis    HIGH  25% adhere │     │
│          │  │ 6 crisis calls · 4 missed appts  │     │
│          │  │ [View] [Screen Now] [Add Note]   │     │
│          │  └──────────────────────────────────┘     │
│          │                                           │
│          │  RISK TREND (30 days)                     │
│          │  [line chart: risk scores over time]      │
│          │                                           │
│          │  UPCOMING APPOINTMENTS                    │
│          │  Today: 3 sessions | This week: 12        │
└──────────┴───────────────────────────────────────────┘
```

**Clinic Administrator Dashboard:**
```
┌──────────────────────────────────────────────────────┐
│  MindBridge Health AI                   👤 Dr. Chen  │
├──────────┬───────────────────────────────────────────┤
│          │                                           │
│ Overview │  CLINIC OVERVIEW              Feb 2026    │
│ Staff    │  ┌────────┐ ┌────────┐ ┌────────┐       │
│ Patients │  │  847   │ │  12%   │ │  94%   │       │
│ Reports  │  │PATIENTS│ │HIGH RSK│ │SCREENED│       │
│ Compliance│  └────────┘ └────────┘ └────────┘       │
│ Billing  │                                           │
│          │  CASELOAD DISTRIBUTION                    │
│          │  [bar chart: patients per case manager]   │
│          │                                           │
│          │  STAFF PERFORMANCE                        │
│          │  Screening completion rate: 94%           │
│          │  Avg response to high-risk: 2.3 hours    │
└──────────┴───────────────────────────────────────────┘
```

**Patient Portal:**
```
┌──────────────────────────────────────────────────────┐
│  MindBridge Health              👤 Sarah Johnson     │
├──────────┬───────────────────────────────────────────┤
│          │                                           │
│ My Health│  NEXT APPOINTMENT                         │
│ Appts    │  Feb 18, 2026 · 10:00 AM                 │
│ Messages │  Dr. Garcia · Therapy Session              │
│ Resources│  [Reschedule] [Cancel]                    │
│          │                                           │
│          │  MY WELLNESS CHECK-IN                     │
│          │  How are you feeling today?               │
│          │                                           │
│          │  MEDICATION REMINDER                      │
│          │  Morning dose taken                       │
│          │  Evening dose (8:00 PM) - pending         │
│          │                                           │
│          │  Crisis Hotline: 988                      │
└──────────┴───────────────────────────────────────────┘
```

### Frontend Project Structure

```
frontend/
├── app/                              # Next.js App Router
│   ├── layout.tsx                    # Root layout
│   ├── page.tsx                      # Landing page
│   ├── (auth)/                       # Auth group (no sidebar)
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   └── forgot-password/page.tsx
│   ├── (dashboard)/                  # Dashboard group (with sidebar)
│   │   ├── layout.tsx                # Dashboard layout
│   │   ├── dashboard/page.tsx
│   │   ├── patients/
│   │   │   ├── page.tsx              # Patient list
│   │   │   └── [id]/page.tsx         # Patient detail
│   │   ├── screening/
│   │   │   ├── page.tsx              # Run new screening
│   │   │   └── [id]/page.tsx         # View result
│   │   ├── reports/
│   │   │   ├── page.tsx              # Report list
│   │   │   └── generate/page.tsx     # Generate new
│   │   ├── alerts/page.tsx
│   │   ├── audit/page.tsx
│   │   └── settings/page.tsx
│   └── (patient-portal)/
│       ├── layout.tsx
│       ├── my-health/page.tsx
│       ├── appointments/page.tsx
│       └── messages/page.tsx
│
├── components/
│   ├── ui/                           # shadcn/ui base
│   ├── dashboard/
│   │   ├── RiskOverviewCards.tsx
│   │   ├── RiskTrendChart.tsx
│   │   ├── CaseloadChart.tsx
│   │   └── RecentAlerts.tsx
│   ├── patients/
│   │   ├── PatientTable.tsx
│   │   ├── PatientCard.tsx
│   │   ├── RiskBadge.tsx
│   │   └── PatientTimeline.tsx
│   ├── screening/
│   │   ├── ScreeningForm.tsx
│   │   ├── ScreeningProgress.tsx
│   │   └── ScreeningResult.tsx
│   ├── reports/
│   │   ├── ReportGenerator.tsx
│   │   └── ReportList.tsx
│   └── layout/
│       ├── Sidebar.tsx
│       ├── Header.tsx
│       └── BreadcrumbNav.tsx
│
├── lib/
│   ├── api.ts                        # API client
│   ├── auth.ts                       # NextAuth config
│   ├── hooks/
│   │   ├── usePatients.ts
│   │   ├── useScreening.ts
│   │   └── useDashboard.ts
│   └── utils/
│       ├── risk-colors.ts
│       ├── formatters.ts
│       └── validators.ts
│
├── types/
│   ├── patient.ts
│   ├── screening.ts
│   ├── user.ts
│   └── api.ts
│
├── tailwind.config.ts
├── next.config.ts
└── package.json
```

### Real-Time Data Strategy

- **SWR** for data that changes infrequently (patient lists, historical screenings) — 30s revalidation
- **Server-Sent Events (SSE)** for time-sensitive data (new high-risk screening alerts) — server pushes to connected case managers
- SSE chosen over WebSockets because it's simpler, works through hospital firewalls/proxies, and communication is one-directional

### State Management

- **Server state (90%)** — SWR handles caching, deduplication, revalidation
- **UI state (10%)** — React's useState/useContext (sidebar collapsed, active filter, modal open)
- No Redux/Zustand needed at this scale

### Accessibility

1. **Component-level** — shadcn/ui built on Radix UI primitives (keyboard nav, screen readers, ARIA)
2. **Color never the only indicator** — risk badges use color + text + icons
3. **CI checks** — axe-core in CI, build fails on WCAG 2.1 AA violations

---

## 6. AI Engine Design

### Structured Prompt System

```python
SCREENING_PROMPT_V2 = """
You are a clinical decision support system for behavioral health.
Analyze the following patient data and provide a structured risk assessment.

PATIENT DATA:
- Name: {name}
- Diagnosis: {diagnosis} (ICD-10: {icd_code})
- Medication Adherence: {med_adherence}%
- Appointments Missed (last 90 days): {missed_appts}
- Last Appointment: {last_appt}
- Crisis Calls (last 30 days): {crisis_calls}
- Days Since Last Contact: {days_since_contact}

RESPOND IN EXACTLY THIS JSON FORMAT:
{
    "risk_level": "high" | "medium" | "low",
    "risk_score": <float 0-100>,
    "primary_risk_factor": "<single most important factor>",
    "contributing_factors": ["<factor1>", "<factor2>"],
    "recommended_actions": [
        {
            "action": "<specific action>",
            "urgency": "immediate" | "this_week" | "routine",
            "assigned_to": "case_manager" | "psychiatrist" | "crisis_team"
        }
    ],
    "clinical_reasoning": "<2-3 sentence explanation>"
}

CLINICAL GUIDELINES:
- Crisis calls >= 3 in 30 days → minimum MEDIUM risk
- Medication adherence < 50% → minimum MEDIUM risk
- Both crisis calls >= 3 AND adherence < 50% → HIGH risk
- Missed appointments >= 3 in 90 days → elevate risk by one level
- Days since last contact > 30 → flag for immediate outreach
"""
```

### Clinical Guardrails

Hard-coded rules that override AI decisions for patient safety:

```python
class ClinicalGuardrails:
    @staticmethod
    def apply(patient_data: dict, ai_result: dict) -> dict:
        # Rule 1: Crisis calls threshold
        if patient_data["crisis_calls_30days"] >= 5:
            ai_result["risk_level"] = "high"
            ai_result["override_reason"] = ">=5 crisis calls (clinical rule)"

        # Rule 2: No contact override
        if days_since_contact > 45 and ai_result["risk_level"] == "low":
            ai_result["risk_level"] = "medium"
            ai_result["override_reason"] = ">45 days no contact (clinical rule)"

        # Rule 3: Cannot AI-downgrade manually escalated patients
        if patient_data.get("manually_escalated"):
            if risk_rank(ai_result["risk_level"]) < risk_rank(patient_data["current_risk_level"]):
                ai_result["risk_level"] = patient_data["current_risk_level"]

        return ai_result
```

### AI Safety Layers

1. **Structured output validation** — Pydantic schema validation on every AI response. Malformed = flagged for manual review.
2. **Clinical rule overrides** — Hard-coded rules override AI. AI can escalate but never downgrade past thresholds.
3. **Confidence scoring** — Risk score 40-60 = "uncertain zone" → flagged for clinician review.
4. **Human-in-the-loop** — Every AI screening is "pending_review" until a clinician confirms.

### Prompt Versioning

- Every screening stores `ai_prompt_hash` and `ai_model` version
- "Golden dataset" of 200 patients with clinician-confirmed risk levels
- Before deploying prompt changes, run against golden dataset and compare F1 scores
- Automated alerts if high-risk classification rate changes suddenly (model drift detection)

### FDA/Regulatory Positioning

The system is a Clinical Decision Support (CDS) tool, NOT a Software as a Medical Device (SaMD). It meets the four 21st Century Cures Act CDS exemption criteria:
1. Not intended to acquire medical data
2. Intended for healthcare professionals
3. Intended for enabling review of patient-specific information
4. The professional makes the final decision

### PHI De-identification for AI

If no BAA with Anthropic, strip HIPAA identifiers before sending:

```python
class PHIDeidentifier:
    def deidentify(self, patient: Patient) -> dict:
        return {
            "patient_ref": f"PT-{hash(patient.id)}",
            "diagnosis": patient.diagnosis,
            "medication_adherence": patient.medication_adherence,
            "appointments_missed": patient.appointments_missed,
            "crisis_calls_30days": patient.crisis_calls_30days,
            "days_since_last_appointment": self._days_since(patient.last_appointment),
            # EXCLUDED: name, DOB, address, MRN, SSN
        }

    def rehydrate(self, ai_result: dict, patient: Patient) -> ScreeningResult:
        return ScreeningResult(patient_id=patient.id, **ai_result)
```

---

## 7. HIPAA Compliance Architecture

### Compliance Mapping

```
HIPAA Requirement          →  MindBridge Implementation
─────────────────────────────────────────────────────────────
Access Control (§164.312a) →  RBAC + Row-Level Security + MFA
Audit Controls (§164.312b) →  audit_logs table, append-only, 6yr retention
Integrity (§164.312c)      →  Report checksums (SHA-256), DB transactions
Transmission (§164.312e)   →  TLS 1.3 everywhere, HSTS headers, no HTTP
Encryption (§164.312a2iv)  →  AES-256-GCM for PHI fields, TDE for volumes
Authentication (§164.312d) →  Argon2 password hashing, JWT + refresh, MFA
Session Management         →  15-min idle timeout, concurrent session limits
Minimum Necessary          →  Role-based data filtering, field-level redaction
Breach Detection           →  Anomaly detection on access patterns
BAA (§164.502e)            →  Required for all cloud vendors
```

### Encryption Strategy

**Two-Tier Encryption:**
1. **Application-level** — AES-256-GCM for most sensitive PHI (names, DOB, notes). Keys in AWS KMS / HashiCorp Vault. App encrypts before writing, decrypts after reading.
2. **Transparent Data Encryption (TDE)** — Entire database volume encrypted on disk. Even non-individually-encrypted fields are protected.

Defense in depth: if TDE is compromised, individual fields are protected. If app encryption has a bug, TDE protects storage.

### Audit Logging

- **Append-only** — No UPDATE or DELETE on audit_logs
- **Every PHI access logged** — who, what, when, from where, why
- **6-year minimum retention** (HIPAA requirement)
- **Partitioned by month** for query performance
- **Anomaly detection** — Unusual access patterns (e.g., 500 records at 2 AM) trigger security alerts

---

## 8. Testing Strategy

### Test Pyramid

```
                    /\
                   /  \          E2E (Playwright)
                  /    \         ~20 tests, run nightly
                 /------\
                /        \       Integration Tests
               /          \      ~100 tests, run on every PR
              /------------\
             /              \    Unit Tests
            /                \   ~500 tests, run on every commit
           /------------------\
          /                    \  AI Regression Tests
         /                      \ ~200 golden dataset, prompt changes
        /------------------------\
```

### Test Types

1. **Unit tests** — Every service method, guardrail rule, data transformation. Mock Claude API.
2. **Integration tests** — Full request lifecycle (endpoint → service → database). Test PostgreSQL container.
3. **AI regression tests** — Golden dataset of 200 patients. Sensitivity must stay >95% for high-risk.
4. **E2E tests** — Playwright: login → dashboard → screening → report download. Nightly against staging.

---

## 9. Deployment & DevOps

### Deployment Path

```
Development     →  Docker Compose (local)
Staging         →  Railway ($5/mo)
Production      →  Vercel (frontend, free) + Railway (backend, $20/mo) + Supabase (PostgreSQL, free)
Growth          →  AWS ECS + RDS (enterprise scale)
```

### CI/CD Pipeline (GitHub Actions)

```
Push to GitHub
    ↓
├── Lint (ESLint + Ruff)
├── Type check (TypeScript + mypy)
├── Unit tests (pytest + Jest)
├── Security scan (Snyk/Trivy)
└── Build Docker images
    ↓
All pass → Deploy to Staging (auto)
    ↓
Manual approval → Deploy to Production
```

### Zero-Downtime Deployment

Blue-green deployment: two identical environments. New version deploys to green, health checks pass, load balancer switches. Rollback in seconds by switching back to blue. Database migrations use expand-contract pattern so both versions coexist.

---

## 10. Interview Knowledge Base

### Architecture Questions

**Q: How would you architect a healthcare AI platform?**

> "I'd start with a modular monolith with clear domain boundaries. Premature decomposition into microservices adds network latency, distributed transaction complexity, and operational overhead without the scale to justify it. I'd extract services only when a specific module has different scaling, deployment, or team-ownership requirements. The AI inference engine is the first extraction candidate because it's compute-heavy and benefits from independent scaling."

**Q: How do you prevent domains from becoming tightly coupled?**

> "Each domain exposes a service interface — other domains communicate through that interface, never by directly accessing another domain's database tables or internal models. The Clinical Analysis domain calls PatientService.get_patient(), it doesn't query the patients table directly. This preserves encapsulation and allows extraction into a standalone service without changing callers."

### API Design Questions

**Q: Why REST and not GraphQL for healthcare?**

> "Three reasons. First, HIPAA audit logging — each REST endpoint maps to a specific resource/action, making granular logging straightforward. GraphQL traverses multiple entities in one query, making audit logging significantly harder. Second, caching — REST endpoints are individually cacheable with HTTP headers; GraphQL responses are harder to cache. Third, the HL7 FHIR healthcare integration ecosystem is REST-based."

**Q: How do you handle pagination?**

> "Cursor-based, not offset. Offset breaks when records change between page loads. Cursor-based uses the last record's ID, so results are stable regardless of concurrent modifications."

**Q: How do you handle errors?**

> "RFC 7807 Problem Details — standardized format with machine-readable error types, human-readable messages, and correlation IDs for tracing. In healthcare, '500 Internal Server Error' is unacceptable. The case manager needs to know: transient AI timeout (retry) or data validation issue (fix input)."

**Q: How do you handle long-running AI requests?**

> "Async task queue. Return 202 Accepted with a task_id immediately. Queue to Celery/Redis. Provide polling endpoint and SSE for progress. Frontend shows: 'Analyzing patient 23 of 50...' Critical UX: case managers can't stare at spinners."

### Backend Questions

**Q: Explain your backend architecture.**

> "Three layers. API layer: thin, handles HTTP concerns, delegates to domain. Domain layer: all business logic, framework-agnostic, doesn't know about FastAPI or databases. Infrastructure layer: adapters for external services. Testing is trivial: swap real database for in-memory, mock Claude client, run same endpoint code."

**Q: Why FastAPI over Django/Flask?**

> "Async support (AI calls take 2-10s, can't block threads), automatic OpenAPI docs (HIPAA compliance requirement), and Pydantic validation (patient data validation isn't a bug, it's patient safety)."

**Q: What's your approach to dependency injection?**

> "FastAPI's Depends() system. Each endpoint declares dependencies. Swap real database for test SQLite, real Claude for mock. Business logic never instantiates its own dependencies. Dependency Inversion Principle from SOLID."

### Database Questions

**Q: Why PostgreSQL for healthcare?**

> "ACID transactions (screening + risk update + audit log: all succeed or none), JSONB for semi-structured AI responses alongside strict schemas, and Row-Level Security — case managers see only their patients at the DATABASE level, not just application level. Defense-in-depth."

**Q: How do you handle PHI encryption?**

> "Two-tier. Application-level AES-256-GCM for most sensitive fields (names, DOB, notes) with keys in AWS KMS. Plus PostgreSQL TDE for entire volume encryption. If one layer is compromised, the other still protects data."

**Q: How do you handle migrations in production?**

> "Alembic with three rules. Every migration reversible (upgrade + downgrade). No destructive migrations — use expand-contract pattern. All tested against production-size dataset in staging first."

**Q: Explain Row-Level Security.**

> "PostgreSQL filters rows based on current user context at the database level. If application auth code has a bug, the database itself blocks unauthorized access. Two independent access control layers. HIPAA auditors love defense-in-depth."

**Q: Scaling strategy?**

> "Indexing first (handles 100K patients), read replicas second (dashboard is read-heavy), table partitioning third (audit_logs by month), sharding only past 10M patients."

### Frontend Questions

**Q: How do you handle real-time dashboard data?**

> "SWR for data that changes infrequently (30s revalidation). SSE for time-sensitive alerts (new high-risk screening). SSE over WebSockets because it's simpler, works through hospital firewalls, and communication is one-directional."

**Q: State management approach?**

> "SWR for server state (90%). React useState/useContext for UI state (10%). No Redux. Adding a state management library at this scale is premature complexity."

**Q: How do you ensure accessibility?**

> "Three layers. shadcn/ui (Radix primitives) for keyboard/screen reader support. Color never the only indicator (badges use color + text + icons). axe-core in CI — build fails on WCAG 2.1 AA violations."

**Q: Walk through a batch screening interaction.**

> "POST to /screenings/batch → 202 Accepted with task_id. Frontend opens SSE connection. Progress bar: 'Analyzing 12 of 35 — Jennifer Brown — 45s remaining.' Complete → dashboard revalidates via SWR, new high-risk patients appear with animation. If one analysis fails, that patient shows retry button, rest continue."

### AI in Healthcare Questions

**Q: Regulatory considerations for clinical AI?**

> "Our system is CDS (Clinical Decision Support), not SaMD (Software as Medical Device). Meets 21st Century Cures Act four-criteria exemption: not acquiring medical data, for healthcare professionals, enabling review of patient-specific info, professional makes final decision. Explicitly NOT autonomous — labeled as recommendations requiring clinical review."

**Q: How do you evaluate clinical AI performance?**

> "Four metrics. Sensitivity (95%+ for high-risk — false negatives are dangerous). Specificity (avoid alert fatigue). Positive Predictive Value (determines clinician trust). Calibration (risk score 80 should mean ~80% actual event rate). Monthly calibration checks against clinician-confirmed outcomes."

**Q: How do you handle model drift?**

> "Every screening stores prompt hash + model version. Golden dataset of 200 clinician-confirmed cases. Run before prompt changes, compare F1 scores. Automated alerts if high-risk classification rate changes suddenly. Model drift in healthcare isn't a quality issue, it's a patient safety issue."

**Q: How do you handle PHI with external AI APIs?**

> "If BAA exists with Anthropic, direct PHI transmission. If not, de-identification layer strips 18 HIPAA identifiers, sends pseudonymized data to Claude, re-hydrates results. Architecture supports both modes. This is a design decision most AI healthcare engineers miss."

### HIPAA Questions

**Q: Walk through your HIPAA compliance.**

> "Three rules. Privacy Rule: minimum necessary access (RBAC, case managers see only their patients). Security Rule: Administrative (RBAC, training), Physical (cloud BAA, encrypted backups), Technical (AES-256, TLS 1.3, MFA, 15-min timeout, audit logging). Breach Notification: automated anomaly detection, security officer alerts, account locking."

**Q: What's a BAA and when do you need one?**

> "Business Associate Agreement. Required for ANY vendor that handles PHI on your behalf — cloud hosting (AWS), AI API (Anthropic), email service (SendGrid), analytics, backups. No BAA = no PHI transmission. Period."

### Deployment Questions

**Q: Zero-downtime deployment strategy?**

> "Blue-green. Two identical environments. Deploy to green, health check, switch load balancer. Rollback: switch back to blue in seconds. Database: expand-contract pattern so both versions work with same schema during transition. Non-negotiable in healthcare — can't interrupt a clinician reviewing a high-risk patient."

---

## Appendix: 6-Month Roadmap

| Month | Focus | Key Deliverables |
|-------|-------|-----------------|
| 1 | Foundation | Docker, PostgreSQL schema, FastAPI REST API, Authentication |
| 2 | Frontend | Next.js setup, Dashboard, Patient views, Screening workflow |
| 3 | AI & Reports | Migrate AI to API, Real-time alerts, Batch screening, HIPAA audit |
| 4 | Multi-Tenant | Organizations, Admin dashboard, Patient portal, Notifications |
| 5 | Integration | EHR/FHIR prep, Insurance reporting, Advanced analytics |
| 6 | Production | Security hardening, CI/CD, Cloud deployment, Documentation |

---

*Document generated: 2026-02-16*
*Architecture diagrams: see `docs/architecture/mindbridge-architecture.md`*
