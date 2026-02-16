# MindBridge Health AI - System Architecture

## High-Level System Architecture

```mermaid
graph TB
    subgraph Users["User Roles"]
        CM[Case Managers]
        CA[Clinic Administrators]
        PT[Patients]
        IP[Insurance/Payers]
        RG[Regulatory Bodies]
    end

    subgraph Frontend["Next.js Application (React + TypeScript)"]
        UI[Dashboard UI]
        AUTH[NextAuth.js<br/>Authentication]
        BFF[API Routes<br/>Backend-for-Frontend]
        PAGES[Pages & Components]

        UI --> AUTH
        UI --> BFF
        UI --> PAGES
    end

    subgraph Backend["Python FastAPI Microservice"]
        API[REST API<br/>Endpoints]
        AIE[AI Analysis Engine<br/>Claude API]
        RPT[Report Generator<br/>Word / Excel / PDF]
        SCH[Task Scheduler<br/>Background Jobs]
        NTF[Notification Service<br/>Email / SMS]
        AUD[Audit Logger<br/>HIPAA Compliance]

        API --> AIE
        API --> RPT
        API --> SCH
        API --> NTF
        API --> AUD
    end

    subgraph Data["Data Layer"]
        PG[(PostgreSQL<br/>Primary Database)]
        RD[(Redis<br/>Cache & Sessions)]
        S3[File Storage<br/>Generated Reports]
    end

    subgraph Infrastructure["Infrastructure & DevOps"]
        DK[Docker<br/>Containers]
        CI[GitHub Actions<br/>CI/CD Pipeline]
        MON[Monitoring<br/>Logging & Alerts]
    end

    Users --> Frontend
    BFF --> Backend
    Backend --> Data
    Infrastructure -.-> Frontend
    Infrastructure -.-> Backend
    Infrastructure -.-> Data
```

## Detailed Backend Architecture

```mermaid
graph LR
    subgraph FastAPI["FastAPI Service"]
        direction TB
        MW[Middleware Layer<br/>CORS / Rate Limit / Auth]

        subgraph Routes["API Routes"]
            R1[/api/patients]
            R2[/api/analysis]
            R3[/api/reports]
            R4[/api/users]
            R5[/api/audit]
            R6[/api/notifications]
        end

        subgraph Services["Service Layer"]
            S1[Patient Service]
            S2[Analysis Service]
            S3[Report Service]
            S4[User Service]
            S5[Audit Service]
            S6[Notification Service]
        end

        subgraph Core["Core"]
            AI[Claude AI Client]
            DOC[Document Engine<br/>python-docx / openpyxl / reportlab]
            MAIL[Email Client<br/>SMTP / SendGrid]
        end

        MW --> Routes
        R1 --> S1
        R2 --> S2
        R3 --> S3
        R4 --> S4
        R5 --> S5
        R6 --> S6
        S2 --> AI
        S3 --> DOC
        S6 --> MAIL
    end
```

## Database Schema (Entity Relationship)

```mermaid
erDiagram
    ORGANIZATION ||--o{ CLINIC : has
    CLINIC ||--o{ USER : employs
    USER ||--o{ PATIENT : manages
    PATIENT ||--o{ SCREENING : has
    SCREENING ||--o{ RISK_ASSESSMENT : produces
    USER ||--o{ AUDIT_LOG : generates
    PATIENT ||--o{ APPOINTMENT : schedules
    PATIENT ||--o{ CRISIS_EVENT : records
    SCREENING ||--o{ REPORT : generates

    ORGANIZATION {
        uuid id PK
        string name
        string subscription_tier
        timestamp created_at
    }

    CLINIC {
        uuid id PK
        uuid org_id FK
        string name
        string address
        string phone
        boolean hipaa_certified
    }

    USER {
        uuid id PK
        uuid clinic_id FK
        string email
        string password_hash
        string role
        string full_name
        boolean mfa_enabled
        timestamp last_login
    }

    PATIENT {
        uuid id PK
        uuid case_manager_id FK
        string name
        string diagnosis
        float medication_adherence
        date last_appointment
        int appointments_missed
        int crisis_calls_30days
        timestamp created_at
        timestamp updated_at
    }

    SCREENING {
        uuid id PK
        uuid patient_id FK
        uuid performed_by FK
        string risk_level
        text ai_analysis
        text primary_factor
        text recommended_action
        timestamp screened_at
    }

    RISK_ASSESSMENT {
        uuid id PK
        uuid screening_id FK
        string risk_category
        float risk_score
        json risk_factors
        text clinical_notes
    }

    APPOINTMENT {
        uuid id PK
        uuid patient_id FK
        timestamp scheduled_at
        string status
        text notes
    }

    CRISIS_EVENT {
        uuid id PK
        uuid patient_id FK
        timestamp occurred_at
        string severity
        text description
        text resolution
    }

    REPORT {
        uuid id PK
        uuid screening_id FK
        uuid generated_by FK
        string format
        string file_path
        timestamp generated_at
    }

    AUDIT_LOG {
        uuid id PK
        uuid user_id FK
        string action
        string resource_type
        uuid resource_id
        json changes
        string ip_address
        timestamp created_at
    }
```

