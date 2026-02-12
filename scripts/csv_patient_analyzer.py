import anthropic
import os
import csv
from datetime import datetime

def analyze_patient_from_csv(patient_row, client):
    """Analyze a patient from CSV data"""
    
    # Build patient summary from CSV row
    patient_summary = f"""
Patient ID: {patient_row['patient_id']}
Name: {patient_row['name']}
Last Appointment: {patient_row['last_appointment']}
Appointments Missed (last 6 months): {patient_row['appointments_missed']}
Medication Adherence: {float(patient_row['medication_adherence'])*100:.0f}%
Crisis Calls (30 days): {patient_row['crisis_calls_30days']}
Diagnosis: {patient_row['diagnosis']}
Case Manager: {patient_row['case_manager']}
"""
    
    # Use Claude to analyze
    prompt = f"""
You are a clinical risk assessment assistant.

Analyze this patient and provide:
1. Risk Level (Low/Medium/High)
2. Primary Risk Factor
3. Recommended Action

PATIENT DATA:
{patient_summary}

Return in this exact format:
Risk Level: [level]
Primary Factor: [factor]
Action: [action]
"""
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

def process_csv_patients(input_csv, output_report):
    """Read CSV, analyze all patients, generate report"""
    
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # Read CSV file
    print(f"Reading patient data from: {input_csv}")
    patients = []
    
    with open(input_csv, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            patients.append(row)
    
    print(f"✓ Loaded {len(patients)} patients\n")
    
    # Start building report
    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("OAKWOOD BEHAVIORAL HEALTH - DAILY RISK SCREENING REPORT")
    report_lines.append(f"Generated: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}")
    report_lines.append("=" * 70)
    report_lines.append("")
    
    # Track statistics
    high_risk_patients = []
    medium_risk_patients = []
    low_risk_patients = []
    
    # Analyze each patient
    print("Analyzing patients...\n")
    
    for i, patient in enumerate(patients, 1):
        print(f"[{i}/{len(patients)}] Analyzing {patient['name']} (ID: {patient['patient_id']})...")
        
        # Get analysis
        analysis = analyze_patient_from_csv(patient, client)
        
        # Categorize by risk
        if "High" in analysis:
            risk_level = "HIGH RISK"
            high_risk_patients.append({
                'patient': patient,
                'analysis': analysis
            })
        elif "Medium" in analysis:
            risk_level = "MEDIUM RISK"
            medium_risk_patients.append({
                'patient': patient,
                'analysis': analysis
            })
        else:
            risk_level = "LOW RISK"
            low_risk_patients.append({
                'patient': patient,
                'analysis': analysis
            })
        
        # Add to report
        report_lines.append(f"{risk_level} - {patient['name']} (ID: {patient['patient_id']})")
        report_lines.append(f"Case Manager: {patient['case_manager']}")
        report_lines.append(f"Diagnosis: {patient['diagnosis']}")
        report_lines.append(f"Last Appointment: {patient['last_appointment']}")
        report_lines.append(f"Missed Appointments: {patient['appointments_missed']}")
        report_lines.append(f"Med Adherence: {float(patient['medication_adherence'])*100:.0f}%")
        report_lines.append(f"Crisis Calls: {patient['crisis_calls_30days']}")
        report_lines.append("")
        report_lines.append(f"{analysis}")
        report_lines.append("-" * 70)
        report_lines.append("")
    
    # Add summary section
    report_lines.append("")
    report_lines.append("=" * 70)
    report_lines.append("EXECUTIVE SUMMARY")
    report_lines.append("=" * 70)
    report_lines.append("")
    report_lines.append(f"Total Patients Screened: {len(patients)}")
    report_lines.append(f"HIGH RISK: {len(high_risk_patients)} ({len(high_risk_patients)/len(patients)*100:.1f}%)")
    report_lines.append(f"MEDIUM RISK: {len(medium_risk_patients)} ({len(medium_risk_patients)/len(patients)*100:.1f}%)")
    report_lines.append(f"LOW RISK: {len(low_risk_patients)} ({len(low_risk_patients)/len(patients)*100:.1f}%)")
    report_lines.append("")
    
    # High risk patient list
    if high_risk_patients:
        report_lines.append("IMMEDIATE ATTENTION REQUIRED:")
        for item in high_risk_patients:
            p = item['patient']
            report_lines.append(f"  • {p['name']} (ID: {p['patient_id']}) - Case Manager: {p['case_manager']}")
        report_lines.append("")
    
    # Medium risk patient list
    if medium_risk_patients:
        report_lines.append("FOLLOW-UP WITHIN 48-72 HOURS:")
        for item in medium_risk_patients:
            p = item['patient']
            report_lines.append(f"  • {p['name']} (ID: {p['patient_id']}) - Case Manager: {p['case_manager']}")
        report_lines.append("")
    
    report_lines.append("=" * 70)
    report_lines.append("Report completed successfully")
    report_lines.append("=" * 70)
    
    # Write report to file
    with open(output_report, 'w', encoding='utf-8') as file:
        file.write('\n'.join(report_lines))
    
    print(f"\n✓ ANALYSIS COMPLETE!")
    print(f"✓ Report saved: {output_report}")
    print(f"\n📊 SUMMARY:")
    print(f"   Total: {len(patients)}")
    print(f"   High Risk: {len(high_risk_patients)}")
    print(f"   Medium Risk: {len(medium_risk_patients)}")
    print(f"   Low Risk: {len(low_risk_patients)}")
    
    return output_report

# Run the analysis
if __name__ == "__main__":
    input_file = "patients.csv"
    output_file = f"reports/daily_screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    print("=" * 70)
    print("OAKWOOD BEHAVIORAL HEALTH - AUTOMATED PATIENT SCREENING")
    print("=" * 70)
    print("")
    
    process_csv_patients(input_file, output_file)
    
    print(f"\n📄 Open report: {output_file}")