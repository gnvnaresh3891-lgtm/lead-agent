# Automated Deployment Script for Lead Qualification & SDR Agent

Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  Lead SDR Agent Platform — Cloud Deployment Helper  " -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

# Check if authenticated with GitHub
$ghStatus = & "C:\Program Files\GitHub CLI\gh.exe" auth status 2>&1
if ($ghStatus -like "*not logged into*") {
    Write-Host "Step 1: Logging into GitHub CLI..." -ForegroundColor Yellow
    & "C:\Program Files\GitHub CLI\gh.exe" auth login --web -h github.com
}

# Create GitHub Repo and Push
Write-Host ""
Write-Host "Step 2: Creating GitHub Repository and Pushing Code..." -ForegroundColor Yellow
& "C:\Program Files\GitHub CLI\gh.exe" repo create lead-agent --public --source=. --remote=origin --push

Write-Host ""
Write-Host "Step 3: Opening Cloud Provider Setup Pages in your Browser..." -ForegroundColor Green

# Open Render Blueprint Page
Start-Process "https://dashboard.render.com/select-repo?type=blueprint"

# Open Vercel Import Page
Start-Process "https://vercel.com/new"

Write-Host ""
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  Setup Links Opened! Follow instructions on browser. " -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
