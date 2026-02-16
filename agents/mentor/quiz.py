#!/usr/bin/env python3
"""MindBridge Mentor - Quiz yourself with spaced repetition"""
import sqlite3
import os
from datetime import date, timedelta

# Database path relative to this script
DB_PATH = os.path.join(os.path.dirname(__file__), "mentor.db")


def get_conn():
    """Get database connection."""
    if not os.path.exists(DB_PATH):
        print(f"❌ Error: Database not found at {DB_PATH}")
        print("Please run 'mentor init' first to initialize the database.")
        exit(1)
    return sqlite3.connect(DB_PATH)


def get_due_cards(limit=5):
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
        {
            "id": r[0],
            "topic": r[1],
            "question": r[2],
            "ideal_answer": r[3],
            "times_reviewed": r[4],
            "times_correct": r[5],
        }
        for r in c.fetchall()
    ]
    conn.close()
    return cards


def quiz_session():
    """Run an interactive quiz session."""
    cards = get_due_cards(limit=5)
    
    if not cards:
        print("\n" + "=" * 70)
        print("🎉 NO CARDS DUE TODAY - YOU'RE ALL CAUGHT UP!")
        print("=" * 70)
        print("\n📅 Come back tomorrow for more review.")
        print("💡 Spaced repetition works best when you review daily!\n")
        return
    
    print("\n" + "=" * 70)
    print("📚 MINDBRIDGE MENTOR - Quiz Session")
    print("=" * 70)
    print(f"\n🎯 {len(cards)} flashcards due for review today")
    print("💡 Rate each answer honestly - this optimizes your learning schedule\n")
    print("=" * 70)
    
    score = 0
    results = []
    
    for i, card in enumerate(cards, 1):
        print(f"\n╔═══ Question {i} of {len(cards)} " + "═" * 50)
        print(f"║ 📖 Topic: {card['topic']}")
        print(f"║ 📊 History: Reviewed {card['times_reviewed']} times, Correct {card['times_correct']} times")
        print("╠" + "═" * 68)
        print(f"║")
        print(f"║ ❓ {card['question']}")
        print(f"║")
        print("╚" + "═" * 68)
        print()
        
        input("💭 Think about your answer... Press ENTER when ready to see the ideal answer ▶")
        
        print("\n" + "─" * 70)
        print("✅ IDEAL ANSWER:")
        print("─" * 70)
        print(f"{card['ideal_answer']}")
        print("─" * 70 + "\n")
        
        while True:
            print("Rate your knowledge:")
            print("  1 = ❌ Completely forgot / No idea")
            print("  2 = 😓 Struggled / Partial recall")
            print("  3 = ✓  Got it / Good recall")
            print("  4 = ⭐ Perfect / Immediate recall")
            
            rating = input("\nYour rating (1-4): ").strip()
            if rating in ['1', '2', '3', '4']:
                rating = int(rating)
                break
            print("❌ Please enter 1, 2, 3, or 4\n")
        
        if rating >= 3:
            score += 1
            result_icon = "✓"
            result_text = "Correct!"
        else:
            result_icon = "✗"
            result_text = "Review this one!"
        
        print(f"\n{result_icon} {result_text}")
        results.append((card['question'][:50], rating, result_icon))
        
        # Update the card's spaced repetition schedule
        next_review_info = update_card_schedule(card['id'], rating)
        
        if next_review_info:
            if rating >= 3:
                print(f"📅 Next review: {next_review_info['next_review']} ({next_review_info['interval_days']} days)")
            else:
                print(f"📅 Next review: Tomorrow (needs more practice)")
        
        if i < len(cards):
            print("\n" + "=" * 70)
    
    # Session summary
    print("\n" + "=" * 70)
    print("📊 SESSION COMPLETE!")
    print("=" * 70)
    print(f"\n🎯 Score: {score}/{len(cards)} ({score/len(cards)*100:.0f}%)")
    
    if score == len(cards):
        print("🏆 PERFECT SCORE! You're crushing it!")
        print("💪 Your spaced repetition intervals have been extended.")
    elif score >= len(cards) * 0.7:
        print("⭐ GREAT WORK! Keep up the momentum!")
        print("📈 Most cards will come back in a few days.")
    else:
        print("💪 KEEP PRACTICING! These concepts need more review.")
        print("📅 Cards you struggled with will come back tomorrow.")
    
    print("\n📋 Session Breakdown:")
    for q, rating, icon in results:
        rating_label = ["", "Forgot", "Struggled", "Good", "Perfect"][rating]
        print(f"  {icon} {q}... → {rating_label}")
    
    print("\n" + "=" * 70 + "\n")


