# 🏥 Project 2 — ClinicalScribe AI

> AI-powered clinical documentation assistant for behavioral health

## Core Problem

Behavioral health clinicians spend 30-40% of their time on documentation.
SOAP notes, treatment plans, progress notes — all manual, repetitive, error-prone.
Tobe has 10 years experience knowing exactly what good clinical documentation looks like.

## Solution

ClinicalScribe AI listens to clinician input (text or voice) and generates:

- Structured SOAP notes (Subjective, Objective, Assessment, Plan)
- DSM-5 aligned diagnoses
- Treatment plan updates
- Progress note summaries
- Medication management notes

## Tech Stack (planned)

- Frontend: Next.js (same pattern as MindBridge)
- Backend: FastAPI (same pattern as MindBridge)
- AI: Anthropic Claude API (claude-sonnet)
- Database: PostgreSQL on Railway
- Deployment: Vercel + Railway
- New: Whisper API for voice-to-text (optional)

## Key Features

1. Voice/text input from clinician
2. AI generates structured SOAP note
3. Clinician reviews and edits
4. Note saved to PostgreSQL with audit trail
5. Export to PDF or EHR format

## HIPAA Considerations

- No real PHI stored (demo mode)
- All AI processing via API (no local models)
- Audit log for every note generated
- Session management same as MindBridge

## Why This Project

- Addresses #1 pain point in behavioral health
- Tobe's domain expertise = unfair advantage
- Demonstrates AI integration (Claude API)
- Directly relevant to healthcare AI roles
- Natural extension of MindBridge

## Target Completion

Week 7-9 (Days 31-45)

## Week 4 Starter Prompt

"Week 4 Day 16 — Starting Project 2 planning for ClinicalScribe AI.
Tech stack: Next.js + FastAPI + Claude API + PostgreSQL.
First milestone: Claude API integration generating SOAP notes from clinician input."

## Connection to MindBridge

ClinicalScribe can eventually integrate with MindBridge:

- Generate notes directly from patient dashboard
- Link notes to patient records
- Complete behavioral health platform

## Interview Talking Point

"I built two production healthcare AI applications:
MindBridge — patient risk management platform
ClinicalScribe — AI clinical documentation assistant
Both HIPAA-compliant, both live in production, both solving real problems
I experienced firsthand as a behavioral health clinician for 10 years."
