# DOCUMENT GENERATION REFERENCE SHEET
**MindBridge Health - Healthcare AI Engineer Training**
**Last Updated: Day 3 - February 11, 2026**

---

## 📚 OVERVIEW: THREE DOCUMENT LIBRARIES

### 🎯 WHEN TO USE EACH FORMAT

**WORD (.docx) - python-docx**
- ✅ Case managers need to ADD NOTES
- ✅ Content needs to be EDITED
- ✅ Collaborative documents
- ✅ Templates with fillable sections
- ❌ When you need sorting/filtering (use Excel)
- ❌ When document must be locked (use PDF)

**EXCEL (.xlsx) - openpyxl**
- ✅ Data needs to be SORTED
- ✅ Data needs to be FILTERED
- ✅ Multiple views of same data (separate sheets)
- ✅ Formulas and calculations
- ✅ Data export to other systems
- ❌ When editing should be prevented (use PDF)
- ❌ Heavy narrative content (use Word)

**PDF (.pdf) - reportlab**
- ✅ Must be PRINT-READY
- ✅ Document should be LOCKED (no editing)
- ✅ Official records and archives
- ✅ Email attachments for review
- ✅ Universal compatibility required
- ❌ When data needs manipulation (use Excel)
- ❌ When editing is needed (use Word)

---

## 📦 LIBRARY INSTALLATION
```bash
# Install all three at once:
pip install python-docx openpyxl reportlab
```

**Dependencies installed automatically:**
- python-docx → lxml (XML processing)
- openpyxl → et-xmlfile (Excel XML)
- reportlab → pillow (image processing)

---

## 📄 WORD DOCUMENTS (python-docx)

### BASIC TEMPLATE
```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Create document
doc = Document()

# Add title (centered)
title = doc.add_heading('DOCUMENT TITLE', 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Add subtitle
subtitle = doc.add_heading('Subtitle Here', level=1)
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Add regular paragraph
doc.add_paragraph('Regular text here')

# Add colored heading
heading = doc.add_heading('Section Name', level=2)
heading.runs[0].font.color.rgb = RGBColor(255, 0, 0)  # Red

# Add paragraph with formatting
para = doc.add_paragraph()
para.add_run('Bold text').bold = True
para.add_run(' normal text ')
para.add_run('Italic text').font.italic = True

# Page break
doc.add_page_break()

# Save
doc.save('output.docx')
```

### COLOR CODING (RGB)
```python
from docx.shared import RGBColor

# Common colors for healthcare
red = RGBColor(255, 0, 0)      # High risk
orange = RGBColor(255, 165, 0)  # Medium risk
green = RGBColor(0, 128, 0)     # Low risk
blue = RGBColor(0, 0, 255)      # Information
gray = RGBColor(128, 128, 128)  # Neutral

# Apply to text
heading.runs[0].font.color.rgb = red
```

### ALIGNMENT OPTIONS
```python
from docx.enum.text import WD_ALIGN_PARAGRAPH

paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT     # Default
paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER   # Centered
paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT    # Right-aligned
paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY  # Justified
```

### COMMON PATTERNS
```python
# Pattern 1: Report with sections
doc = Document()
doc.add_heading('REPORT TITLE', 0)
doc.add_heading('Section 1', level=1)
doc.add_paragraph('Content here...')
doc.add_heading('Section 2', level=1)
doc.add_paragraph('More content...')
doc.save('report.docx')

# Pattern 2: Risk-coded patients
for patient in patients:
    if patient['risk'] == 'High':
        color = RGBColor(255, 0, 0)
    elif patient['risk'] == 'Medium':
        color = RGBColor(255, 165, 0)
    else:
        color = RGBColor(0, 128, 0)
    
    heading = doc.add_heading(f"{patient['risk']} - {patient['name']}", level=2)
    heading.runs[0].font.color.rgb = color
    doc.add_paragraph(f"Details: {patient['info']}")
```

---

## 📊 EXCEL SPREADSHEETS (openpyxl)

### BASIC TEMPLATE
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

# Create workbook
wb = Workbook()

# First sheet (active by default)
ws = wb.active
ws.title = "Summary"

# Add data
ws['A1'] = "Header 1"
ws['B1'] = "Header 2"
ws['A2'] = "Data 1"
ws['B2'] = "Data 2"

# Create additional sheets
ws2 = wb.create_sheet("Details")
ws3 = wb.create_sheet("Analysis")

# Save
wb.save('output.xlsx')
```

### FORMATTING CELLS
```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Font styling
cell.font = Font(bold=True, size=14, color="FFFFFF")

# Background color
cell.fill = PatternFill(start_color="4472C4", 
                        end_color="4472C4", 
                        fill_type="solid")

# Alignment
cell.alignment = Alignment(horizontal="center", 
                           vertical="center",
                           wrap_text=True)

