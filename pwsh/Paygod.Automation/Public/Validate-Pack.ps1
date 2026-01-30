function Validate-Pack {
  [CmdletBinding()]
  param([Parameter(Mandatory=$true)][string]$PackPath)
  $t = Get-Content $PackPath -Raw
  if ($t -notmatch 'pack_id\s*:') { throw "pack_id missing" }
  if ($t -notmatch 'version\s*:') { throw "version missing" }
  Write-Host "OK: $PackPath"
}
