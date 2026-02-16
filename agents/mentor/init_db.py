#!/usr/bin/env python3
"""Initialize the MindBridge Mentor database with schema and seed data."""
import sqlite3
import os
from datetime import date

# Database will be created in the same directory as this script (agents/mentor/)
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

    # Seed curriculum weeks (12-week backend-focused program)
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
            c.execute(
                "INSERT INTO curriculum_progress (week, topic, phase, status) VALUES (?, ?, ?, ?)",
                (week, topic, phase, status),
            )

    # Seed Week 1 flashcards - High-value interview questions
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
            "What is a database migration and why does MindBridge use Alembic?",
            "A migration is a version-controlled change to the database schema — like git for your database structure. Alembic tracks every schema change (add table, add column, create index) as a numbered migration file. This matters for healthcare because: (1) every schema change is auditable, (2) you can roll back a bad migration, and (3) multiple developers or environments stay in sync. In production, a migration that works on 100 rows might lock the table for 20 minutes on 100,000 rows — Alembic lets us test against production-size data in staging first."
        ),
        (
            "Docker & PostgreSQL", 1,
            "What is a UUID and why does MindBridge use UUIDs instead of auto-increment IDs?",
            "A UUID is a 128-bit universally unique identifier (like 'a1b2c3d4-e5f6-...'). We use them instead of auto-increment (1, 2, 3...) for three reasons: (1) Security — sequential IDs leak information (an attacker knows patient 1000 exists and can guess 1001). UUIDs are unguessable. (2) Multi-tenant safety — if we merge databases from two clinics, auto-increment IDs collide. UUIDs never do. (3) HIPAA — UUIDs in URLs don't reveal patient count or ordering, reducing information disclosure risk."
        ),
        (
            "Docker & PostgreSQL", 1,
            "What does the HIPAA Security Rule require for database storage?",
            "Three categories of safeguards. Technical: encryption at rest (AES-256 for the database volume), encryption in transit (TLS for connections), access controls (authentication required), and audit logging (every access recorded). Physical: the server must be in a secured facility (cloud providers handle this via BAA). Administrative: policies for who can access the database, regular access reviews, and workforce training. For MindBridge specifically: we encrypt PHI fields (patient names, DOB) at the application level AND use volume encryption — two independent layers."
        ),
        (
            "Docker & PostgreSQL", 1,
            "INTERVIEW: 'Tell me about a project you've built recently.'",
            "CLINICAL CONTEXT: 'In my 10 years as a Mental Health Technician and CNA, I watched case managers spend 6+ hours every day manually assessing patient risk — going through charts, checking medication adherence, counting crisis calls. High-risk patients sometimes fell through the cracks.' TECHNICAL SOLUTION: 'I built MindBridge Health AI — a full-stack platform using FastAPI, PostgreSQL, and Claude AI that automates behavioral health risk screening. It ingests patient data, runs AI-powered risk assessments with clinical guardrails, and generates professional reports in Word, Excel, and PDF.' BUSINESS IMPACT: 'What used to take 6 hours now takes 2 minutes. The system correctly identifies high-risk patients with 95%+ sensitivity, and clinical guardrails ensure the AI can never downgrade a manually-escalated patient. It's HIPAA-compliant with audit logging, PHI encryption, and role-based access control.'"
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
    
    print("=" * 70)
    print("✅ MindBridge Mentor Database Initialized!")
    print("=" * 70)
    print(f"\n📍 Database location: {DB_PATH}")
    print(f"📊 12 curriculum weeks seeded")
    print(f"📚 {len(week1_cards)} Week 1 flashcards loaded\n")
    print("🎯 Your 12-Week Healthcare AI Engineer Curriculum:\n")
    
    for week, topic, phase in curriculum:
        status_icon = "🟢" if week == 1 else "🔒"
        phase_label = phase.upper()
        print(f"  {status_icon} Week {week:2d}: {topic:40s} [{phase_label}]")
    
    print("\n" + "=" * 70)
    print("🚀 Next step: Run 'mentor quiz' to start learning!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    init_db()
