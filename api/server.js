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

function getPathname(req) {
  try {
    return new URL(req.url, 'http://localhost').pathname;
  } catch {
    return null;
  }
}

const server = http.createServer((req, res) => {
  const pathname = getPathname(req);
  if (pathname === null) {
    return json(res, 400, { error: 'Invalid request URL' });
  }

  if (req.method === 'GET' && pathname === '/health') {
    return json(res, 200, { status: 'OK' });
  }

  // Repository Boundary Closure v0.1: this demo server is not an execution
  // authority. Until it delegates to the canonical kernel, execution-like
  // routes fail closed instead of fabricating decisions or evidence.
  if (req.method === 'POST' && pathname === '/run') {
    return json(res, 410, {
      error: 'Demo execution endpoint deprecated',
      authority: 'canonical-kernel-required'
    });
  }

  const runMatch = pathname.match(/^\/runs\/([^/]+)$/);
  if (req.method === 'GET' && runMatch) {
    return json(res, 410, {
      error: 'Demo run store deprecated',
      authority: 'canonical-kernel-required'
    });
  }

  const zipMatch = pathname.match(/^\/runs\/([^/]+)\/zip$/);
  if (req.method === 'GET' && zipMatch) {
    return json(res, 410, {
      error: 'Demo bundle endpoint deprecated',
      authority: 'canonical-kernel-required'
    });
  }

  return json(res, 404, { error: 'Not found' });
});

server.listen(PORT, () => {
  console.log(`API listening on http://localhost:${PORT}`);
});
