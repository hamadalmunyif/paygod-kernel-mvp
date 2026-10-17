import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import {
  parseIssuerTrustStore,
  verifyBundle,
} from "../web/verifier/verifier-core.mjs";

const enc = new TextEncoder();
const corpusUrl = new URL("../spec/test-vectors/transport-parity-v1.json", import.meta.url);
const raw = await readFile(corpusUrl);
const blobSha = createHash("sha1")
  .update(`blob ${raw.byteLength}\0`)
  .update(raw)
  .digest("hex");

assert.equal(
  blobSha,
  "d3e682cb7f4f82cc88c4b8fd3ec7fb99d53357da",
  "transport parity corpus bytes changed without an explicit version/pin update",
);

const corpus = JSON.parse(raw.toString("utf8"));
assert.equal(corpus.profile, "paygod-transport-parity-v1");
assert.equal(corpus.cases.length, 10);

function materializeFiles(name) {
  const source = corpus.fixtures[name]?.files;
  assert.ok(source, "unknown fixture: " + name);
  return new Map(
    Object.entries(source).map(([fileName, content]) => [fileName, enc.encode(content)]),
  );
}

function expectedField(result, expected, key) {
  if (Object.hasOwn(expected, key)) {
    assert.equal(result[key], expected[key], key);
  }
}

for (const testCase of corpus.cases) {
  const files = materializeFiles(testCase.fixture);

  if (testCase.set_file) {
    files.set(testCase.set_file.name, enc.encode(testCase.set_file.content));
  }
  if (testCase.remove_file) {
    files.delete(testCase.remove_file);
  }

  const trustedIssuerKeys = testCase.trust_store
    ? parseIssuerTrustStore(corpus.trust_stores[testCase.trust_store])
    : {};

  const result = await verifyBundle(files, {
    expectedReceiptSha256: testCase.expected_receipt_sha256 ?? null,
    trustedIssuerKeys,
  });

  const expected = testCase.expected;
  assert.equal(result.status, expected.status, testCase.name + ": status");
  assert.equal(
    result.verification.integrity,
    expected.integrity,
    testCase.name + ": integrity",
  );

  if (Object.hasOwn(expected, "issuer_authenticity")) {
    assert.equal(
      result.verification.issuer_authenticity,
      expected.issuer_authenticity,
      testCase.name + ": issuer_authenticity",
    );
  }
  if (Object.hasOwn(expected, "replay")) {
    assert.equal(result.verification.replay, expected.replay, testCase.name + ": replay");
  }
  if (Object.hasOwn(expected, "time_authority")) {
    assert.equal(
      result.verification.time_authority,
      expected.time_authority,
      testCase.name + ": time_authority",
    );
  }
  if (Object.hasOwn(expected, "issuer_reason")) {
    assert.equal(
      result.issuer_signature?.reason,
      expected.issuer_reason,
      testCase.name + ": issuer reason",
    );
  }

  for (const key of [
    "receipt_sha256",
    "manifest_sha256",
    "bundle_digest",
    "ledger_head",
  ]) {
    expectedField(result, expected, key);
  }

  console.log("PASS:", testCase.name);
}

console.log(
  "PASS: Kernel JS verifier consumed exact paygod-transport-parity-v1 corpus",
);
