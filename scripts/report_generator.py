import anthropic
import os
from datetime import datetime

def analyze_patient(patient_data, client):
    """Analyze a single patient"""
    
    prompt = f"""
You are a clinical documentation assistant.

Analyze this patient and provide:
1. Risk Level (Low/Medium/High)
2. Primary Risk Factor
3. Recommended Action

PATIENT DATA:
{patient_data}

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

def generate_report(patient_list, output_file):
    """Analyze patients and generate text report"""
    
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # Start building report
    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("DAILY PATIENT RISK SCREENING REPORT")
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("=" * 60)
    report_lines.append("")
    
    # Track statistics
    high_risk_count = 0
    medium_risk_count = 0
    low_risk_count = 0
    
    print(f"Analyzing {len(patient_list)} patients...")
    print(f"Generating report: {output_file}\n")
    
    # Analyze each patient
    for i, patient in enumerate(patient_list, 1):
        print(f"Processing patient {i}/{len(patient_list)}...")
        
        # Get analysis
        analysis = analyze_patient(patient, client)
        
        # Count risk levels
        if "High" in analysis:
            high_risk_count += 1
            risk_emoji = "HIGH RISK"
        elif "Medium" in analysis:
            medium_risk_count += 1
            risk_emoji = "MEDIUM RISK"
        else:
            low_risk_count += 1
            risk_emoji = "LOW RISK"
        
        # Add to report
        report_lines.append(f"{risk_emoji} - PATIENT #{i}")
        report_lines.append(f"Data: {patient}")
        report_lines.append(f"{analysis}")
        report_lines.append("-" * 60)
        report_lines.append("")
    
    # Add summary
    report_lines.append("=" * 60)
    report_lines.append("SUMMARY")
    report_lines.append("=" * 60)
    report_lines.append(f"Total Patients Analyzed: {len(patient_list)}")
    report_lines.append(f"HIGH RISK: {high_risk_count}")
    report_lines.append(f"MEDIUM RISK: {medium_risk_count}")
    report_lines.append(f"LOW RISK: {low_risk_count}")
    report_lines.append("")
    report_lines.append(f"High Risk Percentage: {(high_risk_count/len(patient_list)*100):.1f}%")
    report_lines.append("=" * 60)
    
    # Write to file with UTF-8 encoding
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(report_lines))
    
    print(f"\n✓ Report generated: {output_file}")
    print(f"✓ Total patients: {len(patient_list)}")
    print(f"✓ High risk: {high_risk_count}")
    
    return output_file

# Test data
test_patients = [
    "Patient ID: 001, Missed 3 appts, Med adherence 40%, 4 crisis calls",
    "Patient ID: 002, All appts attended, Med adherence 95%, 0 crisis calls",
    "Patient ID: 003, Missed 1 appt, Med adherence 75%, 1 crisis call",
    "Patient ID: 004, Missed 4 appts, Med adherence 25%, 6 crisis calls",
    "Patient ID: 005, Missed 2 appts, Med adherence 60%, 2 crisis calls"
]

# Generate report
output_filename = f"patient_risk_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
generate_report(test_patients, output_filename)

print(f"\n📄 Open the file to see your report: {output_filename}")