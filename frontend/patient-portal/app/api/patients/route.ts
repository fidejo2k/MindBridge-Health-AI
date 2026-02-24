import { Pool } from "pg";
import { NextResponse } from "next/server";
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
  connectionTimeoutMillis: 30000,
  idleTimeoutMillis: 30000,
  max: 1,
});

export async function GET() {
  try {

    console.log("DB URL exists:", !!process.env.DATABASE_URL);
console.log("DB URL prefix:", process.env.DATABASE_URL?.substring(0, 20));
    const client = await pool.connect();
    
    const result = await client.query(`
      SELECT 
        id,
        patient_name,
        risk_level,
        medication_adherence,
        appointments_missed,
        crisis_calls_30days,
        diagnosis
      FROM patients
      ORDER BY id ASC
    `);
    
    client.release();
    
    return NextResponse.json({
      success: true,
      patients: result.rows,
      count: result.rows.length,
      source: "Railway PostgreSQL"
    });

  } catch (error) {
    console.error("Database connection error:", error);
    return NextResponse.json(
      { success: false, error: "Failed to connect to database" },
      { status: 500 }
    );
  }
}
