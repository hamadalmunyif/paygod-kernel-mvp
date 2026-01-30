# Admin Drift Detection Pack

**Prevent unauthorized privilege escalation and maintain IAM hygiene.**

## 🛑 The Pain Point
In cloud environments, "Admin Drift" occurs when developers or ops teams grant `AdministratorAccess` or high-privilege roles directly to users for "temporary debugging" but never revoke them. This leads to:
- **Expanded Attack Surface:** More users with god-mode keys means higher risk of catastrophic compromise.
- **Compliance Failures:** SOC2 and ISO 27001 require strict access controls and "least privilege" enforcement.
- **Shadow IT:** Admins can bypass standard change management processes.

## ✅ The Solution
This Paygod pack acts as a guardrail for your Identity & Access Management (IAM) events. It strictly enforces that any grant of `AdministratorAccess` **MUST** be accompanied by a valid Change Request (ticket ID).

### Policy Logic
- **DENY:** If `AdministratorAccess` is attached to a user/role AND `change_request_id` is missing.
- **ALLOW:** If `AdministratorAccess` is attached AND a valid `change_request_id` is present.
- **ALLOW:** All other non-admin policy changes (monitored but not blocked by this specific rule).

## 🛠️ Integration
Connect this pack to your CloudTrail logs or IAM event stream.

```yaml
# Example Input
iam_event:
  event_name: "AttachUserPolicy"
  user_identity: "arn:aws:iam::123:user/dave"
  policy_attached: "AdministratorAccess"
  change_request_id: null # ❌ This triggers a DENY
```

## 📉 ROI & Business Value
- **Zero "Shadow Admins":** Automatically prevent unauthorized admin creation.
- **Audit Readiness:** Every admin grant is cryptographically linked to a business justification (ticket ID).
- **Reduced Insurance Premiums:** Demonstrable control over privileged access often lowers cyber insurance costs.
