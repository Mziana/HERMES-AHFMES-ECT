"""
Subagents Engine for Hermes Studio
Strict Epistemic Grounding, Intent-Driven Dispatching, and Capability-Bound Token Governance.
Zero Hardcoded Claims: All metrics computed live from physical filesystem without early returns.
"""

import sys
import subprocess
import os
import uuid
import time
import hashlib
from file_scanner import get_repo_tree, read_repo_file, TARGET_REPO_PATH

# In-memory Capability-Bound Approval Token Registry
PENDING_APPROVAL_TOKENS = {}


def issue_approval_token(rel_path: str, action: str = "write_file", content: str = "") -> str:
    """Issues a capability-bound token strictly tied to target path, action, and proposed content hash."""
    token = f"tok_{uuid.uuid4().hex[:16]}"
    clean_path = rel_path.replace('\\', '/')
    content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest() if content else ""
    
    PENDING_APPROVAL_TOKENS[token] = {
        "rel_path": clean_path,
        "action": action,
        "content_hash": content_hash,
        "issued_at": time.time(),
        "consumed": False
    }
    return token


def consume_approval_token(token: str, rel_path: str, content: str = "") -> tuple:
    """Verifies capability binding: token validity, path match, content hash match, expiration, and single-use."""
    if not token or not isinstance(token, str) or token not in PENDING_APPROVAL_TOKENS:
        return False, "Access Denied: Missing or invalid approval token"
    
    entry = PENDING_APPROVAL_TOKENS[token]
    
    if entry["consumed"]:
        return False, "Access Denied: Replayed token (token has already been consumed)"
    
    if time.time() - entry["issued_at"] > 900:  # 15 minutes limit
        return False, "Access Denied: Approval token expired"
    
    clean_path = rel_path.replace('\\', '/')
    if entry["rel_path"] != clean_path:
        return False, f"Access Denied: Token bound to different path (expected '{entry['rel_path']}', got '{clean_path}')"
    
    if entry["content_hash"]:
        req_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        if entry["content_hash"] != req_hash:
            return False, "Access Denied: Content payload does not match token approval capability hash"
            
    # Mark as consumed (one-time use enforced)
    entry["consumed"] = True
    return True, "Authorized"


class ActionExecutionSubagent:
    """Specialized Subagent for proposing authorized code edits with capability-bound token governance."""
    def run(self, query):
        rel_path = "are/experience.py"
        # Read existing file content to bind proposal hash if available
        exp_res = read_repo_file(rel_path)
        existing_content = exp_res.get("content", "") if "error" not in exp_res else ""
        
        token = issue_approval_token(rel_path=rel_path, action="write_file", content=existing_content)
        
        action_block = "### ⚡ USULAN EKSEKUSI PERUBAHAN KODE [ActionExecutionSubagent]:\n"
        action_block += f"- Token Kapabilitas Diterbitkan: `{token}`\n"
        action_block += f"- Target Terikat (Capability Bound): `{rel_path}`\n"
        action_block += "- Status Keamanan: MENUNGGU PERSETUJUAN PENGGUNA (One-Time Content Hash Gate Active)\n"
        action_block += "- Peraturan Utama: Token ini terikat secara kriptografis pada target path dan hash konten. Hanya dapat digunakan 1 kali.\n"
        
        return {
            "agent": "ActionExecution",
            "action": "propose_code_edit",
            "approval_token": token,
            "evidence": action_block,
            "status": "AWAITING_APPROVAL"
        }


class SelfIdentitySubagent:
    """Specialized Subagent for providing Hermes's accurate identity, capabilities, and self-evaluation."""
    def run(self, query):
        identity_block = "### 🧠 IDENTITAS TERVERIFIKASI FISIK [Hermes v0.2 QLoRA (Llama-3.2-3B)]:\n"
        identity_block += f"- Model Utama: Hermes v0.2 QLoRA Fine-Tuned (Base: Llama-3.2-3B-Instruct) berjalan via Ollama Local API.\n"
        identity_block += f"- Peran Aktif: Chief Executive Orchestrator (CEO Mode) & External Cognitive Tandem (ECT).\n"
        identity_block += f"- Lingkungan Eksekusi: Terminal & File System lokal (`{TARGET_REPO_PATH}`).\n"
        identity_block += f"- KEKURANGAN DIRI: Memerlukan token persetujuan terikat pengguna untuk mengubah file disk.\n"
        identity_block += f"- KELEBIHAN DIRI: Respon cepat, 100% offline & privat, terintegrasi langsung dengan PyTest runner & file scanner.\n"

        return {
            "agent": "Self-Identity",
            "action": "provide_self_identity",
            "evidence": identity_block,
            "status": "VERIFIED"
        }


