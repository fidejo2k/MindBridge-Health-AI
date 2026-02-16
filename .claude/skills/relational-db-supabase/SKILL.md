---
name: relational-db-supabase
description: Relational database design and Supabase patterns for schema design, SQL queries, RLS policies, auth, real-time subscriptions, and migrations. Use when working with databases, Supabase, PostgreSQL, SQL queries, row-level security, or data modeling.
tools: Read, Glob, Grep, Bash, Write, Edit
---

# Relational Database & Supabase Patterns

Comprehensive guide for relational database design and Supabase-specific patterns including schema design, security, queries, and real-time features.

---

## 1. Relational Database Fundamentals

### Schema Design Principles

**Normalization rules (aim for 3NF):**
- 1NF: Atomic values, no repeating groups
- 2NF: No partial dependencies on composite keys
- 3NF: No transitive dependencies (non-key columns depend only on the key)

**Naming conventions:**
```sql
-- Tables: snake_case, plural nouns
CREATE TABLE patient_records (...);
CREATE TABLE appointment_slots (...);

-- Columns: snake_case
created_at TIMESTAMPTZ DEFAULT now()
updated_at TIMESTAMPTZ DEFAULT now()
patient_id UUID REFERENCES patients(id)

-- Primary keys: always 'id'
id UUID DEFAULT gen_random_uuid() PRIMARY KEY

-- Foreign keys: {table_singular}_id
user_id UUID REFERENCES users(id) ON DELETE CASCADE
```

**Standard columns on every table:**
```sql
id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
created_at  TIMESTAMPTZ DEFAULT now() NOT NULL,
updated_at  TIMESTAMPTZ DEFAULT now() NOT NULL
```

### Data Types (PostgreSQL / Supabase)

| Use case | Type |
|----------|------|
| Primary keys | `UUID` (gen_random_uuid()) |
| Short text | `TEXT` (not VARCHAR - TEXT is simpler in PG) |
| Long text | `TEXT` |
| Whole numbers | `INTEGER` or `BIGINT` |
| Decimals | `NUMERIC(precision, scale)` |
| Money | `NUMERIC(12, 2)` (never FLOAT for money) |
| Boolean | `BOOLEAN` |
| Dates | `DATE` |
| Date+time | `TIMESTAMPTZ` (always with timezone) |
| JSON data | `JSONB` (indexed, not JSON) |
| Arrays | `TEXT[]`, `UUID[]` |
| Enums | `TEXT` with CHECK constraint or PG ENUM |

### Constraints

```sql
-- Not null
column_name TEXT NOT NULL

-- Unique
email TEXT UNIQUE NOT NULL

-- Check constraints
risk_level TEXT CHECK (risk_level IN ('low', 'medium', 'high'))
adherence_rate NUMERIC(3,2) CHECK (adherence_rate BETWEEN 0 AND 1)
age INTEGER CHECK (age > 0 AND age < 150)

-- Foreign key with cascades
patient_id UUID REFERENCES patients(id) ON DELETE CASCADE
appointment_id UUID REFERENCES appointments(id) ON DELETE SET NULL

-- Composite unique
UNIQUE (patient_id, appointment_date)
```

### Indexes

```sql
-- Single column (for frequent WHERE / JOIN conditions)
CREATE INDEX idx_patients_case_manager ON patients(case_manager_id);

-- Composite (for queries filtering on multiple columns)
CREATE INDEX idx_appointments_patient_date
  ON appointments(patient_id, scheduled_at DESC);

-- Partial (only index subset of rows)
CREATE INDEX idx_active_patients ON patients(id)
  WHERE status = 'active';

-- Full-text search
CREATE INDEX idx_patients_name_fts ON patients
  USING GIN (to_tsvector('english', name));

-- JSONB
CREATE INDEX idx_metadata ON records USING GIN (metadata jsonb_path_ops);
```

---

## 2. Supabase Setup

### Project Initialization

