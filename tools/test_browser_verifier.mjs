import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import {
  canonicalJson,
  sha256Bytes,
  sha256Text,
  strictJsonParse,
  verifyBundle,
} from "../web/verifier/verifier-core.mjs";

const enc = new TextEncoder();

function bytes(text) {
  return enc.encode(text);
}

function cloneFiles(files) {
  return new Map(Array.from(files, ([name, value]) => [name, new Uint8Array(value)]));
}

async function buildBundle(verdict = "allow") {
  const runTs = "2026-10-03T00:00:00+00:00";
  const pack = {
    name: "browser-parity",
    version: "0.1.0",
    path: "packs/browser-parity",
    digest_sha256: "1".repeat(64),
  };
  const inputHash = "2".repeat(64);
  const ledgerData = {
    verdict,
    rule_name: "browser-rule",
    reason: `browser verdict: ${verdict}`,
    pack,
    input_hash: inputHash,
    evidence_refs: [],
  };
  const payload = {
    previous_hash: "0".repeat(64),
    timestamp: runTs,
    data: ledgerData,
  };
  const ledgerHead = await sha256Text(canonicalJson(payload));
  const ledger = {
    entry_index: 0,
    timestamp: runTs,
    previous_hash: "0".repeat(64),
    data: ledgerData,
    record_hash: ledgerHead,
  };

  const files = new Map();
  files.set("ledger.jsonl", bytes(JSON.stringify(ledger) + "\n"));
  files.set(
    "findings.json",
    bytes(JSON.stringify({ api_version: "paygod/v1", kind: "FindingsReport", findings: [] }) + "\n"),
  );

  const entries = [];
  for (const name of ["findings.json", "ledger.jsonl"]) {
    const value = files.get(name);
    entries.push({
      name,
      sha256: await sha256Bytes(value),
      bytes: value.byteLength,
    });
  }

  const digestLines = entries
    .map((entry) => `${entry.name}=${entry.sha256}\n`)
    .sort()
    .join("");
  const bundleDigest = await sha256Text(digestLines);

  const manifest = {
    api_version: "paygod/v1",
    kind: "Manifest",
    generated_at: runTs,
    pack,
    input: { canonical_hash: inputHash },
    bundle: {
      algorithm: "sha256",
      digest_method: "sha256(join_lines(name='name=sha256' sorted by name))",
      file_count: entries.length,
      bundle_digest: bundleDigest,
    },
    files: entries,
  };
  const manifestBytes = bytes(JSON.stringify(manifest, null, 2) + "\n");
  files.set("manifest.json", manifestBytes);

  const receipt = {
    api_version: "paygod/v1",
    kind: "Receipt",
    spec_version: "0.2.0",
    generated_at: runTs,
    clock: { value: runTs, source: "env:PAYGOD_CLOCK" },
    canonicalization: { json: "paygod-c14n-v1" },
    runner: { image: "paygod/browser-parity", image_digest: "unknown" },
    pack,
    input: { canonical_hash: inputHash },
    bundle: {
      bundle_digest: bundleDigest,
      manifest_sha256: await sha256Bytes(manifestBytes),
      files: entries,
    },
    verdict: {
      value: verdict,
      rule_name: "browser-rule",
      reason: `browser verdict: ${verdict}`,
    },
    replay: { command: "not performed by integrity verifier" },
  };
  const receiptBytes = bytes(JSON.stringify(receipt, null, 2) + "\n");
  files.set("receipt.json", receiptBytes);

  return {
    files,
    receiptSha: await sha256Bytes(receiptBytes),
    ledgerHead,
  };
}

async function coherentRewrite(files, verdict) {
  const rewritten = cloneFiles(files);

  const ledger = JSON.parse(new TextDecoder().decode(rewritten.get("ledger.jsonl")).trim());
  ledger.data.verdict = verdict;
  ledger.data.reason = `browser verdict: ${verdict}`;
  ledger.record_hash = await sha256Text(
    canonicalJson({
      previous_hash: ledger.previous_hash,
      timestamp: ledger.timestamp,
      data: ledger.data,
    }),
  );
  const ledgerBytes = bytes(JSON.stringify(ledger) + "\n");
  rewritten.set("ledger.jsonl", ledgerBytes);

  const manifest = JSON.parse(new TextDecoder().decode(rewritten.get("manifest.json")));
  for (const entry of manifest.files) {
    const member = rewritten.get(entry.name);
    entry.sha256 = await sha256Bytes(member);
    entry.bytes = member.byteLength;
  }
  const lines = manifest.files
    .map((entry) => `${entry.name}=${entry.sha256}\n`)
    .sort()
    .join("");
  manifest.bundle.bundle_digest = await sha256Text(lines);
  const manifestBytes = bytes(JSON.stringify(manifest, null, 2) + "\n");
  rewritten.set("manifest.json", manifestBytes);

  const receipt = JSON.parse(new TextDecoder().decode(rewritten.get("receipt.json")));
  receipt.bundle.files = manifest.files;
  receipt.bundle.bundle_digest = manifest.bundle.bundle_digest;
  receipt.bundle.manifest_sha256 = await sha256Bytes(manifestBytes);
  receipt.verdict.value = verdict;
  receipt.verdict.reason = `browser verdict: ${verdict}`;
  const receiptBytes = bytes(JSON.stringify(receipt, null, 2) + "\n");
  rewritten.set("receipt.json", receiptBytes);

  return {
    files: rewritten,
    receiptSha: await sha256Bytes(receiptBytes),
  };
}

