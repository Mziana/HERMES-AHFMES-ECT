# One-Click PowerShell Launcher for Hermes Studio Control Center
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " 🚀 LAUNCHING HERMES STUDIO (EXTERNAL COGNITIVE TANDEM V0.3)" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

# 1. Ensure storage directory exists in Drive D
$StorageDir = "D:\Hermes\HERMES-AHFMES-ECT\storage"
if (!(Test-Path -Path $StorageDir)) {
    New-Item -ItemType Directory -Path $StorageDir -Force | Out-Null
}
Write-Host "[1/3] Local Storage DB Verified: $StorageDir\hermes_studio.db" -ForegroundColor Green

# 2. Start FastAPI Backend Server
Write-Host "[2/3] Starting FastAPI Backend API Server on http://127.0.0.1:8000..." -ForegroundColor Yellow
$BackendProcess = Start-Process python -ArgumentList "STUDIO/backend/main.py" -PassThru -WindowStyle Hidden

# 3. Check Frontend Node Modules & Start Vite Dev Server
Set-Location -Path "STUDIO/frontend"
if (!(Test-Path -Path "node_modules")) {
    Write-Host "[Frontend] Installing npm packages (first time setup)..." -ForegroundColor Yellow
    cmd /c npm install
}

Write-Host "[3/3] Starting Hermes Studio Web App on http://localhost:3000..." -ForegroundColor Green
Start-Sleep -Seconds 2
Start-Process "http://localhost:3000"

cmd /c npm run dev
