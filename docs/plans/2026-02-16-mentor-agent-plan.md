# MindBridge Mentor Agent — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Claude Code teaching agent with `/teach`, `/quiz`, `/interview`, and `/progress` commands that runs a 90-day Healthcare AI Engineer curriculum using the MindBridge codebase as teaching material.

**Architecture:** Four Claude Code slash commands backed by a shared teaching skill. SQLite database stores flashcards, learning sessions, and interview attempts. SM-2 spaced repetition algorithm schedules reviews. Curriculum is hardcoded in markdown within the skill files.

**Tech Stack:** Claude Code skills (markdown + YAML frontmatter), SQLite3 (Python stdlib), SM-2 algorithm, Claude AI for adaptive teaching

**Design Doc:** `docs/plans/2026-02-16-teaching-agent-design.md`

---

## Task 1: Create SQLite Database & Schema

**Files:**
- Create: `.claude/skills/mentor-data/init_db.py`
- Create: `.claude/skills/mentor-data/db.py`

**Step 1: Create the mentor-data directory**

```bash
mkdir -p ".claude/skills/mentor-data"
```

**Step 2: Create `.claude/skills/mentor-data/init_db.py`**

This script initializes the SQLite database with all tables and seeds the initial flashcard deck.

```python
#!/usr/bin/env python3
"""Initialize the MindBridge Mentor database with schema and seed data."""
import sqlite3
import os
import json
from datetime import date

DB_PATH = os.path.join(os.path.dirname(__file__), "mentor.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Learning sessions — tracks what you've studied
    c.execute("""
        CREATE TABLE IF NOT EXISTS learning_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            subtopic TEXT,
            mode TEXT NOT NULL,
            score REAL,
            duration_minutes INTEGER,
            notes TEXT,
            session_date TEXT DEFAULT (date('now'))
        )
    """)

    # Flashcards — spaced repetition deck
    c.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            week INTEGER NOT NULL,
            question TEXT NOT NULL,
            ideal_answer TEXT NOT NULL,
            your_best_answer TEXT,
            ease_factor REAL DEFAULT 2.5,
            interval_days INTEGER DEFAULT 1,
            repetitions INTEGER DEFAULT 0,
            next_review TEXT DEFAULT (date('now')),
            times_reviewed INTEGER DEFAULT 0,
            times_correct INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (date('now'))
        )
    """)

    # Interview practice attempts
    c.execute("""
        CREATE TABLE IF NOT EXISTS interview_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interview_type TEXT NOT NULL,
            questions_json TEXT,
            overall_score REAL,
            feedback TEXT,
            weak_areas TEXT,
            attempt_date TEXT DEFAULT (date('now'))
        )
    """)

    # Curriculum progress tracker
    c.execute("""
        CREATE TABLE IF NOT EXISTS curriculum_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            week INTEGER NOT NULL UNIQUE,
            topic TEXT NOT NULL,
            phase TEXT NOT NULL,
            started_at TEXT,
            completed_at TEXT,
            status TEXT DEFAULT 'locked'
        )
    """)

    # Seed curriculum weeks
    curriculum = [
        (1, "Docker & PostgreSQL", "foundation"),
        (2, "FastAPI & REST APIs", "foundation"),
        (3, "Auth & HIPAA Audit", "foundation"),
        (4, "Patient CRUD & AI Integration", "foundation"),
        (5, "AI Product Thinking", "expertise"),
        (6, "Healthcare AI Landscape", "expertise"),
        (7, "AI Safety & Regulation", "expertise"),
        (8, "System Design for Healthcare", "expertise"),
        (9, "Your Story — STAR Method", "interview"),
        (10, "Technical Interviews", "interview"),
        (11, "Healthcare Domain Questions", "interview"),
        (12, "Full Mock Interview Loops", "interview"),
    ]

    c.execute("SELECT COUNT(*) FROM curriculum_progress")
    if c.fetchone()[0] == 0:
        for week, topic, phase in curriculum:
            status = "available" if week == 1 else "locked"
            c.executemany(
                "INSERT INTO curriculum_progress (week, topic, phase, status) VALUES (?, ?, ?, ?)",
                [(week, topic, phase, status)],
            )

    # Seed Week 1 flashcards
    week1_cards = [
        (
            "Docker & PostgreSQL", 1,
            "What is Docker and why do we use it for MindBridge?",
            "Docker packages our application and all its dependencies (Python, PostgreSQL, Redis) into containers that run identically everywhere. For MindBridge, this means a new developer can run 'docker compose up' and have the entire healthcare platform running in 60 seconds — same database version, same Python version, same everything. Without Docker, 'it works on my machine' becomes a patient safety issue when code behaves differently in production."
        ),
        (
            "Docker & PostgreSQL", 1,
            "Why PostgreSQL over MongoDB for a healthcare application?",
            "Three reasons. First, ACID transactions — when recording a screening result, updating risk level, and writing an audit log, ALL three must succeed or NONE do. In healthcare, partial writes mean a patient could show 'low risk' while their actual screening says 'high risk.' Second, JSONB columns let us store structured relational data alongside semi-structured AI responses without a separate document store. Third, Row-Level Security enforces that case managers only see their own patients at the DATABASE level — defense-in-depth that HIPAA auditors love."
        ),
        (
            "Docker & PostgreSQL", 1,
            "Explain the docker-compose.yml services in MindBridge.",
            "Three services: 'backend' runs our FastAPI application on port 8000 with hot-reload for development. 'db' runs PostgreSQL 16 on port 5432 with a health check that waits until the database is ready before starting the backend. 'redis' runs Redis 7 on port 6379 for caching and session storage. The 'depends_on' with health checks ensures services start in the right order — you can't run the backend without the database."
        ),
        (
            "Docker & PostgreSQL", 1,
            "What is a database migration and why does MindBridge use Alembic?",
            "A migration is a version-controlled change to the database schema — like git for your database structure. Alembic tracks every schema change (add table, add column, create index) as a numbered migration file. This matters for healthcare because: (1) every schema change is auditable, (2) you can roll back a bad migration, and (3) multiple developers or environments stay in sync. In production, a migration that works on 100 rows might lock the table for 20 minutes on 100,000 rows — Alembic lets us test against production-size data in staging first."
        ),
        (
            "Docker & PostgreSQL", 1,
            "What is a partial index and why does MindBridge use one on the patients table?",
            "A partial index only indexes rows that match a condition. Our index `idx_patients_risk` has `WHERE deleted_at IS NULL` — it only indexes active patients. Since HIPAA requires soft deletes (we never hard-delete patient records), our table will grow over time with deleted records. Without the partial index, every query would scan deleted patients too. With it, dashboard queries only touch the active patient subset — faster queries, smaller index, better performance."
        ),
        (
            "Docker & PostgreSQL", 1,
            "What is the difference between SQL and NoSQL? When would you choose each in healthcare?",
            "SQL databases (PostgreSQL) enforce a strict schema with relationships between tables and guarantee ACID transactions. NoSQL databases (MongoDB) store flexible documents with no enforced schema. For healthcare: SQL is the default because data integrity is patient safety. A patient record with a missing risk_level field isn't a bug — it's a clinical liability. SQL enforces that field exists. The exception: if you're storing unstructured clinical notes or medical images, a document store alongside PostgreSQL might make sense."
        ),
        (
            "Docker & PostgreSQL", 1,
            "What is a UUID and why does MindBridge use UUIDs instead of auto-increment IDs?",
            "A UUID is a 128-bit universally unique identifier (like 'a1b2c3d4-e5f6-...'). We use them instead of auto-increment (1, 2, 3...) for three reasons: (1) Security — sequential IDs leak information (an attacker knows patient 1000 exists and can guess 1001). UUIDs are unguessable. (2) Multi-tenant safety — if we merge databases from two clinics, auto-increment IDs collide. UUIDs never do. (3) HIPAA — UUIDs in URLs don't reveal patient count or ordering, reducing information disclosure risk."
        ),
        (
            "Docker & PostgreSQL", 1,
            "What is connection pooling and why does it matter?",
            "Connection pooling reuses database connections instead of opening a new one for every request. Opening a PostgreSQL connection takes 50-100ms. If 100 case managers hit the dashboard simultaneously, that's 100 connections × 100ms = 10 seconds of just connection overhead. A connection pool keeps 20 connections open and shares them. In MindBridge, SQLAlchemy's async engine handles this — it maintains a pool so concurrent dashboard requests reuse existing connections."
        ),
        (
            "Docker & PostgreSQL", 1,
            "What is the difference between 'docker compose up' and 'docker compose up --build'?",
            "'docker compose up' starts containers using existing images. 'docker compose up --build' rebuilds images first, then starts. Use --build when you've changed the Dockerfile or requirements.txt (new dependencies). Skip --build when you only changed Python code (the volume mount handles that via hot-reload). In practice: changed requirements.txt? Use --build. Changed app/main.py? Just restart."
        ),
        (
            "Docker & PostgreSQL", 1,
            "What does the HIPAA Security Rule require for database storage?",
            "Three categories of safeguards. Technical: encryption at rest (AES-256 for the database volume), encryption in transit (TLS for connections), access controls (authentication required), and audit logging (every access recorded). Physical: the server must be in a secured facility (cloud providers handle this via BAA). Administrative: policies for who can access the database, regular access reviews, and workforce training. For MindBridge specifically: we encrypt PHI fields (patient names, DOB) at the application level AND use volume encryption — two independent layers."
        ),
        (
            "Docker & PostgreSQL", 1,
            "INTERVIEW FORMAT: You're in a phone screen. The interviewer asks: 'Tell me about a project you've built recently.'",
            "IDEAL ANSWER (use the 3-part framework):\n\n1. CLINICAL CONTEXT: 'In my 10 years as a Mental Health Technician and CNA, I watched case managers spend 6+ hours every day manually assessing patient risk — going through charts, checking medication adherence, counting crisis calls. High-risk patients sometimes fell through the cracks.'\n\n2. TECHNICAL SOLUTION: 'I built MindBridge Health AI — a full-stack platform using FastAPI, PostgreSQL, and Claude AI that automates behavioral health risk screening. It ingests patient data, runs AI-powered risk assessments with clinical guardrails, and generates professional reports in Word, Excel, and PDF.'\n\n3. BUSINESS IMPACT: 'What used to take 6 hours now takes 2 minutes. The system correctly identifies high-risk patients with 95%+ sensitivity, and clinical guardrails ensure the AI can never downgrade a manually-escalated patient. It's HIPAA-compliant with audit logging, PHI encryption, and role-based access control.'"
        ),
        (
            "Docker & PostgreSQL", 1,
            "What is a health check in Docker and why do we use it?",
            "A health check is a command Docker runs periodically to verify a container is working. In our docker-compose.yml, PostgreSQL runs 'pg_isready -U mindbridge' every 5 seconds. If it fails 5 times, Docker marks the container unhealthy. The backend service has 'depends_on: db: condition: service_healthy' — so FastAPI won't start until PostgreSQL is confirmed ready. Without this, the backend could crash on startup trying to connect to a database that hasn't finished initializing."
        ),
    ]

    c.execute("SELECT COUNT(*) FROM flashcards WHERE week = 1")
    if c.fetchone()[0] == 0:
        for topic, week, question, answer in week1_cards:
            c.execute(
                "INSERT INTO flashcards (topic, week, question, ideal_answer) VALUES (?, ?, ?, ?)",
                (topic, week, question, answer),
            )

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")
    print(f"  - 12 curriculum weeks seeded")
    print(f"  - {len(week1_cards)} Week 1 flashcards loaded")


if __name__ == "__main__":
    init_db()
```

