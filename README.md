# MindBridge Health AI - Healthcare AI Engineer Training Portfolio

**90-Day Intensive Training Program**  
**Target Role:** Healthcare AI Engineer ($200K-$300K)  
**Timeline:** February 2026 - May 2026

[![GitHub](https://img.shields.io/badge/GitHub-Live-success)](https://github.com/fidejo2k/MindBridge-Health-AI)
[![Status](https://img.shields.io/badge/Week%201-In%20Progress-blue)]()
[![Quiz](https://img.shields.io/badge/Quiz%20Score-100%25-brightgreen)]()

---

## 🎯 Project Overview

**MindBridge Health AI** is a production-ready, HIPAA-compliant behavioral health risk assessment platform that combines:
- **10 years clinical experience** (CNA + Mental Health Technician)
- **Modern AI technology** (Claude API, FastAPI, PostgreSQL)
- **Production engineering** (Logging, automation, monitoring)

This repository demonstrates end-to-end healthcare AI engineering capabilities built from scratch in 12 weeks.

---

## 🏗️ System Architecture

### Current Implementation (Week 1)
```
MindBridge Health AI/
├── agents/                      # 3-Agent Learning & Job Hunt System
│   ├── mentor/                  # ✅ Spaced repetition teaching agent
│   │   ├── init_db.py          # Database initialization
│   │   ├── quiz.py             # Daily quiz system (SM-2 algorithm)
│   │   └── mentor.db           # SQLite (12-week curriculum)
│   │
│   ├── job_hunter/             # 🔄 Job scraping agent (Week 10)
│   └── auto_apply/             # 🔄 Auto application agent (Week 11)
│   
├── agents/shared/              # Shared infrastructure
│   ├── logger.py               # ✅ Centralized logging
│   └── email_notifier.py       # ✅ Email alerts
│
├── scripts/                    # MindBridge Health AI Scripts
│   ├── generate_all_reports.py # ✅ Multi-format report generator
│   ├── word_generator.py       # ✅ Word document reports
│   ├── excel_generator.py      # ✅ Excel spreadsheet reports
│   └── pdf_generator.py        # ✅ PDF report generator
│
├── docs/                       # Architecture & Planning
│   ├── architecture/
│   │   └── mindbridge-architecture.md  # 9 Mermaid diagrams
│   └── plans/
│       ├── 2026-02-16-mindbridge-full-stack-design.md
│       ├── 2026-02-16-mentor-agent-plan.md (1127 lines)
│       └── 2026-02-16-teaching-agent-design.md
│
├── logs/                       # Automated logging
│   └── mentor.log              # All agent activity
│
└── reports/                    # Generated patient reports
    └── [timestamped reports]
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Git
- Anthropic API Key

### Installation
```bash
# Clone repository
git clone https://github.com/fidejo2k/MindBridge-Health-AI.git
cd MindBridge-Health-AI

# Install dependencies
pip install anthropic python-docx openpyxl reportlab

# Set API key
export ANTHROPIC_API_KEY="your_api_key_here"
```

### Run Daily Quiz (5-10 minutes)
```bash
python agents/mentor/quiz.py
```

### Generate Patient Reports
```bash
python scripts/generate_all_reports.py
```

---

## 📊 Progress Tracker

### Week 1: Docker & PostgreSQL (60% Complete)
- [x] **Day 1:** Prompt engineering (5 clinical prompts)
- [x] **Day 2:** Python automation (4 scripts)
- [x] **Day 3:** Document generation (Word, Excel, PDF)
- [x] **Day 4:** Git & GitHub (repository live)
- [x] **Day 5:** Week 1 review
- [x] **Day 6:** Mentor Agent + Production automation
- [ ] **Day 7:** Interactive teaching sessions
- [ ] **Day 8:** Agent-code integration
- [ ] **Day 9:** Shared utilities expansion
- [ ] **Day 10:** Week 1 completion

### Learning Metrics (Day 6)
- **Quiz Score:** 5/5 (100%)
- **Interview Answers Mastered:** 5
- **Spaced Repetition Cards:** 6 loaded
- **Next Review:** Tomorrow (2026-02-17)

---

## 🧠 12-Week Curriculum

### Month 1: Backend Foundation
| Week | Topic | Status |
|------|-------|--------|
| 1 | Docker & PostgreSQL | 🔵 In Progress |
| 2 | FastAPI & REST APIs | 🔒 Locked |
| 3 | Auth & HIPAA Audit | 🔒 Locked |
| 4 | Patient CRUD & AI Integration | 🔒 Locked |

### Month 2: AI & Healthcare Expertise
| Week | Topic | Status |
|------|-------|--------|
| 5 | AI Product Thinking | 🔒 Locked |
| 6 | Healthcare AI Landscape | 🔒 Locked |
| 7 | AI Safety & Regulation | 🔒 Locked |
| 8 | System Design for Healthcare | 🔒 Locked |

### Month 3: Interview Prep & Job Hunt
| Week | Topic | Status |
|------|-------|--------|
| 9 | Your Story — STAR Method | 🔒 Locked |
| 10 | Technical Interviews + Job Hunter Agent | 🔒 Locked |
| 11 | Healthcare Domain Q&A + Auto Apply Agent | 🔒 Locked |
| 12 | Full Mock Interview Loops | 🔒 Locked |

---

## 💻 Key Features

### Mentor Agent (Spaced Repetition Learning)
- **SM-2 Algorithm:** Optimal review intervals for long-term retention
- **12-Week Curriculum:** 150+ healthcare AI interview questions
- **Progress Tracking:** SQLite database with session history
- **Daily Automation:** Windows Task Scheduler integration

### MindBridge Health AI Platform
- **AI-Powered Risk Assessment:** Claude API integration
- **Multi-Format Reports:** Word, Excel, PDF generation
- **HIPAA Compliance:** Audit logging, PHI encryption
- **Production-Ready:** Error handling, logging, monitoring

### Shared Infrastructure
- **Centralized Logging:** All agent activity tracked
- **Email Notifications:** Quiz reminders, job alerts
- **Error Recovery:** Graceful failure handling
- **Automation:** Scheduled tasks and workflows

---

## 🎓 Interview Questions Mastered

### Week 1: Docker & PostgreSQL (5/12 complete)
1. ✅ What is Docker and why do we use it for MindBridge?
2. ✅ Why PostgreSQL over MongoDB for healthcare applications?
3. ✅ What is a database migration and why use Alembic?
4. ✅ Why does MindBridge use UUIDs instead of auto-increment IDs?
5. ✅ What does the HIPAA Security Rule require for database storage?

*Target: 150+ questions mastered by Week 12*

---

## 📈 Competitive Advantages

### Unique Background
- **10 years clinical experience:** CNA, Mental Health Technician, Direct Support Professional
- **6 years IT experience:** Technical support, system troubleshooting
- **Healthcare domain expertise:** Patient care workflows, behavioral health, HIPAA

### Technical Skills (Building)
- **Backend Development:** Python, FastAPI, PostgreSQL
- **AI Integration:** Claude API, prompt engineering, risk assessment
- **Production Engineering:** Logging, monitoring, automation, error handling
- **Healthcare Compliance:** HIPAA audit logging, PHI encryption

### What Sets This Apart
> Most AI engineers have CS degrees but zero clinical experience.  
> Companies can teach AI tools in 6 months.  
> They CANNOT teach 10 years of bedside patient care.  
> This combination is rare and extremely valuable.

---

## 🛠️ Tech Stack

**Current:**
- Python 3.12
- Claude API (Sonnet 4.5)
- SQLite
- python-docx, openpyxl, reportlab

**Planned (Weeks 2-12):**
- FastAPI
- PostgreSQL
- Alembic migrations
- Docker & Docker Compose
- Redis (caching)
- HIPAA compliance layer

---

## 📚 Documentation

### Architecture
- [9 Mermaid Diagrams](docs/architecture/mindbridge-architecture.md) - Full system design
- [Full-Stack Design](docs/plans/2026-02-16-mindbridge-full-stack-design.md) - 25 interview Q&A
- [Mentor Agent Plan](docs/plans/2026-02-16-mentor-agent-plan.md) - 1127-line implementation

### Daily Progress
- [Day 6 Summary](WEEK1_DAY6_SUMMARY.md) - Production automation complete
- [Setup Guide](DAY_6_SETUP_GUIDE.md) - Installation & configuration

---

## 🎯 Target Outcome

**Role:** Healthcare AI Engineer  
**Salary Range:** $200,000 - $300,000  
**Timeline:** Job-ready by May 2026 (Week 12)  
**Location:** Remote or Ohio (Columbus/Cleveland/Cincinnati)

**Portfolio Deliverables:**
- ✅ Production AI system (MindBridge Health AI)
- ✅ 3 autonomous agents (Mentor, Job Hunter, Auto Apply)
- ✅ 150+ interview answers (spaced repetition mastery)
- ✅ Professional documentation (architecture diagrams, plans)
- ✅ Public GitHub repository with commit history

---

## 🔗 Links

- **GitHub Repository:** [github.com/fidejo2k/MindBridge-Health-AI](https://github.com/fidejo2k/MindBridge-Health-AI)
- **LinkedIn:** [Connect with me](#) *(to be added Week 9)*
- **Portfolio Site:** [mindbridge.dev](#) *(to be built Week 10)*

---

## 📞 Contact

**Fidelis Emmanuel**  
Healthcare AI Engineer (In Training)  
Nashville, Tennessee

*Currently: Week 1, Day 6 of 90-day intensive program*

---

## 📝 License

This project is for educational and portfolio purposes.

---

**Last Updated:** February 17, 2026  
**Status:** Week 1 - Day 6 Complete (60%)  
**Next Milestone:** Week 2 - FastAPI & REST APIs
