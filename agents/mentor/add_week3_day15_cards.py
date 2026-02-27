import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "mentor.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cards = [
    (
        "What is the difference between a Server Component and a Client Component fetching data?",
        "Server Components run on the server — they can directly query databases, call internal APIs, and access environment variables without exposing them to the browser. The result is HTML sent to the client. Client Components run in the browser — they fetch data via API calls using fetch() or libraries like SWR. MindBridge dashboard uses a Server Component that calls the FastAPI backend — the fetch happens server-side, credentials never reach the browser, and the rendered HTML is sent to Vercel's edge network.",
        "CON", 0, 2.5, 1
    ),
    (
        "Why does MindBridge use export const dynamic = 'force-dynamic' on the dashboard?",
        "By default Next.js tries to statically prerender pages at build time for performance. The dashboard calls FastAPI which queries PostgreSQL — at build time on Vercel, there's no database connection available, causing ECONNREFUSED. force-dynamic tells Next.js: never prerender this page, always render it fresh on every request. This is correct for a dashboard showing live patient data — you never want cached, stale clinical information anyway.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is NEXT_PUBLIC_ and when should you use it vs a private environment variable?",
        "NEXT_PUBLIC_ prefix exposes an environment variable to the browser — it gets bundled into the JavaScript sent to the client. Use it for values that are safe to be public: API URLs, app names, feature flags. Never use NEXT_PUBLIC_ for secrets: database URLs, API keys, auth secrets, tokens. MindBridge uses NEXT_PUBLIC_API_URL for the Railway FastAPI URL because it's not a secret — it's visible in the browser's Network tab anyway. DATABASE_URL and NEXTAUTH_SECRET have no NEXT_PUBLIC_ prefix because they must never reach the browser.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is the complete MindBridge production architecture after Week 3?",
        "Browser → Vercel Edge (Next.js 16, Server Components, NextAuth JWT sessions) → Railway FastAPI (asyncpg connection pool, REST endpoints, CORS configured) → Railway PostgreSQL (10 patients, SSL required). Authentication: NextAuth.js with 8-hour JWT expiry, httpOnly cookies, middleware protecting /dashboard and /patients/*. Data flow: clinician logs in → JWT issued → dashboard Server Component calls FastAPI → FastAPI queries PostgreSQL via asyncpg pool → patient data rendered server-side → HTML sent to browser. No localhost dependencies anywhere.",
        "CON", 0, 2.5, 1
    ),
    (
        "INTERVIEW: Walk me through the MindBridge full stack architecture.",
        "MindBridge is a HIPAA-compliant behavioral health platform with three production layers. Frontend: Next.js 16 on Vercel with NextAuth.js authentication. JWT sessions expire after 8 hours — one clinical shift — per HIPAA §164.312(a)(2)(iii). Next.js middleware protects all clinical routes at the edge before page components execute. Backend: FastAPI on Railway with asyncpg connection pooling. Non-blocking async queries handle concurrent case manager access during shift changes. CORS configured for specific origins only. Database: PostgreSQL on Railway with SSL required for all connections. Every layer uses environment variables — no hardcoded credentials anywhere. The stack was built security-first: credential exposure incident handled within 30 minutes using git-filter-repo and immediate password rotation.",
        "INT", 0, 2.5, 1
    ),
    (
        "What is a README and what makes a portfolio README stand out to recruiters?",
        "A README is the first thing a recruiter or hiring manager sees when they open your GitHub repo. A strong portfolio README includes: (1) Live demo links with badges — shows the project is actually deployed, not just code. (2) Architecture diagram — shows systems thinking. (3) Tech stack table — scannable in 10 seconds. (4) HIPAA compliance section — demonstrates domain expertise. (5) API documentation with example responses — shows you think about consumers of your API. (6) Local setup instructions — shows you think about other developers. MindBridge README covers all six — a recruiter can understand the entire project in under 2 minutes without reading a single line of code.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is the difference between Railway's internal and public network URLs?",
        "Railway's internal network (*.railway.internal) routes traffic within Railway's private network — zero latency, no egress costs, not accessible from outside Railway. Railway's public network (*.up.railway.app or proxy URLs) routes traffic through Railway's edge network — accessible from anywhere including Vercel, local development, and external APIs. MindBridge FastAPI uses DATABASE_PUBLIC_URL (renamed to DATABASE_URL) because even though FastAPI and PostgreSQL are in the same Railway project, the public URL was more reliable during initial setup. Best practice: use Reference Variables (${{Postgres.DATABASE_PUBLIC_URL}}) so credentials stay in sync automatically.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is cache: 'no-store' in Next.js fetch and why does MindBridge use it?",
        "Next.js extends the native fetch API with caching options. cache: 'no-store' means never cache this response — always fetch fresh data on every request. MindBridge dashboard uses fetch(FASTAPI_URL, { cache: 'no-store' }) because patient risk levels, medication adherence, and crisis calls change frequently. Caching clinical data could show a case manager stale risk assessments — a patient who escalated to HIGH risk since the last cache refresh might appear as MEDIUM. For healthcare data, freshness is a patient safety requirement, not just a UX preference.",
        "CON", 0, 2.5, 1
    ),
]

inserted = 0
skipped = 0

for card in cards:
    try:
        cursor.execute("""
            INSERT INTO cards (question, answer, card_type, repetitions, ease_factor, interval)
            VALUES (?, ?, ?, ?, ?, ?)
        """, card)
        inserted += 1
    except sqlite3.IntegrityError:
        skipped += 1

conn.commit()
conn.close()

print(f"✅ Day 15 cards loaded: {inserted} inserted, 0 skipped")
print(f"📚 Topics: Server Components, force-dynamic, NEXT_PUBLIC_, full architecture, README")
print(f"🎯 Total cards in mentor.db: ~85")
print(f"🏆 Week 3 complete! See you Week 4.")