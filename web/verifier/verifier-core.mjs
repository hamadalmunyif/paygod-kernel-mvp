export const VERIFIER_VERSION = "0.4.0";
export const CANONICALIZATION_PROFILE = "paygod-c14n-v1";
export const SAFE_INTEGER_MAX = 9007199254740991n;
export const ISSUER_SIGNATURE_PROFILE = "paygod-ed25519-receipt-v1";
export const ISSUER_TRUST_PROFILE = "paygod-ed25519-trust-v1";

const HEX64 = /^[a-f0-9]{64}$/;
const CANONICAL_VERDICTS = new Set(["allow", "deny", "flag", "error"]);
const KEY_ID = /^[A-Za-z0-9._:-]{1,128}$/;
const ED25519_DOMAIN = encoder => encoder.encode("PAYGOD-RECEIPT-v1\0");
const encoder = new TextEncoder();
const utf8Fatal = new TextDecoder("utf-8", { fatal: true });

function cryptoApi() {
  if (!globalThis.crypto?.subtle) {
    throw new Error("Web Crypto SHA-256 is unavailable");
  }
  return globalThis.crypto;
}

export function bytesToHex(bytes) {
  return Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
}

export async function sha256Bytes(bytes) {
  const digest = await cryptoApi().subtle.digest("SHA-256", bytes);
  return bytesToHex(new Uint8Array(digest));
}

export async function sha256Text(text) {
  return sha256Bytes(encoder.encode(text));
}


function hexToBytes(hex) {
  if (!HEX64.test(hex)) throw new Error("receipt_sha256 must be 64 lowercase hex characters");
  const out = new Uint8Array(32);
  for (let i = 0; i < 32; i += 1) out[i] = Number.parseInt(hex.slice(i * 2, i * 2 + 2), 16);
  return out;
}

function base64ToBytes(value, expectedLength, label) {
  if (typeof value !== "string") throw new Error(`${label} must be base64 text`);
  let raw;
  try {
    const binary = atob(value);
    raw = Uint8Array.from(binary, (ch) => ch.charCodeAt(0));
  } catch {
    throw new Error(`${label} is not valid base64`);
  }
  if (raw.length !== expectedLength) throw new Error(`${label} must decode to ${expectedLength} bytes`);
  return raw;
}

export function parseIssuerTrustStore(value) {
  if (!value || Array.isArray(value) || typeof value !== "object" || value.profile !== ISSUER_TRUST_PROFILE) {
    throw new Error(`trust store profile must be ${ISSUER_TRUST_PROFILE}`);
  }
  if (!Array.isArray(value.keys)) throw new Error("trust store keys must be an array");
  const result = {};
  for (let i = 0; i < value.keys.length; i += 1) {
    const item = value.keys[i];
    if (!item || Array.isArray(item) || typeof item !== "object") throw new Error(`trust store key entry ${i} must be an object`);
    const fields = Object.keys(item).sort().join(",");
    if (fields !== "algorithm,key_id,public_key_b64") throw new Error(`trust store key entry ${i} has unsupported fields`);
    if (!KEY_ID.test(item.key_id)) throw new Error(`trust store key entry ${i} has invalid key_id`);
    if (item.algorithm !== "Ed25519") throw new Error(`trust store key entry ${i} algorithm must be Ed25519`);
    if (Object.hasOwn(result, item.key_id)) throw new Error(`duplicate trust-store key_id: ${item.key_id}`);
    base64ToBytes(item.public_key_b64, 32, "public_key_b64");
    result[item.key_id] = item.public_key_b64;
  }
  return result;
}

export function issuerSigningMessage(keyId, receiptSha) {
  if (!KEY_ID.test(keyId)) throw new Error("invalid issuer key_id");
  const domain = ED25519_DOMAIN(encoder);
  const key = encoder.encode(keyId);
  const digest = hexToBytes(receiptSha);
  const out = new Uint8Array(domain.length + key.length + 1 + digest.length);
  out.set(domain, 0);
  out.set(key, domain.length);
  out[domain.length + key.length] = 0;
  out.set(digest, domain.length + key.length + 1);
  return out;
}

