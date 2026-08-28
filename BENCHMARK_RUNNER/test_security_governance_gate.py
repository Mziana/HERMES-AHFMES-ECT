"""
Acceptance Security & Governance Gate Test Suite for HERMES-AHFMES-ECT
Verifies 100% of User Acceptance Criteria:
1. Path traversal              -> DENIED (HTTP 403)
2. No approval token            -> DENIED (HTTP 403 / 422)
3. Invalid token                -> DENIED (HTTP 403)
4. Token for different action   -> DENIED (HTTP 403)
5. Replayed token               -> DENIED (HTTP 403)
6. Authorized matching action   -> ALLOWED (HTTP 200 SUCCESS)
7. Dynamic physical evidence    -> CATEGORIZED (OBSERVED / DERIVED / UNKNOWN)
"""

import sys
import os
import json
import urllib.request
import urllib.error

# Import subagents module from STUDIO/backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "STUDIO", "backend"))
import subagents

BACKEND_URL = "http://localhost:8000"


def send_post(endpoint, payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(f"{BACKEND_URL}{endpoint}", data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))


def send_get(endpoint):
    req = urllib.request.Request(f"{BACKEND_URL}{endpoint}")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))


def test_governance_acceptance_gate():
    print("=" * 65)
    print("  HERMES V0.3 TOOL GOVERNANCE & SECURITY ACCEPTANCE GATE TEST")
    print("=" * 65)

    passed_count = 0
    total_tests = 7

    # 1. Path Traversal -> DENIED (403)
    status, res = send_get("/api/repo/file?path=../../WINDOWS/System32/drivers/etc/hosts")
    if status == 403 and "PATH TRAVERSAL DENIED" in str(res):
        print(" [PASS] 1. Path Traversal -> DENIED (HTTP 403)")
        passed_count += 1
    else:
        print(f" [FAIL] 1. Path Traversal -> Expected 403, got {status} {res}")

    # 2. No approval token -> 403
    status, res = send_post("/api/action/execute", {"rel_path": "tests/test_dummy.py", "content": "# test"})
    if status == 422 or status == 403:
        print(" [PASS] 2. No Approval Token -> DENIED (HTTP 403 / 422 Validation)")
        passed_count += 1
    else:
        print(f" [FAIL] 2. No Approval Token -> Expected 403/422, got {status}")

    # 3. Invalid token -> 403
    status, res = send_post("/api/action/execute", {"approval_token": "fake-invalid-uuid-123", "rel_path": "tests/test_dummy.py", "content": "# test"})
    if status == 403 and "invalid" in str(res).lower():
        print(" [PASS] 3. Invalid Token -> DENIED (HTTP 403)")
        passed_count += 1
    else:
        print(f" [FAIL] 3. Invalid Token -> Expected 403, got {status} {res}")

    # Helper: Trigger backend propose endpoint to get real capability-bound approval_token
    def fetch_live_approval_token(rel_path="are/experience.py", content=""):
        status, res = send_post("/api/action/propose", {"rel_path": rel_path, "content": content, "action": "write_file"})
        return res.get("approval_token")

    # 4. Token for different action / path -> 403
    token_diff_path = fetch_live_approval_token(rel_path="are/experience.py")
    status, res = send_post("/api/action/execute", {"approval_token": token_diff_path, "rel_path": "tests/WRONG_PATH.py", "content": "# content"})
    if status == 403 and "different path" in str(res).lower():
        print(" [PASS] 4. Token for Different Path -> DENIED (HTTP 403 Capability Mismatch)")
        passed_count += 1
    else:
        print(f" [FAIL] 4. Token for Different Path -> Expected 403, got {status} {res}")

    # 5. Authorized matching action -> ALLOWED (200)
    token_valid = fetch_live_approval_token(rel_path="are/experience.py")
    # Read existing content to avoid destroying file
    exp_file = read_repo_file("are/experience.py")
    existing_content = exp_file.get("content", "# experience module") if isinstance(exp_file, dict) else "# experience module"
    status, res = send_post("/api/action/execute", {"approval_token": token_valid, "rel_path": "are/experience.py", "content": existing_content})
    if status == 200 and res.get("status") == "SUCCESS":
        print(" [PASS] 5. Authorized Matching Action -> ALLOWED (HTTP 200 SUCCESS)")
        passed_count += 1
    else:
        print(f" [FAIL] 5. Authorized Matching Action -> Expected 200, got {status} {res}")

    # 6. Replayed token (consumed token) -> 403
    status, res = send_post("/api/action/execute", {"approval_token": token_valid, "rel_path": "are/experience.py", "content": existing_content})
    if status == 403 and "replayed" in str(res).lower():
        print(" [PASS] 6. Replayed Token (Consumed) -> DENIED (HTTP 403 Single-Use Gate)")
        passed_count += 1
    else:
        print(f" [FAIL] 6. Replayed Token -> Expected 403, got {status} {res}")

    # 7. Dynamic physical evidence -> ZERO hardcoded claims (Categorized)
    analyst = subagents.AREAnalystSubagent()
    result = analyst.run("test AnomalyDetector")
    evidence = result.get("evidence", "")
    if "[OBSERVED]" in evidence and "[DERIVED]" in evidence and "[UNKNOWN]" in evidence:
        print(" [PASS] 7. Dynamic Physical Evidence -> Categorized (OBSERVED / DERIVED / UNKNOWN)")
        passed_count += 1
    else:
        print(f" [FAIL] 7. Dynamic Physical Evidence -> Missing epistemic categories: {evidence}")

    print("=" * 65)
    print(f" GOVERNANCE GATE RESULT: {passed_count}/{total_tests} PASSED ({(passed_count/total_tests)*100:.1f}%)")
    print("=" * 65)

    if passed_count == total_tests:
        print(">>> ALL 7 SECURITY & GOVERNANCE ACCEPTANCE CRITERIA 100% PASSED! <<<")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    from file_scanner import read_repo_file
    test_governance_acceptance_gate()
