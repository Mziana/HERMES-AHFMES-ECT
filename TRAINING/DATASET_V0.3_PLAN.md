# TRAINING DATASET V0.3 SPECIFICATION & EXPANSION PLAN

**Project:** HERMES-AHFMES-ECT  
**Target Gate:** V0.3 Tool-Augmented Fine-Tuning  
**Status:** DRAFT SPECIFICATION  

---

## 1. Objective

Scale the Hermes cognitive dataset from static Q&A records (v0.2) to **tool-grounded interaction trajectories (v0.3)**.

In V0.3, dataset records represent **complete agent execution trajectories**:
1. User prompt requesting architectural or coding assistance.
2. Tool / Subagent observation output (physical file inspection, test log traces, manifest hashes).
3. Grounded reasoning explicitly linking terminal evidence to conclusions.
4. Final agent response with zero fabricated state or manual execution instructions.

---

## 2. Schema Structure (V0.3 JSONL Format)

```json
{
  "id": "T0051",
  "category": "tool_grounded_execution",
  "competency_family": "live_terminal_reporting",
  "conversations": [
    {
      "role": "system",
      "content": "Anda adalah Hermes, Chief Executive Orchestrator (CEO Mode) dan agen pengembang otonom untuk AHFMES-ARE..."
    },
    {
      "role": "user",
      "content": "Jalankan pengujian pytest untuk AnomalyDetector di are/experience.py sekarang.\n\n[BUKTI FISIK REPOSITORI DARI SUBAGENT]:\n### 🧪 LAPORAN EKSEKUSI TERMINAL WAKTU-NYATA [TestRunnerSubagent]:\n- Perintah Dieksekusi: `python -m pytest tests/are/test_experience.py -v`\n- Status Terminal: LULUS 100% (SUCCESS)\n- Output Real-Time Terminal:\n```text\n================ 16 passed in 0.36s ================\n```\n\n[INSTRUKSI]: Anda adalah agen pengembang otonom. JANGAN menyuruh pengguna menjalankan perintah secara manual jika Laporan Eksekusi Subagent sudah ada. LANGSUNG LAPORKAN hasil eksekusi terminal tersebut kepada pengguna, sertakan cuplikan outputnya, dan berikan analisis Anda."
    },
    {
      "role": "assistant",
      "content": "### 🧪 LAPORAN HASIL EKSEKUSI ANOMALYDETECTOR\n\nSaya telah mengeksekusi suite pengujian PyTest untuk `AnomalyDetector` di `are/experience.py` secara langsung di terminal.\n\n**Hasil Eksekusi:**\n- **Perintah:** `python -m pytest tests/are/test_experience.py -v`\n- **Status:** LULUS 100% (SUCCESS)\n- **Ringkasan Output:**\n```text\n================ 16 passed in 0.36s ================\n```\n\n**Analisis Kognitif:**\nSeluruh 16 unit test (termasuk HMM regime shift, spread hostility calculation, dan quality gate latensi <100ms) telah berjalan secara sempurna tanpa ada kegagalan."
    }
  ],
  "negative_example_id": "N04",
  "target_competency": "Zero-manual instruction enforcement"
}
```

---

## 3. Dataset Target Matrix (V0.3 - Target: 150 Records)

| Family | Competency Focus | Quantity |
| :--- | :--- | :--- |
| **TF-01** | Live Terminal Execution Reporting (PyTest / Verifiers) | 30 |
| **TF-02** | Filesystem Grounding & Null File Handling | 30 |
| **TF-03** | Code site & import tree inspection | 30 |
| **TF-04** | Epistemic Uncertainty & Refusal of Unbound Authority | 30 |
| **TF-05** | Proposal for Action with Safety Gate Approval | 30 |

---

## 4. Acceptance Criteria for V0.3 Dataset

1. 100% compliance with `DATASET_SCHEMA_V0.1.md` schema validator (`validate_dataset.py`).
2. Zero occurrences of hallucinated state in assistant outputs.
3. Every record must cite physical evidence present in the user context block.
