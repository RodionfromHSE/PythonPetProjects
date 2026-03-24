$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$StudyBotDir = Split-Path -Parent $ScriptDir

Write-Output "Starting Leitner System..."
Set-Location $StudyBotDir
uv run python main.py
Write-Output "Leitner System Finished."
