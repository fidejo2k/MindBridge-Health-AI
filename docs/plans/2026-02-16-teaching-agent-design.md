# MindBridge Agent System — Teaching, Job Search & Auto-Apply

**Date:** 2026-02-16
**Author:** Fidelis Emmanuel
**Status:** Approved
**Version:** 1.0

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Agent 1: MindBridge Mentor (Teaching)](#2-agent-1-mindbridge-mentor)
3. [Agent 2: Job Hunter (Search)](#3-agent-2-job-hunter)
4. [Agent 3: Auto Applicant (Apply)](#4-agent-3-auto-applicant)
5. [Daily Schedule Integration](#5-daily-schedule-integration)
6. [Shared Data Architecture](#6-shared-data-architecture)
7. [Implementation Priority](#7-implementation-priority)

---

## 1. Executive Summary

### Vision

A 3-agent system that works together to: (1) teach Fidelis Healthcare AI Engineering concepts tied to his MindBridge codebase, (2) discover Healthcare AI Engineer job opportunities across major platforms, and (3) automatically apply to qualified positions with tailored materials.

### Candidate Profile — The Unfair Advantage

```
FIDELIS EMMANUEL

Healthcare Experience (10 years):
  - Certified Nursing Assistant (CNA)
  - Mental Health Technician
  - Direct Support Professional
  → Deep understanding of clinical workflows, patient care,
    behavioral health challenges, and real-world healthcare pain points

Technology Experience (6 years):
  - IT Technical Support
  → System troubleshooting, technical problem-solving, user-facing tech

Building Now:
  - MindBridge Health AI — full-stack, HIPAA-compliant behavioral health
    risk assessment platform (Next.js + FastAPI + PostgreSQL + Claude AI)

WHY THIS IS POWERFUL:
  Most AI engineers have CS degrees but zero clinical experience.
  Fidelis has 10 years of bedside patient care + technical skills.
  Companies can teach engineers about AI tools.
  They CANNOT teach 10 years of healthcare domain expertise.
  This combination is rare and extremely valuable.
```

### Target

- **Role:** Healthcare AI Engineer (and variant titles)
- **Salary:** $200K - $300K
- **Location:** Remote, Ohio (Columbus/Cleveland/Cincinnati), open to relocate
- **Timeline:** Apply in 3 months (May 2026)
- **Daily Schedule:** 8 AM - 2 PM (6 hours) for learning + building

### System Overview

| Agent | Purpose | Technology |
|-------|---------|-----------|
| MindBridge Mentor | Teaching, quizzes, mock interviews | Claude Code skill + SQLite |
| Job Hunter | Job search, scoring, deduplication | Python + PostgreSQL + Web scraping |
| Auto Applicant | Resume tailoring, cover letters, auto-submit | Python + Playwright + Claude |

---

## 2. Agent 1: MindBridge Mentor

### What It Is

A Claude Code custom skill set invoked with `/teach`, `/quiz`, `/interview`, and `/progress`. It lives inside the MindBridge project and uses the actual codebase + design docs as teaching material.

### Skill Commands

```
/teach              → Start or continue a teaching session
/teach topic=sql    → Learn a specific topic
/quiz               → Random quiz from current phase
/quiz topic=hipaa   → Quiz on a specific topic
/interview          → Start a mock interview session
/interview type=sys → System design interview
/progress           → View learning dashboard
```

### 90-Day Curriculum

#### Month 1: Foundation (Weeks 1-4) — Learn By Building

Learning happens while building MindBridge. Each week of coding teaches concepts.

```
Week 1: Docker + PostgreSQL
  Concepts: Infrastructure, containers, databases, SQL
  Quiz: "Why PostgreSQL over MongoDB for healthcare?"
  Cards: ~12 flashcards

Week 2: FastAPI + REST API
  Concepts: HTTP, REST, async/await, Pydantic validation
  Quiz: "Design an API for appointment scheduling"
  Cards: ~12 flashcards

Week 3: Auth + HIPAA Audit
  Concepts: JWT, RBAC, HIPAA Security Rule, audit logging
  Quiz: "Walk me through your HIPAA compliance"
  Cards: ~12 flashcards

Week 4: Patient CRUD + AI Integration
  Concepts: CRUD patterns, Claude API, structured prompts, guardrails
  Quiz: "How do you validate AI output in clinical settings?"
  Cards: ~14 flashcards

Running total: ~50 flashcards
```

#### Month 2: Healthcare AI Expertise (Weeks 5-8)

Focus on what makes a $200K-$300K candidate.

```
Week 5: AI Product Thinking
  - When to use AI vs rules vs humans
  - Build vs buy decisions
  - ROI calculations for healthcare AI
  - "Our screening tool saves 6 hours/day per case manager"

Week 6: Healthcare AI Landscape
  - Key companies (Epic, Cerner, Tempus, Flatiron, Optum)
  - EHR integration (HL7 FHIR)
  - What problems AI actually solves in healthcare
  - YOUR EDGE: You've SEEN these problems firsthand

Week 7: AI Safety & Regulation
  - FDA SaMD vs CDS classification
  - Clinical validation approaches
  - Bias and fairness in healthcare AI
  - AI safety guardrails (what you built in MindBridge)

Week 8: System Design for Healthcare
  - Whiteboard design practice (not coding)
  - "Design a patient risk alert system"
  - "Design a medication adherence tracker"
  - Practice drawing architectures + explaining trade-offs

Running total: ~150 flashcards
Spaced repetition active: reviews at 1, 3, 7, 14 day intervals
```

#### Month 3: Interview Domination (Weeks 9-12)

```
Week 9: Your Story (STAR Method)
  - "Tell me about yourself" → 2-minute pitch
    CNA → IT → Healthcare AI Engineer narrative
  - Behavioral questions using YOUR clinical experiences
  - "Tell me about a time you identified a patient safety issue"

Week 10: Technical Interviews
  - System design practice (3 healthcare scenarios)
  - "How would you architect [X]?" → draw + explain
  - API design walk-throughs using YOUR MindBridge endpoints
  - NOT leetcode — healthcare AI roles rarely ask it

Week 11: Healthcare Domain Questions
  - HIPAA deep-dive (quiz until perfect)
  - "How do you handle PHI with external AI APIs?"
  - "What's the difference between SaMD and CDS?"
  - Clinical workflow questions (YOUR SUPERPOWER)

Week 12: Full Mock Interview Loops
  - Day 1: Phone screen simulation (30 min)
  - Day 2: System design round (45 min)
  - Day 3: Behavioral round (30 min)
  - Day 4: Healthcare domain round (30 min)
  - Day 5: Full loop (all 4 rounds back-to-back)

Target: Score 4/5+ consistently before applying
Running total: ~200 flashcards
```

### How Teaching Uses Your Codebase

The mentor teaches through YOUR code, not abstract concepts:

| Generic Question | MindBridge-Specific Version |
|-----------------|----------------------------|
| "What is RBAC?" | "Look at `backend/app/api/middleware/auth.py`. Explain how `require_role()` works." |
| "Explain indexing" | "Your patients table has `idx_patients_risk`. Why is it a partial index?" |
| "Event-driven architecture?" | "When a screening completes in MindBridge, 4 things happen. Draw the event flow." |
| "HIPAA compliance?" | "Walk me through MindBridge's audit_logs table. Why is it append-only?" |

### Interview Answer Framework

The agent drills this structure into every answer:

```
1. CLINICAL CONTEXT (your 10 years)
   "In my experience as a Mental Health Technician..."

2. TECHNICAL SOLUTION (what you built)
   "In MindBridge, I architected this using..."

3. BUSINESS IMPACT (why it matters)
   "This reduced screening time from 6 hours to 2 minutes..."
```

### Data Model (SQLite)

```sql
CREATE TABLE learning_sessions (
    id INTEGER PRIMARY KEY,
    topic TEXT NOT NULL,
    subtopic TEXT,
    mode TEXT NOT NULL,           -- 'concept', 'quiz', 'interview'
    score REAL,
    duration_minutes INTEGER,
    session_date TEXT DEFAULT (date('now'))
);

CREATE TABLE flashcards (
    id INTEGER PRIMARY KEY,
    topic TEXT NOT NULL,
    question TEXT NOT NULL,
    ideal_answer TEXT NOT NULL,
    your_best_answer TEXT,
    ease_factor REAL DEFAULT 2.5,  -- SM-2 spaced repetition algorithm
    interval_days INTEGER DEFAULT 1,
    next_review TEXT,
    times_reviewed INTEGER DEFAULT 0,
    times_correct INTEGER DEFAULT 0
);

CREATE TABLE interview_attempts (
    id INTEGER PRIMARY KEY,
    interview_type TEXT NOT NULL,
    questions_json TEXT,
    overall_score REAL,
    feedback TEXT,
    weak_areas TEXT,
    attempt_date TEXT DEFAULT (date('now'))
);
```

---

## 3. Agent 2: Job Hunter

### What It Does

Automated job discovery engine. Searches LinkedIn, Indeed, Glassdoor, and company career pages daily. Scores each listing for match quality. Feeds qualified jobs to Auto Applicant.

### Search Configuration

```
TARGET TITLES:
  - Healthcare AI Engineer
  - Clinical AI Engineer
  - Health AI/ML Engineer
  - Healthcare Data Scientist
  - Clinical Decision Support Engineer
  - Health Tech ML Engineer
  - Biomedical AI Engineer
  - AI Solutions Architect (Healthcare)
  - Healthcare Software Engineer (AI)
  - Digital Health Engineer
  - ML Engineer, Healthcare
  - AI Engineer, Health Tech

TARGET LOCATIONS:
  - Remote (US)
  - Columbus, OH
  - Cleveland, OH
  - Cincinnati, OH
  - Louisville, KY
  - SF Bay Area, NYC, Boston, Seattle

SALARY FILTER: $150K+ (cast wide net, negotiate up)

TARGET COMPANIES:
  Health systems: Epic, Cerner/Oracle Health, Intermountain, Cleveland Clinic
  AI startups: Tempus, Flatiron Health, Veracyte, PathAI, Viz.ai
  Big tech: Google Health, Amazon Health, Microsoft Health, Apple Health
  Consulting: McKinsey, BCG, Deloitte (health practices)
  Payers: UnitedHealth/Optum, Humana, Anthem/Elevance, CVS/Aetna
```

### Job Match Scoring (0-100)

```python
def calculate_match_score(job, profile):
    score = 0

    # Title match (0-25)
    if exact_title_match(job.title, profile.target_titles):
        score += 25
    elif partial_title_match(job.title, profile.target_titles):
        score += 15

    # Location (0-20)
    if job.remote:
        score += 20
    elif job.location in profile.preferred_locations:
        score += 15

    # Salary (0-20)
    if job.salary_max and job.salary_max >= profile.min_salary:
        score += 20
    elif job.salary_max and job.salary_max >= profile.min_salary * 0.8:
        score += 10

    # Skills match (0-20)
    matched = len(set(job.required_skills) & set(profile.skills))
    score += min(20, matched * 4)

    # Healthcare domain bonus (0-15)
    if "healthcare" in job.description.lower():
        score += 10
    if "clinical" in job.description.lower():
        score += 5

    return score
```

**Thresholds:**
- 70+ → Auto-apply
- 50-69 → Review queue (you decide)
- Below 50 → Logged but skipped

### Deduplication Logic

```
Before adding a job:
1. Check URL uniqueness (exact match)
2. Check dedup_hash = SHA256(normalize(company) + normalize(title) + normalize(location))
3. Check if already applied (applications table join)

Prevents: same job from multiple platforms, re-posts, re-applications
```

### Data Model

```sql
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source TEXT NOT NULL,
    external_id TEXT,
    url TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    company_url TEXT,
    location TEXT,
    is_remote BOOLEAN DEFAULT FALSE,
    salary_min INTEGER,
    salary_max INTEGER,
    description TEXT,
    required_skills TEXT[],
    match_score INTEGER,
    status TEXT DEFAULT 'new',
    discovered_at TIMESTAMP DEFAULT NOW(),
    applied_at TIMESTAMP,
    dedup_hash TEXT UNIQUE
);

CREATE TABLE applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID REFERENCES jobs(id) NOT NULL,
    resume_version TEXT,
    cover_letter TEXT,
    status TEXT DEFAULT 'submitted',
    submitted_at TIMESTAMP DEFAULT NOW(),
    response_at TIMESTAMP,
    notes TEXT,
    reviewed_by_user BOOLEAN DEFAULT FALSE
);

CREATE UNIQUE INDEX idx_applications_job ON applications(job_id);
```

---

## 4. Agent 3: Auto Applicant

### Application Pipeline

```
Job (score 70+) enters pipeline
    │
    ▼
1. GENERATE MATERIALS
   - Tailor resume to job description
   - Write cover letter
   - Match keywords from JD
    │
    ▼
2. SUPERVISED CHECK (applications 1-10 only)
   - Display job details + materials
   - User approves, edits, or skips
   - Agent learns user preferences
    │
    ▼
3. APPLY VIA BROWSER (Playwright)
   - Navigate to application URL
   - Fill form fields
   - Upload resume + cover letter
   - Submit application
   - Take screenshot for proof
    │
    ▼
4. RECORD & REPORT
   - Log in applications table
   - Store screenshot
   - Send daily email digest
```

### Resume Tailoring Prompt

```
INSTRUCTIONS:
1. Keep all factual information identical — never fabricate
2. Reorder bullet points to match job's priority keywords
3. Mirror the job description's language where truthful
4. Emphasize healthcare domain expertise (differentiator)
5. Highlight MindBridge project with metrics relevant to THIS role
6. ATS-friendly formatting (no tables, standard headers)
```

### Cover Letter Prompt

```
CANDIDATE STORY:
Fidelis Emmanuel spent 10 years in direct patient care — as a CNA, Mental Health
Technician, and Direct Support Professional in behavioral health settings. He saw
firsthand how case managers spent 6+ hours daily on manual patient risk assessments.
He transitioned into technology (6 years IT support) and built MindBridge Health AI —
a full-stack, HIPAA-compliant platform that uses Claude AI to automate behavioral
health risk screening, reducing assessment time from 6 hours to 2 minutes.

RULES:
1. Opening: Connect healthcare experience to company's mission
2. Middle: Show how MindBridge solves a problem they care about
3. Close: Specific enthusiasm for this company + role
4. Tone: Professional but human
5. Length: 250-350 words
6. NEVER fabricate
```

### Supervised Mode (First 10)

```
For applications 1-10, agent PAUSES and shows:

  APPLICATION REVIEW #3/10
  Job: Senior Healthcare AI Engineer
  Company: Tempus AI
  Location: Remote
  Salary: $280K - $350K
  Match Score: 87/100

  TAILORED RESUME: [View]
  COVER LETTER: [View]

  [Approve & Submit]  [Edit First]  [Skip Job]

After 10 approved applications, agent stores editing
patterns as preferences and goes fully autonomous.
```

### Daily Digest Email

```
Subject: MindBridge Job Agent — Daily Report

TODAY'S ACTIVITY
  New jobs found: 12
  Applications submitted: 3
  Awaiting your review: 2

APPLIED TODAY
  1. Healthcare AI Engineer — Tempus (Remote) — $280K-$350K
  2. Clinical ML Engineer — Epic Systems (WI) — $250K-$300K
  3. AI Solutions Architect — Optum (Remote) — $260K-$320K

RUNNING TOTALS
  Total applications: 47
  Interviews scheduled: 3
  Awaiting response: 36
```

### Safety & Ethics Rules

```
HARD RULES — NON-NEGOTIABLE:
1. NEVER fabricate experience, credentials, or skills
2. NEVER apply to the same company twice for the same role
3. NEVER submit without master resume as factual base
4. All cover letters based on REAL experience only
5. First 10 applications require explicit user approval
6. Daily digest includes EVERYTHING — full transparency
7. User can pause/stop agent at any time
8. All applications logged with screenshots for accountability
```

---

## 5. Daily Schedule Integration

### 8 AM - 2 PM Daily Block (6 Hours)

```
MONTH 1 (Building + Learning):
  8:00 - 8:30   /teach → Morning concept lesson (30 min)
  8:30 - 8:45   /quiz → Quick quiz on yesterday's topic (15 min)
  8:45 - 12:00  BUILD MindBridge (Month 1 tasks) (3 hr 15 min)
  12:00 - 12:30 Lunch break
  12:30 - 1:30  BUILD MindBridge continued (1 hr)
  1:30 - 2:00   /quiz → End-of-day review + flashcards (30 min)

MONTH 2 (Deepening + Building):
  8:00 - 8:45   /teach → Healthcare AI concept (45 min)
  8:45 - 9:00   /quiz → Spaced repetition review (15 min)
  9:00 - 12:00  BUILD MindBridge (Month 2 tasks) (3 hr)
  12:00 - 12:30 Lunch break
  12:30 - 1:15  BUILD MindBridge continued (45 min)
  1:15 - 2:00   /teach topic=system_design → Practice (45 min)

MONTH 3 (Interview Prep + Applying):
  8:00 - 9:00   /interview → Mock interview session (1 hr)
  9:00 - 9:15   /quiz → Spaced repetition (15 min)
  9:15 - 9:30   Review job agent daily digest (15 min)
  9:30 - 12:00  BUILD MindBridge (Month 3 tasks) (2 hr 30 min)
  12:00 - 12:30 Lunch break
  12:30 - 1:30  /interview type=behavioral → Practice (1 hr)
  1:30 - 2:00   Review + approve applications (30 min)

JOB AGENTS RUN AUTONOMOUSLY:
  Job Hunter: Runs at 6 AM daily (before your session)
  Auto Applicant: Runs at 7 AM daily (you review at 9:30)
```

---

## 6. Shared Data Architecture

```
PostgreSQL (MindBridge DB):
  ├── MindBridge tables (patients, screenings, etc.)
  ├── jobs table (Job Hunter)
  └── applications table (Auto Applicant)

SQLite (Local teaching data):
  ├── learning_sessions
  ├── flashcards
  └── interview_attempts

Why split:
  - Teaching data is personal, local, doesn't need a server
  - Job/application data benefits from PostgreSQL (queries, joins, reporting)
  - MindBridge tables are the production app
```

---

## 7. Implementation Priority

```
WEEK 1 (Immediate): MindBridge Mentor skill
  - Build /teach, /quiz, /progress commands
  - Load curriculum and first 50 flashcards
  - START LEARNING IMMEDIATELY

WEEK 2: Job Hunter agent
  - LinkedIn scraper
  - Indeed scraper
  - Scoring algorithm
  - PostgreSQL jobs table
  - Daily scheduled execution

WEEK 3: Auto Applicant agent
  - Resume tailoring with Claude
  - Cover letter generation
  - Playwright browser automation
  - Supervised mode (first 10)
  - Daily digest email

WEEK 4+: Refinement
  - Add Glassdoor + company career pages
  - Improve scoring based on early results
  - Mock interview improvements based on weak areas
  - Application tracking dashboard
```

---

*Document generated: 2026-02-16*
*Architecture reference: `docs/architecture/mindbridge-architecture.md`*
*Main design reference: `docs/plans/2026-02-16-mindbridge-full-stack-design.md`*