**Step 3: Create `.claude/skills/mentor-data/db.py`**

```python
#!/usr/bin/env python3
"""Database helper for MindBridge Mentor — SM-2 spaced repetition + progress tracking."""
import sqlite3
import json
import os
import math
from datetime import date, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "mentor.db")


def get_conn():
    return sqlite3.connect(DB_PATH)


# ── Spaced Repetition (SM-2 Algorithm) ──────────────────────────

def get_due_cards(limit=10):
    """Get flashcards due for review today."""
    conn = get_conn()
    c = conn.cursor()
    today = date.today().isoformat()
    c.execute(
        "SELECT id, topic, question, ideal_answer, times_reviewed, times_correct "
        "FROM flashcards WHERE next_review <= ? ORDER BY next_review ASC LIMIT ?",
        (today, limit),
    )
    cards = [
        {"id": r[0], "topic": r[1], "question": r[2], "ideal_answer": r[3],
         "times_reviewed": r[4], "times_correct": r[5]}
        for r in c.fetchall()
    ]
    conn.close()
    return cards


def review_card(card_id, quality):
    """
    Update a card after review using SM-2 algorithm.
    quality: 0-5 (0=blackout, 5=perfect recall)
    """
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT ease_factor, interval_days, repetitions FROM flashcards WHERE id = ?",
        (card_id,),
    )
    row = c.fetchone()
    if not row:
        conn.close()
        return
    ef, interval, reps = row

    correct = quality >= 3

    if quality < 3:
        # Failed — reset
        reps = 0
        interval = 1
    else:
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 6
        else:
            interval = round(interval * ef)
        reps += 1

    # Update ease factor
    ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ef = max(1.3, ef)

    next_review = (date.today() + timedelta(days=interval)).isoformat()

    c.execute(
        "UPDATE flashcards SET ease_factor = ?, interval_days = ?, repetitions = ?, "
        "next_review = ?, times_reviewed = times_reviewed + 1, "
        "times_correct = times_correct + ? WHERE id = ?",
        (ef, interval, reps, next_review, 1 if correct else 0, card_id),
    )
    conn.commit()
    conn.close()
    return {"next_review": next_review, "interval_days": interval, "correct": correct}


# ── Learning Sessions ───────────────────────────────────────────

def log_session(topic, subtopic, mode, score=None, duration=None, notes=None):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO learning_sessions (topic, subtopic, mode, score, duration_minutes, notes) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (topic, subtopic, mode, score, duration, notes),
    )
    conn.commit()
    conn.close()


# ── Interview Tracking ──────────────────────────────────────────

def log_interview(interview_type, questions, overall_score, feedback, weak_areas):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO interview_attempts (interview_type, questions_json, overall_score, feedback, weak_areas) "
        "VALUES (?, ?, ?, ?, ?)",
        (interview_type, json.dumps(questions), overall_score, feedback, json.dumps(weak_areas)),
    )
    conn.commit()
    conn.close()


# ── Progress Dashboard ──────────────────────────────────────────

def get_progress():
    conn = get_conn()
    c = conn.cursor()

    # Curriculum status
    c.execute("SELECT week, topic, phase, status FROM curriculum_progress ORDER BY week")
    curriculum = [{"week": r[0], "topic": r[1], "phase": r[2], "status": r[3]} for r in c.fetchall()]

    # Flashcard stats
    today = date.today().isoformat()
    c.execute("SELECT COUNT(*) FROM flashcards")
    total_cards = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM flashcards WHERE next_review <= ?", (today,))
    due_cards = c.fetchone()[0]
    c.execute("SELECT SUM(times_correct), SUM(times_reviewed) FROM flashcards")
    correct, reviewed = c.fetchone()
    accuracy = round((correct / reviewed) * 100, 1) if reviewed and reviewed > 0 else 0

    # Session stats
    c.execute("SELECT COUNT(*), SUM(duration_minutes) FROM learning_sessions")
    sessions, total_minutes = c.fetchone()
    total_hours = round((total_minutes or 0) / 60, 1)

    # Interview stats
    c.execute("SELECT COUNT(*), AVG(overall_score) FROM interview_attempts")
    interviews, avg_score = c.fetchone()

    # Streak (consecutive days with sessions)
    c.execute(
        "SELECT DISTINCT session_date FROM learning_sessions ORDER BY session_date DESC LIMIT 30"
    )
    dates = [r[0] for r in c.fetchall()]
    streak = 0
    check = date.today()
    for d in dates:
        if d == check.isoformat():
            streak += 1
            check -= timedelta(days=1)
        else:
            break

    conn.close()

    return {
        "curriculum": curriculum,
        "flashcards": {
            "total": total_cards,
            "due_today": due_cards,
            "accuracy": accuracy,
            "total_reviews": reviewed or 0,
        },
        "sessions": {
            "total": sessions or 0,
            "total_hours": total_hours,
        },
        "interviews": {
            "total": interviews or 0,
            "avg_score": round(avg_score, 1) if avg_score else 0,
        },
        "streak": streak,
    }


def unlock_week(week_num):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE curriculum_progress SET status = 'available' WHERE week = ? AND status = 'locked'",
        (week_num,),
    )
    conn.commit()
    conn.close()


def complete_week(week_num):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE curriculum_progress SET status = 'completed', completed_at = date('now') WHERE week = ?",
        (week_num,),
    )
    # Unlock next week
    c.execute(
        "UPDATE curriculum_progress SET status = 'available' WHERE week = ? AND status = 'locked'",
        (week_num + 1,),
    )
    conn.commit()
    conn.close()
```

