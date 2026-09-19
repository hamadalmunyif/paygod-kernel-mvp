const assert = require('assert');
const http = require('http');
const { spawn } = require('child_process');

const PORT = 31337;
const child = spawn(process.execPath, ['server.js'], {
  cwd: __dirname + '/..',
  env: { ...process.env, PORT: String(PORT) },
  stdio: ['ignore', 'pipe', 'pipe']
});

function request(options, body) {
  return new Promise((resolve, reject) => {
    const req = http.request({ host: '127.0.0.1', port: PORT, ...options }, (res) => {
      let responseBody = '';
      res.setEncoding('utf8');
      res.on('data', (chunk) => { responseBody += chunk; });
      res.on('end', () => resolve({ statusCode: res.statusCode, body: responseBody }));
    });
    req.on('error', reject);
    if (body) req.write(body);
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

    const run = await request(
      { method: 'POST', path: '/run', headers: { 'Content-Type': 'application/json' } },
      '{"demo":"must-not-create-authority"}'
    );
    assert.strictEqual(run.statusCode, 410);
    const payload = JSON.parse(run.body);
    assert.strictEqual(payload.authority, 'canonical-kernel-required');
    assert.strictEqual(payload.bundle_digest, undefined);
    assert.strictEqual(payload.status, undefined);

    console.log('PASS: demo API fails closed and does not originate execution truth');
  } finally {
    child.kill();
  }
})().catch((error) => {
  console.error(error);
  child.kill();
  process.exitCode = 1;
});
