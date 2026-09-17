const assert = require('assert');
const http = require('http');
const { spawn } = require('child_process');

const PORT = 31337;
const child = spawn(process.execPath, ['server.js'], {
  cwd: __dirname + '/..',
  env: { ...process.env, PORT: String(PORT) },
  stdio: ['ignore', 'pipe', 'pipe']
});

function request(options) {
  return new Promise((resolve, reject) => {
    const req = http.request({ host: '127.0.0.1', port: PORT, ...options }, (res) => {
      let body = '';
      res.setEncoding('utf8');
      res.on('data', (chunk) => { body += chunk; });
      res.on('end', () => resolve({ statusCode: res.statusCode, body }));
    });
    req.on('error', reject);
    req.end();
  });
}

async function waitForServer() {
  for (let i = 0; i < 50; i += 1) {
    try {
      const result = await request({ method: 'GET', path: '/health' });
      if (result.statusCode === 200) return;
    } catch {}
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error('server did not start');
}

(async () => {
  try {
    await waitForServer();

    const health = await request({ method: 'GET', path: '/health' });
    assert.strictEqual(health.statusCode, 200);
    assert.deepStrictEqual(JSON.parse(health.body), { status: 'OK' });

    const malformedHost = await request({
      method: 'GET',
      path: '/health',
      headers: { Host: '[::1' }
    });
    assert.strictEqual(malformedHost.statusCode, 200);
    assert.deepStrictEqual(JSON.parse(malformedHost.body), { status: 'OK' });

    assert.strictEqual(child.exitCode, null, 'server exited after malformed Host header');
    console.log('PASS: API remains healthy with malformed Host header');
  } finally {
    child.kill();
  }
})().catch((error) => {
  console.error(error);
  child.kill();
  process.exitCode = 1;
});
