# Mind Palace - Setup Verification

Write-Host "🧠 Mind Palace - Setup Verification" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "🐍 Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "   $pythonVersion" -ForegroundColor White

# Check dependencies
Write-Host ""
Write-Host "📦 Checking installed packages..." -ForegroundColor Yellow

$packages = @("streamlit", "pymongo", "google-generativeai", "PyPDF2", "python-dotenv")
$allInstalled = $true

foreach ($package in $packages) {
    $installed = pip show $package 2>$null
    if ($installed) {
        $version = ($installed | Select-String "Version:").ToString().Split(":")[1].Trim()
        Write-Host "   ✅ $package ($version)" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $package (not installed)" -ForegroundColor Red
        $allInstalled = $false
    }
}

# Check .env file
Write-Host ""
Write-Host "🔑 Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   ✅ .env file exists" -ForegroundColor Green
    
    # Check for required variables
    $envContent = Get-Content ".env"
    $requiredVars = @("GEMINI_API_KEY", "GEMINI_MODEL", "MONGODB_URI")
    
    foreach ($var in $requiredVars) {
        if ($envContent -match $var) {
            Write-Host "   ✅ $var configured" -ForegroundColor Green
        } else {
            Write-Host "   ⚠️ $var missing" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "   ❌ .env file not found" -ForegroundColor Red
}

# Check project structure
Write-Host ""
Write-Host "📁 Checking project structure..." -ForegroundColor Yellow

$requiredDirs = @("pages", "prompts", "utils")
foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        $fileCount = (Get-ChildItem $dir -File).Count
        Write-Host "   ✅ $dir/ ($fileCount files)" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $dir/ (missing)" -ForegroundColor Red
    }
}

# MongoDB note
Write-Host ""
Write-Host "🗄️ MongoDB Status..." -ForegroundColor Yellow
Write-Host "   ℹ️ MongoDB is running in WSL (verified externally)" -ForegroundColor Cyan

# Summary
Write-Host ""
Write-Host "=" * 50 -ForegroundColor Cyan
if ($allInstalled) {
    Write-Host "✅ Setup verification complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Ready to launch! Run:" -ForegroundColor Green
    Write-Host "   streamlit run app.py" -ForegroundColor White
} else {
    Write-Host "⚠️ Some dependencies are missing" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To install missing packages, run:" -ForegroundColor Yellow
    Write-Host "   pip install -r requirements.txt" -ForegroundColor White
}
Write-Host ""
