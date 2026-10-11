@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "TOOL=%SCRIPT_DIR%pdf_merge_tool.pyw"

where pythonw >nul 2>nul
if %errorlevel%==0 (
    start "" pythonw "%TOOL%"
    exit /b 0
)

where python >nul 2>nul
if %errorlevel%==0 (
    start "" python "%TOOL%"
    exit /b 0
)

echo Python was not found in PATH.
pause
