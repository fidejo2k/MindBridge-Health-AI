# MindBridge Health AI - Complete File Organizer
# Run from: E:\Mindbridge health care\

$root = "E:\Mindbridge health care"
Set-Location $root

Write-Host "🗂️  MindBridge Complete File Organizer" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

# Move documentation files to docs/
Write-Host "`n📄 Moving documentation files..." -ForegroundColor Yellow

$docFiles = @(
    "COMPLETE_ROADMAP.md",
    "COURSE_MATERIAL_ANALYSIS.md",
    "DOCKER_SETUP_GUIDE.md",
    "NEW_SIMULATION_SCENARIOS.md",
    "CLAUDE.md"
)

foreach ($file in $docFiles) {
    $src = Join-Path $root $file
    if (Test-Path $src) {
        Move-Item $src "$root\docs\$file" -Force
        Write-Host "  ✅ Moved to docs/: $file" -ForegroundColor Green
    }
}

# Move plan files to docs/schedule/
Write-Host "`n📅 Moving schedule files..." -ForegroundColor Yellow

$scheduleFiles = @(
    "DAY_9_PLAN.md"
)

foreach ($file in $scheduleFiles) {
    $src = Join-Path $root $file
    if (Test-Path $src) {
        Move-Item $src "$root\docs\schedule\$file" -Force
        Write-Host "  ✅ Moved to docs/schedule/: $file" -ForegroundColor Green
    }
}

# Move Python scripts to scripts/
Write-Host "`n🐍 Moving Python scripts..." -ForegroundColor Yellow

$scriptFiles = @(
    "setup_railway_mindbridge.py",
    "test_railway_connection.py",
    "test_docker_db.py",
    "generate_railway_report.py",
    "test_railway_simple.py",
    "organize_mindbridge.ps1"
)

foreach ($file in $scriptFiles) {
    $src = Join-Path $root $file
    if (Test-Path $src) {
        Move-Item $src "$root\scripts\$file" -Force
        Write-Host "  ✅ Moved to scripts/: $file" -ForegroundColor Green
    }
}

# Files that should STAY in root
Write-Host "`n✅ Files staying in root (correct location):" -ForegroundColor Cyan
$rootFiles = @(
    "README.md",
    "docker-compose.yml",
    ".gitignore",
    ".dockerignore",
    ".env.example"
)

foreach ($file in $rootFiles) {
    $src = Join-Path $root $file
    if (Test-Path $src) {
        Write-Host "  ✓ $file" -ForegroundColor Gray
    }
}

# Summary
Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "✅ ORGANIZATION COMPLETE!" -ForegroundColor Green
Write-Host ("=" * 70) -ForegroundColor Cyan

Write-Host "`n📊 Final root directory structure:" -ForegroundColor Cyan
Get-ChildItem -Path $root -Directory | Sort-Object Name | ForEach-Object {
    Write-Host "  📁 $($_.Name)" -ForegroundColor Blue
}

Write-Host "`n📄 Root files:" -ForegroundColor Cyan
Get-ChildItem -Path $root -File | Sort-Object Name | ForEach-Object {
    Write-Host "  📄 $($_.Name)" -ForegroundColor Gray
}

Write-Host "`n✅ Ready to commit to GitHub!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
