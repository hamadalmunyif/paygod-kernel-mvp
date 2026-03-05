const http = require('http');

const PORT = process.env.PORT || 3000;

function json(res, status, payload) {
  const body = JSON.stringify(payload);
  res.writeHead(status, {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(body)
  });
  res.end(body);
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  if (req.method === 'GET' && url.pathname === '/health') {
    return json(res, 200, { status: 'OK' });
  }

  if (req.method === 'POST' && url.pathname === '/run') {
    return json(res, 201, { bundle_digest: 'demo-bundle', status: 'created' });
  }

  const runMatch = url.pathname.match(/^\/runs\/([^/]+)$/);
  if (req.method === 'GET' && runMatch) {
    return json(res, 200, { bundle_digest: runMatch[1], status: 'available' });
  }

  const zipMatch = url.pathname.match(/^\/runs\/([^/]+)\/zip$/);
  if (req.method === 'GET' && zipMatch) {
    res.writeHead(200, {
      'Content-Type': 'application/zip',
      'Content-Disposition': `attachment; filename="${zipMatch[1]}.zip"`
    });
    return res.end('');
  }

  return json(res, 404, { error: 'Not found' });
});

server.listen(PORT, () => {
  console.log(`API listening on http://localhost:${PORT}`);
});
