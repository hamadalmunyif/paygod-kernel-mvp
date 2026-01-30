"""\
WARNING: NOT SOURCE OF TRUTH.

This script is a DEV/MOCK helper only.
Do not use it for pack results, CI gating, or compliance decisions.
Use the PayGod CLI instead: `dotnet run --project src/PayGod.Cli -- test --pack ...`
"""

import yaml
import json
import argparse
import sys
import re
from pathlib import Path

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def mock_engine_evaluate(pack_path, input_data):
    """
    MOCK ENGINE: In a real scenario, this would call the actual Paygod Control Engine.
    Here, we implement simple logic for the example packs to demonstrate the runner.
    """
    pack_name = Path(pack_path).name
    
    # Logic for 'memory-waste-guardrails'
    if pack_name == "memory-waste-guardrails":
        mem_value = input_data.get('value', 0)
        if mem_value > 85:
            return {
                "decision": "deny",
                "reason": "Memory usage exceeds threshold of 85%",
                "payload": {"risk_score": 0.9}
            }
        else:
            return {
                "decision": "allow",
                "reason": "Memory usage within limits",
                "payload": {"risk_score": 0.1}
            }

    # Logic for 'admin-drift-detection'
    elif pack_name == "admin-drift-detection":
        event = input_data.get('iam_event', {})
        policy = event.get('policy_attached')
        ticket = event.get('change_request_id')
        
        if policy == 'AdministratorAccess' and not ticket:
            return {
                "decision": "deny",
                "reason": "AdministratorAccess granted without a linked Change Request ID."
            }
        elif policy == 'AdministratorAccess' and ticket:
            return {
                "decision": "allow",
                "reason": "AdministratorAccess granted with valid Change Request."
            }
        else:
            return {
                "decision": "allow",
                "reason": "Non-critical policy change."
            }

    # Logic for 'critical-cve-blocker'
    elif pack_name == "critical-cve-blocker":
        report = input_data.get('scan_report', {})
        vulns = report.get('vulnerabilities', [])
        
        has_critical = any(v.get('cvss_score', 0) >= 9.0 and v.get('status') != 'fixed' for v in vulns)
        has_high = any(7.0 <= v.get('cvss_score', 0) < 9.0 and v.get('status') != 'fixed' for v in vulns)
        
        if has_critical:
            return {
                "decision": "deny",
                "reason": "Artifact contains unpatched critical vulnerabilities (CVSS >= 9.0)."
            }
        elif has_high:
            return {
                "decision": "warn",
                "reason": "Artifact contains unpatched high severity vulnerabilities."
            }
        else:
            return {
                "decision": "allow",
                "reason": "No critical or high vulnerabilities found."
            }

    # Logic for 'secrets-in-repo-guard'
    elif pack_name == "secrets-in-repo-guard":
        report = input_data.get('scan_report', {})
        secrets_count = report.get('secrets_found', 0)
        
        if secrets_count > 0:
            return {
                "decision": "deny",
                "reason": "Secrets detected in repository. Rotate keys immediately."
            }
        else:
            return {
                "decision": "allow",
                "reason": "No secrets detected."
            }
    
    # Default fallback for unknown packs
    return {"decision": "flag", "reason": f"Unknown pack logic for {pack_name}"}

def assert_match(actual, matcher):
    field = matcher['field']
    operator = matcher['operator']
    expected_value = matcher['value']
    
    # Simple field extraction (nested support could be added)
    actual_value = actual.get(field)
    
    if operator == 'equals':
        return actual_value == expected_value
    elif operator == 'contains':
        return expected_value in str(actual_value)
    elif operator == 'gt':
        return actual_value > expected_value
    elif operator == 'lt':
        return actual_value < expected_value
    elif operator == 'regex':
        return re.search(expected_value, str(actual_value)) is not None
    
    return False

def run_tests(pack_path):
    cases_path = Path(pack_path) / "tests" / "cases.yaml"
    if not cases_path.exists():
        print(f"❌ No tests found for pack: {pack_path}")
        return False

    print(f"🔍 Running tests for pack: {pack_path}")
    try:
        test_suite = load_yaml(cases_path)
    except Exception as e:
        print(f"❌ Failed to load test cases: {e}")
        return False
    
    all_passed = True
    
    for case in test_suite.get('cases', []):
        print(f"  • Running case: {case['name']}...", end=" ")
        
        # 1. Execute
        actual_output = mock_engine_evaluate(pack_path, case['input'])
        
        # 2. Assert Decision
        if actual_output['decision'] != case['expected']['decision']:
            print(f"FAILED ❌")
            print(f"    Expected decision: {case['expected']['decision']}")
            print(f"    Actual decision:   {actual_output['decision']}")
            print(f"    Actual reason:     {actual_output.get('reason')}")
            all_passed = False
            continue

        # 3. Assert Matchers
        matchers_passed = True
        if 'matchers' in case['expected']:
            for matcher in case['expected']['matchers']:
                if not assert_match(actual_output, matcher):
                    print(f"FAILED ❌")
                    print(f"    Matcher failed: {matcher}")
                    print(f"    Actual output:  {actual_output}")
                    matchers_passed = False
                    all_passed = False
                    break
        
        if matchers_passed:
            print(f"PASSED ✅")

    return all_passed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Paygod Pack Test Runner")
    parser.add_argument("pack_path", help="Path to the pack directory")
    args = parser.parse_args()

    success = run_tests(args.pack_path)
    sys.exit(0 if success else 1)