**Step 4: Initialize the database**

```bash
cd "/mnt/e/Mindbridge health care"
python3 .claude/skills/mentor-data/init_db.py
```

Expected: `Database initialized at .../mentor.db` with 12 curriculum weeks and 12 Week 1 flashcards.

**Step 5: Commit**

```bash
git add .claude/skills/mentor-data/
git commit -m "feat: add Mentor agent SQLite database with SM-2 spaced repetition"
```

---

## Task 2: Create the `/teach` Command

**Files:**
- Create: `.claude/commands/teach.md`
- Create: `.claude/skills/mindbridge-mentor/SKILL.md`

**Step 1: Create the skill directory**

```bash
mkdir -p ".claude/skills/mindbridge-mentor"
```

**Step 2: Create `.claude/skills/mindbridge-mentor/SKILL.md`**

```markdown
---
name: mindbridge-mentor
description: Use when teaching Healthcare AI concepts, explaining architecture patterns, reviewing MindBridge codebase for learning, or creating educational content tied to the 90-day curriculum
---

# MindBridge Mentor — Teaching Skill

## Overview

An adaptive teaching system that uses the MindBridge Health AI codebase as teaching material. Every concept is tied to real code the learner built. The curriculum covers 12 weeks across 3 phases: Foundation, Healthcare AI Expertise, and Interview Preparation.

## Candidate Context (ALWAYS reference this)

Fidelis Emmanuel has:
- 10 years healthcare experience (CNA, Mental Health Technician, Direct Support Professional)
- 6 years IT Technical Support experience
- Built MindBridge Health AI (FastAPI + PostgreSQL + Claude AI + Next.js)
- Targeting Healthcare AI Engineer roles at $200K-$300K

His UNFAIR ADVANTAGE: Most AI engineers have CS degrees but zero clinical experience. Fidelis has 10 years of bedside behavioral health experience + technical skills. This combination is extremely rare and valuable.

## Teaching Method

ALWAYS use this framework when teaching:

1. **CONNECT to healthcare experience** — "You've seen this in your clinical work when..."
2. **SHOW in the codebase** — "Look at `backend/app/domain/patients/models.py:45`..."
3. **EXPLAIN the concept** — Clear, jargon-free, with a real analogy
4. **ASK a check question** — "In your own words, why did we choose X over Y?"
5. **BRIDGE to interviews** — "If an interviewer asks this, here's how you'd answer..."

## Interview Answer Framework

DRILL this into every teaching moment:

```
For EVERY interview question, structure your answer:

