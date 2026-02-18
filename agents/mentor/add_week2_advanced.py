#!/usr/bin/env python3
"""
Add 12 high-value Week 2 FastAPI cards for interview readiness.
Focus: Practical, job-critical knowledge.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "mentor.db")


def add_week2_advanced():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # High-value Week 2 cards - FastAPI deep dive
    week2_advanced = [
        (
            "FastAPI & REST APIs", 2,
            "What is dependency injection in FastAPI and why does MindBridge use it everywhere?",
            "Dependency injection provides shared resources to endpoints automatically without manual setup. In MindBridge: Depends(get_db) injects a database session - FastAPI creates it before the request, passes it to your function, and closes it after (even if an error occurs). Depends(get_current_user) validates the JWT and gives you the user object. Depends(require_role('admin')) blocks non-admins. Without DI, every endpoint would manually: open DB connection, validate token, check role, handle errors, close connection. That's 15+ lines of duplicated code per endpoint. DI means: one line, zero duplication, impossible to forget. Interview gold: 'FastAPI's DI is why our codebase has zero SQL connection leaks despite 40+ endpoints.'",
            "concept"
        ),
        (
            "FastAPI & REST APIs", 2,
            "What is Pydantic and how does it prevent bad data from reaching your database?",
            "Pydantic validates data at the API boundary using Python type hints. When a case manager submits patient data, Pydantic checks: medication_adherence must be float between 0.0-1.0 (not 5.0, not 'high', not null). appointments_missed must be int >= 0 (not -3, not 'five'). If validation fails, FastAPI returns 422 Unprocessable Entity BEFORE the data touches business logic or database. This is critical for MindBridge because garbage data in a risk assessment could flag the wrong patients for crisis intervention - a patient safety issue. Interview answer: 'Pydantic turned data validation from 50 lines of manual if-checks into 5 lines of type hints. Our database has zero schema violations in production because bad data never gets past the API layer.'",
            "concept"
        ),
        (
            "FastAPI & REST APIs", 2,
            "Explain async/await in FastAPI. Why can't you just make everything synchronous?",
            "Async allows the server to handle other requests while waiting for slow operations (database queries, API calls). If a Claude API call takes 3 seconds and you have 20 case managers hitting 'Screen Patient' simultaneously: SYNCHRONOUS: Server handles 1 request, blocks for 3 seconds, then the next request. Total time = 20 × 3 = 60 seconds. The 20th case manager waits a full minute. ASYNC: All 20 requests start immediately. While waiting for Claude's response, the server handles dashboard loads, patient searches, report downloads. Total time ≈ 3-4 seconds. The difference in a healthcare emergency is patient safety, not just performance. Interview gold: 'We chose FastAPI over Flask specifically for native async. When a high-risk patient needs immediate attention, async ensures the system stays responsive under load.'",
            "concept"
        ),
        (
            "FastAPI & REST APIs", 2,
            "What HTTP status codes does MindBridge return and when? Give specific examples.",
            "200 OK - successful GET/PUT. Example: GET /patients returns patient list. 201 Created - resource created. Example: POST /patients creates new patient. 400 Bad Request - malformed request. Example: POST /patients with missing required field. 401 Unauthorized - missing/invalid token. Example: API call without JWT Bearer token. 403 Forbidden - authenticated but wrong permissions. Example: case manager trying to access admin-only endpoint. 404 Not Found - resource doesn't exist. Example: GET /patients/nonexistent-uuid or patient belongs to different clinic. 422 Unprocessable Entity - data format correct but values invalid. Example: medication_adherence = 5.0 (must be 0.0-1.0). 500 Internal Server Error - unexpected failure. Example: database connection lost. Always logged to HIPAA audit trail. Interview answer: 'Proper status codes aren't just REST compliance - they help frontend developers debug without seeing backend code.'",
            "concept"
        ),
        (
            "FastAPI & REST APIs", 2,
            "What is CORS and why does it matter for MindBridge's architecture?",
            "CORS (Cross-Origin Resource Sharing) is a browser security feature that blocks requests between different domains. MindBridge needs CORS because: Frontend runs on app.mindbridge.com. Backend runs on api.mindbridge.com. Without CORS config, the browser blocks ALL frontend-to-backend calls - the app is completely broken. We configure: allow_origins=['https://app.mindbridge.com'], allow_credentials=True (for cookies/auth), allow_methods=['GET','POST','PUT','DELETE'], allow_headers=['Authorization','Content-Type']. In development: allow_origins=['http://localhost:3000']. CRITICAL: NEVER use allow_origins=['*'] in production for a healthcare app - that means ANY website can call your patient data API. Interview answer: 'CORS misconfiguration is a common HIPAA violation vector. We whitelist specific origins and review the list quarterly.'",
            "concept"
        ),
        (
            "FastAPI & REST APIs", 2,
            "SIMULATION: Your FastAPI endpoint suddenly returns 500 errors. Walk me through debugging it.",
            "STEP 1 - Check the logs immediately: tail -f logs/app.log or check CloudWatch/Railway logs. The 500 error will have a stack trace showing exactly where it failed. STEP 2 - Identify the error type: DatabaseError = connection pool exhausted or DB down. ClientError (Anthropic) = API key invalid or rate limit hit. ValidationError = data schema mismatch. AttributeError = code trying to access a field that's None. STEP 3 - Common MindBridge 500 causes and fixes: 'Connection pool exhausted' → Increase max_connections in SQLAlchemy pool (default 5 is too low). 'anthropic.APIError: Invalid API key' → Environment variable not set in production (worked in dev with .env, missing in Railway). 'NoneType has no attribute' → Database returned null, code didn't check before accessing. Fix: Add null check or use Pydantic Optional. STEP 4 - Reproduce locally: Copy the exact request from logs, replay in Postman/curl. Fix and deploy. Interview gold: 'Read the logs first. The stack trace tells you exactly what failed. Most 500 errors are fixed in under 10 minutes if you read the error message carefully.'",
            "simulation"
        ),
        (
            "FastAPI & REST APIs", 2,
            "What is middleware and what middleware does MindBridge use?",
            "Middleware runs on EVERY request before it reaches your endpoint functions. MindBridge uses four critical middleware layers: (1) CORS middleware - allows frontend to call backend across different domains. (2) Auth middleware - validates JWT token on every protected route, extracts user_id. (3) HIPAA audit middleware - logs every request with user_id, endpoint, timestamp, IP address to immutable audit_log table. This is what regulators check after a breach. (4) Rate limiting middleware - limits each IP to 100 requests/minute, prevents enumeration attacks where someone tries to discover all patient IDs. Middleware is the security perimeter - it catches authentication failures, rate limit abuse, and audit requirements BEFORE business logic runs. Interview answer: 'Middleware is where we enforce HIPAA compliance at the infrastructure level, not the application level. If there's a bug in endpoint code, the audit middleware still logs the access.'",
            "concept"
        ),
        (
            "FastAPI & REST APIs", 2,
            "Explain the difference between PUT and PATCH. When does MindBridge use each?",
            "PUT replaces the ENTIRE resource. PATCH updates only specific fields. Example: A case manager updates a patient's medication_adherence from 0.7 to 0.8. PUT /patients/{id} - sends complete patient object with ALL fields. If you forget a field, it gets set to null. Dangerous. PATCH /patients/{id} - sends ONLY {'medication_adherence': 0.8}. Other fields unchanged. Safe. MindBridge uses PATCH for partial updates because: (1) Safety - can't accidentally wipe fields you didn't intend to change. (2) Efficiency - less data over the network. (3) Better audit trail - HIPAA audit log shows exactly which field changed, not a full object replacement. (4) Clinical workflow - case managers update one metric at a time, not the entire patient record. Interview answer: 'We chose PATCH over PUT because a case manager updating medication adherence shouldn't have to resend diagnosis, treatment history, and 15 other fields just to change one number.'",
            "concept"
        ),
        (
            "FastAPI & REST APIs", 2,
            "How do you test a FastAPI endpoint? Show me the pattern.",
            "Use pytest with TestClient. Pattern: (1) Create a test database (SQLite in-memory for speed). (2) Create test data fixtures (known patient records). (3) Call endpoint via TestClient (simulates real HTTP request). (4) Assert response status and data. Example test for GET /patients: def test_get_patients(): client = TestClient(app); response = client.get('/api/patients', headers={'Authorization': 'Bearer test-token'}); assert response.status_code == 200; assert len(response.json()) > 0. Example test for POST /patients: def test_create_patient(): data = {'name': 'Test Patient', 'medication_adherence': 0.8}; response = client.post('/api/patients', json=data); assert response.status_code == 201; assert response.json()['name'] == 'Test Patient'. For MindBridge we also test: (1) Authentication - 401 if no token. (2) Authorization - 403 if wrong role. (3) RBAC - case manager can't see other clinic's patients. (4) HIPAA audit - every request logged. Interview answer: 'We have 95% test coverage on API endpoints. Every HIPAA control has at least one test - audit logging, RBAC, data encryption.'",
            "concept"
        ),
        (
            "FastAPI & REST APIs", 2,
            "SIMULATION: A case manager reports the API is 'slow'. How do you diagnose and fix it?",
            "STEP 1 - Define 'slow': Get specifics. Which endpoint? How slow (2 seconds? 30 seconds?)? Happens always or intermittently? STEP 2 - Check the obvious: Is Claude API down? (Check Anthropic status page). Is database connection pool exhausted? (Check logs for 'Timeout waiting for connection'). Is the network slow? (Check CloudWatch/Railway metrics). STEP 3 - Add timing logs: import time; start = time.time(); result = await db.query(...); print(f'Query took {time.time()-start}s'). This shows which part is slow - database? Claude API? Data processing? STEP 4 - Common MindBridge performance issues: N+1 queries - loading 50 patients then fetching each patient's screenings individually. Fix: Use JOIN or eager loading. Missing database index - querying patients WHERE clinic_id without an index scans entire table. Fix: CREATE INDEX idx_patients_clinic ON patients(clinic_id). Large response payloads - returning 10MB of data when frontend only needs 50KB. Fix: Use Pydantic response model to include only necessary fields. Synchronous blocking - Claude API call blocks all other requests. Already fixed with async. Interview gold: 'Performance issues are usually database queries. Add timing, find the slow query, add an index. 90% of the time that's the fix.'",
            "simulation"
        ),
        (
            "FastAPI & REST APIs", 2,
            "What is connection pooling and why is it critical for MindBridge?",
            "Connection pooling reuses database connections instead of opening a new one for every request. Opening a PostgreSQL connection takes 50-100ms. If 100 case managers hit the dashboard simultaneously, without pooling: 100 × 100ms = 10 seconds of connection overhead. The last user waits 10 seconds just to START their query. With pooling: SQLAlchemy maintains 10 open connections (configurable). Requests queue and reuse existing connections. Max wait time ≈ query execution time, not connection setup time. MindBridge configuration: engine = create_async_engine('postgresql://...', pool_size=10, max_overflow=20). This means: 10 persistent connections, can burst to 30 under heavy load. Pool exhaustion symptoms: 'Timeout waiting for connection from pool' errors, 500 errors during high traffic. Fix: Increase pool_size or find leaking connections (endpoints not closing DB sessions). Interview answer: 'Connection pooling is why MindBridge can handle 50 concurrent users on a single backend instance. Without it, we'd need 10× the server capacity.'",
            "concept"
        ),
        (
            "FastAPI & REST APIs", 2,
            "INTERVIEW SIMULATION: Explain how you'd architect a new feature - bulk patient import from CSV.",
            "ANSWER FRAMEWORK: Start with user workflow, then technical design. USER WORKFLOW: Case manager uploads CSV with 500 patients. System validates, imports, returns summary (450 imported, 50 errors with reasons). TECHNICAL DESIGN: (1) POST /patients/import endpoint accepts file upload. (2) Validate file: Check CSV format, required columns present. Return 400 if malformed. (3) Background processing: 500 patients is too slow for synchronous request (would timeout). Use Celery worker to process async. Return 202 Accepted immediately with task_id. (4) Row-level validation: For each row, Pydantic validates data types. Check for duplicates (same name + DOB). Log invalid rows, don't fail entire import. (5) Database transaction: Wrap insert in transaction. If DB fails mid-import, rollback everything (no partial imports). (6) HIPAA audit: Log who uploaded, when, how many patients, which file. (7) Result endpoint: GET /imports/{task_id} returns status (processing/completed), success count, error details. SECURITY CONSIDERATIONS: File size limit (10MB max - prevent DOS). Virus scan the file. RBAC - only admins can bulk import. Rate limit - 1 import per hour per user. Interview gold: 'I'd prototype with synchronous for 50 patients, then add Celery when we hit scale. Always validate MVP assumptions with real usage before building complex async systems.'",
            "simulation"
        ),
    ]

    added = 0
    for topic, week, question, answer, card_type in week2_advanced:
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
    c.execute("SELECT COUNT(*) FROM flashcards WHERE week = 2")
    week2_total = c.fetchone()[0]

    conn.close()

    print("=" * 70)
    print("✅ Week 2 Advanced Cards Added!")
    print("=" * 70)
    print(f"\n   Cards added: {added}")
    print(f"   Week 2 total: {week2_total}")
    print(f"   Total in deck: {total}")
    print(f"\n📚 New Topics Covered:")
    print(f"   💡 Dependency Injection (FastAPI's secret weapon)")
    print(f"   💡 Pydantic validation (data safety)")
    print(f"   💡 Async/await deep dive (why it matters)")
    print(f"   💡 HTTP status codes (professional APIs)")
    print(f"   💡 CORS (frontend-backend communication)")
    print(f"   💡 Middleware (security perimeter)")
    print(f"   💡 PUT vs PATCH (RESTful updates)")
    print(f"   💡 Testing FastAPI (pytest patterns)")
    print(f"   💡 Connection pooling (performance)")
    print(f"   🎭 Debug 500 errors (live troubleshooting)")
    print(f"   🎭 API performance issues (real diagnosis)")
    print(f"   🎤 Architect bulk CSV import (design thinking)")
    print(f"\n🎯 These are INTERVIEW-CRITICAL topics!")
    print("=" * 70)


if __name__ == "__main__":
    add_week2_advanced()