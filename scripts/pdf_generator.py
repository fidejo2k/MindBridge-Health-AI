import anthropic
import os
import csv
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def analyze_patient_from_csv(patient_row, client):
    """Analyze a patient from CSV data"""
    
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
    
    prompt = f"""
You are a clinical risk assessment assistant.

Analyze this patient and provide:
1. Risk Level (Low/Medium/High)
2. Primary Risk Factor (max 80 characters)
3. Recommended Action (max 120 characters)

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

def create_pdf_report(csv_file, output_file):
    """Create a professional PDF report"""
    
    # Initialize Claude client
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # Read patient data
    print(f"Reading patient data from: {csv_file}")
    patients = []
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            patients.append(row)
    
    print(f"✓ Loaded {len(patients)} patients\n")
    
    # Analyze all patients
    patient_analyses = []
    high_risk_patients = []
    medium_risk_patients = []
    low_risk_patients = []
    
    print("Analyzing patients...\n")
    
    for i, patient in enumerate(patients, 1):
        print(f"[{i}/{len(patients)}] Analyzing {patient['name']}...")
        
        # Get AI analysis
        analysis = analyze_patient_from_csv(patient, client)
        
        # Parse analysis
        risk_level = "Unknown"
        primary_factor = "Not analyzed"
        action = "No action specified"
        
        for line in analysis.split('\n'):
            if line.startswith('Risk Level:'):
                risk_level = line.replace('Risk Level:', '').strip()
            elif line.startswith('Primary Factor:'):
                primary_factor = line.replace('Primary Factor:', '').strip()
            elif line.startswith('Action:'):
                action = line.replace('Action:', '').strip()
        
        # Store analysis
        patient_analysis = {
            'patient': patient,
            'risk_level': risk_level,
            'primary_factor': primary_factor,
            'action': action
        }
        patient_analyses.append(patient_analysis)
        
        # Categorize by risk
        if "High" in risk_level:
            high_risk_patients.append(patient_analysis)
        elif "Medium" in risk_level:
            medium_risk_patients.append(patient_analysis)
        else:
            low_risk_patients.append(patient_analysis)
    
    print(f"\n✓ Analysis complete!")
    print(f"  High Risk: {len(high_risk_patients)}")
    print(f"  Medium Risk: {len(medium_risk_patients)}")
    print(f"  Low Risk: {len(low_risk_patients)}\n")
    
    print("Creating PDF document...\n")
    
    # Create PDF
    doc = SimpleDocTemplate(output_file, pagesize=letter,
                            rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Container for PDF elements
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.white,
        backColor=colors.HexColor('#1f4788'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    # Add title page
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("OAKWOOD BEHAVIORAL HEALTH", title_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Daily Patient Risk Screening Report", subtitle_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}", date_style))
    
    # Add summary statistics
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("Executive Summary", section_style))
    elements.append(Spacer(1, 0.2*inch))
    
    summary_data = [
        ['Risk Level', 'Count', 'Percentage', 'Status'],
        ['HIGH RISK', str(len(high_risk_patients)), 
         f"{len(high_risk_patients)/len(patients)*100:.1f}%", 'IMMEDIATE ATTENTION'],
        ['MEDIUM RISK', str(len(medium_risk_patients)), 
         f"{len(medium_risk_patients)/len(patients)*100:.1f}%", 'FOLLOW-UP 48-72 HRS'],
        ['LOW RISK', str(len(low_risk_patients)), 
         f"{len(low_risk_patients)/len(patients)*100:.1f}%", 'ROUTINE MONITORING'],
        ['TOTAL', str(len(patients)), '100%', '']
    ]
    
    summary_table = Table(summary_data, colWidths=[1.5*inch, 1*inch, 1.2*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#ffcccc')),  # Red for high
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#ffe6cc')),  # Orange for medium
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#ccffcc')),  # Green for low
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ]))
    
    elements.append(summary_table)
    elements.append(PageBreak())
    
    # Add patient details
    elements.append(Paragraph("Patient Details", section_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Sort patients by risk (High, Medium, Low)
    sorted_patients = high_risk_patients + medium_risk_patients + low_risk_patients
    
    for i, patient_analysis in enumerate(sorted_patients):
        patient = patient_analysis['patient']
        risk_level = patient_analysis['risk_level']
        
        # Determine background color
        if "High" in risk_level:
            bg_color = colors.HexColor('#ffcccc')
        elif "Medium" in risk_level:
            bg_color = colors.HexColor('#ffe6cc')
        else:
            bg_color = colors.HexColor('#ccffcc')
        
        # Patient header
        patient_header_style = ParagraphStyle(
            'PatientHeader',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.black,
            backColor=bg_color,
            fontName='Helvetica-Bold',
            spaceAfter=5
        )
        
        elements.append(Paragraph(
            f"{risk_level.upper()} - {patient['name']} (ID: {patient['patient_id']})", 
            patient_header_style
        ))
        
        # Patient data table
        patient_data = [
            ['Case Manager:', patient['case_manager'], 
             'Diagnosis:', patient['diagnosis']],
            ['Last Appointment:', patient['last_appointment'], 
             'Missed Appointments:', patient['appointments_missed']],
            ['Med Adherence:', f"{float(patient['medication_adherence'])*100:.0f}%", 
             'Crisis Calls (30d):', patient['crisis_calls_30days']],
        ]
        
        patient_table = Table(patient_data, colWidths=[1.3*inch, 1.8*inch, 1.3*inch, 1.8*inch])
        patient_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        elements.append(patient_table)
        elements.append(Spacer(1, 0.1*inch))
        
        # Analysis
        analysis_text = f"<b>Primary Factor:</b> {patient_analysis['primary_factor']}<br/>"
        analysis_text += f"<b>Recommended Action:</b> {patient_analysis['action']}"
        
        elements.append(Paragraph(analysis_text, styles['Normal']))
        elements.append(Spacer(1, 0.15*inch))
        
        # Add separator line
        line_data = [['_' * 100]]
        line_table = Table(line_data, colWidths=[6.5*inch])
        line_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # Page break after every 3 patients
        if (i + 1) % 3 == 0 and i < len(sorted_patients) - 1:
            elements.append(PageBreak())
    
    # Build PDF
    doc.build(elements)
    
    print(f"✓ PDF DOCUMENT CREATED!")
    print(f"✓ File saved: {output_file}")
    print(f"\n📄 SUMMARY:")
    print(f"   Total Pages: ~{len(sorted_patients)//3 + 2}")
    print(f"   Total: {len(patients)} patients")
    print(f"   High Risk: {len(high_risk_patients)}")
    print(f"   Medium Risk: {len(medium_risk_patients)}")
    print(f"   Low Risk: {len(low_risk_patients)}")
    
    return output_file

# Run the script
if __name__ == "__main__":
    input_csv = "patients.csv"
    output_pdf = f"reports/patient_screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    print("=" * 70)
    print("PDF DOCUMENT GENERATOR")
    print("=" * 70)
    print()
    
    create_pdf_report(input_csv, output_pdf)
    
    print(f"\n📑 Open the PDF file: {output_pdf}")
    print("\nThis PDF is PRINT-READY and can be emailed or archived!")
