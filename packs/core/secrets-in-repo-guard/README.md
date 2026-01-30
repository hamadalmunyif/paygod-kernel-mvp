# Secrets in Repo Guard Pack

**Never leak API keys, tokens, or passwords to source control.**

## 🛑 The Pain Point
Hardcoded secrets are the #1 cause of cloud breaches. A developer accidentally commits an AWS key or database password, and within minutes, bots scrape it and launch crypto-miners or steal data. Revoking and rotating keys is painful and disruptive.

## ✅ The Solution
This Paygod pack wraps secret scanning tools (like Gitleaks or TruffleHog) to provide a definitive "Go/No-Go" decision for commits and pull requests.

### Policy Logic
- **DENY:** If `secrets_found > 0`. The commit is rejected immediately.
- **ALLOW:** If `secrets_found == 0`.

## 🛠️ Integration
Run this pack as a pre-commit hook or a blocking CI step.

```yaml
# Example Input
scan_report:
  secrets_found: 1
  details:
    - file: "config/database.yml"
      rule: "AWS Access Key"
      secret: "AKIA..." # ❌ This triggers a DENY
```

## 📉 ROI & Business Value
- **Breach Prevention:** Stop the most common attack vector at the source.
- **Cost Avoidance:** remediating a leaked key costs average $5,000+ in engineering time (rotation, investigation, incident response).
- **Compliance:** Meets requirements for PCI-DSS, HIPAA, and SOC2 regarding credential management.
