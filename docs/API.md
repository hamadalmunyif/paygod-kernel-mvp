# API Reference

This service exposes four HTTP endpoints for health checks and run bundle retrieval.

Base URL (local): `http://localhost:3000`

## GET /health
Returns service liveness.

### curl
```bash
curl -s http://localhost:3000/health
```

### PowerShell
```powershell
Invoke-RestMethod -Method GET -Uri "http://localhost:3000/health"
```

Expected response:
```json
{"status":"OK"}
```

## POST /run
Starts a run and returns metadata including a `bundle_digest` used for retrieval.

### curl
```bash
curl -s -X POST http://localhost:3000/run \
  -H "Content-Type: application/json" \
  -d '{"input":"demo"}'
```

### PowerShell
```powershell
$body = @{ input = "demo" } | ConvertTo-Json
Invoke-RestMethod -Method POST -Uri "http://localhost:3000/run" -ContentType "application/json" -Body $body
```

Example response:
```json
{
  "bundle_digest":"demo-bundle",
  "status":"created"
}
```

## GET /runs/:bundle_digest
Fetches JSON metadata for a specific bundle digest.

### curl
```bash
curl -s http://localhost:3000/runs/demo-bundle
```

### PowerShell
```powershell
Invoke-RestMethod -Method GET -Uri "http://localhost:3000/runs/demo-bundle"
```

## GET /runs/:bundle_digest/zip
Downloads the zip artifact for a specific bundle digest.

### curl
```bash
curl -L -o demo-bundle.zip http://localhost:3000/runs/demo-bundle/zip
```

### PowerShell
```powershell
Invoke-WebRequest -Method GET -Uri "http://localhost:3000/runs/demo-bundle/zip" -OutFile "demo-bundle.zip"
```