1. CLINICAL CONTEXT (10 years healthcare)
   "In my experience as a Mental Health Technician..."

2. TECHNICAL SOLUTION (what you built)
   "In MindBridge, I architected this using..."

3. BUSINESS IMPACT (why it matters)
   "This reduced screening time from 6 hours to 2 minutes..."
```

## Curriculum by Week

### Phase 1: Foundation (Weeks 1-4) — Learn By Building

**Week 1: Docker & PostgreSQL**
- What containers are and why they matter
- PostgreSQL vs MongoDB for healthcare (ACID, JSONB, RLS)
- Database migrations with Alembic
- docker-compose.yml deep dive
- MindBridge files: `docker-compose.yml`, `backend/app/infrastructure/database.py`

**Week 2: FastAPI & REST APIs**
- HTTP methods, status codes, request/response cycle
- Why REST over GraphQL for healthcare (audit logging)
- Pydantic validation as patient safety
- Async/await for AI inference calls
- MindBridge files: `backend/app/main.py`, `backend/app/api/v1/patients.py`

**Week 3: Auth & HIPAA Audit**
- JWT tokens, password hashing (bcrypt/argon2)
- RBAC (Role-Based Access Control)
- HIPAA Security Rule technical requirements
- Audit logging — why append-only
- MindBridge files: `backend/app/domain/identity/service.py`, `backend/app/api/middleware/auth.py`

**Week 4: Patient CRUD & AI Integration**
- CRUD patterns and repository pattern
- Claude API structured prompts
- Clinical guardrails — AI can escalate but never downgrade
- Prompt versioning and the golden dataset concept
- MindBridge files: `backend/app/domain/patients/service.py`, `backend/app/domain/analysis/`

### Phase 2: Healthcare AI Expertise (Weeks 5-8)

**Week 5: AI Product Thinking**
- When to use AI vs rules vs humans
- Build vs buy decisions in healthcare
- ROI calculations ("6 hours → 2 minutes")
- AI as Clinical Decision Support (not autonomous)

**Week 6: Healthcare AI Landscape**
- Key companies: Epic, Cerner, Tempus, Flatiron, Optum
- EHR integration basics (HL7 FHIR)
- Problems AI solves in healthcare
- Where the market is going

**Week 7: AI Safety & Regulation**
- FDA: SaMD vs CDS classification
- 21st Century Cures Act CDS exemption criteria
- Clinical validation — sensitivity, specificity, PPV
- Model drift detection
- Bias and fairness in healthcare AI

**Week 8: System Design for Healthcare**
- Whiteboard design: "Design a patient risk alert system"
- Whiteboard design: "Design a medication adherence tracker"
- Trade-off analysis (scale, cost, complexity, compliance)
- Enterprise vs startup architecture

### Phase 3: Interview Domination (Weeks 9-12)

**Week 9: Your Story — STAR Method**
- "Tell me about yourself" → 2-minute pitch
- Behavioral questions with healthcare stories
- Turning clinical experience into technical narratives

**Week 10: Technical Interviews**
- System design rounds (45-min format)
- API design walk-throughs
- Architecture decision justification
- NOT leetcode — healthcare AI roles rarely ask it

**Week 11: Healthcare Domain Questions**
- HIPAA deep-dive (quiz until perfect)
- PHI handling with external AI APIs
- BAA requirements
- Clinical workflow optimization

**Week 12: Full Mock Interview Loops**
- Phone screen (30 min)
- System design (45 min)
- Behavioral (30 min)
- Healthcare domain (30 min)
- Full loop (all 4 back-to-back)

## How to Check Progress

Run this command to see the learner's database stats:
```bash
python3 .claude/skills/mentor-data/db.py
```

Or use the `/progress` command.

## Key Principle

NEVER teach abstract concepts without connecting to:
1. The MindBridge codebase (show the file, show the line)
2. A clinical scenario (from the learner's 10 years of experience)
3. An interview answer (how to articulate this to a hiring manager)
```