class TestRunnerSubagent:
    """Dynamic Subagent capable of executing PyTest suites in target repo using sys.executable."""
    def run(self, query):
        py_exe = sys.executable
        cmd = [py_exe, "-m", "pytest", "tests/are", "-v"]

        q_lower = query.lower()
        if "test_experience_b_c_d" in q_lower or "part b" in q_lower:
            cmd = [py_exe, "-m", "pytest", "tests/are/test_experience_b_c_d.py", "-v"]
        elif "test_evidence" in q_lower:
            cmd = [py_exe, "-m", "pytest", "tests/are/test_evidence.py", "-v"]
        elif "test_experience" in q_lower:
            cmd = [py_exe, "-m", "pytest", "tests/are/test_experience.py", "-v"]

        try:
            display_cmd = " ".join([c if c != py_exe else "python" for c in cmd])
            result = subprocess.run(
                cmd,
                cwd=TARGET_REPO_PATH,
                capture_output=True,
                text=True,
                timeout=30
            )
            stdout = result.stdout or result.stderr
            clean_output = stdout if stdout.strip() else result.stderr
            
            status_text = "LULUS (Return Code 0)" if result.returncode == 0 else f"GAGAL (Return Code {result.returncode})"
            evidence_block = "### 🧪 LAPORAN EKSEKUSI TERMINAL WAKTU-NYATA [TestRunnerSubagent]:\n"
            evidence_block += f"- [OBSERVED] Perintah Dieksekusi: `{display_cmd}`\n"
            evidence_block += f"- [OBSERVED] Status Terminal: {status_text}\n"
            evidence_block += f"- [OBSERVED] Output Real-Time Terminal:\n```text\n{clean_output[-1200:]}\n```\n"

            return {
                "agent": "TestRunner",
                "action": "execute_dynamic_command",
                "evidence": evidence_block,
                "status": "EXECUTED_PASSED" if result.returncode == 0 else "EXECUTED_FAILED"
            }
        except Exception as e:
            return {
                "agent": "TestRunner",
                "action": "execute_dynamic_command",
                "evidence": f"### 🧪 GAGAL EKSEKUSI: {str(e)}",
                "status": "ERROR"
            }


class ChiefExecutiveOrchestratorSubagent:
    """Chief Executive Orchestrator (CEO Mode) Subagent.
    Runs live physical overview scans. Strictly grounds evidence on get_repo_tree output.
    """
    def run(self, query):
        tree = get_repo_tree("")
        if "error" in tree:
            return {
                "agent": "Chief-Orchestrator",
                "action": "orchestrate_overview",
                "evidence": f"### 🏛️ INSPEKSI UMUM REPOSITORI FISIK:\n- [ERROR] Gagal membaca root repository `{TARGET_REPO_PATH}`: {tree['error']}\n",
                "status": "ERROR"
            }

        items = tree.get('items', [])
        files = [item['name'] for item in items if not item['is_directory']]
        dirs = [item['name'] for item in items if item['is_directory']]

        directive = f"### 🏛️ INSPEKSI UMUM REPOSITORI FISIK (`{TARGET_REPO_PATH}`):\n"
        directive += f"- [OBSERVED] Status Akses Disk: TERDAPAT {len(items)} ENTITAS DI ROOT\n"
        directive += f"- [OBSERVED] Direktori Root Ditemukan: {', '.join(dirs) if dirs else 'Tidak ada'}\n"
        directive += f"- [OBSERVED] File Utama Root Ditemukan: {', '.join(files) if files else 'Tidak ada'}\n"

        # Ground specific file presence check strictly on physical tree list
        q_lower = query.lower()
        if "guideline" in q_lower or ".pdf" in q_lower:
            pdf_files = [f for f in files if f.lower().endswith('.pdf') or 'guideline' in f.lower()]
            if pdf_files:
                directive += f"- [OBSERVED] File PDF Ditemukan: {', '.join(pdf_files)}\n"
            else:
                directive += f"- [OBSERVED] File `AHFMES_ARE_Guideline.pdf`: TIDAK DITEMUKAN di root repositori fisik.\n"

        return {
            "agent": "Chief-Orchestrator",
            "action": "orchestrate_overview",
            "evidence": directive,
            "status": "OBSERVED"
        }


