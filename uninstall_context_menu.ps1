$ErrorActionPreference = "Stop"

$baseKey = "HKCU\Software\Classes\SystemFileAssociations\.pdf\shell\PdfMergeTool"

reg delete $baseKey /f | Out-Null

Write-Host "Context menu removed successfully."
