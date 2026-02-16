"""
Shared email notification utility for all MindBridge agents.
Sends email alerts for quiz reminders, job alerts, and application confirmations.
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

# Email configuration (will be moved to environment variables later)
DEFAULT_FROM_EMAIL = "mindbridge.agent@gmail.com"  # Replace with your email
DEFAULT_TO_EMAIL = "your.email@example.com"  # Replace with your email


def send_email(subject, body, to_email=None, from_email=None):
    """
    Send an email notification.
    
    Args:
        subject: Email subject line
        body: Email body (plain text or HTML)
        to_email: Recipient email (defaults to DEFAULT_TO_EMAIL)
        from_email: Sender email (defaults to DEFAULT_FROM_EMAIL)
    
    Returns:
        bool: True if sent successfully, False otherwise
    
    Example:
        >>> send_email(
        ...     subject="Quiz Reminder - 5 Cards Due Today",
        ...     body="Good morning! You have 5 flashcards due for review."
        ... )
    
    Note:
        For production, configure environment variables:
        - EMAIL_USER: Your email address
        - EMAIL_PASSWORD: App-specific password (not your main password!)
        - SMTP_SERVER: smtp.gmail.com (for Gmail)
        - SMTP_PORT: 587
    """
    to_email = to_email or DEFAULT_TO_EMAIL
    from_email = from_email or DEFAULT_FROM_EMAIL
    
    # Get credentials from environment (safer than hardcoding)
    email_password = os.environ.get("EMAIL_PASSWORD")
    
    if not email_password:
        print("⚠️  EMAIL_PASSWORD environment variable not set")
        print("   Skipping email notification (would have sent):")
        print(f"   To: {to_email}")
        print(f"   Subject: {subject}")
        print(f"   Body preview: {body[:100]}...")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        
        # Add body
        part = MIMEText(body, 'html' if '<html>' in body.lower() else 'plain')
        msg.attach(part)
        
        # Send via SMTP
        smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, email_password)
            server.send_message(msg)
        
        print(f"✅ Email sent: {subject}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False


def send_quiz_reminder(cards_due_count):
    """
    Send a quiz reminder email.
    
    Args:
        cards_due_count: Number of flashcards due today
    """
    subject = f"🎯 MindBridge Mentor - {cards_due_count} Cards Due Today"
    
    body = f"""
Good morning!

Your daily quiz is ready:
- {cards_due_count} flashcards due for review
- Estimated time: {cards_due_count * 2} minutes
- Streak: Keep your learning momentum!

Run this command to start:
    mentor quiz

Remember: Consistent daily practice = Interview mastery

- MindBridge Mentor Agent
"""
    
    return send_email(subject, body)


def send_job_alert(jobs_found_count, top_jobs):
    """
    Send a job alert email (for Job Hunter agent).
    
    Args:
        jobs_found_count: Total number of new jobs found
        top_jobs: List of top job dictionaries with 'title', 'company', 'url'
    """
    subject = f"🔔 Job Alert - {jobs_found_count} New Healthcare AI Jobs"
    
    jobs_html = "\n".join([
        f"• {job['title']} at {job['company']}\n  {job['url']}"
        for job in top_jobs[:5]  # Top 5
    ])
    
    body = f"""
New Healthcare AI Engineer jobs found:

{jobs_html}

Run 'jobs review' to see all {jobs_found_count} opportunities.

- MindBridge Job Hunter Agent
"""
    
    return send_email(subject, body)


def send_application_confirmation(job_title, company, application_count_today):
    """
    Send application confirmation (for Auto Apply agent).
    
    Args:
        job_title: Job title applied to
        company: Company name
        application_count_today: Total applications sent today
    """
    subject = f"✅ Applied - {job_title} at {company}"
    
    body = f"""
Application submitted successfully!

Position: {job_title}
Company: {company}
Applications today: {application_count_today}

Your tailored resume and cover letter were sent.

- MindBridge Auto Apply Agent
"""
    
    return send_email(subject, body)


def send_weekly_summary(stats):
    """
    Send weekly progress summary (all agents).
    
    Args:
        stats: Dictionary with 'quiz_sessions', 'jobs_found', 'applications_sent'
    """
    subject = "📊 MindBridge Weekly Summary"
    
    body = f"""
Your progress this week:

📚 Learning (Mentor Agent):
   - Quiz sessions: {stats.get('quiz_sessions', 0)}
   - Cards mastered: {stats.get('cards_mastered', 0)}
   - Average score: {stats.get('avg_score', 0):.0f}%

💼 Job Hunt (Job Hunter Agent):
   - New jobs found: {stats.get('jobs_found', 0)}
   - Jobs saved: {stats.get('jobs_saved', 0)}

📤 Applications (Auto Apply Agent):
   - Applications sent: {stats.get('applications_sent', 0)}
   - Response rate: {stats.get('response_rate', 0):.0f}%

Keep up the great work! You're on track for that $250K-$300K role.

- MindBridge Agent System
"""
    
    return send_email(subject, body)


# Example usage and testing
if __name__ == "__main__":
    print("Testing MindBridge Email Notifier...")
    print()
    print("⚠️  Note: Email sending requires EMAIL_PASSWORD environment variable")
    print("   Without it, emails will be simulated (printed to console)")
    print()
    
    # Test quiz reminder
    print("Test 1: Quiz Reminder")
    send_quiz_reminder(cards_due_count=5)
    print()
    
    # Test job alert
    print("Test 2: Job Alert")
    sample_jobs = [
        {
            'title': 'Healthcare AI Engineer',
            'company': 'Epic Systems',
            'url': 'https://epic.com/jobs/12345'
        },
        {
            'title': 'AI Product Manager - Healthcare',
            'company': 'Google Health',
            'url': 'https://careers.google.com/jobs/56789'
        }
    ]
    send_job_alert(jobs_found_count=15, top_jobs=sample_jobs)
    print()
    
    # Test weekly summary
    print("Test 3: Weekly Summary")
    sample_stats = {
        'quiz_sessions': 7,
        'cards_mastered': 25,
        'avg_score': 92,
        'jobs_found': 45,
        'jobs_saved': 12,
        'applications_sent': 8,
        'response_rate': 25
    }
    send_weekly_summary(sample_stats)
    
    print("\n✅ Email notifier tests complete!")
    print("\nTo enable real emails:")
    print("1. Create app-specific password in Gmail")
    print("2. Set environment variable: set EMAIL_PASSWORD=your_app_password")
    print("3. Update DEFAULT_TO_EMAIL with your email address")
