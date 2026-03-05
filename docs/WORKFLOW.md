# Developer Workflow

## 1) Clone and install
```bash
git clone <repo-url>
cd paygod-cloud-starter/api
npm install
```

## 2) Start the API
```bash
node server.js
```

## 3) Execute a run
```bash
curl -s -X POST http://localhost:3000/run \
  -H "Content-Type: application/json" \
  -d '{"input":"demo"}'
```

## 4) Download result bundle
Use the `bundle_digest` returned from `/run`:
```bash
curl -L -o bundle.zip http://localhost:3000/runs/<bundle_digest>/zip
```
