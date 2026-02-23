#!/usr/bin/env python3
"""
Add Week 3 Frontend & Deployment cards for interview readiness.
Focus: Next.js, Tailwind CSS, Vercel, CI/CD, React concepts.
Run daily as new content is covered.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "mentor.db")


def add_week3_cards():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    week3_cards = [
        (
            "Next.js & Frontend", 3,
            "What is the difference between a Server Component and Client Component in Next.js?",
            "Server Components (default) render on the server — no interactivity, no browser APIs, no useState/useEffect. Faster, SEO-friendly, can access database directly. Client Components use 'use client' directive at the top — handle clicks, form submissions, state, and browser APIs. MindBridge login page uses 'use client' because the Sign In button needs onClick/useRouter. The dashboard is a Server Component because it just displays data. Interview answer: 'I default to Server Components for performance and only add use client when I need interactivity. Most of MindBridge's pages are server-rendered for speed and SEO.'",
            "concept"
        ),
        (
            "Next.js & Frontend", 3,
            "What is the Next.js App Router and how does file-based routing work?",
            "App Router is Next.js 13+ routing system where the file system IS the router. Every folder inside /app becomes a URL segment. Every page.tsx file becomes a page. Examples: app/page.tsx → / (login). app/dashboard/page.tsx → /dashboard. app/patients/[id]/page.tsx → /patients/1, /patients/2, etc. Special files: page.tsx (UI), layout.tsx (shared wrapper), loading.tsx (loading state), error.tsx (error boundary). Interview answer: 'File-based routing eliminated 50 lines of React Router configuration. Adding a new page is just creating a folder and page.tsx — the URL exists automatically.'",
            "concept"
        ),
        (
            "Next.js & Frontend", 3,
            "What is dynamic routing in Next.js and how does MindBridge use it?",
            "Dynamic routes use bracket notation [param] in folder names to match variable URL segments. MindBridge: app/patients/[id]/page.tsx matches /patients/1, /patients/2, /patients/any-uuid. Next.js 15 breaking change: params is now a Promise. Correct pattern: export default async function PatientPage({ params }: { params: Promise<{ id: string }> }) { const { id } = await params }. Without async/await in Next.js 15, params returns undefined and you get a 404. Interview answer: 'I hit the Next.js 15 async params breaking change in production on Day 1. Fixed it in 2 minutes once I understood params is now a Promise — a real-world debugging experience I won't forget.'",
            "concept"
        ),
        (
            "Next.js & Frontend", 3,
            "What is Tailwind CSS and why did MindBridge choose it over regular CSS?",
            "Tailwind is a utility-first CSS framework. Instead of writing .button { background: blue; border-radius: 8px }, you apply classes directly in JSX: className='bg-blue-600 rounded-lg'. Key advantages for MindBridge: (1) Speed — no switching between files. (2) Consistency — predefined scale (blue-600, slate-900) prevents random color choices. (3) Responsive — md:grid-cols-2 applies only on medium screens. (4) No dead CSS — only classes you use get included in the build. Common classes used: bg-slate-900 (dark bg), text-white, rounded-xl (large border radius), shadow-sm, border, flex, grid, p-4/p-6 (padding), gap-4 (flexbox gap). Interview answer: 'Tailwind let me build a professional healthcare UI in one day without a designer. The constraint of predefined values actually produces more consistent results than freeform CSS.'",
            "concept"
        ),
        (
            "Next.js & Frontend", 3,
            "What is Vercel and why is it the natural deployment choice for Next.js?",
            "Vercel is the cloud platform created by the Next.js team. It has native Next.js support — zero configuration needed. Features: (1) Auto-detection: sees next.config.js and knows exactly how to build. (2) Edge Network: deploys to 100+ locations globally, low latency worldwide. (3) Preview deployments: every PR gets its own preview URL automatically. (4) CI/CD built-in: every git push to main triggers automatic rebuild and deployment. (5) Free tier: generous for portfolio projects. MindBridge deployment: Vercel reads from GitHub, builds frontend/patient-portal, serves at mind-bridge-health-ai.vercel.app. Interview answer: 'I chose Vercel because the Next.js team builds both products. Zero config, automatic HTTPS, global CDN, and CI/CD in one platform — it would take a week to replicate this on AWS.'",
            "concept"
        ),
        (
            "Next.js & Frontend", 3,
            "What is CI/CD and how does MindBridge implement it?",
            "CI/CD = Continuous Integration / Continuous Deployment. CI: every code push automatically runs tests and builds. CD: if build passes, automatically deploys to production. MindBridge CI/CD pipeline: (1) Developer runs git push to GitHub main branch. (2) GitHub webhook notifies Vercel instantly. (3) Vercel clones repo, runs npm run build. (4) If build succeeds: live site updates in ~60 seconds. If build fails: previous version stays live, developer gets email. This means: no manual deployments, no 'it works on my machine', every push is potentially live. Interview answer: 'CI/CD means I can fix a bug, push, and it's live in 60 seconds. More importantly, broken builds never reach production — the pipeline acts as a safety net. In healthcare, deploying broken code that affects patient care is unacceptable.'",
            "concept"
        ),
        (
            "Next.js & Frontend", 3,
            "What is the useRouter hook in Next.js and when do you use it?",
            "useRouter is a Next.js Client Component hook for programmatic navigation — redirecting users without them clicking a link. MindBridge login page: after form submit, router.push('/dashboard') sends the user to the dashboard. Pattern: 'use client'; import { useRouter } from 'next/navigation'; const router = useRouter(); function handleLogin(e) { e.preventDefault(); router.push('/dashboard'); }. Key methods: router.push('/path') — navigate forward (adds to history). router.replace('/path') — navigate without history entry (good for login redirects). router.back() — go back one page. Only works in Client Components. Server Components use the redirect() function instead. Interview answer: 'useRouter handles post-login redirects. After authentication, router.push sends users to their dashboard without exposing the navigation logic in the URL.'",
            "concept"
        ),
        (
            "Next.js & Frontend", 3,
            "What is the difference between Link and useRouter for navigation in Next.js?",
            "Link component: declarative navigation for clickable elements. Renders as an <a> tag, prefetches page on hover for instant navigation. Use for: nav menus, buttons, 'View patient' links. Example: <Link href='/dashboard'>Back to Dashboard</Link>. useRouter hook: programmatic navigation after an event. Use for: redirects after form submit, conditional navigation, navigate after API call completes. Example: after login validation passes, router.push('/dashboard'). MindBridge uses both: Link for 'Back to Dashboard' button and 'View →' patient links. useRouter in login page to redirect after form submit. Rule of thumb: if a user clicks something visible → Link. If code decides where to navigate → useRouter. Interview answer: 'Link handles user-initiated navigation with prefetching for performance. useRouter handles system-initiated navigation like post-authentication redirects.'",
            "concept"
        ),
        (
            "Next.js & Frontend", 3,
            "SIMULATION: An employer asks 'Walk me through the MindBridge frontend architecture.'",
            "STRONG ANSWER: 'MindBridge uses Next.js 14 with the App Router for the frontend, deployed on Vercel. The architecture has three pages: Login (app/page.tsx), Dashboard (app/dashboard/page.tsx), and Patient Detail (app/patients/[id]/page.tsx). I used dynamic routing with bracket notation for the patient detail view — [id] matches any patient UUID from the database. The login page is a Client Component using useRouter for post-submit redirect. The dashboard and patient detail are Server Components since they just display data. Styling is Tailwind CSS throughout — utility classes gave me a consistent design system without a dedicated designer. The frontend currently uses static data, with Railway PostgreSQL integration planned for next sprint. CI/CD is handled by Vercel — every git push to main deploys automatically in under 60 seconds. I can show you the live demo at mind-bridge-health-ai.vercel.app right now.' WHY THIS WORKS: Shows architecture thinking, explains tradeoffs (Server vs Client), mentions real technical decisions, and ends with live demo evidence.",
            "simulation"
        ),
        (
            "Next.js & Frontend", 3,
            "What is HIPAA PHI and why is the MindBridge demo banner clinically important?",
            "PHI (Protected Health Information) is any data that can identify a patient AND relates to their health condition, treatment, or payment. Examples: patient name + diagnosis, medical record number, date of birth + condition. MindBridge demo banner states all patient data is fictional — this matters because: (1) Legal protection — clearly distinguishes demo from production PHI. (2) Clinical awareness — shows understanding of when HIPAA applies vs doesn't. (3) Professional standard — all real healthcare platforms label demo/test environments. (4) Portfolio professionalism — employers see you understand compliance boundaries, not just code. The 10 MindBridge patients (Marcus Thompson, Sarah Chen, etc.) are completely fabricated — no real PHI exists. But displaying real-looking clinical data (PHQ-9 scores, medications, diagnoses) without the banner could mislead users. Interview answer: 'The demo banner is a one-line addition that demonstrates clinical judgment. Any healthcare engineer who deploys realistic-looking patient data without labeling it as synthetic has a compliance blind spot.'",
            "concept"
        ),
        (
            "Next.js & Frontend", 3,
            "What environment variables does MindBridge frontend need and how are they handled in Next.js?",
            "Next.js has two types of environment variables: Server-only (default): stored in .env.local, NEVER exposed to browser. Example: DATABASE_URL, ANTHROPIC_API_KEY, JWT_SECRET. Access: process.env.DATABASE_URL. Public (browser-accessible): must be prefixed with NEXT_PUBLIC_. Example: NEXT_PUBLIC_API_URL=https://api.mindbridge.com. Access: process.env.NEXT_PUBLIC_API_URL. MindBridge .env.local: NEXT_PUBLIC_API_URL=http://localhost:8000 (local FastAPI). Production (Vercel dashboard): NEXT_PUBLIC_API_URL=https://mindbridge-backend.railway.app. CRITICAL HIPAA rule: NEVER prefix sensitive keys with NEXT_PUBLIC_ — they get embedded in the JavaScript bundle and are visible to anyone who opens DevTools. DATABASE_URL with NEXT_PUBLIC_ = patient data URL exposed to the public. Interview answer: 'In a healthcare app, the NEXT_PUBLIC_ prefix decision is a security decision. I default to server-only variables and only make something public after explicitly confirming it contains no sensitive data.'",
            "concept"
        ),
        (
            "Next.js & Frontend", 3,
            "SIMULATION: Employer asks 'How would you add authentication to protect the MindBridge dashboard?'",
            "STRONG ANSWER: 'Currently the dashboard is publicly accessible for demo purposes. In production I'd add NextAuth.js for authentication. Implementation plan: (1) Install NextAuth: npm install next-auth. (2) Create app/api/auth/[...nextauth]/route.ts — handles all auth routes automatically. (3) Configure providers: CredentialsProvider for email/password against our FastAPI backend, or OAuth providers like Google for enterprise SSO. (4) Add middleware.ts at the project root — Next.js middleware runs before every request. Protect all routes under /dashboard and /patients: export { default } from next-auth/middleware; export const config = { matcher: [/dashboard/:path*, /patients/:path*] }. (5) Unauthenticated users get redirected to /login automatically. (6) Access session in components: const session = await getServerSession() — server-side, no API call needed. HIPAA considerations: JWT session tokens expire after 8 hours (clinical shift length). Refresh tokens rotated on every request. Failed login attempts logged to audit trail. Interview answer shows: knows the tool (NextAuth), knows the pattern (middleware), knows the HIPAA implications (session expiry, audit logging).'",
            "simulation"
        ),
    ]

    added = 0
    for topic, week, question, answer, card_type in week3_cards:
        c.execute("SELECT id FROM flashcards WHERE question = ?", (question,))
        if not c.fetchone():
            c.execute(
                "INSERT INTO flashcards (topic, week, question, ideal_answer) VALUES (?, ?, ?, ?)",
                (topic, week, question, answer),
            )
            added += 1

    conn.commit()

    # Show summary
    c.execute("SELECT COUNT(*) FROM flashcards")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM flashcards WHERE week = 3")
    week3_total = c.fetchone()[0]

    conn.close()

    print("=" * 70)
    print("✅ Week 3 Frontend & Deployment Cards Added!")
    print("=" * 70)
    print(f"\n   Cards added this run: {added}")
    print(f"   Week 3 total: {week3_total}")
    print(f"   Total in deck: {total}")
    print(f"\n📚 Topics Covered:")
    print(f"   💡 Server vs Client Components (Next.js core concept)")
    print(f"   💡 App Router & file-based routing")
    print(f"   💡 Dynamic routing + Next.js 15 async params fix")
    print(f"   💡 Tailwind CSS philosophy and common classes")
    print(f"   💡 Vercel deployment and edge network")
    print(f"   💡 CI/CD pipeline (GitHub → Vercel)")
    print(f"   💡 useRouter hook for programmatic navigation")
    print(f"   💡 Link vs useRouter — when to use each")
    print(f"   💡 Environment variables (NEXT_PUBLIC_ security)")
    print(f"   💡 HIPAA PHI and demo environment importance")
    print(f"   🎭 Walk through MindBridge frontend architecture")
    print(f"   🎭 Add authentication to protect dashboard")
    print(f"\n🎯 Run quiz.py tomorrow at 8 AM to start these cards!")
    print("=" * 70)


if __name__ == "__main__":
    add_week3_cards()
