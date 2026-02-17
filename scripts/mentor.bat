@echo off
REM MindBridge Mentor Agent - Quick Command Interface
REM Location: E:\Mindbridge health care\mentor.bat
REM Database: E:\Mindbridge health care\agents\mentor\mentor.db

if "%1"=="" goto :help
if /i "%1"=="init" goto :init
if /i "%1"=="quiz" goto :quiz
if /i "%1"=="progress" goto :progress
if /i "%1"=="help" goto :help
goto :help

:init
echo.
echo ════════════════════════════════════════════════════════════════════
echo   MINDBRIDGE MENTOR - Initializing Database
echo ════════════════════════════════════════════════════════════════════
echo.
python agents\mentor\init_db.py
echo.
goto :end

:quiz
echo.
echo ════════════════════════════════════════════════════════════════════
echo   MINDBRIDGE MENTOR - Starting Quiz Session
echo ════════════════════════════════════════════════════════════════════
echo.
python agents\mentor\quiz.py
goto :end

:progress
echo.
echo ════════════════════════════════════════════════════════════════════
echo   MINDBRIDGE MENTOR - Loading Progress Dashboard
echo ════════════════════════════════════════════════════════════════════
echo.
python agents\mentor\quiz.py progress
goto :end

:help
echo.
echo ════════════════════════════════════════════════════════════════════
echo   MINDBRIDGE MENTOR AGENT - Command Line Interface
echo ════════════════════════════════════════════════════════════════════
echo.
echo   🎯 3-Month Healthcare AI Engineer Training Program
echo   📍 Database: agents\mentor\mentor.db
echo.
echo   COMMANDS:
echo   ─────────────────────────────────────────────────────────────────
echo   mentor init       Initialize database (run once at setup)
echo   mentor quiz       Start a quiz session (daily practice)
echo   mentor progress   View learning dashboard and curriculum
echo   mentor help       Show this help message
echo.
echo   EXAMPLES:
echo   ─────────────────────────────────────────────────────────────────
echo   mentor init       (First time setup - creates database)
echo   mentor quiz       (Daily quiz - 5 cards, 5-10 minutes)
echo   mentor progress   (Check your progress anytime)
echo.
echo   CURRICULUM:
echo   ─────────────────────────────────────────────────────────────────
echo   Month 1 (Weeks 1-4):  Backend Foundation
echo   Month 2 (Weeks 5-8):  AI & Healthcare Expertise
echo   Month 3 (Weeks 9-12): Interview Prep + Job Hunt
echo.
echo   TARGET ROLE: Healthcare AI Engineer ($200K-$300K)
echo   YOUR ADVANTAGE: 10 years clinical experience + AI skills
echo.
echo ════════════════════════════════════════════════════════════════════
echo.
goto :end

:end