def update_card_schedule(card_id, quality):
    """Update card using simplified SM-2 spaced repetition algorithm."""
    conn = get_conn()
    c = conn.cursor()
    
    # Get current card state
    c.execute(
        "SELECT interval_days, repetitions FROM flashcards WHERE id = ?",
        (card_id,),
    )
    row = c.fetchone()
    if not row:
        conn.close()
        return None
    
    interval, reps = row
    
    # Simplified SM-2 algorithm
    if quality <= 2:
        # Forgot or struggled - reset interval but keep some progress
        interval = 1
        reps = 0
    else:
        # Good or perfect - increase interval
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 3
        elif reps == 2:
            interval = 7
        else:
            interval = int(interval * 2)  # Double the interval
        reps += 1
    
    next_review = (date.today() + timedelta(days=interval)).isoformat()
    correct = 1 if quality >= 3 else 0
    
    c.execute(
        "UPDATE flashcards SET interval_days = ?, repetitions = ?, "
        "next_review = ?, times_reviewed = times_reviewed + 1, "
        "times_correct = times_correct + ? WHERE id = ?",
        (interval, reps, next_review, correct, card_id),
    )
    
    conn.commit()
    conn.close()
    
    return {"next_review": next_review, "interval_days": interval}


def show_progress():
    """Show learning progress dashboard."""
    conn = get_conn()
    c = conn.cursor()
    
    # Get curriculum progress
    c.execute(
        "SELECT week, topic, phase, status FROM curriculum_progress ORDER BY week"
    )
    curriculum = c.fetchall()
    
    # Get flashcard stats
    c.execute("SELECT COUNT(*) FROM flashcards WHERE times_reviewed > 0")
    reviewed_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM flashcards")
    total_cards = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM flashcards WHERE times_reviewed > 0 AND times_correct >= times_reviewed * 0.8")
    mastered_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM flashcards WHERE next_review <= date('now')")
    due_today = c.fetchone()[0]
    
    # Get recent session stats
    c.execute("SELECT COUNT(*), AVG(score) FROM learning_sessions WHERE session_date >= date('now', '-7 days')")
    recent_sessions, avg_score = c.fetchone()
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("📊 MINDBRIDGE MENTOR - Learning Progress Dashboard")
    print("=" * 70)
    
    print(f"\n📚 Flashcard Statistics:")
    print(f"   Total cards: {total_cards}")
    print(f"   Reviewed: {reviewed_count}/{total_cards} ({reviewed_count/total_cards*100:.0f}%)")
    print(f"   Mastered (≥80% accuracy): {mastered_count}")
    print(f"   Due today: {due_today}")
    
    if recent_sessions and avg_score:
        print(f"\n📈 Last 7 Days:")
        print(f"   Sessions completed: {recent_sessions}")
        print(f"   Average score: {avg_score:.1f}%")
    
    print(f"\n🎯 12-Week Healthcare AI Engineer Curriculum:")
    print()
    
    current_phase = None
    for week, topic, phase, status in curriculum:
        # Print phase header when it changes
        if phase != current_phase:
            current_phase = phase
            phase_name = {
                "foundation": "MONTH 1: FOUNDATION (Build Backend)",
                "expertise": "MONTH 2: EXPERTISE (AI & Healthcare)",
                "interview": "MONTH 3: INTERVIEW PREP (Get Hired)"
            }.get(phase, phase.upper())
            print(f"\n  ┌─ {phase_name}")
            print(f"  │")
        
        status_icon = {
            "available": "🟢",
            "in_progress": "🔵", 
            "completed": "✅",
            "locked": "🔒"
        }.get(status, "◯")
        
        status_label = status.upper().replace("_", " ")
        print(f"  │ {status_icon} Week {week:2d}: {topic:42s} [{status_label}]")
    
    print("\n" + "=" * 70)
    
    if due_today > 0:
        print(f"💡 You have {due_today} cards due today! Run 'mentor quiz' to review.")
    else:
        print("🎉 No cards due today! Great job staying on top of reviews!")
    
    print("=" * 70 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "progress":
        show_progress()
    else:
        quiz_session()
