#!/usr/bin/env python3
"""
Test connection to Docker PostgreSQL and generate a sample report.
This proves MindBridge can work with containerized databases.
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from datetime import datetime

# Docker PostgreSQL connection
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'mindbridge_user',
    'password': 'mindbridge_dev_password_2026',
    'database': 'mindbridge'
}


def test_connection():
    """Test basic connection to Docker PostgreSQL."""
    print("=" * 70)
    print("🐳 Testing Docker PostgreSQL Connection")
    print("=" * 70)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        print(f"\n✅ Connection successful!")
        print(f"📊 PostgreSQL version: {version[:50]}...")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print(f"\nMake sure Docker is running:")
        print(f"   docker compose up -d")
        return False


def create_sample_table():
    """Create a sample patients table."""
    print("\n" + "=" * 70)
    print("📝 Creating Sample Patient Table")
    print("=" * 70)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Create patients table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id SERIAL PRIMARY KEY,
                patient_name VARCHAR(100),
                risk_level VARCHAR(20),
                medication_adherence FLOAT,
                appointments_missed INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Insert sample data
        sample_patients = [
            ('John Doe', 'HIGH', 0.3, 4),
            ('Jane Smith', 'MEDIUM', 0.7, 1),
            ('Bob Johnson', 'LOW', 0.9, 0),
        ]
        
        cursor.executemany("""
            INSERT INTO patients (patient_name, risk_level, medication_adherence, appointments_missed)
            VALUES (%s, %s, %s, %s)
        """, sample_patients)
        
        conn.commit()
        
        # Count records
        cursor.execute("SELECT COUNT(*) FROM patients")
        count = cursor.fetchone()[0]
        
        print(f"\n✅ Table created successfully!")
        print(f"📊 Sample patients inserted: {count}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Table creation failed: {e}")
        return False


def generate_report():
    """Generate a simple report from Docker database."""
    print("\n" + "=" * 70)
    print("📄 Generating Report from Docker Database")
    print("=" * 70)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Query patients
        cursor.execute("""
            SELECT patient_name, risk_level, medication_adherence, appointments_missed
            FROM patients
            ORDER BY 
                CASE risk_level
                    WHEN 'HIGH' THEN 1
                    WHEN 'MEDIUM' THEN 2
                    WHEN 'LOW' THEN 3
                END
        """)
        
        patients = cursor.fetchall()
        
        # Generate text report
        report_filename = f"reports/docker_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)
        
        with open(report_filename, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("MINDBRIDGE HEALTH AI - DOCKER DATABASE TEST REPORT\n")
            f.write("=" * 70 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Database: Docker PostgreSQL (localhost:5432)\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("PATIENT RISK SUMMARY\n")
            f.write("-" * 70 + "\n\n")
            
            for patient in patients:
                name, risk, adherence, missed = patient
                f.write(f"Patient: {name}\n")
                f.write(f"  Risk Level: {risk}\n")
                f.write(f"  Medication Adherence: {adherence * 100:.1f}%\n")
                f.write(f"  Appointments Missed: {missed}\n")
                f.write("\n")
            
            f.write("-" * 70 + "\n")
            f.write(f"Total Patients: {len(patients)}\n")
            f.write("=" * 70 + "\n")
        
        print(f"\n✅ Report generated successfully!")
        print(f"📁 Location: {report_filename}")
        print(f"📊 Patients included: {len(patients)}")
        
        # Display summary
        print("\n" + "=" * 70)
        print("PATIENT SUMMARY")
        print("=" * 70)
        for patient in patients:
            name, risk, adherence, missed = patient
            emoji = "🔴" if risk == "HIGH" else "🟡" if risk == "MEDIUM" else "🟢"
            print(f"{emoji} {name:20s} | {risk:6s} | Adherence: {adherence*100:4.1f}% | Missed: {missed}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Report generation failed: {e}")
        return False


def cleanup():
    """Optional: Drop the test table."""
    print("\n" + "=" * 70)
    print("🧹 Cleanup (Optional)")
    print("=" * 70)
    
    response = input("\nDrop test table? (y/N): ").strip().lower()
    
    if response == 'y':
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute("DROP TABLE IF EXISTS patients;")
            conn.commit()
            
            print("\n✅ Test table dropped successfully!")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"\n❌ Cleanup failed: {e}")
    else:
        print("\n✓ Keeping test table for future use")


def main():
    """Run full Docker database test."""
    print("\n")
    print("🏥 MINDBRIDGE DOCKER DATABASE TEST")
    print("=" * 70)
    
    # Step 1: Test connection
    if not test_connection():
        print("\n⚠️  Start Docker first:")
        print("   docker compose up -d")
        return
    
    # Step 2: Create sample table
    if not create_sample_table():
        return
    
    # Step 3: Generate report
    if not generate_report():
        return
    
    # Step 4: Optional cleanup
    cleanup()
    
    print("\n" + "=" * 70)
    print("✅ DOCKER TEST COMPLETE!")
    print("=" * 70)
    print("\nYou just proved MindBridge can:")
    print("  ✓ Connect to Docker PostgreSQL")
    print("  ✓ Create tables with proper schema")
    print("  ✓ Insert patient data")
    print("  ✓ Query and generate reports")
    print("  ✓ Work in a containerized environment")
    print("\n🎯 This is a REAL portfolio piece!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
