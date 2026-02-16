# MindBridge Mentor - Day 6 Completion Guide
# Production Automation Setup

## 🎯 What We're Building Today

Transform your manual quiz into a fully automated learning system:

1. ✅ Shared logging (track all activity)
2. ✅ Email notifications (daily reminders)
3. ✅ Windows Task Scheduler (automatic 8 AM quiz)
4. ✅ Error handling (never lose progress)

## 📁 Files to Download & Install

### Shared Utilities (agents/shared/)
- `logger.py` → `E:\Mindbridge health care\agents\shared\logger.py`
- `email_notifier.py` → `E:\Mindbridge health care\agents\shared\email_notifier.py`

### Automation Scripts (root/)
- `setup_daily_quiz.ps1` → `E:\Mindbridge health care\setup_daily_quiz.ps1`

## 🚀 Installation Steps

### Step 1: Create Shared Folder
```powershell
cd "E:\Mindbridge health care"
mkdir agents\shared
```

### Step 2: Download Files
Download the 3 files above and place them in:
- `agents\shared\logger.py`
- `agents\shared\email_notifier.py`
- `setup_daily_quiz.ps1` (root folder)

### Step 3: Test Logging
```powershell
python agents\shared\logger.py
```

Expected output:
```
Testing MindBridge Shared Logger...
Logs directory: E:\Mindbridge health care\logs

2026-02-17 09:00:00 | mentor | INFO | Mentor agent initialized
2026-02-17 09:00:00 | mentor | INFO | QUIZ | score=5/5 | duration_minutes=8 ...

✅ Logs written to: E:\Mindbridge health care\logs
   Check: E:\Mindbridge health care\logs\mentor.log
```

### Step 4: Test Email Notifier
```powershell
python agents\shared\email_notifier.py
```

Expected output (without EMAIL_PASSWORD set):
```
⚠️  EMAIL_PASSWORD environment variable not set
   Skipping email notification (would have sent):
   To: your.email@example.com
   Subject: 🎯 MindBridge Mentor - 5 Cards Due Today
   ...
```

### Step 5: Setup Daily Quiz (Optional - Advanced)
```powershell
# Run PowerShell as Administrator
# Then run:
.\setup_daily_quiz.ps1
```

This creates a Windows Task that runs your quiz at 8 AM daily!

## 📧 Email Configuration (Optional)

To enable real email notifications:

### For Gmail:
1. Go to: https://myaccount.google.com/apppasswords
2. Create app password for "MindBridge Agents"
3. Set environment variable:
   ```powershell
   $env:EMAIL_PASSWORD = "your-16-char-app-password"
   ```
4. Edit `email_notifier.py`:
   - Change `DEFAULT_TO_EMAIL` to your email
   - Change `DEFAULT_FROM_EMAIL` to your Gmail

### For Other Email:
Update in `email_notifier.py`:
- `SMTP_SERVER` (e.g., smtp.outlook.com)
- `SMTP_PORT` (usually 587)

## 📊 Daily Workflow (After Setup)

### Manual (Current):
```powershell
python agents\mentor\quiz.py
```

### Automated (After Task Scheduler):
- Quiz automatically pops up at 8 AM
- Email reminder if you have cards due
- All activity logged to `logs/mentor.log`

## 🎯 Success Criteria - Day 6 Complete

✅ Shared logging working (check logs/mentor.log)
✅ Email notifier configured (tested)
✅ Task scheduler setup (optional)
✅ Quiz runs automatically (or manually daily)

## 📅 Tomorrow (Day 7): Add /teach Command

We'll add interactive teaching sessions to complement the quiz!

## 💡 Quick Reference

View logs:
```powershell
Get-Content logs\mentor.log -Tail 20
```

Check scheduled task:
```powershell
Get-ScheduledTask -TaskName "MindBridge-Mentor-Daily-Quiz"
```

Test task manually:
```powershell
Start-ScheduledTask -TaskName "MindBridge-Mentor-Daily-Quiz"
```

## 🏆 You're Building Production Systems

Most developers don't:
- Set up logging
- Configure email alerts  
- Automate daily workflows
- Track every session

You're doing all of this. This is senior-level engineering.

This is WHY you'll get that $250K-$300K job! 🚀