async function verifyIssuerSignature(signatureBytes, receiptSha, trustedIssuerKeys) {
  const details = {
    present: signatureBytes instanceof Uint8Array,
    profile: null,
    algorithm: null,
    key_id: null,
    receipt_sha256_matches: false,
    key_trusted: false,
    signature_valid: false,
    reason: null,
  };
  if (!(signatureBytes instanceof Uint8Array)) {
    details.reason = "signature_not_present";
    return ["not_verified", details];
  }

  try {
    const envelope = strictJsonParse(decodeUtf8(signatureBytes));
    if (!envelope || Array.isArray(envelope) || typeof envelope !== "object") throw new Error("signature envelope must be an object");
    const fields = Object.keys(envelope).sort().join(",");
    if (fields !== "algorithm,key_id,profile,receipt_sha256,signature_b64") throw new Error("signature envelope fields do not match the profile");

    details.profile = envelope.profile;
    details.algorithm = envelope.algorithm;
    details.key_id = envelope.key_id;

    if (envelope.profile !== ISSUER_SIGNATURE_PROFILE) throw new Error(`signature profile must be ${ISSUER_SIGNATURE_PROFILE}`);
    if (envelope.algorithm !== "Ed25519") throw new Error("signature algorithm must be Ed25519");
    if (!KEY_ID.test(envelope.key_id)) throw new Error("invalid signature key_id");
    if (!HEX64.test(envelope.receipt_sha256)) throw new Error("signature receipt_sha256 must be 64 lowercase hex characters");

    details.receipt_sha256_matches = envelope.receipt_sha256 === receiptSha;
    if (!details.receipt_sha256_matches) {
      details.reason = "receipt_commitment_mismatch";
      return ["failed", details];
    }

    const signature = base64ToBytes(envelope.signature_b64, 64, "signature_b64");
    const keys = trustedIssuerKeys ?? {};
    if (Object.keys(keys).length === 0) {
      details.reason = "no_trust_anchor_supplied";
      return ["not_verified", details];
    }
    if (!Object.hasOwn(keys, envelope.key_id)) {
      details.reason = "key_id_not_in_trust_store";
      return ["failed", details];
    }

    const publicKeyBytes = base64ToBytes(keys[envelope.key_id], 32, "public_key_b64");
    details.key_trusted = true;
    if (!globalThis.crypto?.subtle) {
      details.reason = "webcrypto_backend_unavailable";
      return ["not_verified", details];
    }

    let publicKey;
    try {
      publicKey = await globalThis.crypto.subtle.importKey(
        "raw",
        publicKeyBytes,
        { name: "Ed25519" },
        false,
        ["verify"],
      );
    } catch {
      details.reason = "ed25519_backend_unavailable";
      return ["not_verified", details];
    }

    const valid = await globalThis.crypto.subtle.verify(
      { name: "Ed25519" },
      publicKey,
      signature,
      issuerSigningMessage(envelope.key_id, receiptSha),
    );
    if (!valid) {
      details.reason = "signature_invalid";
      return ["failed", details];
    }

    details.signature_valid = true;
    details.reason = "verified";
    return ["verified", details];
  } catch (error) {
    details.reason = `signature_envelope_invalid: ${error.message}`;
    return ["failed", details];
  }
}

function stripUtf8Bom(text) {
  return text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;
}

export function decodeUtf8(bytes, { allowBom = false } = {}) {
  const text = utf8Fatal.decode(bytes);
  return allowBom ? stripUtf8Bom(text) : text;
}

function validateNumberLexemes(text) {
  let inString = false;
  let escaped = false;

  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];

    if (inString) {
      if (escaped) {
        escaped = false;
      } else if (ch === "\\") {
        escaped = true;
      } else if (ch === '"') {
        inString = false;
      }
      continue;
    }

    if (ch === '"') {
      inString = true;
      continue;
    }

    if (ch === "-" || (ch >= "0" && ch <= "9")) {
      const match = text.slice(i).match(/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/);
      if (!match) continue;

      const token = match[0];
      if (/[.eE]/.test(token)) {
        throw new Error("floating-point and exponent numbers are not allowed by paygod-c14n-v1");
      }

      const value = BigInt(token);
      if (value < -SAFE_INTEGER_MAX || value > SAFE_INTEGER_MAX) {
        throw new Error("integer outside paygod-c14n-v1 safe range");
      }
      i += token.length - 1;
    }
  }
}

