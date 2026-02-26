import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "mentor.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cards = [
    (
        "What is asyncpg and why did MindBridge choose it over psycopg2?",
        "asyncpg is a fully async PostgreSQL driver for Python. psycopg2 is synchronous — it blocks the entire thread while waiting for a database response. In FastAPI, which is async by design, a blocking database call prevents handling other requests. asyncpg uses Python's asyncio event loop so FastAPI can handle hundreds of concurrent requests while waiting for database responses. MindBridge switched from psycopg2-binary to asyncpg specifically for this non-blocking behavior.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is a connection pool and how does MindBridge configure it with asyncpg?",
        "A connection pool maintains a set of persistent database connections ready to use, instead of opening/closing a new connection on every request. Opening a connection takes ~100ms — a pool eliminates this overhead. MindBridge configures asyncpg with: create_pool(DATABASE_URL, min_size=2, max_size=10, ssl='require'). min_size=2 keeps 2 connections always open. max_size=10 allows bursting to 10 under load. ssl='require' because Railway PostgreSQL requires SSL. Use async with db_pool.acquire() as conn: to borrow a connection from the pool.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is the FastAPI lifespan context manager and why does MindBridge use it?",
        "The lifespan context manager runs code at application startup and shutdown. MindBridge uses it to create the asyncpg connection pool when FastAPI starts and close it cleanly when FastAPI stops. This ensures the pool exists before any request handlers run. The pattern: @asynccontextmanager async def lifespan(app): [startup code] yield [shutdown code]. Pass it to FastAPI(lifespan=lifespan). Without lifespan, you'd create the pool globally which can cause issues with async initialization.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is Railway's DATABASE_PUBLIC_URL vs DATABASE_URL and when do you use each?",
        "Railway automatically generates two connection URLs for PostgreSQL services: DATABASE_URL uses the internal Railway network (postgres.railway.internal) — only works service-to-service within Railway, not from external services. DATABASE_PUBLIC_URL uses the public proxy (switchback.proxy.rlwy.net) — works from anywhere including Vercel, local dev, and external services. MindBridge FastAPI service uses DATABASE_PUBLIC_URL renamed to DATABASE_URL because even though both services are on Railway, the environment variable injection required the public URL. Key lesson: when in doubt, use the public URL.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is a Railway healthcheck and how did MindBridge configure it?",
        "A Railway healthcheck is an HTTP request Railway makes to verify your service is running after deployment. If the healthcheck fails, Railway marks the deployment as failed and can roll back. MindBridge configures it in railway.toml: healthcheckPath = '/health' and healthcheckTimeout = 30. The /health endpoint must return a 200 status code. Critical lesson: the /health endpoint must work even if the database is unavailable — otherwise database connection failures cause deployment failures even though the app code is correct.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is Nixpacks and how does Railway use it to deploy Python apps?",
        "Nixpacks is Railway's build system that automatically detects your language and framework without a Dockerfile. For Python it: detects requirements.txt, creates a virtual environment, runs pip install -r requirements.txt, detects FastAPI and sets start command to uvicorn app.main:app --host 0.0.0.0 --port $PORT. Railway injects $PORT automatically. You can override the start command in Settings → Deploy → Start Command. MindBridge needed this override because Nixpacks didn't detect the app correctly from the backend subdirectory initially.",
        "CON", 0, 2.5, 1
    ),
    (
        "Why does load_dotenv() cause problems in Railway deployments?",
        "load_dotenv() reads from a .env file on disk. In Railway, environment variables are injected directly into os.environ at container startup — there is no .env file. load_dotenv() is harmless if no .env file exists, but it can cause subtle issues if a stale .env file exists in the container or if it overwrites Railway-injected variables. Best practice: use load_dotenv() only in development (inside an if __name__ == '__main__' block or with override=False), and rely purely on os.environ.get() in production Railway deployments.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is CORS and how does MindBridge configure it for the Vercel-Railway connection?",
        "CORS (Cross-Origin Resource Sharing) is a browser security policy that blocks requests from one origin to another unless the server explicitly allows it. Vercel (mind-bridge-health-ai.vercel.app) calling Railway (mindbridge-health-ai-production.up.railway.app) is a cross-origin request. MindBridge configures FastAPI's CORSMiddleware with allow_origins=['http://localhost:3000', 'https://mind-bridge-health-ai.vercel.app']. Without this, browsers block all API calls from the frontend to the backend with a CORS error.",
        "CON", 0, 2.5, 1
    ),
    (
        "INTERVIEW: Walk me through your FastAPI deployment on Railway.",
        "I deployed a FastAPI backend to Railway with asyncpg for non-blocking database queries. Three key decisions: (1) asyncpg over psycopg2 — FastAPI is async, blocking DB calls kill performance. asyncpg uses asyncio so hundreds of requests can be in-flight simultaneously. (2) Connection pooling with min_size=2, max_size=10 — eliminates 100ms connection overhead on every request, handles traffic bursts. (3) Non-fatal database startup — wrapped pool creation in try/except so the app starts and /health returns 200 even if DB is temporarily unavailable. This prevented Railway healthcheck failures during database restarts. Biggest debugging lesson: Railway's DATABASE_PUBLIC_URL vs DATABASE_URL — internal URLs only work within Railway's network.",
        "INT", 0, 2.5, 1
    ),
    (
        "What does ssl='require' mean in asyncpg and why does Railway need it?",
        "ssl='require' tells asyncpg to use SSL/TLS encryption for all database connections and to fail if SSL is unavailable. Railway PostgreSQL requires SSL for all connections as a security requirement — unencrypted connections are rejected. Without ssl='require', asyncpg attempts an unencrypted connection and Railway drops it. This is a HIPAA-relevant configuration: SSL ensures patient data is encrypted in transit between the FastAPI service and the PostgreSQL database, satisfying §164.312(e)(2)(ii) encryption in transit requirements.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is the difference between a Railway service and a Railway project?",
        "A Railway project is the top-level container — celebrated-stillness is MindBridge's project. A service is a deployable unit within a project. MindBridge has two services: the PostgreSQL database service (managed by Railway) and the MindBridge-Health-AI service (deployed from GitHub). Services within the same project can communicate via private networking using internal URLs. Services can share environment variables via Shared Variables at the project level. Each service has its own deployments, logs, metrics, and environment variables.",
        "CON", 0, 2.5, 1
    ),
    (
        "What is the full MindBridge production architecture after Day 14?",
        "Browser → Vercel CDN (Next.js Server Components) → Railway FastAPI (asyncpg connection pool) → Railway PostgreSQL. Vercel serves the Next.js frontend globally via CDN. Currently the dashboard queries PostgreSQL directly via Server Components — the next step is to route through FastAPI instead. Railway FastAPI handles business logic, validation, and AI processing. Railway PostgreSQL stores all patient data. All connections use SSL. Sessions managed by NextAuth with 8-hour JWT expiry. No localhost dependencies anywhere in the stack.",
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

print(f"✅ Day 14 cards loaded: {inserted} inserted, {skipped} skipped")
print(f"🚀 Topics: asyncpg, connection pooling, Railway deployment, Nixpacks, CORS, healthchecks")
print(f"🎯 Run: python quiz.py")