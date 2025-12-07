# PowerShell script to set up virtual environment and install dependencies
# Usage: .\runme.ps1

Write-Host "===================================" -ForegroundColor Cyan
Write-Host "Setting up Python Virtual Environment" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan

# Step 1: Create virtual environment
Write-Host "`nStep 1: Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Skipping creation." -ForegroundColor Green
} else {
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Virtual environment created successfully." -ForegroundColor Green
    } else {
        Write-Host "Failed to create virtual environment." -ForegroundColor Red
        exit 1
    }
}

# Step 2: Activate virtual environment
Write-Host "`nStep 2: Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "Virtual environment activated." -ForegroundColor Green

# Step 3: Upgrade pip
Write-Host "`nStep 3: Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Step 4: Install requirements
Write-Host "`nStep 4: Installing dependencies from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n===================================" -ForegroundColor Cyan
    Write-Host "Setup completed successfully!" -ForegroundColor Green
    Write-Host "===================================" -ForegroundColor Cyan
    Write-Host "`nTo activate the virtual environment in the future, run:" -ForegroundColor Yellow
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "`nTo deactivate, run:" -ForegroundColor Yellow
    Write-Host "  deactivate" -ForegroundColor White
} else {
    Write-Host "`nSetup failed. Please check the errors above." -ForegroundColor Red
    exit 1
}
