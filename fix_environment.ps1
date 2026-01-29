Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "   AI Stock Platform - Environment Fix Script" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Kill any process on Port 8000
Write-Host "[Step 1/4] Checking for processes on Port 8000..." -ForegroundColor Yellow
$port8000 = netstat -ano | findstr :8000 | findstr LISTENING
if ($port8000) {
    $process_id = ($port8000 -split '\s+')[-1]
    Write-Host "   Found process $process_id on port 8000. Killing it..." -ForegroundColor Red
    taskkill /PID $process_id /F
    Start-Sleep -Seconds 2
    Write-Host "   [OK] Port 8000 cleared" -ForegroundColor Green
}
else {
    Write-Host "   [OK] Port 8000 is free" -ForegroundColor Green
}
Write-Host ""

# 2. Activate Virtual Environment
Write-Host "[Step 2/4] Activating virtual environment..." -ForegroundColor Yellow
$venvPath = "C:\infosys1\AI-powered-stock-and-ETF-trading-platform\venv\Scripts\Activate.ps1"

if (Test-Path $venvPath) {
    & $venvPath
    Write-Host "   [OK] Virtual environment activated" -ForegroundColor Green
}
else {
    Write-Host "   [ERROR] ERROR: Virtual environment not found at $venvPath" -ForegroundColor Red
    Write-Host "   Creating new virtual environment..." -ForegroundColor Yellow
    python -m venv "C:\infosys1\AI-powered-stock-and-ETF-trading-platform\venv"
    & $venvPath
    Write-Host "   [OK] New virtual environment created and activated" -ForegroundColor Green
}
Write-Host ""

# 3. Force Install Required Packages
Write-Host "[Step 3/4] Installing required packages..." -ForegroundColor Yellow
Write-Host "   This may take a few minutes..." -ForegroundColor Gray

$packages = @(
    "xgboost",
    "pandas",
    "numpy",
    "scikit-learn",
    "requests",
    "fastapi",
    "uvicorn[standard]",
    "yfinance",
    "pydantic",
    "joblib"
)

foreach ($package in $packages) {
    Write-Host "   Installing $package..." -ForegroundColor Gray
    python -m pip install --upgrade --force-reinstall $package --quiet
}

Write-Host "   [OK] All packages installed" -ForegroundColor Green
Write-Host ""

# 4. Verify Installation
Write-Host "[Step 4/4] Verifying installation..." -ForegroundColor Yellow

$testScript = @"
import sys
try:
    import xgboost
    import pandas
    import sklearn
    import requests
    import fastapi
    import yfinance
    print('[OK] All modules imported successfully')
    print(f'  - xgboost: {xgboost.__version__}')
    print(f'  - pandas: {pandas.__version__}')
    print(f'  - scikit-learn: {sklearn.__version__}')
    sys.exit(0)
except ImportError as e:
    print(f'[ERROR] Import failed: {e}')
    sys.exit(1)
"@

$testScript | python

if ($LASTEXITCODE -eq 0) {
    Write-Host "   [OK] Verification successful" -ForegroundColor Green
}
else {
    Write-Host "   [ERROR] Verification failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "   Environment Setup Complete!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Start the API: .\venv\Scripts\python.exe scripts\run_api.py" -ForegroundColor White
Write-Host "  2. Start the Dashboard: .\venv\Scripts\python.exe -m streamlit run 0_Overview.py" -ForegroundColor White
Write-Host ""
