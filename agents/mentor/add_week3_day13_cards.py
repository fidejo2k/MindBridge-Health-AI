import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "mentor.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cards = [
    (
        "What is NextAuth.js and what problem does it solve?",
        "NextAuth.js is an authentication library for Next.js that handles sessions, JWT tokens, OAuth providers, and credential-based login. It solves the problem of building secure authentication from scratch — instead of writing JWT signing, session management, and CSRF protection yourself, NextAuth handles it all. One install, three files, and authentication is production-ready.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is Next.js middleware and how does MindBridge use it?",
        "Middleware runs before every request reaches a page. In Next.js, middleware.ts at the project root intercepts requests matching the config matcher. MindBridge uses withAuth middleware to protect /dashboard/:path* and /patients/:path* — any unauthenticated request to these routes is automatically redirected to the login page. No code changes needed in the page components themselves.",
        "CON", 0, 2.5, 1
    ),
    (
        "Why does MindBridge set JWT session maxAge to 8 hours?",
        "8 hours aligns with a standard clinical shift length. HIPAA requires automatic session termination after inactivity to prevent unauthorized access if a clinician leaves their workstation. After 8 hours, the JWT expires and the case manager must re-authenticate. This is a HIPAA administrative safeguard baked into the architecture, not added as an afterthought.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is the difference between redirect: true and redirect: false in NextAuth signIn?",
        "redirect: true (default) causes NextAuth to handle the redirect server-side after login — you lose control of what happens next. redirect: false returns a result object so you can handle success and failure yourself. MindBridge uses redirect: false to check result.ok — if true, manually push to /dashboard. If false, show an error message to the user. This gives better UX control.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is NEXTAUTH_SECRET and why is it required?",
        "NEXTAUTH_SECRET is a random string used to sign and encrypt JWT tokens. Without it, NextAuth cannot securely sign session tokens — anyone could forge a valid session. Generate it with: node -e \"console.log(require('crypto').randomBytes(32).toString('hex'))\". Store it in .env.local locally and in Vercel's environment variables for production. Never commit it to git.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is NEXTAUTH_URL and when does it matter?",
        "NEXTAUTH_URL tells NextAuth the base URL of your application so it can construct correct callback and redirect URLs. In development: http://localhost:3000. In production: https://mind-bridge-health-ai.vercel.app. Without it in production, OAuth callbacks and redirects break because NextAuth doesn't know the correct domain. Must be set in Vercel environment variables before deploying.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is a CredentialsProvider in NextAuth and what are its limitations?",
        "CredentialsProvider allows username/password authentication in NextAuth. The authorize() function receives the submitted credentials and returns a user object (authenticated) or null (rejected). Limitation: NextAuth disables JWT rotation for credentials providers by default — sessions don't refresh automatically. For production MindBridge, the authorize() function should query PostgreSQL and use bcrypt.verify() to check the password hash instead of hardcoded demo credentials.",
        "CON", 0, 2.5, 1
    ),
    (
        "How does Next.js middleware protect routes without modifying page components?",
        "Middleware intercepts requests at the edge BEFORE they reach page components. The matcher config specifies which routes to protect. When withAuth runs, it checks for a valid NextAuth session token in the request cookie. If the token is missing or expired, the request is redirected to the signIn page immediately — the dashboard page component never even executes. This is defense in depth: route protection is separate from page logic.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is the difference between getServerSession and useSession in NextAuth?",
        "getServerSession runs on the server — use it in Server Components and API routes to get the current session without an API call. useSession runs on the client — use it in Client Components to reactively update the UI when session state changes (e.g., show user name in header). MindBridge dashboard uses getServerSession because it's a Server Component. A hypothetical user menu component would use useSession because it needs client-side reactivity.",
        "CON", 0, 2.5, 1
    ),
    (
        "INTERVIEW: How did you implement authentication in MindBridge?",
        "I used NextAuth.js with a CredentialsProvider. Three components: (1) app/api/auth/[...nextauth]/route.ts — the auth handler that validates credentials and issues JWT tokens with 8-hour expiry aligned to clinical shift length. (2) middleware.ts — protects /dashboard and /patients/* routes at the edge, redirecting unauthenticated users to login automatically. (3) Updated login page to call signIn() from next-auth/react with redirect: false for controlled error handling. HIPAA alignment: 8-hour session expiry, audit logging on every login, httpOnly cookies prevent XSS token theft.",
        "INT", 0, 2.5, 1
    ),
    (
        "What is an httpOnly cookie and why does NextAuth use it?",
        "An httpOnly cookie cannot be read by JavaScript — only the browser sends it automatically with requests. NextAuth stores JWT session tokens in httpOnly cookies to prevent XSS attacks. If an attacker injects malicious JavaScript into a page, they cannot steal the session token because document.cookie doesn't expose httpOnly cookies. This is critical for healthcare apps where session hijacking could mean unauthorized access to patient records.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is the [...nextauth] catch-all route and what does it handle?",
        "The [...nextauth] bracket notation creates a catch-all API route that matches any path segment. This single file handles all NextAuth endpoints automatically: POST /api/auth/signin (login), GET /api/auth/session (get current session), POST /api/auth/signout (logout), GET /api/auth/csrf (CSRF token), and OAuth callbacks. Without this file, none of the NextAuth functionality works. The three dots mean 'match zero or more path segments'.",
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

print(f"✅ Day 13 cards loaded: {inserted} inserted, {skipped} skipped")
print(f"🔐 Topics: NextAuth.js, middleware, JWT sessions, HIPAA auth, httpOnly cookies")
print(f"🎯 Run: python quiz.py")