# Borders
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
cell.border = thin_border
```

### COLOR FILLS (HEALTHCARE)
```python
from openpyxl.styles import PatternFill

# Define colors
red_fill = PatternFill(start_color="FFE6E6", end_color="FFE6E6", fill_type="solid")
orange_fill = PatternFill(start_color="FFF4E6", end_color="FFF4E6", fill_type="solid")
green_fill = PatternFill(start_color="E6FFE6", end_color="E6FFE6", fill_type="solid")
blue_fill = PatternFill(start_color="E6F2FF", end_color="E6F2FF", fill_type="solid")
header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")

# Apply to cells
ws['A1'].fill = header_fill
ws['A2'].fill = red_fill    # High risk row
ws['A3'].fill = orange_fill # Medium risk row
ws['A4'].fill = green_fill  # Low risk row
```

### COLUMN WIDTHS
```python
# Set specific width
ws.column_dimensions['A'].width = 20
ws.column_dimensions['B'].width = 15

# Set multiple columns
for col in ['A', 'B', 'C', 'D']:
    ws.column_dimensions[col].width = 15
```

### FREEZE PANES (KEEP HEADERS VISIBLE)
```python
# Freeze top row (header stays visible when scrolling)
ws.freeze_panes = 'A2'

# Freeze top row and first column
ws.freeze_panes = 'B2'
```

### COMMON PATTERN: MULTI-SHEET WORKBOOK
```python
wb = Workbook()

# Sheet 1: Summary with statistics
ws_summary = wb.active
ws_summary.title = "Summary"
ws_summary['A1'] = "Total Patients"
ws_summary['B1'] = 100

# Sheet 2: All data
ws_all = wb.create_sheet("All Patients")
headers = ["ID", "Name", "Risk", "Status"]
for col, header in enumerate(headers, 1):
    ws_all.cell(1, col, header)

# Sheet 3: Filtered view (high risk only)
ws_high = wb.create_sheet("High Risk")
# Add only high-risk patients here

wb.save('multi_sheet.xlsx')
```

---

## 📑 PDF DOCUMENTS (reportlab)

### BASIC TEMPLATE
```python
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# Create PDF
doc = SimpleDocTemplate("output.pdf", pagesize=letter)
elements = []
styles = getSampleStyleSheet()

# Add title
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1f4788'),
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)
elements.append(Paragraph("TITLE HERE", title_style))
elements.append(Spacer(1, 0.5*inch))

# Add paragraph
elements.append(Paragraph("Regular text here", styles['Normal']))

# Build PDF
doc.build(elements)
```

### COLOR DEFINITIONS
```python
from reportlab.lib import colors

# Hex colors
blue = colors.HexColor('#1f4788')
red = colors.HexColor('#ff0000')
orange = colors.HexColor('#ffa500')
green = colors.HexColor('#008000')

# RGB colors
light_red = colors.HexColor('#ffcccc')
light_orange = colors.HexColor('#ffe6cc')
light_green = colors.HexColor('#ccffcc')
```

### TABLES IN PDF
```python
from reportlab.platypus import Table, TableStyle

# Create table data
data = [
    ['Header 1', 'Header 2', 'Header 3'],
    ['Row 1 Col 1', 'Row 1 Col 2', 'Row 1 Col 3'],
    ['Row 2 Col 1', 'Row 2 Col 2', 'Row 2 Col 3']
]

# Create table
table = Table(data, colWidths=[2*inch, 2*inch, 2*inch])

