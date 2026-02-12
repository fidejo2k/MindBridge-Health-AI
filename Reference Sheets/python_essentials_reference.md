markdown# PYTHON ESSENTIALS FOR HEALTHCARE AI ENGINEERS
**Last Updated:** February 10, 2026  
**Version:** 1.0

---

## THE 15 CORE PATTERNS (90% of Your Code)

### 1️⃣ IMPORTS - Bringing in Tools
```python
import anthropic          # Claude API
import os                 # Environment variables & file operations
import csv                # Read/write CSV files
import json               # Work with JSON data
from datetime import datetime, timedelta  # Dates and times
```

**When to use:**
- Every script needs imports at the top
- Import only what you need (keeps code clean)

---

### 2️⃣ VARIABLES - Storing Data
```python
# Basic types
patient_name = "John Doe"           # String
risk_score = 85                     # Integer
medication_adherence = 0.75         # Float (75%)
is_high_risk = True                 # Boolean

# Healthcare examples
diagnosis = "Major Depressive Disorder"
crisis_calls = 3
last_appointment = "2026-02-10"
```

**Pro tip:** Use descriptive names! `risk_score` is better than `rs`

---

### 3️⃣ F-STRINGS - Text Formatting (USE THESE CONSTANTLY!)
```python
patient_id = 12345
risk = 85

# Basic f-string
message = f"Patient {patient_id} has risk score {risk}"
# Output: "Patient 12345 has risk score 85"

# Multi-line f-strings (PERFECT FOR PROMPTS!)
prompt = f"""
Analyze this patient:
ID: {patient_id}
Risk Score: {risk}
Diagnosis: {diagnosis}
"""

# Formatting numbers
adherence = 0.756
formatted = f"Adherence: {adherence:.1%}"  # "Adherence: 75.6%"
formatted = f"Adherence: {adherence*100:.0f}%"  # "Adherence: 76%"
```

**This is how you build Claude prompts!** 🎯

---

### 4️⃣ LISTS - Multiple Items
```python
# Create list
patients = ["John", "Mary", "Bob"]
scores = [85, 45, 92]

# Add to list
patients.append("Sarah")

# Access items
first_patient = patients[0]      # "John"
last_patient = patients[-1]      # "Sarah"

# Length
count = len(patients)             # 4

# Loop through list (SUPER COMMON!)
for patient in patients:
    print(f"Processing {patient}")

# Loop with index
for i, patient in enumerate(patients, 1):
    print(f"Patient {i}: {patient}")
    # Output: Patient 1: John, Patient 2: Mary...

# List comprehension (advanced)
high_scores = [s for s in scores if s > 80]  # [85, 92]
```

---

### 5️⃣ DICTIONARIES - Structured Data
```python
# Create dictionary (like JSON)
patient = {
    "id": 12345,
    "name": "John Doe",
    "risk_score": 85,
    "diagnosis": "MDD"
}

# Access values
name = patient["name"]              # "John Doe"
risk = patient.get("risk_score")    # 85 (safe - returns None if missing)

# Add/modify
patient["last_visit"] = "2026-02-10"
patient["risk_score"] = 90

# Check if key exists
if "diagnosis" in patient:
    print(patient["diagnosis"])

# Loop through dictionary
for key, value in patient.items():
    print(f"{key}: {value}")
```

**Dictionaries = CSV rows, JSON data, API responses!**

---

### 6️⃣ FUNCTIONS - Reusable Code
```python
def analyze_patient(patient_data):
    """
    Analyze patient risk
    
    Args:
        patient_data (dict): Patient information
        
    Returns:
        str: Risk level (Low/Medium/High)
    """
    risk_score = patient_data.get("risk_score", 0)
    
    if risk_score > 80:
        return "High"
    elif risk_score > 50:
        return "Medium"
    else:
        return "Low"

# Use the function
risk = analyze_patient({"risk_score": 85})  # "High"

# Function with multiple return values
def calculate_risk(missed_appts, adherence):
    score = (missed_appts * 20) + ((1 - adherence) * 50)
    level = "High" if score > 60 else "Medium" if score > 30 else "Low"
    return score, level

# Unpack results
score, level = calculate_risk(3, 0.45)
```

---

### 7️⃣ IF STATEMENTS - Decisions
```python
risk_score = 85

if risk_score > 80:
    action = "Immediate intervention"
elif risk_score > 50:
    action = "Schedule follow-up"
else:
    action = "Routine monitoring"

# Multiple conditions (AND)
if missed_appointments > 3 and med_adherence < 0.5:
    risk = "High"

# Multiple conditions (OR)
if crisis_calls > 0 or suicidal_ideation:
    urgent = True

# Not
if not appointment_scheduled:
    send_reminder()
```

---