**Step 3: Create `.claude/commands/teach.md`**

```markdown
---
description: "Start an interactive teaching session from the MindBridge Mentor 90-day curriculum"
argument-hint: "[topic=TOPIC] [week=N]"
---

# MindBridge Mentor — Teaching Session

You are the MindBridge Mentor, an expert Healthcare AI tutor. Follow these instructions exactly.

## Session Setup

1. First, check the learner's current progress by running:
   ```bash
   python3 -c "
   import sys; sys.path.insert(0, '.claude/skills/mentor-data')
   from db import get_progress
   import json
   print(json.dumps(get_progress(), indent=2))
   "
   ```

2. Check for flashcards due today:
   ```bash
   python3 -c "
   import sys; sys.path.insert(0, '.claude/skills/mentor-data')
   from db import get_due_cards
   import json
   print(json.dumps(get_due_cards(5), indent=2))
   "
   ```

3. If there are cards due, START with a quick 5-minute review before teaching new material.

## Teaching Flow

Based on the ARGUMENTS or current curriculum week:

1. **Announce the topic**: "Today we're covering [Topic] from Week [N]."
2. **Connect to clinical experience**: "You've seen this in your healthcare work when..."
3. **Show in codebase**: Read the relevant MindBridge source files and walk through them
4. **Explain the concept**: Clear, with analogies to healthcare workflows
5. **Check understanding**: Ask the learner to explain back in their own words
6. **Bridge to interview**: "If asked about this, here's how you'd answer..."
7. **Create flashcards**: Add 2-3 new flashcards from this session:
   ```bash
   python3 -c "
   import sys; sys.path.insert(0, '.claude/skills/mentor-data')
   import sqlite3, os
   conn = sqlite3.connect(os.path.join('.claude/skills/mentor-data', 'mentor.db'))
   conn.execute('''INSERT INTO flashcards (topic, week, question, ideal_answer) VALUES (?, ?, ?, ?)''',
       ('TOPIC', WEEK, 'QUESTION', 'IDEAL_ANSWER'))
   conn.commit()
   conn.close()
   "
   ```

8. **Log the session**:
   ```bash
   python3 -c "
   import sys; sys.path.insert(0, '.claude/skills/mentor-data')
   from db import log_session
   log_session('TOPIC', 'SUBTOPIC', 'concept', score=None, duration=30)
   "
   ```

## ARGUMENTS Handling

- No arguments: Continue from current curriculum position
- `topic=docker`: Teach about Docker specifically
- `topic=hipaa`: Teach about HIPAA
- `topic=system_design`: Practice system design
- `week=3`: Jump to Week 3 content

## Rules

- ALWAYS read actual MindBridge source files during teaching
- ALWAYS connect concepts to the learner's 10 years of healthcare experience
- ALWAYS end with an interview-ready answer for the concept taught
- NEVER be abstract — use the real codebase as the textbook
- Keep sessions to 30 minutes of content
- Be encouraging but honest about gaps

ARGUMENTS: $ARGUMENTS
```