## Frontend Component Architecture

```mermaid
graph TB
    subgraph NextJS["Next.js App Router"]
        Layout[Root Layout<br/>ThemeProvider / AuthProvider]

        subgraph PublicPages["Public Pages"]
            Login[/login]
            Register[/register]
            Landing[/ Landing Page]
        end

        subgraph AuthPages["Authenticated Pages"]
            Dashboard[/dashboard<br/>Risk Overview & Stats]
            Patients[/patients<br/>Patient List & Search]
            PatientDetail[/patients/:id<br/>Patient Profile]
            Screening[/screening<br/>Run New Screening]
            Reports[/reports<br/>Report History & Download]
            Settings[/settings<br/>User & Clinic Settings]
            AuditLog[/audit<br/>HIPAA Audit Trail]
        end

        subgraph Components["Shared Components"]
            Nav[Navigation Sidebar]
            RiskBadge[Risk Level Badge]
            PatientCard[Patient Card]
            Charts[Dashboard Charts<br/>Recharts]
            DataTable[Data Table<br/>Sortable / Filterable]
            AlertBanner[Alert Banner<br/>High-Risk Notifications]
        end

        Layout --> PublicPages
        Layout --> AuthPages
        AuthPages --> Components
    end
```

## Authentication & Authorization Flow

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Next.js Frontend
    participant NA as NextAuth.js
    participant API as FastAPI Backend
    participant DB as PostgreSQL
    participant AL as Audit Log

    U->>FE: Login (email + password)
    FE->>NA: Authenticate
    NA->>API: POST /api/auth/verify
    API->>DB: Validate credentials
    DB-->>API: User record
    API->>API: Check MFA requirement
    API-->>NA: JWT Token + Role
    NA-->>FE: Session cookie (httpOnly, secure)
    FE-->>U: Redirect to dashboard

    Note over U,AL: Subsequent API Requests
    U->>FE: View patient data
    FE->>API: GET /api/patients (Bearer token)
    API->>API: Validate JWT + Check RBAC
    API->>DB: Query patients (scoped to user role)
    API->>AL: Log data access (HIPAA)
    DB-->>API: Patient records
    API-->>FE: JSON response
    FE-->>U: Render patient list
```

## Data Flow: Patient Screening Pipeline

```mermaid
flowchart TD
    A[Patient Data Input] --> B{Input Source}
    B -->|Manual Entry| C[Web Form]
    B -->|CSV Upload| D[Batch Import]
    B -->|EHR Integration| E[HL7/FHIR API]

    C --> F[Validation & Sanitization]
    D --> F
    E --> F

    F --> G[Save to PostgreSQL]
    G --> H[Queue for AI Analysis]

    H --> I[Claude AI Analysis Engine]
    I --> J{Risk Level}

    J -->|High Risk| K[Immediate Alert<br/>Email + Dashboard]
    J -->|Medium Risk| L[Flagged for Review<br/>Dashboard Update]
    J -->|Low Risk| M[Standard Monitoring<br/>Dashboard Update]

    K --> N[Generate Reports]
    L --> N
    M --> N

    N --> O[Word Document]
    N --> P[Excel Spreadsheet]
    N --> Q[PDF Report]

    O --> R[File Storage]
    P --> R
    Q --> R

    R --> S[Available for Download]

    K --> T[Audit Log Entry]
    L --> T
    M --> T
    T --> U[(HIPAA Audit Trail)]
