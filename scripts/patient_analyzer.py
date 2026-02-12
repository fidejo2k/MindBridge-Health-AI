import anthropic
import os

def analyze_patient(patient_data):
    """Analyze a single patient using Claude"""
    
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # Use your Prompt #1 from yesterday!
    prompt = f"""
You are a clinical documentation assistant for training purposes.

Task: Extract risk indicators from patient data.

PATIENT DATA:
{patient_data}

Return:
1. Risk Level (Low/Medium/High)
2. Key Risk Factors
3. Immediate Actions Needed
"""
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

# Test it!
test_patient = """
Patient ID: 12345
Last appointment: Missed (2 weeks ago)
Medication adherence: 45%
Crisis calls: 3 in past month
Diagnosis: Major Depressive Disorder
"""

result = analyze_patient(test_patient)
print("=== PATIENT RISK ANALYSIS ===")
print(result)