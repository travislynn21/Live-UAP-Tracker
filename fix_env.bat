@echo off
echo Searching for python.exe...

set "P1=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
set "P2=%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe"
set "P3=C:\Windows\py.exe"
set "P4=python.exe"

set "FOUND_PYTHON="

if exist "%P1%" set "FOUND_PYTHON=%P1%"
if not defined FOUND_PYTHON if exist "%P2%" set "FOUND_PYTHON=%P2%"
if not defined FOUND_PYTHON if exist "%P3%" set "FOUND_PYTHON=%P3%"

if defined FOUND_PYTHON (
    echo Found python at: %FOUND_PYTHON%
    "%FOUND_PYTHON%" -m pip install numpy folium
    "%FOUND_PYTHON%" uaps_found.py
    echo Map successfully generated.
) else (
    echo Python not found manually, attempting global command...
    python -m pip install numpy folium
    python uaps_found.py
)
