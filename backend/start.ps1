# PowerShell script to start the backend server
# Usage: .\start.ps1

Write-Host "🚀 Starting AI Textbook Backend Server..." -ForegroundColor Cyan

# Check if virtual environment exists
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "✓ Activating virtual environment..." -ForegroundColor Green
    & .\venv\Scripts\Activate.ps1
} else {
    Write-Host "⚠ Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv venv
    & .\venv\Scripts\Activate.ps1
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

# Start the server
Write-Host "🌐 Starting server on http://localhost:8001" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
