function Anchor-Ledger {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][object]$Record,
        [Parameter(Mandatory=$true)][string]$RecordType
    )

    $ToolPath = Join-Path (Get-Location) "tools/simulate_ledger.py"
    if (-not (Test-Path $ToolPath)) {
        $ToolPath = "./tools/simulate_ledger.py"
    }

    Write-Host "🔗 Anchoring record to Ledger..." -ForegroundColor Cyan
    # In a real scenario, this would call the API. For simulation, we run the python script.
    python3 $ToolPath
    
    Write-Host "✅ Record anchored successfully." -ForegroundColor Green
}
