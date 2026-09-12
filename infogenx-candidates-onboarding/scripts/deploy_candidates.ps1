# Candidates Portal One-Click Deployment Script
param (
    [string]$ServerIP = "209.182.232.150",
    [string]$SiteUser = "infogenx-candidates",
    [string]$SitePass = "infogenx@1234",
    [string]$Domain = "candidates.infogenx.com"
)

$baseDir = Split-Path -Parent $PSScriptRoot
$frontendDir = "$baseDir\frontend"
if (-not (Test-Path "$frontendDir\package.json")) {
    $frontendDir = $baseDir
}

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Infogenx Candidates Portal Deployment Tool" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Target Domain : $Domain" -ForegroundColor Green
Write-Host "Server Host   : $ServerIP" -ForegroundColor Green
Write-Host "Site User     : $SiteUser" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan

# Step 1: Install & Build
Write-Host "1. Checking dependencies and building bundle (dist)..." -ForegroundColor Yellow
Push-Location $frontendDir
if (-not (Test-Path "$frontendDir\node_modules")) {
    Write-Host "Installing dependencies in frontend..." -ForegroundColor Cyan
    & npm install
}
& npm run build
Pop-Location

if (-not (Test-Path "$frontendDir\dist\index.html")) {
    Write-Host "Build failed! index.html not found in dist." -ForegroundColor Red
    exit 1
}

# Step 2: SCP Upload
Write-Host "2. Uploading files to server via SCP..." -ForegroundColor Yellow
$remotePath = "/home/$SiteUser/htdocs/$Domain/dist/"
$pscpCmd = "echo y | pscp -batch -r -scp -pw `"$SitePass`" `"$frontendDir\dist\*`" $SiteUser@${ServerIP}:$remotePath"
Invoke-Expression $pscpCmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: Candidates Portal deployed to https://$Domain/" -ForegroundColor Green
} else {
    Write-Host "Deployment failed!" -ForegroundColor Red
}