export function strictJsonParse(text, { allowBom = false } = {}) {
  const source = allowBom ? stripUtf8Bom(text) : text;
  validateNumberLexemes(source);
  return JSON.parse(source);
}

function ensurePairedSurrogates(value) {
  for (let i = 0; i < value.length; i += 1) {
    const unit = value.charCodeAt(i);
    if (unit >= 0xd800 && unit <= 0xdbff) {
      if (i + 1 >= value.length) throw new Error("unpaired Unicode surrogate");
      const next = value.charCodeAt(i + 1);
      if (next < 0xdc00 || next > 0xdfff) throw new Error("unpaired Unicode surrogate");
      i += 1;
    } else if (unit >= 0xdc00 && unit <= 0xdfff) {
      throw new Error("unpaired Unicode surrogate");
    }
  }
}

function profileString(value) {
  ensurePairedSurrogates(value);
  let out = '"';

  for (let i = 0; i < value.length; i += 1) {
    const unit = value.charCodeAt(i);
    if (unit === 0x22) out += '\\"';
    else if (unit === 0x5c) out += "\\\\";
    else if (unit === 0x08) out += "\\b";
    else if (unit === 0x0c) out += "\\f";
    else if (unit === 0x0a) out += "\\n";
    else if (unit === 0x0d) out += "\\r";
    else if (unit === 0x09) out += "\\t";
    else if (unit < 0x20 || unit > 0x7e) out += `\\u${unit.toString(16).padStart(4, "0")}`;
    else out += String.fromCharCode(unit);
  }

  return out + '"';
}

function ordinalCompare(a, b) {
  const length = Math.min(a.length, b.length);
  for (let i = 0; i < length; i += 1) {
    const diff = a.charCodeAt(i) - b.charCodeAt(i);
    if (diff !== 0) return diff;
  }
  return a.length - b.length;
}

function pythonCodePointCompare(a, b) {
  const aa = Array.from(a, (c) => c.codePointAt(0));
  const bb = Array.from(b, (c) => c.codePointAt(0));
  const length = Math.min(aa.length, bb.length);
  for (let i = 0; i < length; i += 1) {
    const diff = aa[i] - bb[i];
    if (diff !== 0) return diff;
  }
  return aa.length - bb.length;
}

export function canonicalJson(value) {
  if (value === null) return "null";
  if (value === true) return "true";
  if (value === false) return "false";

  if (typeof value === "string") return profileString(value);

  if (Array.isArray(value)) {
    return "[" + value.map((item) => canonicalJson(item)).join(",") + "]";
  }

  if (typeof value === "number") {
    if (!Number.isInteger(value)) {
      throw new Error("floating-point numbers are not allowed by paygod-c14n-v1");
    }
    if (!Number.isSafeInteger(value)) {
      throw new Error("integer outside paygod-c14n-v1 safe range");
    }
    return Object.is(value, -0) ? "0" : String(value);
  }

  if (typeof value === "object") {
    const prototype = Object.getPrototypeOf(value);
    if (prototype !== Object.prototype && prototype !== null) {
      throw new Error("unsupported JSON object representation");
    }

    const keys = Object.keys(value);
    for (const key of keys) {
      ensurePairedSurrogates(key);
      if (key.normalize("NFC") !== key) {
        throw new Error("JSON object key is not NFC-normalized");
      }
    }

    keys.sort(ordinalCompare);
    return "{" + keys.map((key) => `${profileString(key)}:${canonicalJson(value[key])}`).join(",") + "}";
  }

  throw new Error(`unsupported JSON value: ${typeof value}`);
}

function deepEqual(a, b) {
  if (a === b) return true;
  if (typeof a !== typeof b || a === null || b === null) return false;

  if (Array.isArray(a) || Array.isArray(b)) {
    if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) return false;
    return a.every((item, i) => deepEqual(item, b[i]));
  }

  if (typeof a === "object") {
    const ak = Object.keys(a).sort(ordinalCompare);
    const bk = Object.keys(b).sort(ordinalCompare);
    if (ak.length !== bk.length) return false;
    return ak.every((key, i) => key === bk[i] && deepEqual(a[key], b[key]));
  }

  return false;
}

