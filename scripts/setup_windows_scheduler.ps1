$TaskName = "InfogenX_Auto_Client_Acquisition"
$Action = New-ScheduledTaskAction -Execute "python.exe" -Argument "d:\infonix\scripts\auto_daemon_engine.py" -WorkingDirectory "d:\infonix"
$Trigger = New-ScheduledTaskTrigger -AtStartup
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "Automated 100% Background Client Acquisition Engine for Mohamed Yasar" -User "NT AUTHORITY\SYSTEM" -ErrorAction SilentlyContinue

Write-Host "  [🎉] Windows Task Scheduler Automation Successfully Configured for '$TaskName'!"
