param(
  [Parameter(Mandatory=$true)][string]$InputPath,
  [string]$RepoRoot = (Get-Location).Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Fail($code, $msg) {
  $o = [pscustomobject]@{ ok=$false; code=$code; message=$msg }
  $o | ConvertTo-Json -Depth 20
  exit 2
}

function Ok($msg) {
  $o = [pscustomobject]@{ ok=$true; message=$msg }
  $o | ConvertTo-Json -Depth 20
  exit 0
}

# ---------- Load input ----------
if (-not (Test-Path $InputPath)) { Fail "INPUT_MISSING" "Missing input: $InputPath" }
$raw = Get-Content $InputPath -Raw
try { $env = $raw | ConvertFrom-Json } catch { Fail "ENV_JSON_INVALID" "Invalid JSON envelope" }

# ---------- Gate 1: Envelope ----------
$allowedKinds = @("decision","evidence","ledger_entry")
if (-not $env) { Fail "ENV_MISSING" "Envelope missing" }

if (-not ($env.PSObject.Properties.Name -contains "kind")) { Fail "ENV_KIND_MISSING" "Missing kind" }
if ($allowedKinds -notcontains [string]$env.kind) { Fail "ENV_KIND_INVALID" "Invalid kind: $($env.kind)" }

if (-not ($env.PSObject.Properties.Name -contains "schema_version")) { Fail "ENV_SCHEMA_VERSION_MISSING" "Missing schema_version" }
if ([string]$env.schema_version -notmatch "^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$") {
  Fail "ENV_SCHEMA_VERSION_INVALID" "schema_version must be SemVer MAJOR.MINOR.PATCH"
}

$hasSchemaRef = ($env.PSObject.Properties.Name -contains "schema_ref") -and ([string]$env.schema_ref).Trim().Length -gt 0
$hasSchema    = ($env.PSObject.Properties.Name -contains "schema")     -and ([string]$env.schema).Trim().Length -gt 0
$hasSchemaId  = ($env.PSObject.Properties.Name -contains "schema_id")  -and ([string]$env.schema_id).Trim().Length -gt 0
if (-not ($hasSchemaRef -or $hasSchema -or $hasSchemaId)) {
  Fail "ENV_SCHEMA_REF_MISSING" "Need one of: schema_ref (preferred) | schema (legacy) | schema_id (legacy)"
}

if (-not ($env.PSObject.Properties.Name -contains "timestamp")) { Fail "ENV_TIMESTAMP_MISSING" "Missing timestamp" }
try { [DateTimeOffset]::Parse([string]$env.timestamp) | Out-Null } catch { Fail "ENV_TIMESTAMP_INVALID" "Invalid timestamp" }

if (-not ($env.PSObject.Properties.Name -contains "producer")) { Fail "ENV_PRODUCER_MISSING" "Missing producer" }
if (-not $env.producer.name -or -not $env.producer.version) { Fail "ENV_PRODUCER_INVALID" "producer.name and producer.version required" }

if (-not ($env.PSObject.Properties.Name -contains "data")) { Fail "ENV_DATA_MISSING" "Missing data" }

# ---------- Gate 2: Schema binding (Python jsonschema Draft 2020-12 with file registry) ----------
$schemaPath = switch ([string]$env.kind) {
  "decision"     { "contracts/schemas/decision.schema.json" }
  "evidence"     { "contracts/schemas/evidence.schema.json" }
  "ledger_entry" { "contracts/schemas/ledger_entry.schema.json" }
  default        { "" }
}
if (-not $schemaPath) { Fail "SCHEMA_NOT_FOUND" "No schema mapping for kind=$($env.kind)" }

$fullSchema = Join-Path $RepoRoot $schemaPath
if (-not (Test-Path $fullSchema)) { Fail "SCHEMA_NOT_FOUND" "Missing schema file: $schemaPath" }

$tmpPayload = New-TemporaryFile
try {
  # Write payload JSON (UTF-8)
  $payloadJson = ($env.data | ConvertTo-Json -Depth 50)
  [System.IO.File]::WriteAllText($tmpPayload.FullName, $payloadJson, (New-Object System.Text.UTF8Encoding($false)))

  # Build temp python validator (avoids -c quoting AND fixes local $ref by registry + $id injection)
  $pyTmp = New-TemporaryFile
  $pyPath = $pyTmp.FullName + ".py"
  Remove-Item $pyTmp.FullName -Force -ErrorAction SilentlyContinue

  $schemasDir = Join-Path $RepoRoot "contracts/schemas"

  $pyCode = @'
import json, sys, os
from pathlib import Path
from jsonschema import Draft202012Validator
import referencing
from referencing import Registry, Resource

schema_path = Path(sys.argv[1]).resolve()
payload_path = Path(sys.argv[2]).resolve()
schemas_dir  = Path(sys.argv[3]).resolve()

def file_uri(p: Path) -> str:
    # file:///C:/... with forward slashes
    return p.as_uri()

def load_json(p: Path):
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

# Preload all schemas in contracts/schemas into a registry, inject $id if missing.
reg = Registry()
if schemas_dir.exists():
    for p in schemas_dir.glob("*.json"):
        try:
            s = load_json(p)
        except Exception:
            continue
        uri = file_uri(p.resolve())
        if isinstance(s, dict) and "$id" not in s:
            s["$id"] = uri
        reg = reg.with_resource(uri, Resource.from_contents(s))

# Load the target schema and ensure it has a base $id so relative $ref works.
schema = load_json(schema_path)
schema_uri = file_uri(schema_path)
if isinstance(schema, dict) and "$id" not in schema:
    schema["$id"] = schema_uri
    reg = reg.with_resource(schema_uri, Resource.from_contents(schema))

payload = load_json(payload_path)

try:
    v = Draft202012Validator(schema, registry=reg)
    errs = sorted(v.iter_errors(payload), key=lambda e: list(e.path))
except Exception as e:
    out = {"ok": False, "code": "SCHEMA_VALIDATION_FAILED", "python_error": str(e)}
    print(json.dumps(out, ensure_ascii=False))
    sys.exit(2)

if errs:
    out = {"ok": False, "code": "SCHEMA_VALIDATION_FAILED", "errors": []}
    for e in errs[:20]:
        out["errors"].append({"path": "/" + "/".join([str(p) for p in e.path]), "message": e.message})
    print(json.dumps(out, ensure_ascii=False))
    sys.exit(2)

print(json.dumps({"ok": True, "code": "SCHEMA_OK"}, ensure_ascii=False))
'@

  [System.IO.File]::WriteAllText($pyPath, $pyCode, (New-Object System.Text.UTF8Encoding($false)))
$res = python -W ignore $pyPath $fullSchema $tmpPayload.FullName $schemasDir 2>&1
  if (-not $res) { Fail "SCHEMA_VALIDATION_FAILED" "Schema validation failed (no output)" }

  try { $r = ($res | Out-String | ConvertFrom-Json) } catch {
    Fail "SCHEMA_VALIDATION_FAILED" ("Python error: " + ($res | Out-String).Trim())
  }

  if (-not $r.ok) {
    $r | ConvertTo-Json -Depth 50
    exit 2
  }

  Remove-Item $pyPath -Force -ErrorAction SilentlyContinue
}
finally {
  Remove-Item $tmpPayload.FullName -Force -ErrorAction SilentlyContinue
}

# ---------- Gate 3: References-only ----------
if ($env.kind -in @("evidence","ledger_entry")) {
  $jsonData = ($env.data | ConvertTo-Json -Depth 50)
  if ($jsonData -match '"uri"\s*:\s*"\s*data:') { Fail "REF_RAW_CONTENT_DETECTED" "data: URI detected in artifacts[].uri" }
  if ($jsonData -match '"raw"\s*:') { Fail "REF_RAW_CONTENT_DETECTED" "raw field detected (not allowed)" }
}

Ok "VALID: $($env.kind)"