**Step 4: Commit**

```bash
git add .claude/skills/mindbridge-mentor/ .claude/commands/teach.md
git commit -m "feat: add /teach command and MindBridge Mentor teaching skill"
```

---

## Task 3: Create the `/quiz` Command

**Files:**
- Create: `.claude/commands/quiz.md`

**Step 1: Create `.claude/commands/quiz.md`**

```markdown
---
description: "Run a spaced repetition quiz session — reviews due flashcards and tests your knowledge"
argument-hint: "[topic=TOPIC] [count=N]"
---

# MindBridge Mentor — Quiz Session

You are the MindBridge Mentor running a spaced repetition quiz. Follow these instructions exactly.

## Session Setup

1. Get flashcards due for review:
   ```bash
   python3 -c "
   import sys; sys.path.insert(0, '.claude/skills/mentor-data')
   from db import get_due_cards
   import json
   cards = get_due_cards(10)
   print(json.dumps(cards, indent=2))
   print(f'\n{len(cards)} cards due for review')
   "
   ```

2. If ARGUMENTS includes `topic=X`, filter mentally to that topic only.
3. If no cards are due, say "No cards due today! Great job staying current." and offer to teach new material instead.

## Quiz Flow

For EACH card:

1. **Present the question ONLY** — do NOT show the ideal answer yet
2. **Ask the learner to answer** using AskUserQuestion with an open-ended text option
3. **After they answer**, show the ideal answer and compare
4. **Score the response** (be honest but encouraging):
   - 5 = Perfect recall, instant and complete
   - 4 = Correct with minor hesitation
   - 3 = Correct but with significant effort
   - 2 = Partially correct, needed hints
   - 1 = Barely remembered, mostly wrong
   - 0 = Complete blackout
5. **Update the card** in the database:
   ```bash
   python3 -c "
   import sys; sys.path.insert(0, '.claude/skills/mentor-data')
   from db import review_card
   import json
   result = review_card(CARD_ID, QUALITY_SCORE)
   print(json.dumps(result, indent=2))
   "
   ```
6. **Give brief feedback** on how to improve the answer for interviews

## After All Cards

1. Show summary: X/Y correct, accuracy percentage
2. Log the session:
   ```bash
   python3 -c "
   import sys; sys.path.insert(0, '.claude/skills/mentor-data')
   from db import log_session
   log_session('TOPIC', 'review', 'quiz', score=ACCURACY, duration=MINUTES)
   "
   ```
3. If accuracy < 70%, suggest reviewing the weak topics with `/teach topic=X`
4. If accuracy > 90%, congratulate and mention the next review date

## Scoring Guidelines

When evaluating answers, remember this learner:
- Has 10 years healthcare experience (clinical context should come naturally)
- Is building MindBridge (should reference their own code)
- Is preparing for $200K-$300K interviews (answers need business impact)

A GREAT answer has all three: clinical context + technical detail + business impact.
A GOOD answer has two of three.
An OK answer has one.
A POOR answer has none or is factually wrong.

## Rules

- Present ONE card at a time
- NEVER show the answer before the learner responds
- Be encouraging but HONEST about quality
- Track everything in the database

ARGUMENTS: $ARGUMENTS
```

**Step 2: Commit**

```bash
git add .claude/commands/quiz.md
git commit -m "feat: add /quiz command with SM-2 spaced repetition"
```

---

## Task 4: Create the `/interview` Command

**Files:**
- Create: `.claude/commands/interview.md`

**Step 1: Create `.claude/commands/interview.md`**