```bash
# Install Supabase CLI
npm install -g supabase

# Initialize in project
supabase init

# Start local dev stack (Docker required)
supabase start

# Link to remote project
supabase link --project-ref your-project-ref

# Pull remote schema
supabase db pull
```

### Environment Variables

```bash
# .env.local (never commit)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key  # server-side only, never expose
```

### Client Initialization

```typescript
// lib/supabase/client.ts - Browser client
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}

// lib/supabase/server.ts - Server client (Next.js App Router)
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() { return cookieStore.getAll() },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options))
        },
      },
    }
  )
}

// lib/supabase/admin.ts - Admin client (service role, server only)
import { createClient } from '@supabase/supabase-js'

export const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)
```

---

## 3. Migrations

### Creating Migrations

```bash
# Create a new migration
supabase migration new create_patients_table

# This creates: supabase/migrations/20260215_create_patients_table.sql
```

### Migration File Template

```sql
-- supabase/migrations/20260215_create_patients_table.sql

-- Create table
CREATE TABLE patients (
  id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name            TEXT NOT NULL,
  date_of_birth   DATE,
  diagnosis       TEXT,
  case_manager_id UUID REFERENCES users(id) ON DELETE SET NULL,
  risk_level      TEXT CHECK (risk_level IN ('low', 'medium', 'high')),
  adherence_rate  NUMERIC(3,2) CHECK (adherence_rate BETWEEN 0 AND 1),
  crisis_calls_30d INTEGER DEFAULT 0,
  created_at      TIMESTAMPTZ DEFAULT now() NOT NULL,
  updated_at      TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER patients_updated_at
  BEFORE UPDATE ON patients
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Indexes
CREATE INDEX idx_patients_case_manager ON patients(case_manager_id);
CREATE INDEX idx_patients_risk_level ON patients(risk_level);

-- Enable RLS
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;

-- Comments
COMMENT ON TABLE patients IS 'Behavioral health patient records';
COMMENT ON COLUMN patients.adherence_rate IS 'Medication adherence 0.0-1.0';
```

### Running Migrations

```bash
# Apply locally
supabase db reset   # resets and re-runs all migrations

# Push to remote
supabase db push

# Check status
supabase migration list
```

---

## 4. Row Level Security (RLS)

**CRITICAL: Always enable RLS on every table. Without it, any authenticated user can read all rows.**

### Core Pattern

```sql
-- Step 1: Enable RLS (blocks ALL access by default)
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;

-- Step 2: Add policies for each operation
-- Policy: Users can only see their own patients
CREATE POLICY "case_managers_see_own_patients"
  ON patients FOR SELECT
  USING (case_manager_id = auth.uid());

-- Policy: Admins see all
CREATE POLICY "admins_see_all_patients"
  ON patients FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_id = auth.uid() AND role = 'admin'
    )
  );

-- Policy: Insert only as own case manager
CREATE POLICY "case_managers_insert_patients"
  ON patients FOR INSERT
  WITH CHECK (case_manager_id = auth.uid());

-- Policy: Update own patients only
CREATE POLICY "case_managers_update_own_patients"
  ON patients FOR UPDATE
  USING (case_manager_id = auth.uid())
  WITH CHECK (case_manager_id = auth.uid());

-- Policy: Soft delete (mark inactive instead of delete)
CREATE POLICY "case_managers_delete_own_patients"
  ON patients FOR DELETE
  USING (case_manager_id = auth.uid());
```

### RLS with Custom Claims (user roles)

```sql
-- Store roles in a profiles table
CREATE TABLE profiles (
  id   UUID REFERENCES auth.users(id) PRIMARY KEY,
  role TEXT CHECK (role IN ('admin', 'case_manager', 'viewer')) DEFAULT 'viewer'
);

-- Helper function for role checks
CREATE OR REPLACE FUNCTION get_user_role()
RETURNS TEXT AS $$
  SELECT role FROM profiles WHERE id = auth.uid()
$$ LANGUAGE SQL SECURITY DEFINER STABLE;

-- Use in policies
CREATE POLICY "admins_full_access"
  ON patients FOR ALL
  USING (get_user_role() = 'admin');
```