function dimensions(integrity, timeAuthority = "failed", issuerAuthenticity = "not_verified") {
  return {
    integrity,
    issuer_authenticity: issuerAuthenticity,
    replay: "not_performed",
    time_authority: timeAuthority,
  };
}

function invalid(errors, extra = {}) {
  const timeAuthority = extra.time_authority ?? "failed";
  const { time_authority: _ignored, ...rest } = extra;
  return {
    status: "invalid",
    portable: false,
    verifier_version: VERIFIER_VERSION,
    verification: dimensions("failed", timeAuthority),
    errors,
    ...rest,
  };
}

function safeManifestName(name) {
  return (
    typeof name === "string" &&
    name.length > 0 &&
    name !== "." &&
    name !== ".." &&
    !name.includes("/") &&
    !name.includes("\\")
  );
}

function parseInstant(value) {
  if (typeof value !== "string" || value.length === 0) return null;
  if (!/(?:Z|[+-]\d{2}:\d{2})$/.test(value)) return null;
  const ms = Date.parse(value);
  return Number.isFinite(ms) ? ms : null;
}

async function verifyLedger(bytes, errors) {
  if (!bytes) return null;

  let text;
  try {
    text = decodeUtf8(bytes);
  } catch (error) {
    errors.push(`ledger read failed: ${error.message}`);
    return null;
  }

  let previous = "0".repeat(64);
  let expectedIndex = 0;
  let lastEntry = null;

  const lines = text.split(/\r?\n/);
  for (let i = 0; i < lines.length; i += 1) {
    const raw = lines[i];
    if (!raw.trim()) continue;

    let entry;
    try {
      entry = strictJsonParse(raw);
    } catch (error) {
      errors.push(`ledger line ${i + 1}: invalid JSON: ${error.message}`);
      return null;
    }

    if (!entry || Array.isArray(entry) || typeof entry !== "object") {
      errors.push(`ledger line ${i + 1}: entry must be an object`);
      return null;
    }

    if (entry.entry_index !== expectedIndex) {
      errors.push(`ledger line ${i + 1}: unexpected entry_index`);
    }
    if (entry.previous_hash !== previous) {
      errors.push(`ledger line ${i + 1}: previous_hash mismatch`);
    }

    const payload = {
      previous_hash: entry.previous_hash ?? null,
      timestamp: entry.timestamp ?? null,
      data: entry.data ?? null,
    };

    let calculated;
    try {
      calculated = await sha256Text(canonicalJson(payload));
    } catch (error) {
      errors.push(`ledger line ${i + 1}: canonicalization failed: ${error.message}`);
      return null;
    }

    const recordHash = entry.record_hash;
    if (typeof recordHash !== "string" || !HEX64.test(recordHash)) {
      errors.push(`ledger line ${i + 1}: record_hash must be 64 lowercase hex characters`);
    }
    if (recordHash !== calculated) {
      errors.push(`ledger line ${i + 1}: record_hash mismatch`);
    }

    previous = typeof recordHash === "string" ? recordHash : "";
    expectedIndex += 1;
    lastEntry = entry;
  }

  return lastEntry;
}