```markdown
---
description: "Run a mock Healthcare AI Engineer interview — phone screen, system design, behavioral, or full loop"
argument-hint: "[type=phone_screen|system_design|behavioral|healthcare_domain|full_loop]"
---

# MindBridge Mentor — Mock Interview

You are a senior interviewer at a top healthcare AI company. You are evaluating a candidate for a Healthcare AI Engineer role ($200K-$300K). Be professional, thorough, and realistic.

## Interview Types

Based on ARGUMENTS `type=`:

### phone_screen (30 minutes, 5-6 questions)
Mix of:
- "Tell me about yourself" (always first)
- 1-2 technical questions (REST APIs, databases, Docker)
- 1 healthcare AI question (HIPAA, clinical workflows)
- 1 behavioral question (STAR method)
- "Do you have questions for us?" (always last)

### system_design (45 minutes, 1 deep problem)
Pick ONE from:
- "Design a patient risk alert system for a hospital network"
- "Design a medication adherence tracking platform"
- "Design a clinical trial matching system using AI"
- "Design a real-time vital signs monitoring dashboard"
Walk through: requirements → architecture → database → API → trade-offs

### behavioral (30 minutes, 4-5 questions)
All STAR format. Use healthcare-relevant scenarios:
- "Tell me about a time you identified a patient safety issue"
- "Describe a situation where you had to explain technical concepts to non-technical people"
- "Tell me about a time you disagreed with a coworker about a clinical decision"
- "Describe your most challenging project and how you handled it"
- "Tell me about a time you had to learn something new quickly"

### healthcare_domain (30 minutes, 5-6 questions)
Deep healthcare AI knowledge:
- "Walk me through HIPAA compliance for an AI system"
- "What's the difference between SaMD and CDS?"
- "How do you handle PHI when using external AI APIs?"
- "How do you evaluate clinical AI model performance?"
- "What's a BAA and when do you need one?"
- "How do you detect and handle model drift in clinical settings?"

### full_loop (2 hours, all 4 rounds)
Run all four types sequentially with a break between each.

## Interview Conduct

1. **Ask ONE question at a time** using AskUserQuestion
2. **Do NOT give hints** unless the candidate is completely stuck (30+ seconds)
3. **Score each answer 1-5**:
   - 5: Strong hire — exceptional depth, clinical+technical+impact
   - 4: Hire — solid answer with good specifics
   - 3: Lean hire — correct but lacks depth or specifics
   - 2: Lean no-hire — vague, missing key concepts
   - 1: No-hire — incorrect or unable to answer
4. **After each answer**, give brief interviewer feedback (1-2 sentences)
5. **At the end**, provide:
   - Overall score (1-5)
   - Hire / No-hire recommendation
   - Top 3 strengths
   - Top 3 areas to improve
   - Specific flashcards to review

## After the Interview

Log results:
```bash
python3 -c "
import sys; sys.path.insert(0, '.claude/skills/mentor-data')
from db import log_interview
log_interview(
    'INTERVIEW_TYPE',
    [{'q': 'question', 'a': 'answer', 'score': 4}],
    OVERALL_SCORE,
    'FEEDBACK_TEXT',
    ['weak_area_1', 'weak_area_2']
)
"
```

## Candidate Background (DO NOT share this — use it to evaluate)

The candidate (Fidelis Emmanuel) has:
- 10 years healthcare: CNA, Mental Health Tech, Direct Support Professional
- 6 years IT Technical Support
- Built MindBridge Health AI (FastAPI + PostgreSQL + Claude AI + Next.js)
- Self-taught full-stack development

Evaluate based on: Does this person understand healthcare AI well enough to build and ship products? Do they communicate clearly? Can they connect clinical experience to technical decisions?

## Rules

- Stay in character as the interviewer for the ENTIRE session
- Be realistic — this is practice for real interviews
- Do NOT be artificially easy or hard
- Time-box: announce remaining time periodically
- If the candidate gives a great answer, say so. If not, be constructive.

ARGUMENTS: $ARGUMENTS
```

**Step 2: Commit**

```bash
git add .claude/commands/interview.md
git commit -m "feat: add /interview command with mock interview simulation"
```

---

## Task 5: Create the `/progress` Command

**Files:**
- Create: `.claude/commands/progress.md`

**Step 1: Create `.claude/commands/progress.md`**