---

## 5. CRUD Queries with Supabase JS Client

### Select

```typescript
const supabase = createClient()

// Basic select
const { data, error } = await supabase
  .from('patients')
  .select('*')

// Select specific columns
const { data, error } = await supabase
  .from('patients')
  .select('id, name, risk_level, adherence_rate')

// Join related tables
const { data, error } = await supabase
  .from('patients')
  .select(`
    id,
    name,
    risk_level,
    case_manager:users(id, full_name, email),
    appointments(id, scheduled_at, status)
  `)

// Filter
const { data, error } = await supabase
  .from('patients')
  .select('*')
  .eq('risk_level', 'high')
  .gte('crisis_calls_30d', 3)
  .order('created_at', { ascending: false })
  .limit(20)

// Pagination
const { data, error, count } = await supabase
  .from('patients')
  .select('*', { count: 'exact' })
  .range(0, 9)  // first 10 rows

// Single row
const { data, error } = await supabase
  .from('patients')
  .select('*')
  .eq('id', patientId)
  .single()  // throws if 0 or >1 rows
```

### Insert

```typescript
// Single insert
const { data, error } = await supabase
  .from('patients')
  .insert({
    name: 'John Doe',
    risk_level: 'medium',
    adherence_rate: 0.75,
    case_manager_id: userId
  })
  .select()
  .single()

// Bulk insert
const { data, error } = await supabase
  .from('patients')
  .insert([
    { name: 'Alice', risk_level: 'low' },
    { name: 'Bob', risk_level: 'high' },
  ])
  .select()
```

### Update

```typescript
// Update by id
const { data, error } = await supabase
  .from('patients')
  .update({ risk_level: 'high', updated_at: new Date().toISOString() })
  .eq('id', patientId)
  .select()
  .single()

// Upsert (insert or update)
const { data, error } = await supabase
  .from('profiles')
  .upsert({ id: userId, role: 'case_manager' })
  .select()
```

### Delete

```typescript
// Hard delete
const { error } = await supabase
  .from('patients')
  .delete()
  .eq('id', patientId)

// Soft delete (preferred for healthcare data)
const { error } = await supabase
  .from('patients')
  .update({ deleted_at: new Date().toISOString() })
  .eq('id', patientId)
```

---

## 6. Raw SQL via RPC (Stored Procedures)

For complex queries, use PostgreSQL functions exposed via RPC:

```sql
-- Create function
CREATE OR REPLACE FUNCTION get_high_risk_patients(
  p_case_manager_id UUID DEFAULT NULL
)
RETURNS TABLE (
  patient_id   UUID,
  patient_name TEXT,
  risk_level   TEXT,
  risk_score   NUMERIC
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    p.id,
    p.name,
    p.risk_level,
    (p.crisis_calls_30d * 0.4 + (1 - p.adherence_rate) * 0.6) AS risk_score
  FROM patients p
  WHERE
    p.risk_level = 'high'
    AND (p_case_manager_id IS NULL OR p.case_manager_id = p_case_manager_id)
  ORDER BY risk_score DESC;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

```typescript
// Call via JS client
const { data, error } = await supabase
  .rpc('get_high_risk_patients', {
    p_case_manager_id: userId
  })
```

---

## 7. Real-time Subscriptions

```typescript
// Subscribe to changes on a table
const channel = supabase
  .channel('patients-changes')
  .on(
    'postgres_changes',
    {
      event: '*',         // INSERT | UPDATE | DELETE | *
      schema: 'public',
      table: 'patients',
      filter: `case_manager_id=eq.${userId}`  // optional filter
    },
    (payload) => {
      console.log('Change:', payload.eventType, payload.new)
      // Update local state
    }
  )
  .subscribe()

// Cleanup
supabase.removeChannel(channel)
```

---

## 8. Authentication

```typescript
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'secure-password',
  options: { data: { full_name: 'Dr. Smith' } }
})

