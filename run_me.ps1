$ErrorActionPreference = "Stop"
Write-Host "Locating Python installation..."

# List of probable python paths after a winget user scope install
$paths = @(
    "python.exe",
    "py.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    "$env:LOCALAPPDATA\Microsoft\WindowsApps\python.exe"
)

$found = $null

foreach ($p in $paths) {
    if (Get-Command $p -ErrorAction SilentlyContinue) {
        $found = (Get-Command $p).Source
        break
    } elseif (Test-Path $p) {
        $found = $p
        break
    }
}

if ($found) {
    Write-Host "Found Python at: $found"
    Write-Host "Installing dependencies..."
    & $found -m pip install numpy folium
    Write-Host "Running UAP analysis map generator..."
    & $found e:\Gdrive...+\trading_bot\backend\uaps_found.py
    Write-Host "Done! Check for test_uap_map.html"
} else {
    Write-Host "Python could not be located. Restart your terminal."
}