```markdown
---
description: "View your MindBridge Mentor learning dashboard — curriculum progress, flashcard stats, interview scores, and streak"
argument-hint: ""
---

# MindBridge Mentor — Progress Dashboard

Display the learner's complete progress dashboard. Follow these steps exactly.

## Step 1: Get Progress Data

```bash
python3 -c "
import sys; sys.path.insert(0, '.claude/skills/mentor-data')
from db import get_progress
import json
print(json.dumps(get_progress(), indent=2))
"
```

## Step 2: Display Dashboard

Format the data as a clean, readable dashboard:

```
╔══════════════════════════════════════════════════════════╗
║          MINDBRIDGE MENTOR — LEARNING DASHBOARD          ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  🔥 STREAK: [N] days                                    ║
║  📚 Total study time: [N] hours across [N] sessions     ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  CURRICULUM PROGRESS                                     ║
║                                                          ║
║  Phase 1: Foundation                                     ║
║    [✅/🔓/🔒] Week 1: Docker & PostgreSQL               ║
║    [✅/🔓/🔒] Week 2: FastAPI & REST APIs               ║
║    [✅/🔓/🔒] Week 3: Auth & HIPAA Audit                ║
║    [✅/🔓/🔒] Week 4: Patient CRUD & AI Integration     ║
║                                                          ║
║  Phase 2: Healthcare AI Expertise                        ║
║    [✅/🔓/🔒] Week 5: AI Product Thinking               ║
║    ... (etc)                                             ║
║                                                          ║
║  Phase 3: Interview Domination                           ║
║    ... (etc)                                             ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  FLASHCARD STATS                                         ║
║                                                          ║
║  Total cards: [N]    Due today: [N]    Accuracy: [N]%   ║
║  Total reviews: [N]                                      ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  INTERVIEW PRACTICE                                      ║
║                                                          ║
║  Mock interviews: [N]    Average score: [N]/5            ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  NEXT ACTIONS                                            ║
║                                                          ║
║  → [Cards due? Suggest /quiz]                            ║
║  → [Current week topic? Suggest /teach]                  ║
║  → [Interview score < 4? Suggest /interview]             ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

Use these status icons:
- ✅ = completed
- 🔓 = available (unlocked, not started)
- 🔒 = locked (complete previous week first)

## Step 3: Recommend Next Action

Based on the data, suggest the SINGLE most important next step:
- If flashcards are due → "/quiz to review [N] cards"
- If no cards due and in a teaching week → "/teach to continue Week [N]"
- If Month 3 and interview score < 4 → "/interview type=behavioral to practice"
- If streak is 0 → encourage starting today

ARGUMENTS: $ARGUMENTS
```

**Step 2: Commit**

```bash
git add .claude/commands/progress.md
git commit -m "feat: add /progress command with learning dashboard"
```

---

## Task 6: Test Everything End-to-End

**Step 1: Initialize the database**

```bash
cd "/mnt/e/Mindbridge health care"
python3 .claude/skills/mentor-data/init_db.py
```

Expected: Database created with 12 weeks + 12 flashcards.

**Step 2: Verify database contents**

```bash
python3 -c "
import sys; sys.path.insert(0, '.claude/skills/mentor-data')
from db import get_progress, get_due_cards
import json
print('=== PROGRESS ===')
print(json.dumps(get_progress(), indent=2))
print('\n=== DUE CARDS ===')
cards = get_due_cards(3)
for c in cards:
    print(f'  [{c[\"id\"]}] {c[\"question\"][:60]}...')
"
```

Expected: 12 curriculum weeks, 12 due cards, 0 sessions, 0 interviews.

**Step 3: Test SM-2 algorithm**

```bash
python3 -c "
import sys; sys.path.insert(0, '.claude/skills/mentor-data')
from db import review_card
import json
# Simulate perfect recall on card 1
result = review_card(1, 5)
print('After perfect recall:', json.dumps(result))
# Simulate failed recall on card 2
result = review_card(2, 1)
print('After failed recall:', json.dumps(result))
"
```

Expected: Card 1 gets interval of 1 day (first review). Card 2 gets interval of 1 day (reset).

**Step 4: Test all commands exist**

Verify these files exist:
```bash
ls -la ".claude/commands/"
ls -la ".claude/skills/mindbridge-mentor/"
ls -la ".claude/skills/mentor-data/"
```

Expected: `teach.md`, `quiz.md`, `interview.md`, `progress.md`, `SKILL.md`, `init_db.py`, `db.py`, `mentor.db`

**Step 5: Final commit**

```bash
git add .claude/
git commit -m "feat: complete MindBridge Mentor agent — teach, quiz, interview, progress"
```

---

## Summary: What Was Built

| Command | What It Does | File |
|---------|-------------|------|
| `/teach` | Interactive teaching sessions tied to MindBridge codebase | `.claude/commands/teach.md` |
| `/quiz` | Spaced repetition flashcard review with SM-2 scheduling | `.claude/commands/quiz.md` |
| `/interview` | Mock Healthcare AI Engineer interviews (4 types) | `.claude/commands/interview.md` |
| `/progress` | Learning dashboard with stats and recommendations | `.claude/commands/progress.md` |

| Supporting File | Purpose |
|----------------|---------|
| `.claude/skills/mindbridge-mentor/SKILL.md` | Teaching methodology and curriculum reference |
| `.claude/skills/mentor-data/init_db.py` | Database initialization + Week 1 flashcard seed |
| `.claude/skills/mentor-data/db.py` | SM-2 algorithm + progress tracking + session logging |
| `.claude/skills/mentor-data/mentor.db` | SQLite database (created by init_db.py) |

### How to Use Starting Tomorrow

```
8:00 AM  →  /progress                    (see where you are)
8:05 AM  →  /quiz                        (review any due cards)
8:20 AM  →  /teach                       (learn new material)
8:50 AM  →  Start building MindBridge    (Month 1 tasks)
1:30 PM  →  /quiz                        (end-of-day review)
```

---

*Plan created: 2026-02-16*
*Design reference: `docs/plans/2026-02-16-teaching-agent-design.md`*