// Sign in
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'secure-password'
})

// Get current user
const { data: { user } } = await supabase.auth.getUser()

// Sign out
await supabase.auth.signOut()

// Listen to auth state changes
supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_IN') { /* redirect */ }
  if (event === 'SIGNED_OUT') { /* clear state */ }
})
```

---

## 9. Storage (File Uploads)

```typescript
// Upload file
const { data, error } = await supabase.storage
  .from('patient-documents')
  .upload(`${patientId}/report-${Date.now()}.pdf`, file, {
    contentType: 'application/pdf',
    upsert: false
  })

// Get public URL
const { data } = supabase.storage
  .from('patient-documents')
  .getPublicUrl(`${patientId}/report.pdf`)

// Signed URL (private files)
const { data, error } = await supabase.storage
  .from('patient-documents')
  .createSignedUrl(`${patientId}/report.pdf`, 3600) // 1 hour

// Delete
const { error } = await supabase.storage
  .from('patient-documents')
  .remove([`${patientId}/report.pdf`])
```

---

## 10. Error Handling Pattern

```typescript
// Type-safe error handling
import { PostgrestError } from '@supabase/supabase-js'

async function getPatient(id: string) {
  const { data, error } = await supabase
    .from('patients')
    .select('*')
    .eq('id', id)
    .single()

  if (error) {
    if (error.code === 'PGRST116') {
      return { patient: null, error: 'Patient not found' }
    }
    throw new Error(`Database error: ${error.message}`)
  }

  return { patient: data, error: null }
}

// Common Supabase error codes
// PGRST116 - Row not found (.single() with no results)
// 23505    - Unique constraint violation
// 23503    - Foreign key constraint violation
// 42501    - RLS policy violation (permission denied)
```

---

## 11. Healthcare-Specific Schema (MindBridge Pattern)

```sql
-- Patients table matching patients.csv structure
CREATE TABLE patients (
  id                  UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  patient_id          TEXT UNIQUE NOT NULL,       -- external ID
  name                TEXT NOT NULL,
  last_appointment    DATE,
  appointments_missed INTEGER DEFAULT 0,
  medication_adherence NUMERIC(3,2)               -- 0.0-1.0
    CHECK (medication_adherence BETWEEN 0 AND 1),
  crisis_calls_30days INTEGER DEFAULT 0,
  diagnosis           TEXT,
  case_manager_id     UUID REFERENCES users(id),
  risk_level          TEXT
    CHECK (risk_level IN ('low', 'medium', 'high')),
  risk_notes          TEXT,
  created_at          TIMESTAMPTZ DEFAULT now(),
  updated_at          TIMESTAMPTZ DEFAULT now()
);

-- Screening results (replaces CSV+report files)
CREATE TABLE screening_results (
  id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  patient_id  UUID REFERENCES patients(id) ON DELETE CASCADE,
  risk_level  TEXT CHECK (risk_level IN ('low', 'medium', 'high')),
  primary_factor TEXT,
  action      TEXT,
  ai_model    TEXT,
  screened_at TIMESTAMPTZ DEFAULT now(),
  screened_by UUID REFERENCES users(id)
);
```

---

## 12. Quick Reference: Common Patterns

```typescript
// Check auth before query
const { data: { user } } = await supabase.auth.getUser()
if (!user) throw new Error('Not authenticated')

// Optimistic update pattern
setPatients(prev => prev.map(p =>
  p.id === id ? { ...p, risk_level: newLevel } : p
))
const { error } = await supabase
  .from('patients').update({ risk_level: newLevel }).eq('id', id)
if (error) {
  // Rollback
  setPatients(originalPatients)
}

// Search with ilike
.ilike('name', `%${searchTerm}%`)

// Date range filter
.gte('created_at', startDate.toISOString())
.lte('created_at', endDate.toISOString())

// Null checks
.is('deleted_at', null)       // IS NULL
.not('case_manager_id', 'is', null)  // IS NOT NULL

// In array
.in('risk_level', ['high', 'medium'])
```
