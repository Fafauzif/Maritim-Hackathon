# Phase 04-05 render orchestration. Headless, sequential, logged.
$ErrorActionPreference = 'Continue'
$root = "C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon"
$blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
$scripts = Join-Path $root "3d-art\work\scripts\render_pass.py"
$ck = Join-Path $root "3d-art\work\checkpoints"
$log = Join-Path $root "3d-art\work\logs\render-job.log"

function Log($msg) {
    $line = "$(Get-Date -Format 'HH:mm:ss') $msg"
    Add-Content -Path $log -Value $line
    Write-Output $line
}

Log "=== render job start ==="

foreach ($site in @('tunda', 'amur')) {
    Log "stills $site"
    & $blender -b (Join-Path $ck "03-$site.blend") --python $scripts -- stills $site 2>&1 |
        Select-String -Pattern "STILLS|Traceback|Error" | ForEach-Object { Log $_.ToString() }
}

foreach ($site in @('kodingareng', 'tunda', 'amur')) {
    Log "beforeafter $site"
    & $blender -b (Join-Path $ck "03-$site.blend") --python $scripts -- beforeafter $site 2>&1 |
        Select-String -Pattern "BEFOREAFTER|Traceback|Error" | ForEach-Object { Log $_.ToString() }
}

Log "globe stills"
& $blender -b (Join-Path $ck "04-globe.blend") --python $scripts -- globe 2>&1 |
    Select-String -Pattern "GLOBE|Traceback|Error" | ForEach-Object { Log $_.ToString() }

Log "globe reel frames"
& $blender -b (Join-Path $ck "04-globe.blend") --python $scripts -- reel 2>&1 |
    Select-String -Pattern "REEL|Traceback|Error" | ForEach-Object { Log $_.ToString() }

foreach ($site in @('kodingareng', 'tunda', 'amur')) {
    Log "travel frames $site"
    & $blender -b (Join-Path $ck "04-travel-$site.blend") -a 2>&1 |
        Select-String -Pattern "Saved:|Traceback|Error" | Select-Object -Last 3 | ForEach-Object { Log $_.ToString() }
}

Log "=== render job done ==="