function validateReceiptSemantics(
  manifest,
  receipt,
  ledgerEntry,
  manifestSha,
  errors,
  allowUnboundClock,
) {
  if (receipt.api_version !== "paygod/v1") errors.push("receipt api_version mismatch");
  if (receipt.kind !== "Receipt") errors.push("receipt kind mismatch");

  let clock = receipt.clock;
  if (!clock || Array.isArray(clock) || typeof clock !== "object") {
    errors.push("receipt clock must be an object");
    clock = {};
  }
  if (clock.source !== "env:PAYGOD_CLOCK") errors.push("receipt clock source mismatch");
  if (receipt.generated_at !== clock.value) {
    errors.push("receipt generated_at does not match clock.value");
  }

  const canonicalization = receipt.canonicalization;
  if (
    !canonicalization ||
    Array.isArray(canonicalization) ||
    typeof canonicalization !== "object" ||
    canonicalization.json !== CANONICALIZATION_PROFILE
  ) {
    errors.push("receipt canonicalization declaration mismatch");
  }

  if (!deepEqual(receipt.pack, manifest.pack)) {
    errors.push("receipt pack does not match manifest pack");
  }
  if (!deepEqual(receipt.input, manifest.input)) {
    errors.push("receipt input does not match manifest input");
  }

  const entries = manifest.files;
  let manifestBundle = manifest.bundle;
  let receiptBundle = receipt.bundle;
  if (!manifestBundle || Array.isArray(manifestBundle) || typeof manifestBundle !== "object") {
    errors.push("manifest bundle must be an object");
    manifestBundle = {};
  }
  if (!receiptBundle || Array.isArray(receiptBundle) || typeof receiptBundle !== "object") {
    errors.push("receipt bundle must be an object");
    receiptBundle = {};
  }

  if (receiptBundle.bundle_digest !== manifestBundle.bundle_digest) {
    errors.push("receipt bundle_digest does not bind manifest bundle");
  }
  if (receiptBundle.manifest_sha256 !== manifestSha) {
    errors.push("receipt manifest_sha256 mismatch");
  }
  if (!deepEqual(receiptBundle.files, entries)) {
    errors.push("receipt files do not match manifest files");
  }

  let verdict = receipt.verdict;
  if (!verdict || Array.isArray(verdict) || typeof verdict !== "object") {
    errors.push("receipt verdict must be an object");
    verdict = {};
  }

  const verdictValue = verdict.value;
  const verdictRule = verdict.rule_name;
  const verdictReason = verdict.reason;
  if (!CANONICAL_VERDICTS.has(verdictValue)) {
    errors.push("receipt verdict value must be one of allow/deny/flag/error");
  }
  if (typeof verdictRule !== "string") errors.push("receipt verdict rule_name must be a string");
  if (typeof verdictReason !== "string") errors.push("receipt verdict reason must be a string");

  let receiptPack = receipt.pack;
  if (!receiptPack || Array.isArray(receiptPack) || typeof receiptPack !== "object") {
    errors.push("receipt pack must be an object");
    receiptPack = {};
  }
  for (const key of ["name", "version", "path", "digest_sha256"]) {
    if (typeof receiptPack[key] !== "string") errors.push(`receipt pack ${key} must be a string`);
  }
  if (typeof receiptPack.digest_sha256 === "string" && !HEX64.test(receiptPack.digest_sha256)) {
    errors.push("receipt pack digest_sha256 must be 64 lowercase hex characters");
  }

  let receiptInput = receipt.input;
  if (!receiptInput || Array.isArray(receiptInput) || typeof receiptInput !== "object") {
    errors.push("receipt input must be an object");
    receiptInput = {};
  }
  const receiptInputHash = receiptInput.canonical_hash;
  if (typeof receiptInputHash !== "string" || !HEX64.test(receiptInputHash)) {
    errors.push("receipt input canonical_hash must be 64 lowercase hex characters");
  }

  if (!ledgerEntry) {
    errors.push("missing ledger entry for receipt decision binding");
    return ["invalid", "failed"];
  }

  let ledgerData = ledgerEntry.data;
  if (!ledgerData || Array.isArray(ledgerData) || typeof ledgerData !== "object") {
    errors.push("ledger data must be an object");
    return ["invalid", "failed"];
  }

  const ledgerVerdict = ledgerData.verdict;
  const ledgerRule = ledgerData.rule_name;
  const ledgerReason = ledgerData.reason;
  const ledgerPack = ledgerData.pack;
  const ledgerInputHash = ledgerData.input_hash;

  if (!CANONICAL_VERDICTS.has(ledgerVerdict)) {
    errors.push("locked ledger verdict must be one of allow/deny/flag/error");
  }
  if (typeof ledgerRule !== "string") errors.push("locked ledger rule_name must be a string");
  if (typeof ledgerReason !== "string") errors.push("locked ledger reason must be a string");
  if (!ledgerPack || Array.isArray(ledgerPack) || typeof ledgerPack !== "object") {
    errors.push("locked ledger pack must be an object");
  }
  if (typeof ledgerInputHash !== "string" || !HEX64.test(ledgerInputHash)) {
    errors.push("locked ledger input_hash must be 64 lowercase hex characters");
  }

  if (verdictValue !== ledgerVerdict) {
    errors.push("receipt verdict does not match locked ledger verdict");
  }
  if (verdictRule !== ledgerRule) {
    errors.push("receipt rule_name does not match locked ledger");
  }
  if (verdictReason !== ledgerReason) {
    errors.push("receipt reason does not match locked ledger");
  }
  if (!deepEqual(receiptPack, ledgerPack)) {
    errors.push("receipt pack does not match locked ledger");
  }
  if (receiptInputHash !== ledgerInputHash) {
    errors.push("receipt input hash does not match locked ledger");
  }

  const manifestTime = parseInstant(manifest.generated_at);
  const ledgerTime = parseInstant(ledgerEntry.timestamp);
  if (manifestTime === null || ledgerTime === null) {
    errors.push("invalid or timezone-naive manifest/ledger timestamp");
  } else if (manifestTime !== ledgerTime) {
    errors.push("manifest and locked ledger decision time mismatch");
  }

  const clockValue = clock.value;
  if (clockValue === "unset") {
    if (!allowUnboundClock) {
      errors.push("unbound receipt clock requires explicit allow-unbound-clock opt-in");
      return ["unbound-rejected", "unbound"];
    }
    return ["unbound-opt-in", "unbound"];
  }

  const receiptTime = parseInstant(clockValue);
  if (receiptTime === null) {
    errors.push("invalid or timezone-naive injected receipt clock");
    return ["invalid", "failed"];
  }
  if (manifestTime !== null && receiptTime !== manifestTime) {
    errors.push("receipt clock does not match locked manifest/ledger time");
    return ["invalid", "failed"];
  }

  return ["injected", "producer_supplied"];
}

