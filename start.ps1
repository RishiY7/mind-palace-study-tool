# Mind Palace - Quick Start Script

Write-Host "🧠 Mind Palace - AI-Powered Learning Platform" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check if MongoDB is running
Write-Host "📊 Checking MongoDB..." -ForegroundColor Yellow
$mongoProcess = Get-Process mongod -ErrorAction SilentlyContinue

if ($null -eq $mongoProcess) {
    Write-Host "❌ MongoDB is not running!" -ForegroundColor Red
    Write-Host "Please start MongoDB before running the application." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To start MongoDB, run:" -ForegroundColor Yellow
    Write-Host "  mongod --dbpath <your-data-path>" -ForegroundColor White
    Write-Host ""
    exit 1
} else {
    Write-Host "✅ MongoDB is running" -ForegroundColor Green
}

# Check if .env file exists
Write-Host "🔑 Checking environment configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "Please create a .env file with your configuration." -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "✅ Environment file found" -ForegroundColor Green
}

# Check if requirements are installed
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import streamlit; import pymongo; import google.generativeai; import PyPDF2" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ All dependencies installed" -ForegroundColor Green
    } else {
        throw "Dependencies missing"
    }
} catch {
    Write-Host "⚠️ Some dependencies may be missing" -ForegroundColor Yellow
    Write-Host "Installing requirements..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "🚀 Starting Mind Palace..." -ForegroundColor Green
Write-Host ""

# Start Streamlit
streamlit run app.py