async function testSharedVectors() {
  const vectors = JSON.parse(
    await readFile(new URL("../spec/test-vectors/canonical-json.json", import.meta.url), "utf8"),
  );

  for (const vector of vectors) {
    if (vector.expected_error) {
      assert.throws(() => canonicalJson(vector.input), undefined, vector.description);
      continue;
    }

    const actual = canonicalJson(vector.input);
    assert.equal(actual, vector.expected_canonical, vector.description);
    assert.equal(await sha256Text(actual), vector.expected_hash, `${vector.description} hash`);
  }
}

function testLexicalNumberRejection() {
  assert.throws(() => strictJsonParse('{"n":1.0}'), /floating-point/);
  assert.throws(() => strictJsonParse('{"n":1e2}'), /floating-point/);
  assert.throws(() => strictJsonParse('{"n":-1E+2}'), /floating-point/);
  assert.throws(() => strictJsonParse('{"n":9007199254740992}'), /safe range/);
  assert.equal(strictJsonParse('{"n":9007199254740991}').n, 9007199254740991);
}

async function testCleanAndAttacks() {
  const base = await buildBundle();

  const clean = await verifyBundle(base.files, { expectedReceiptSha256: base.receiptSha });
  assert.equal(clean.status, "valid");
  assert.equal(clean.verification.integrity, "verified");
  assert.equal(clean.verification.issuer_authenticity, "not_verified");
  assert.equal(clean.verification.replay, "not_performed");
  assert.equal(clean.verification.time_authority, "producer_supplied");
  assert.equal(clean.receipt_sha256, base.receiptSha);
  assert.equal(clean.ledger_head, base.ledgerHead);

  const byteTamper = cloneFiles(base.files);
  const findings = new Uint8Array(byteTamper.get("findings.json"));
  findings[findings.length - 1] ^= 1;
  byteTamper.set("findings.json", findings);
  const tampered = await verifyBundle(byteTamper);
  assert.equal(tampered.status, "invalid");
  assert.ok(tampered.errors.some((e) => e.includes("sha256 mismatch: findings.json")));

  const extra = cloneFiles(base.files);
  extra.set(".DS_Store", bytes("noise"));
  const unexpected = await verifyBundle(extra);
  assert.equal(unexpected.status, "invalid");
  assert.ok(unexpected.errors.some((e) => e.includes("unexpected bundle file")));

  const receiptTamper = cloneFiles(base.files);
  const receipt = JSON.parse(new TextDecoder().decode(receiptTamper.get("receipt.json")));
  receipt.verdict.value = "deny";
  receiptTamper.set("receipt.json", bytes(JSON.stringify(receipt, null, 2) + "\n"));
  const receiptResult = await verifyBundle(receiptTamper);
  assert.equal(receiptResult.status, "invalid");
  assert.ok(receiptResult.errors.some((e) => e.includes("locked ledger verdict")));

  const missingLedger = cloneFiles(base.files);
  missingLedger.delete("ledger.jsonl");
  const missing = await verifyBundle(missingLedger);
  assert.equal(missing.status, "invalid");
  assert.ok(missing.errors.some((e) => e.includes("missing manifest file: ledger.jsonl")));

  const wrongPin = await verifyBundle(base.files, {
    expectedReceiptSha256: base.receiptSha === "f".repeat(64) ? "e".repeat(64) : "f".repeat(64),
  });
  assert.equal(wrongPin.status, "invalid");
  assert.ok(wrongPin.errors.some((e) => e.includes("expected external commitment")));

  const rewrite = await coherentRewrite(base.files, "deny");
  assert.notEqual(rewrite.receiptSha, base.receiptSha);

  const unpinned = await verifyBundle(rewrite.files);
  assert.equal(unpinned.status, "valid");
  assert.equal(unpinned.verification.integrity, "verified");

  const pinned = await verifyBundle(rewrite.files, { expectedReceiptSha256: base.receiptSha });
  assert.equal(pinned.status, "invalid");
  assert.ok(pinned.errors.some((e) => e.includes("expected external commitment")));
}

await testSharedVectors();
testLexicalNumberRejection();
await testCleanAndAttacks();

console.log("PASS: browser verifier v0.3 parity regression suite");
