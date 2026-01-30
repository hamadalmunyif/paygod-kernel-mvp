# Paygod Starter Packs

Ready-to-use policy bundles to secure your infrastructure and ensure compliance from Day 1.

## 🚀 Why use Starter Packs?
Instead of writing policies from scratch, start with our battle-tested packs. They address the most common and critical pain points in modern DevOps and Cloud environments.

## 📦 Available Packs

### 1. Security Guardrails

| Pack Name | Description | Value |
| :--- | :--- | :--- |
| **[secrets-in-repo-guard](../../packs/core/secrets-in-repo-guard)** | **Pre-Commit / CI**<br>Scans commits for high-entropy strings (API keys, tokens, passwords). | **Prevent Breaches:** Stops credential leaks before they reach the repo.<br>**Save Money:** Avoids expensive key rotation and incident response ($5k+ per leak). |
| **[critical-cve-blocker](../../packs/core/critical-cve-blocker)** | **CI / CD**<br>Parses container scan reports (Trivy/Grype) and blocks artifacts with Critical CVEs. | **Supply Chain Security:** Ensures no known exploits are shipped to production.<br>**Automated Gate:** Removes manual review bottlenecks. |

### 2. Compliance & Governance

| Pack Name | Description | Value |
| :--- | :--- | :--- |
| **[admin-drift-detection](../../packs/providers/aws/admin-drift-detection)** | **CloudTrail / IAM**<br>Monitors for `AdministratorAccess` grants without a linked Change Request (Ticket ID). | **Audit Readiness:** Meets SOC2/ISO requirements for privileged access control.<br>**Zero Shadow IT:** Prevents unauthorized admin escalation. |

### 3. Cost Control (FinOps) - *Coming Soon*

| Pack Name | Description | Value |
| :--- | :--- | :--- |
| **`idle-resource-reaper`** | **CloudWatch / Metrics**<br>Identifies and terminates EC2/RDS instances with < 1% CPU usage for 7 days. | **Immediate Savings:** Cut cloud waste by 20-30% automatically. |
| **`budget-forecast-alarm`** | **Billing API**<br>Alerts when forecasted spend exceeds budget by > 10%. | **No Bill Shock:** Catch run-away costs early. |

## 🛠️ How to Install
Packs are just directories! Clone the repo and point the Paygod CLI to the pack folder.

```bash
# Validate a pack
paygod validate --pack ./packs/core/critical-cve-blocker --input report.json
```