# Style table
table.setStyle(TableStyle([
    # Header row
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    
    # Data rows
    ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#ffcccc')),  # Row 1 red
    ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#ccffcc')),  # Row 2 green
    
    # All cells
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

elements.append(table)
```

### SPACING AND PAGE BREAKS
```python
from reportlab.platypus import Spacer, PageBreak

# Add vertical space
elements.append(Spacer(1, 0.5*inch))  # 0.5 inch space
elements.append(Spacer(1, 1*inch))    # 1 inch space

# Add page break
elements.append(PageBreak())
```

---

## 🔄 MULTI-FORMAT WORKFLOW PATTERN

### ANALYZE ONCE, GENERATE THREE
```python
# Step 1: Analyze data ONCE (shared across all formats)
analyzed_data = analyze_all_patients(patients)

# Step 2: Generate Word document
create_word_doc(analyzed_data, 'report.docx')

# Step 3: Generate Excel spreadsheet
create_excel_sheet(analyzed_data, 'report.xlsx')

# Step 4: Generate PDF document
create_pdf_doc(analyzed_data, 'report.pdf')

# Result: All three formats from ONE analysis!
```

### MATCHING TIMESTAMPS
```python
from datetime import datetime

# Create timestamp ONCE
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Use for all three files
word_file = f"reports/patient_screening_{timestamp}.docx"
excel_file = f"reports/patient_screening_{timestamp}.xlsx"
pdf_file = f"reports/patient_screening_{timestamp}.pdf"

# Now all files have matching names!
```

---

## 🎨 HEALTHCARE COLOR SCHEME

### CONSISTENT COLORS ACROSS ALL FORMATS
```python
# WORD (RGB)
from docx.shared import RGBColor
high_risk_word = RGBColor(255, 0, 0)
medium_risk_word = RGBColor(255, 165, 0)
low_risk_word = RGBColor(0, 128, 0)

# EXCEL (HEX)
from openpyxl.styles import PatternFill
high_risk_excel = PatternFill(start_color="FFE6E6", end_color="FFE6E6", fill_type="solid")
medium_risk_excel = PatternFill(start_color="FFF4E6", end_color="FFF4E6", fill_type="solid")
low_risk_excel = PatternFill(start_color="E6FFE6", end_color="E6FFE6", fill_type="solid")

# PDF (HEX)
from reportlab.lib import colors
high_risk_pdf = colors.HexColor('#ffcccc')
medium_risk_pdf = colors.HexColor('#ffe6cc')
low_risk_pdf = colors.HexColor('#ccffcc')
```

---

## 🗂️ FILE ORGANIZATION

### RECOMMENDED STRUCTURE
```
project/
├── scripts/
│   ├── word_generator.py
│   ├── excel_generator.py
│   ├── pdf_generator.py
│   └── generate_all_reports.py  ← Combined workflow
├── reports/
│   ├── patient_screening_20260211_122137.docx
│   ├── patient_screening_20260211_122137.xlsx
│   └── patient_screening_20260211_122137.pdf
└── data/
    └── patients.csv
```

### NAMING CONVENTION
```python
# Format: {purpose}_{timestamp}.{extension}
# Example: patient_screening_20260211_122137.docx

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f"patient_screening_{timestamp}.docx"

# Benefits:
# - Sorts chronologically
# - No overwrites
# - Easy to find latest
# - Audit trail
```

---

## 🐛 COMMON ERRORS & SOLUTIONS

### Error: "No module named 'docx'"
```bash
# Solution: Install library
pip install python-docx
```

### Error: "FileNotFoundError: patients.csv"
```bash
# Solution: Run from project root, not from scripts/
cd "E:\Mindbridge health care"
python scripts\word_generator.py  # ✅ Correct
```

### Error: "Permission denied"
```python
# Solution: Close the file before running script
# Word/Excel/PDF must not be open when saving
```

### Error: Colors not showing in Excel
```python
# Solution: Use PatternFill, not Font color for backgrounds
from openpyxl.styles import PatternFill
cell.fill = PatternFill(start_color="FFE6E6", 
                        end_color="FFE6E6", 
                        fill_type="solid")
```

---

## 💡 PRO TIPS

### TIP 1: Always Close Files Before Regenerating
- Word/Excel/PDF locks file when open
- Close before running script
- Or use different filename

### TIP 2: Use Matching Timestamps
- Create timestamp once
- Use for all three formats
- Ensures consistency

### TIP 3: Test with Small Data First
- Use 2-3 patients for testing
- Faster iteration
- Easier to spot errors

### TIP 4: Separate Analysis from Formatting
- Analyze data once
- Format in multiple ways
- Reuse analysis results

### TIP 5: Create Template Functions
- Write once, reuse everywhere
- Example: `format_header()`, `add_patient_section()`
- Consistency across documents

---

## 📚 QUICK REFERENCE CHEAT SHEET

### WORD
```python
from docx import Document
doc = Document()
doc.add_heading('Title', 0)
doc.add_paragraph('Text')
doc.save('file.docx')
```

### EXCEL
```python
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws['A1'] = 'Data'
wb.save('file.xlsx')
```

### PDF
```python
from reportlab.platypus import SimpleDocTemplate
doc = SimpleDocTemplate("file.pdf")
elements = []
doc.build(elements)
```

---

## 🎯 WHEN TO USE WHAT

**Need editing?** → Word
**Need sorting?** → Excel
**Need printing?** → PDF
**Need everything?** → All three!

---

**END OF REFERENCE SHEET**
```

**STEP 3: Save as:**
- **Filename:** `document_generation_reference.md`
- **Location:** `E:\Mindbridge health care\references\`
- **Save as type:** All Files

---

## ✅ NOW YOU HAVE 5 REFERENCE SHEETS!
```
E:\Mindbridge health care\references\
├── python_essentials_reference.md       ← Day 2
├── cli_commands_reference.md            ← Day 2
├── architecture_patterns_reference.md   ← Day 2
├── staying_current_guide.md             ← Day 2
└── document_generation_reference.md     ← NEW! Day 3