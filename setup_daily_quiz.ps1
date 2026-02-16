# MindBridge Mentor - Windows Task Scheduler Setup
# This script creates a scheduled task to run the quiz daily at 8 AM

# Configuration
$TaskName = "MindBridge-Mentor-Daily-Quiz"
$TaskDescription = "Daily quiz reminder for MindBridge Healthcare AI training"
$ScriptPath = "E:\Mindbridge health care\agents\mentor\quiz.py"
$PythonPath = "python"  # Will use system Python
$TriggerTime = "8:00AM"

Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  MINDBRIDGE MENTOR - Task Scheduler Setup" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check if task already exists
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "⚠️  Task already exists: $TaskName" -ForegroundColor Yellow
    $Response = Read-Host "Do you want to replace it? (y/n)"
    
    if ($Response -eq "y") {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "✅ Old task removed" -ForegroundColor Green
    } else {
        Write-Host "❌ Setup cancelled" -ForegroundColor Red
        exit
    }
}

# Create the action (run Python script)
$Action = New-ScheduledTaskAction `
    -Execute $PythonPath `
    -Argument "$ScriptPath" `
    -WorkingDirectory "E:\Mindbridge health care"

# Create the trigger (daily at 8 AM)
$Trigger = New-ScheduledTaskTrigger -Daily -At $TriggerTime

# Create the principal (run whether user is logged on or not)
$Principal = New-ScheduledTaskPrincipal `
    -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType Interactive `
    -RunLevel Highest

# Create the settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30)

# Register the task
try {
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Description $TaskDescription `
        -Action $Action `
        -Trigger $Trigger `
        -Principal $Principal `
        -Settings $Settings `
        -ErrorAction Stop | Out-Null
    
    Write-Host ""
    Write-Host "✅ SUCCESS! Task created successfully" -ForegroundColor Green
    Write-Host ""
    Write-Host "📅 Schedule Details:" -ForegroundColor Cyan
    Write-Host "   Task Name: $TaskName"
    Write-Host "   Runs Daily: $TriggerTime"
    Write-Host "   Script: $ScriptPath"
    Write-Host ""
    Write-Host "🎯 Your quiz will now run automatically every day at 8 AM!"
    Write-Host ""
    Write-Host "💡 Useful Commands:" -ForegroundColor Cyan
    Write-Host "   • View task: Get-ScheduledTask -TaskName '$TaskName'"
    Write-Host "   • Test now: Start-ScheduledTask -TaskName '$TaskName'"
    Write-Host "   • Disable: Disable-ScheduledTask -TaskName '$TaskName'"
    Write-Host "   • Remove: Unregister-ScheduledTask -TaskName '$TaskName'"
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "❌ ERROR: Failed to create task" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)"
    Write-Host ""
    Write-Host "💡 Try running PowerShell as Administrator" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
