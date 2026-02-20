# MindBridge Health AI - Folder Reorganizer
# Run from: E:\Mindbridge health care\

$root = "E:\Mindbridge health care"
Set-Location $root

Write-Host "MindBridge Folder Reorganizer Starting..." -ForegroundColor Cyan

# Create all folders
$folders = @(
    "docs\architecture",
    "docs\onboarding",
    "docs\schedule",
    "docs\compliance",
    "docs\api",
    "backend\app\routers",
    "backend\app\models",
    "backend\app\services",
    "backend\app\ai",
    "frontend\patient-portal",
    "frontend\staff-dashboard",
    "frontend\demos",
    "database\migrations",
    "database\seeds",
    "infrastructure\aws",
    "portfolio",
    "reference"
)

foreach ($f in $folders) {
    $full = Join-Path $root $f
    if (-not (Test-Path $full)) {
        New-Item -ItemType Directory -Path $full -Force | Out-Null
        Write-Host "Created folder: $f" -ForegroundColor Green
    }
}

# Move onboarding files
$onboarding = @(
    "WEEK_1_ONBOARDING_COMPLETE_G*",
    "WEEK_2_ONBOARDING_COMPLETE_G*",
    "WEEK1_DAY6_SUMMARY.md",
    "DAY_6_SETUP_GUIDE.md",
    "Week_2_Starter.txt",
    "WEEKEND_SETUP_INSTRUCTIONS.md"
)

foreach ($pattern in $onboarding) {
    Get-ChildItem -Path $root -Filter $pattern -File | ForEach-Object {
        Move-Item $_.FullName "$root\docs\onboarding\$($_.Name)" -Force
        Write-Host "Moved to onboarding: $($_.Name)" -ForegroundColor Yellow
    }
}

# Move schedule files
Get-ChildItem -Path $root -Filter "MINDBRIDGE_COMPLETE_SCHEDULE*" -File | ForEach-Object {
    Move-Item $_.FullName "$root\docs\schedule\$($_.Name)" -Force
    Write-Host "Moved to schedule: $($_.Name)" -ForegroundColor Yellow
}

Get-ChildItem -Path $root -Filter "MindBridge_Health_Complete_Cal*" -File | ForEach-Object {
    Move-Item $_.FullName "$root\docs\schedule\$($_.Name)" -Force
    Write-Host "Moved to schedule: $($_.Name)" -ForegroundColor Yellow
}

# Move scripts
$scriptFiles = @("mentor.bat", "setup_daily_quiz.ps1")
foreach ($f in $scriptFiles) {
    $src = Join-Path $root $f
    if (Test-Path $src) {
        Move-Item $src "$root\scripts\$f" -Force
        Write-Host "Moved to scripts: $f" -ForegroundColor Yellow
    }
}

# Move simulation lab
$simSrc = Join-Path $root "simulation_lab.html"
if (Test-Path $simSrc) {
    Move-Item $simSrc "$root\frontend\demos\simulation_lab.html" -Force
    Write-Host "Moved to frontend/demos: simulation_lab.html" -ForegroundColor Yellow
}

# Move Reference Sheets contents into reference\
$refSrc = Join-Path $root "Reference Sheets"
if (Test-Path $refSrc) {
    Get-ChildItem -Path $refSrc | ForEach-Object {
        Move-Item $_.FullName "$root\reference\$($_.Name)" -Force
        Write-Host "Moved to reference: $($_.Name)" -ForegroundColor Yellow
    }
    Remove-Item $refSrc -Force -ErrorAction SilentlyContinue
    Write-Host "Removed empty folder: Reference Sheets" -ForegroundColor DarkGray
}

# Create starter files
$mainPy = "$root\backend\app\main.py"
if (-not (Test-Path $mainPy)) {
    Set-Content $mainPy "from fastapi import FastAPI`n`napp = FastAPI(title='MindBridge Health AI', version='0.1.0')"
    Write-Host "Created: backend/app/main.py" -ForegroundColor Green
}

$claudePy = "$root\backend\app\ai\claude_client.py"
if (-not (Test-Path $claudePy)) {
    Set-Content $claudePy "# Claude API Integration - Week 2"
    Write-Host "Created: backend/app/ai/claude_client.py" -ForegroundColor Green
}

$reqs = "$root\backend\requirements.txt"
if (-not (Test-Path $reqs)) {
    Set-Content $reqs "fastapi`nuvicorn`npsycopg2-binary`nsqlalchemy`nanthropic`npython-dotenv"
    Write-Host "Created: backend/requirements.txt" -ForegroundColor Green
}

$envExample = "$root\.env.example"
if (-not (Test-Path $envExample)) {
    Set-Content $envExample "DATABASE_URL=postgresql://user:password@localhost:5432/mindbridge`nANTHROPIC_API_KEY=your_key_here`nSECRET_KEY=your_secret_here`nENVIRONMENT=development"
    Write-Host "Created: .env.example" -ForegroundColor Green
}

$hipaa = "$root\docs\compliance\hipaa-checklist.md"
if (-not (Test-Path $hipaa)) {
    Set-Content $hipaa "# HIPAA Technical Safeguards Checklist`n- [ ] Encryption at rest (AES-256)`n- [ ] Encryption in transit (TLS 1.3)`n- [ ] Automatic logoff`n- [ ] Unique user identification`n- [ ] Audit controls"
    Write-Host "Created: docs/compliance/hipaa-checklist.md" -ForegroundColor Green
}

$portfolio = "$root\portfolio\project-overview.md"
if (-not (Test-Path $portfolio)) {
    Set-Content $portfolio "# MindBridge Health AI`n## Healthcare AI Engineer Portfolio Project`n- FastAPI + PostgreSQL + Claude API`n- HIPAA Compliant Architecture`n- FHIR R4 Data Standard"
    Write-Host "Created: portfolio/project-overview.md" -ForegroundColor Green
}

# Final summary
Write-Host ""
Write-Host "DONE! Top-level structure:" -ForegroundColor Cyan
Get-ChildItem -Path $root -Depth 0 | Sort-Object PSIsContainer -Descending | ForEach-Object {
    if ($_.PSIsContainer) {
        Write-Host "  [DIR]  $($_.Name)" -ForegroundColor Blue
    } else {
        Write-Host "  [FILE] $($_.Name)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Next: Copy mindbridge-architecture.jsx into docs\architecture\" -ForegroundColor Cyan
