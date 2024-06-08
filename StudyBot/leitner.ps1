$root = "C:\Users\rodio\Desktop\Programming\Other"

Write-Output "Starting Leitner System..."
python "$root\PythonPetProjects\StudyBot\SmartishTerminal.py" `
    --config "$root\PythonPetProjects\StudyBot\config.yaml"
Write-Output "Leitner System Finished."
