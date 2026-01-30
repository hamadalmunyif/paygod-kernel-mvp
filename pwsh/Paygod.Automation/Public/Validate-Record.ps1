function Validate-Record {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][string]$SchemaPath,
        [Parameter(Mandatory=$true)][string]$JsonPath
    )

    $ToolPath = Join-Path (Get-Location) "tools/validate.py"
    if (-not (Test-Path $ToolPath)) {
        # Fallback if running from root
        $ToolPath = "./tools/validate.py"
    }

    try {
        # Delegate to strict Python validator
        $result = python3 $ToolPath --schema $SchemaPath --instance $JsonPath
        $json = $result | ConvertFrom-Json
        
        if ($json.valid -eq $true) {
            Write-Host "✅ VALID: $JsonPath" -ForegroundColor Green
        } else {
            Write-Error "❌ INVALID: $JsonPath"
            Write-Error ($json | ConvertTo-Json -Depth 5)
            throw "ValidationFailed"
        }
    }
    catch {
        Write-Error "Validation execution failed: $_"
        throw
    }
}
