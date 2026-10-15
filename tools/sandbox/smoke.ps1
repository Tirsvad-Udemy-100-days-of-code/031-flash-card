<#
.SYNOPSIS
  Smoke test of flash-card.exe, run INSIDE Windows Sandbox (ADR-0005).

.DESCRIPTION
  Starts the executable on the sandbox's own desktop, presses the known button
  with the sandbox's own mouse, reads the progress file, takes screenshots and
  writes result.json to C:\fc\out. Then it shuts the sandbox down.
  It never touches the host: the host sees only the mapped folders.
#>
param(
    [int]$Runs = 5,
    [string]$Exe = 'C:\fc\dist\flash-card.exe',
    [string]$Out = 'C:\fc\out'
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Text;
using System.Runtime.InteropServices;
public static class Win {
    public delegate bool EnumProc(IntPtr h, IntPtr l);
    [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc p, IntPtr l);
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
    [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr h, out RECT r);
    [DllImport("user32.dll")] public static extern bool ClientToScreen(IntPtr h, ref POINT p);
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
    [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint x, uint y, uint d, UIntPtr e);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
    [DllImport("shcore.dll")] public static extern int SetProcessDpiAwareness(int v);
    [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
    [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X, Y; }
    public static IntPtr Find(string title) {
        IntPtr found = IntPtr.Zero;
        EnumWindows(delegate (IntPtr h, IntPtr l) {
            if (IsWindowVisible(h)) {
                var sb = new StringBuilder(256);
                GetWindowText(h, sb, 256);
                if (sb.ToString() == title) { found = h; return false; }
            }
            return true;
        }, IntPtr.Zero);
        return found;
    }
}
'@
[void][Win]::SetProcessDpiAwareness(2)

function Wait-Window([int]$Seconds) {
    $end = (Get-Date).AddSeconds($Seconds)
    while ((Get-Date) -lt $end) {
        $h = [Win]::Find('Flashy')
        if ($h -ne [IntPtr]::Zero) { return $h }
        Start-Sleep -Milliseconds 250
    }
    return [IntPtr]::Zero
}

function Save-Screen([string]$Path) {
    $b = [System.Windows.Forms.SystemInformation]::VirtualScreen
    $bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($b.Left, $b.Top, 0, 0, $bmp.Size)
    $bmp.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose()
}
Add-Type -AssemblyName System.Windows.Forms

$work = Join-Path $env:TEMP 'fc-smoke'
$results = @()
for ($n = 1; $n -le $Runs; $n++) {
    $run = [ordered]@{ run = $n; window = $false; clicked = $false; progress_rows = $null; ok = $false; seconds = 0 }
    $t0 = Get-Date
    $dir = Join-Path $work "run$n"
    Remove-Item $dir -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Path (Join-Path $dir 'data') -Force | Out-Null
    Copy-Item $Exe (Join-Path $dir 'flash-card.exe')
    # three words: after one known word the progress file has a header and two cards
    [IO.File]::WriteAllText((Join-Path $dir 'data\ms-da.csv'), "ms;da`naaa;bbb`nccc;ddd`neee;fff`n", (New-Object Text.UTF8Encoding $false))
    $p = Start-Process -FilePath (Join-Path $dir 'flash-card.exe') -ArgumentList '--level', 'all', '--no-speech' -WorkingDirectory $dir -PassThru
    try {
        $h = Wait-Window 60
        if ($h -ne [IntPtr]::Zero) {
            $run.window = $true
            Start-Sleep -Milliseconds 1500
            if ($n -eq 1) { Save-Screen (Join-Path $Out 'sandbox-card.png') }
            $r = New-Object Win+RECT
            [void][Win]::GetClientRect($h, [ref]$r)
            $pt = New-Object Win+POINT
            [void][Win]::ClientToScreen($h, [ref]$pt)
            $x = $pt.X + 650
            $y = $pt.Y + $r.Bottom - 101
            [void][Win]::SetForegroundWindow($h)
            Start-Sleep -Milliseconds 400
            [void][Win]::SetCursorPos($x - 12, $y - 12)
            Start-Sleep -Milliseconds 300
            [void][Win]::SetCursorPos($x, $y)
            Start-Sleep -Milliseconds 400
            [Win]::mouse_event(0x0002, 0, 0, 0, [UIntPtr]::Zero)
            Start-Sleep -Milliseconds 120
            [Win]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
            $run.clicked = $true
            $prog = Join-Path $dir 'data\words_to_learn.csv'
            $end = (Get-Date).AddSeconds(6)
            while ((Get-Date) -lt $end -and -not (Test-Path $prog)) { Start-Sleep -Milliseconds 250 }
            if (Test-Path $prog) {
                $rows = ([IO.File]::ReadAllLines($prog) | Where-Object { $_.Trim() -ne '' }).Count
                $run.progress_rows = $rows
                $run.ok = ($rows -eq 3)
            }
        }
    }
    finally {
        if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue }
        Get-Process -Name 'flash-card' -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    }
    $run.seconds = [math]::Round(((Get-Date) - $t0).TotalSeconds, 1)
    $results += [pscustomobject]$run
    Start-Sleep -Seconds 1
}

$summary = [ordered]@{
    runs    = $Runs
    passed  = ($results | Where-Object { $_.ok }).Count
    os      = (Get-CimInstance Win32_OperatingSystem).Caption
    results = $results
}
$summary | ConvertTo-Json -Depth 5 | Set-Content -Path (Join-Path $Out 'result.json') -Encoding UTF8
shutdown.exe /s /t 5