export async function verifyBundle(
  files,
  {
    allowUnboundClock = false,
    expectedReceiptSha256 = null,
    trustedIssuerKeys = {},
  } = {},
) {
  const fileMap = files instanceof Map ? files : new Map(Object.entries(files));
  const errors = [];

  const manifestBytes = fileMap.get("manifest.json");
  const receiptBytes = fileMap.get("receipt.json");

  if (!(manifestBytes instanceof Uint8Array)) errors.push("missing manifest.json");
  if (!(receiptBytes instanceof Uint8Array)) errors.push("missing receipt.json");
  if (errors.length) return invalid(errors);

  const receiptSha = await sha256Bytes(receiptBytes);
  if (expectedReceiptSha256 !== null && expectedReceiptSha256 !== "") {
    if (!HEX64.test(expectedReceiptSha256)) {
      errors.push("expected receipt sha256 must be 64 lowercase hex characters");
    } else if (receiptSha !== expectedReceiptSha256) {
      errors.push("receipt sha256 does not match expected external commitment");
    }
  }

  let manifest;
  let receipt;
  try {
    manifest = strictJsonParse(decodeUtf8(manifestBytes, { allowBom: true }));
    receipt = strictJsonParse(decodeUtf8(receiptBytes, { allowBom: true }));
  } catch (error) {
    return invalid([...errors, `invalid control JSON: ${error.message}`], {
      receipt_sha256: receiptSha,
    });
  }

  if (!manifest || Array.isArray(manifest) || typeof manifest !== "object") {
    return invalid([...errors, "manifest must be an object"], { receipt_sha256: receiptSha });
  }
  if (!receipt || Array.isArray(receipt) || typeof receipt !== "object") {
    return invalid([...errors, "receipt must be an object"], { receipt_sha256: receiptSha });
  }

  const entries = manifest.files;
  if (!Array.isArray(entries) || entries.length === 0) {
    return invalid([...errors, "manifest files must be a non-empty array"], {
      receipt_sha256: receiptSha,
    });
  }

  const digestLines = [];
  const seenNames = new Set();

  for (let index = 0; index < entries.length; index += 1) {
    const entry = entries[index];
    if (!entry || Array.isArray(entry) || typeof entry !== "object") {
      errors.push(`manifest file entry ${index} must be an object`);
      continue;
    }

    const name = entry.name;
    const expected = entry.sha256;
    const expectedBytes = entry.bytes;

    if (!safeManifestName(name)) {
      errors.push(`manifest file entry ${index} has invalid name`);
      continue;
    }
    if (seenNames.has(name)) {
      errors.push(`duplicate manifest file: ${name}`);
      continue;
    }
    seenNames.add(name);

    if (typeof expected !== "string" || !HEX64.test(expected)) {
      errors.push(`manifest file entry ${index} has invalid sha256`);
      continue;
    }
    if (!Number.isSafeInteger(expectedBytes) || expectedBytes < 0) {
      errors.push(`manifest file entry ${index} has invalid byte count`);
      continue;
    }

    const bytes = fileMap.get(name);
    if (!(bytes instanceof Uint8Array)) {
      errors.push(`missing manifest file: ${name}`);
      continue;
    }

    const actual = await sha256Bytes(bytes);
    if (actual !== expected) errors.push(`sha256 mismatch: ${name}`);
    if (bytes.byteLength !== expectedBytes) errors.push(`byte count mismatch: ${name}`);
    digestLines.push(`${name}=${expected}\n`);
  }

  const allowedFiles = new Set(["manifest.json", "receipt.json", "receipt.sig.json", ...seenNames]);
  for (const name of fileMap.keys()) {
    if (!allowedFiles.has(name)) errors.push(`unexpected bundle file: ${name}`);
  }

  let manifestBundle = manifest.bundle;
  if (!manifestBundle || Array.isArray(manifestBundle) || typeof manifestBundle !== "object") {
    errors.push("manifest bundle must be an object");
    manifestBundle = {};
  }
  if (manifest.api_version !== "paygod/v1") errors.push("manifest api_version mismatch");
  if (manifest.kind !== "Manifest") errors.push("manifest kind mismatch");
  if (manifestBundle.algorithm !== "sha256") errors.push("manifest bundle algorithm mismatch");
  if (manifestBundle.file_count !== entries.length) errors.push("manifest file_count mismatch");

  const manifestBundleDigest = manifestBundle.bundle_digest;
  digestLines.sort(pythonCodePointCompare);
  const calculatedBundle = await sha256Text(digestLines.join(""));
  if (calculatedBundle !== manifestBundleDigest) {
    errors.push("manifest bundle_digest mismatch");
  }

  const ledgerMembers = entries.filter(
    (entry) => entry && typeof entry === "object" && !Array.isArray(entry) && entry.name === "ledger.jsonl",
  );
  if (ledgerMembers.length !== 1) {
    errors.push("ledger.jsonl must appear exactly once in manifest files");
  }

  const ledgerEntry = await verifyLedger(fileMap.get("ledger.jsonl"), errors);
  let ledgerHead = null;
  if (ledgerEntry && typeof ledgerEntry.record_hash === "string" && HEX64.test(ledgerEntry.record_hash)) {
    ledgerHead = ledgerEntry.record_hash;
  }

  const manifestSha = await sha256Bytes(manifestBytes);
  const [clockBinding, timeAuthority] = validateReceiptSemantics(
    manifest,
    receipt,
    ledgerEntry,
    manifestSha,
    errors,
    allowUnboundClock,
  );

  const [issuerAuthenticity, issuerSignature] = await verifyIssuerSignature(
    fileMap.get("receipt.sig.json"),
    receiptSha,
    trustedIssuerKeys,
  );

  return {
    status: errors.length === 0 ? "valid" : "invalid",
    portable: errors.length === 0,
    verifier_version: VERIFIER_VERSION,
    verification: dimensions(
      errors.length === 0 ? "verified" : "failed",
      timeAuthority,
      issuerAuthenticity,
    ),
    issuer_signature: issuerSignature,
    bundle_digest: manifestBundleDigest ?? null,
    manifest_sha256: manifestSha,
    receipt_sha256: receiptSha,
    ledger_head: ledgerHead,
    verified_files: entries.length,
    clock_binding: clockBinding,
    errors,
  };
}

export async function fileListToMap(fileList) {
  const map = new Map();
  for (const file of Array.from(fileList)) {
    if (map.has(file.name)) throw new Error(`duplicate selected filename: ${file.name}`);
    map.set(file.name, new Uint8Array(await file.arrayBuffer()));
  }
  return map;
}