### 8️⃣ FOR LOOPS - Repeat Actions
```python
# Loop through list
patients = ["John", "Mary", "Bob"]
for patient in patients:
    print(f"Analyzing {patient}")

# Loop with counter
for i in range(5):
    print(f"Patient {i+1}")  # 1, 2, 3, 4, 5

# Loop with index and item
for i, patient in enumerate(patients, 1):
    print(f"{i}. {patient}")

# Loop through dictionary
patient = {"id": 123, "name": "John", "risk": 85}
for key, value in patient.items():
    print(f"{key}: {value}")

# Break out of loop
for patient in patients:
    if patient == "Mary":
        break  # Stop looping
    print(patient)  # Only prints "John"
```

---

### 9️⃣ READING CSV FILES
```python
import csv

# Method 1: Read as dictionaries (RECOMMENDED!)
with open('patients.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        patient_id = row['patient_id']
        name = row['name']
        risk = row['risk_score']
        print(f"{patient_id}: {name} - Risk: {risk}")

# Method 2: Read into list
patients = []
with open('patients.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        patients.append(row)

# Now process all patients
for patient in patients:
    analyze(patient)
```

**ALWAYS use encoding='utf-8' on Windows!** ✅

---

### 🔟 WRITING FILES
```python
# Write text file
with open('report.txt', 'w', encoding='utf-8') as file:
    file.write("Patient Risk Report\n")
    file.write("High risk patients: 5\n")

# Append to file
with open('log.txt', 'a', encoding='utf-8') as file:
    file.write(f"Analysis completed at {datetime.now()}\n")

# Write list of lines
lines = [
    "=== REPORT ===",
    "Patient: John Doe",
    "Risk: High"
]
with open('report.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(lines))

# Write CSV
import csv
with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['id', 'name', 'risk'])
    writer.writeheader()
    writer.writerow({'id': 123, 'name': 'John', 'risk': 'High'})
```

---

### 1️⃣1️⃣ CALLING CLAUDE API (THE MONEY MAKER!)
```python
import anthropic
import os

# Create client (once per script)
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# Basic call
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Your prompt here"}
    ]
)

# Get response
result = message.content[0].text
print(result)

# With f-string prompt
patient_data = "Patient has 3 missed appointments"
prompt = f"""
Analyze this patient:

{patient_data}

Return risk level: Low/Medium/High
"""

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=500,
    messages=[{"role": "user", "content": prompt}]
)

risk = message.content[0].text
```

---

### 1️⃣2️⃣ ERROR HANDLING
```python
# Basic try-except
try:
    result = analyze_patient(data)
    print(f"Success: {result}")
except Exception as error:
    print(f"ERROR: {error}")

# Specific errors
try:
    with open('patients.csv', 'r') as file:
        data = file.read()
except FileNotFoundError:
    print("File not found!")
except PermissionError:
    print("No permission to read file!")
except Exception as e:
    print(f"Unknown error: {e}")

# Try-except-finally
try:
    process_patients()
except Exception as e:
    log_error(e)
finally:
    cleanup()  # Always runs, even if error
```

---

### 1️⃣3️⃣ STRING METHODS
```python
text = "  PATIENT NAME  "

# Clean up
clean = text.strip()           # "PATIENT NAME"
lower = text.lower()           # "  patient name  "
upper = text.upper()           # "  PATIENT NAME  "

# Split
diagnosis = "Major Depressive Disorder"
words = diagnosis.split()      # ["Major", "Depressive", "Disorder"]

# Join
words = ["High", "Risk", "Patient"]
text = " ".join(words)         # "High Risk Patient"

# Replace
note = "Patient has SI"
note = note.replace("SI", "Suicidal Ideation")

# Check contents
if "depression" in diagnosis.lower():
    print("Depression diagnosis")

# Starts with / ends with
if filename.endswith('.csv'):
    process_csv(filename)
```

---

### 1️⃣4️⃣ DATE & TIME
```python
from datetime import datetime, timedelta

# Current date/time
now = datetime.now()
print(now)  # 2026-02-10 14:30:15.123456

# Format date
formatted = now.strftime("%Y-%m-%d")           # "2026-02-10"
formatted = now.strftime("%B %d, %Y")          # "February 10, 2026"
formatted = now.strftime("%Y%m%d_%H%M%S")      # "20260210_143015"

# Parse date string
date_str = "2026-02-10"
date_obj = datetime.strptime(date_str, "%Y-%m-%d")

# Date math
tomorrow = now + timedelta(days=1)
one_week_ago = now - timedelta(days=7)
two_hours_later = now + timedelta(hours=2)

# Compare dates
last_appt = datetime(2026, 1, 15)
if now - last_appt > timedelta(days=30):
    print("Appointment overdue!")

# Useful for filenames
filename = f"report_{now.strftime('%Y%m%d_%H%M%S')}.txt"
# report_20260210_143015.txt
```

---

