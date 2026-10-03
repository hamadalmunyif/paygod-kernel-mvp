import {
  CANONICALIZATION_PROFILE,
  fileListToMap,
  parseIssuerTrustStore,
  verifyBundle,
} from "./verifier-core.mjs";

const $ = (id) => document.getElementById(id);

const fileInput = $("bundleFiles");
const receiptPin = $("receiptPin");
const allowUnbound = $("allowUnbound");
const verifyButton = $("verifyButton");
const selection = $("selection");
const resultSection = $("resultSection");
const issuerTrustInput = $("issuerTrustStore");
const issuerTrustStatus = $("issuerTrustStatus");
let trustedIssuerKeys = {};

$("profileBadge").textContent = CANONICALIZATION_PROFILE;

issuerTrustInput.addEventListener("change", async () => {
  trustedIssuerKeys = {};
  issuerTrustStatus.textContent = "No trusted issuer keys loaded.";
  const file = issuerTrustInput.files?.[0];
  if (!file) return;
  try {
    const parsed = JSON.parse(await file.text());
    trustedIssuerKeys = parseIssuerTrustStore(parsed);
    issuerTrustStatus.textContent = `${Object.keys(trustedIssuerKeys).length} trusted issuer key${Object.keys(trustedIssuerKeys).length === 1 ? "" : "s"} loaded.`;
  } catch (error) {
    issuerTrustStatus.textContent = `Trust store rejected: ${error.message}`;
  }
});

fileInput.addEventListener("change", () => {
  const files = Array.from(fileInput.files ?? []);
  selection.textContent = files.length
    ? `${files.length} file${files.length === 1 ? "" : "s"} selected: ${files.map((f) => f.name).join(", ")}`
    : "No files selected.";
});

verifyButton.addEventListener("click", async () => {
  verifyButton.disabled = true;
  verifyButton.textContent = "Verifying…";

  try {
    const files = await fileListToMap(fileInput.files ?? []);
    const pin = receiptPin.value.trim();

    const result = await verifyBundle(files, {
      allowUnboundClock: allowUnbound.checked,
      expectedReceiptSha256: pin || null,
      trustedIssuerKeys,
    });

    renderResult(result, pin);
  } catch (error) {
    renderFailure(error);
  } finally {
    verifyButton.disabled = false;
    verifyButton.textContent = "Verify evidence";
  }
});

function renderResult(result, pin) {
  resultSection.classList.remove("hidden");

  setState($("integrityValue"), result.verification?.integrity ?? "failed");
  setState($("issuerValue"), result.verification?.issuer_authenticity ?? "not_verified");
  setState($("replayValue"), result.verification?.replay ?? "not_performed");
  setState($("timeValue"), result.verification?.time_authority ?? "failed");

  const integrityVerified = result.verification?.integrity === "verified";
  $("integrityHeadline").textContent = integrityVerified
    ? "Bundle integrity verified"
    : "Bundle integrity failed";

  $("receiptSha").textContent = result.receipt_sha256 ?? "—";
  $("ledgerHead").textContent = result.ledger_head ?? "—";
  $("manifestSha").textContent = result.manifest_sha256 ?? "—";
  $("bundleDigest").textContent = result.bundle_digest ?? "—";

  const pinStatus = $("pinStatus");
  if (!pin) {
    pinStatus.textContent = "NOT PROVIDED";
    pinStatus.className = "state-neutral";
  } else if (result.receipt_sha256 === pin && !result.errors?.some((e) => e.includes("expected external commitment"))) {
    pinStatus.textContent = "MATCHED";
    pinStatus.className = "state-good";
  } else {
    pinStatus.textContent = "MISMATCH";
    pinStatus.className = "state-bad";
  }

  const issuerVerified = result.verification?.issuer_authenticity === "verified";
  $("boundaryText").textContent = integrityVerified
    ? issuerVerified
      ? "The bundle integrity contract passed and the detached receipt signature verified against a trusted Ed25519 key supplied by the recipient. This authenticates the signing key for this receipt commitment only; it does not prove external evidence truth, replay the policy decision, or create a trusted timestamp."
      : "The transferred bundle is internally consistent within the PayGod integrity contract. Issuer authenticity remains separate unless a detached signature verifies against a recipient-supplied trusted key. This result does not replay the original policy decision, establish external evidence truth, or create a trusted timestamp."
    : "One or more integrity checks failed. Do not rely on this bundle as matching its declared commitments. Other trust dimensions remain separate and are not upgraded by a failed integrity result.";

  $("rawResult").textContent = JSON.stringify(result, null, 2);
  resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderFailure(error) {
  resultSection.classList.remove("hidden");
  setState($("integrityValue"), "failed");
  setState($("issuerValue"), "not_verified");
  setState($("replayValue"), "not_performed");
  setState($("timeValue"), "failed");
  $("integrityHeadline").textContent = "Verification could not complete";
  $("boundaryText").textContent =
    "The browser verifier failed before completing the integrity contract. No trust claim should be inferred.";
  $("rawResult").textContent = JSON.stringify(
    { status: "invalid", errors: [String(error?.message ?? error)] },
    null,
    2,
  );
}

function setState(element, value) {
  const display = String(value).replaceAll("_", " ").toUpperCase();
  element.textContent = display;
  element.className =
    value === "verified" || value === "producer_supplied"
      ? "state-good"
      : value === "failed"
        ? "state-bad"
        : "state-neutral";
}
