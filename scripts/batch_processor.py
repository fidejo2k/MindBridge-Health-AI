import anthropic
import os
import csv

def analyze_patient(patient_data, client):
    """Analyze a single patient"""
    
    prompt = f"""
You are a clinical documentation assistant.

Extract risk level from patient data:

{patient_data}

Return ONLY:
Risk Level: [Low/Medium/High]
Key Factor: [Primary concern]
"""
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

def process_batch(patient_list):
    """Process multiple patients"""
    
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    results = []
    
    print("Starting batch analysis...")
    print(f"Total patients: {len(patient_list)}\n")
    
    for i, patient in enumerate(patient_list, 1):
        print(f"Analyzing patient {i}/{len(patient_list)}...")
        
        # Analyze this patient
        result = analyze_patient(patient, client)
        
        # Store result
        results.append({
            'patient_data': patient,
            'analysis': result
        })
        
        print(f"✓ Complete\n")
    
    return results

# Test with 5 patients
test_patients = [
    "Patient A: Missed 2 appts, Med adherence 50%, 1 crisis call",
    "Patient B: All appts attended, Med adherence 95%, 0 crisis calls",
    "Patient C: Missed 4 appts, Med adherence 30%, 5 crisis calls",
    "Patient D: Missed 1 appt, Med adherence 80%, 0 crisis calls",
    "Patient E: Missed 3 appts, Med adherence 40%, 3 crisis calls"
]

# Process all patients
results = process_batch(test_patients)

# Display results
print("\n" + "="*50)
print("BATCH ANALYSIS COMPLETE")
print("="*50 + "\n")

for i, result in enumerate(results, 1):
    print(f"Patient {i}:")
    print(result['analysis'])
    print("-" * 50)