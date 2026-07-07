$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CredentialsFile = Join-Path $ProjectDir "credentials.json"
$RequirementsFile = Join-Path $ProjectDir "requirements.txt"
$ScriptFile = Join-Path $ProjectDir "gmail_connect.py"

function Find-Python {
    $localPythonRoot = Join-Path $env:LOCALAPPDATA "Programs\Python"
    $installedPythons = @()
    if (Test-Path $localPythonRoot) {
        $installedPythons = Get-ChildItem -Path $localPythonRoot -Recurse -Filter python.exe -ErrorAction SilentlyContinue |
            Where-Object { $_.FullName -notmatch "\\Lib\\venv\\" } |
            Sort-Object FullName -Descending |
            ForEach-Object { $_.FullName }
    }

    $candidates = @($installedPythons) + @("python", "py")

    foreach ($candidate in $candidates) {
        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if (-not $command) {
            continue
        }

        try {
            $version = & $candidate --version 2>$null
            if ($LASTEXITCODE -eq 0 -and $version -match "Python 3") {
                return $candidate
            }
        }
        catch {
            continue
        }
    }

    return $null
}

Write-Host "Checking Gmail API connection setup..."

$python = Find-Python
if (-not $python) {
    Write-Host ""
    Write-Host "Python 3 is not available on this computer yet."
    Write-Host "Install it from https://www.python.org/downloads/windows/"
    Write-Host "During install, tick 'Add python.exe to PATH', then run this file again."
    exit 1
}

if (-not (Test-Path $CredentialsFile)) {
    Write-Host ""
    Write-Host "Missing credentials.json."
    Write-Host "Download an OAuth Desktop App JSON from Google Cloud Console,"
    Write-Host "rename it to credentials.json, and place it here:"
    Write-Host $ProjectDir
    exit 1
}

Write-Host "Installing Gmail API dependencies..."
& $python -m pip install -r $RequirementsFile

Write-Host ""
Write-Host "Starting Gmail authorization..."
& $python $ScriptFile
