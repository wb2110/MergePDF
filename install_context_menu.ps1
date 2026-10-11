$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$toolPath = Join-Path $scriptDir "pdf_merge_tool.pyw"

$python = Get-Command python.exe -ErrorAction SilentlyContinue
if (-not $python) {
    throw "python.exe was not found in PATH."
}

$pythonDir = Split-Path -Parent $python.Source
$pythonwPath = Join-Path $pythonDir "pythonw.exe"
if (-not (Test-Path $pythonwPath)) {
    $pythonwPath = $python.Source
}

$baseKey = "HKCU\Software\Classes\SystemFileAssociations\.pdf\shell\PdfMergeTool"
$command = '"' + $pythonwPath + '" "' + $toolPath + '" "%1"'

reg add $baseKey /ve /d "Merge PDFs" /f | Out-Null
reg add $baseKey /v "Icon" /t REG_SZ /d "shell32.dll,70" /f | Out-Null
reg add $baseKey /v "MultiSelectModel" /t REG_SZ /d "Player" /f | Out-Null
reg add $baseKey /v "Position" /t REG_SZ /d "Top" /f | Out-Null
reg add ($baseKey + "\command") /ve /d $command /f | Out-Null

Write-Host "Context menu installed successfully."
Write-Host "Right-click one or more PDF files and choose: Merge PDFs"