### 1️⃣5️⃣ ENVIRONMENT VARIABLES (Secrets!)
```python
import os

# Get API key (NEVER hardcode secrets!)
api_key = os.environ.get("ANTHROPIC_API_KEY")

# Get with default value
database_url = os.environ.get("DATABASE_URL", "localhost:5432")

# Check if exists
if os.environ.get("PRODUCTION_MODE"):
    use_production_settings()
else:
    use_dev_settings()

# File/folder operations
current_dir = os.getcwd()  # Current working directory
os.makedirs("reports", exist_ok=True)  # Create folder if doesn't exist
```

---

## 🎯 COMMON PATTERNS FOR HEALTHCARE AI

### Reading Patient CSV & Analyzing
```python
import csv
import anthropic
import os

def process_patient_csv(filename):
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    results = []
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Build prompt from CSV data
            prompt = f"""
            Analyze patient:
            Name: {row['name']}
            Diagnosis: {row['diagnosis']}
            Adherence: {row['adherence']}
            
            Return risk level.
            """
            
            # Call Claude
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Store result
            results.append({
                'patient': row['name'],
                'risk': message.content[0].text
            })
    
    return results
```

### Generating Reports
```python
from datetime import datetime

def generate_report(data, output_file):
    lines = []
    lines.append("=" * 60)
    lines.append("DAILY RISK REPORT")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 60)
    lines.append("")
    
    for item in data:
        lines.append(f"Patient: {item['name']}")
        lines.append(f"Risk: {item['risk']}")
        lines.append("-" * 60)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines))
```

---

## 🚫 COMMON ERRORS & FIXES

### Error: FileNotFoundError
```python
# Problem
with open('patients.csv', 'r') as file:  # File doesn't exist!

# Fix: Check if file exists first
import os
if os.path.exists('patients.csv'):
    with open('patients.csv', 'r') as file:
        ...
else:
    print("File not found!")
```

### Error: UnicodeEncodeError (Windows!)
```python
# Problem
with open('report.txt', 'w') as file:  # Default encoding fails!

# Fix: Always specify UTF-8
with open('report.txt', 'w', encoding='utf-8') as file:
    ...
```

### Error: IndentationError
```python
# Problem
def my_function():
print("Wrong indent!")  # Not indented!

# Fix: Indent function body
def my_function():
    print("Correct indent!")  # 4 spaces
```

### Error: KeyError (Dictionary)
```python
# Problem
patient = {"name": "John"}
diagnosis = patient["diagnosis"]  # Key doesn't exist!

# Fix: Use .get() with default
diagnosis = patient.get("diagnosis", "Not specified")
```

---

## 📚 QUICK REFERENCE CHEAT SHEET
```python
# IMPORTS
import anthropic, os, csv, json
from datetime import datetime

# VARIABLES
name = "John"              # String
score = 85                 # Int
adherence = 0.75           # Float
is_risk = True             # Bool

# F-STRINGS
msg = f"Score: {score}"
prompt = f"""Multi-line: {name}"""

# LISTS
items = ["a", "b", "c"]
items.append("d")
for item in items:
    print(item)

# DICTIONARIES
patient = {"id": 123, "name": "John"}
name = patient["name"]
name = patient.get("name", "Unknown")

# FUNCTIONS
def analyze(data):
    return "High" if data > 80 else "Low"

# IF/ELSE
if score > 80:
    risk = "High"
elif score > 50:
    risk = "Medium"
else:
    risk = "Low"

# FOR LOOPS
for i in range(5):
    print(i)
for i, item in enumerate(items, 1):
    print(f"{i}: {item}")

# READ CSV
with open('file.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['column'])

# WRITE FILE
with open('file.txt', 'w', encoding='utf-8') as f:
    f.write("content\n")

# CLAUDE API
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
msg = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[{"role": "user", "content": prompt}]
)
result = msg.content[0].text

# ERROR HANDLING
try:
    result = risky_operation()
except Exception as e:
    print(f"Error: {e}")

# DATES
from datetime import datetime, timedelta
now = datetime.now()
formatted = now.strftime("%Y-%m-%d")
yesterday = now - timedelta(days=1)

# ENV VARIABLES
api_key = os.environ.get("ANTHROPIC_API_KEY")
```

---

## 💡 PRO TIPS

1. **Always use UTF-8 encoding** when reading/writing files on Windows
2. **Use f-strings** for building prompts (cleaner than concatenation)
3. **Use .get() for dictionaries** to avoid KeyError
4. **Always handle errors** in production code
5. **Never hardcode API keys** - use environment variables
6. **Comment your code** - future you will thank you!
7. **Keep functions small** - one function, one purpose
8. **Use descriptive variable names** - `patient_risk` not `pr`

---

**THIS IS YOUR BIBLE!** Keep it open while coding! 📖

---
SAVE THAT AS python_essentials_reference.md! 