```

## HIPAA Compliance Architecture

```mermaid
graph TB
    subgraph Security["Security Layers"]
        TLS[TLS 1.3<br/>In-Transit Encryption]
        AES[AES-256<br/>At-Rest Encryption]
        RBAC[Role-Based Access Control]
        MFA[Multi-Factor Authentication]
        SESSION[Session Management<br/>Timeout & Revocation]
    end

    subgraph Compliance["HIPAA Controls"]
        AUDIT[Audit Logging<br/>All PHI Access]
        BAA[Business Associate<br/>Agreements]
        BREACH[Breach Detection<br/>& Notification]
        RETENTION[Data Retention<br/>Policy Engine]
        CONSENT[Patient Consent<br/>Management]
    end

    subgraph Monitoring["Monitoring & Alerts"]
        INTRUSION[Intrusion Detection]
        ANOMALY[Anomaly Detection<br/>Unusual Access Patterns]
        UPTIME[Uptime Monitoring]
        BACKUP[Automated Backups<br/>Encrypted & Offsite]
    end

    Security --> Compliance
    Compliance --> Monitoring
```

## Deployment Architecture

```mermaid
graph TB
    subgraph Dev["Development"]
        LOCAL[Local Docker Compose<br/>Frontend + Backend + DB]
        GIT[GitHub Repository<br/>Branch Protection]
    end

    subgraph CI["CI/CD Pipeline (GitHub Actions)"]
        LINT[Lint & Type Check]
        TEST[Unit & Integration Tests]
        SEC[Security Scan<br/>SAST / Dependencies]
        BUILD[Build Docker Images]

        LINT --> TEST --> SEC --> BUILD
    end

    subgraph Staging["Staging Environment"]
        S_FE[Next.js<br/>Vercel Preview]
        S_API[FastAPI<br/>Railway Staging]
        S_DB[PostgreSQL<br/>Railway DB]
    end

    subgraph Production["Production Environment"]
        P_FE[Next.js<br/>Vercel Production]
        P_API[FastAPI<br/>Railway / AWS ECS]
        P_DB[PostgreSQL<br/>AWS RDS / Supabase]
        P_REDIS[Redis<br/>Upstash]
        P_S3[File Storage<br/>AWS S3]
        P_CDN[CDN<br/>CloudFront]
    end

    Dev --> CI
    CI --> Staging
    Staging -->|Manual Approval| Production
```

## 6-Month Implementation Roadmap

```mermaid
gantt
    title MindBridge Health AI - Implementation Roadmap
    dateFormat YYYY-MM-DD

    section Month 1: Foundation
    Project setup & Docker           :m1a, 2026-02-17, 7d
    PostgreSQL schema & migrations   :m1b, after m1a, 7d
    FastAPI backend & REST API       :m1c, after m1b, 7d
    Authentication & RBAC            :m1d, after m1c, 7d

    section Month 2: Frontend
    Next.js project setup            :m2a, after m1d, 5d
    Dashboard & patient views        :m2b, after m2a, 10d
    Screening workflow UI            :m2c, after m2b, 7d
    Report download & history        :m2d, after m2c, 7d

    section Month 3: AI & Reports
    Migrate AI engine to API         :m3a, after m2d, 7d
    Real-time risk alerts            :m3b, after m3a, 7d
    Batch screening & scheduling     :m3c, after m3b, 7d
    HIPAA audit logging              :m3d, after m3c, 7d

    section Month 4: Multi-Tenant
    Organization & clinic models     :m4a, after m3d, 7d
    Admin dashboard                  :m4b, after m4a, 7d
    Patient portal (basic)           :m4c, after m4b, 7d
    Email notifications              :m4d, after m4c, 7d

    section Month 5: Integration
    EHR/FHIR integration prep       :m5a, after m4d, 7d
    Insurance/payer reporting        :m5b, after m5a, 7d
    Advanced analytics & charts      :m5c, after m5b, 7d
    Performance optimization         :m5d, after m5c, 7d

    section Month 6: Production
    Security hardening               :m6a, after m5d, 7d
    CI/CD pipeline                   :m6b, after m6a, 5d
    Cloud deployment                 :m6c, after m6b, 7d
    Documentation & launch           :m6d, after m6c, 7d
```

## Technology Stack Summary

```mermaid
mindmap
    root((MindBridge<br/>Health AI))
        Frontend
            Next.js 14
            React 18
            TypeScript
            Tailwind CSS
            Recharts
            NextAuth.js
        Backend
            Python 3.12
            FastAPI
            SQLAlchemy ORM
            Celery Workers
            Pydantic
        AI Engine
            Claude API
            Prompt Templates
            Risk Scoring
            NLP Analysis
        Database
            PostgreSQL 16
            Redis Cache
            Alembic Migrations
        Infrastructure
            Docker Compose
            GitHub Actions
            Vercel
            Railway / AWS
        Security
            HIPAA Compliance
            AES-256 Encryption
            TLS 1.3
            RBAC + MFA
            Audit Logging
```