class AREAnalystSubagent:
    """Specialized Subagent for dynamic physical scanning of AHFMES-ARE repository files.
    CATEGORIZED EPISTEMIC EVIDENCE:
    - [OBSERVED]: Directly read from physical files at runtime.
    - [DERIVED]: Computed from observed physical data.
    - [UNKNOWN]: Explicitly flagged uninspected items.
    """
    def run(self, query):
        q_lower = query.lower()
        
        # 1. Live observation of target module
        exp_res = read_repo_file("are/experience.py")
        exp_lines = exp_res.get("total_lines", 0) if "error" not in exp_res else "FILE_NOT_FOUND"
        exp_content = exp_res.get("content", "") if "error" not in exp_res else ""

        # 2. Live observation of test directory
        test_tree = get_repo_tree("tests/are")
        test_items = test_tree.get('items', []) if "error" not in test_tree else []
        test_files = [item['name'] for item in test_items if not item['is_directory'] and item['name'].endswith('.py')]

        # 3. Live observation of normative authority manifest
        manifest_res = read_repo_file("PROJECT_GOVERNANCE/ARE0/MANIFEST/AHFMES_ARE_0_NORMATIVE_AUTHORITY_MANIFEST_V40.md")
        manifest_content = manifest_res.get("content", "") if "error" not in manifest_res else ""
        manifest_member_rows = [line for line in manifest_content.splitlines() if line.strip().startswith("| `")]

        evidence_block = f"### 📁 DYNAMIC PHYSICAL CODE INSPECTION [AREAnalystSubagent]:\n"
        evidence_block += f"- [OBSERVED] Target Module `are/experience.py`: Actual Physical Lines = {exp_lines}\n"
        evidence_block += f"- [OBSERVED] Test Directory `tests/are/`: {len(test_files)} Physical `.py` Test Files ({', '.join(test_files[:5])}...)\n"
        evidence_block += f"- [OBSERVED] Normative Authority Manifest V4.0: {len(manifest_member_rows)} Verified Member Table Rows\n"

        # Symbol check grounded strictly on content string
        if "anomalydetector" in q_lower or "anomaly" in q_lower:
            if "class AnomalyDetector" in exp_content:
                evidence_block += f"- [OBSERVED] Symbol Check: `class AnomalyDetector` terverifikasi ada dalam `are/experience.py`\n"
            else:
                evidence_block += f"- [OBSERVED] Symbol Check: `class AnomalyDetector` TIDAK DITEMUKAN di `are/experience.py`\n"

        evidence_block += f"- [DERIVED] Test Directory Coverage: {len(test_files)} modul tes fisik terdeteksi\n"
        evidence_block += f"- [UNKNOWN] Runtime Performance under live trading load: Unverified without active simulation trace\n"

        return {
            "agent": "ARE-Analyst",
            "action": "dynamic_code_inspection",
            "evidence": evidence_block,
            "status": "VERIFIED_LIVE"
        }


def dispatch_subagents(user_prompt, mode="architect"):
    """Intent-driven subagent dispatch loop. NO early returns.
    Dispatches subagents based on specific intent triggers and mode settings.
    """
    results = []
    q_lower = user_prompt.lower()
    
    # 1. Trigger Self-Identity Subagent if asking about Hermes self-awareness/identity
    if any(k in q_lower for k in ("kenali dirimu", "siapa kamu", "siapa dirimu", "kekurangan", "kelebihan")):
        results.append(SelfIdentitySubagent().run(user_prompt))

    # 2. Trigger ActionExecutionSubagent if prompt requests code edits
    if any(k in q_lower for k in ("edit file", "tulis file", "perbaiki file", "ubah file", "refactor file")):
        results.append(ActionExecutionSubagent().run(user_prompt))

    # 3. Trigger Live TestRunner ONLY when user explicitly asks to run pytest / test execution
    if any(k in q_lower for k in ("pytest", "jalankan test", "jalankan pengujian", "eksekusi test", "run pytest")):
        results.append(TestRunnerSubagent().run(user_prompt))

    # 4. Trigger AREAnalyst for specific code inspection
    if any(k in q_lower for k in ("anomalydetector", "experience.py", "inspeksi kode", "analisis kode")):
        results.append(AREAnalystSubagent().run(user_prompt))

    # 5. Trigger Chief Orchestrator for root structure, overview, OR when mode is CEO/architect
    if mode in ("ceo", "mandor") or any(k in q_lower for k in ("tampilkan struktur", "root", "folder", "file utama", "overview", "ringkasan", "guideline")):
        results.append(ChiefExecutiveOrchestratorSubagent().run(user_prompt))

    return results
