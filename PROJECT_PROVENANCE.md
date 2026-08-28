# PROJECT PROVENANCE MANIFEST — HERMES-AHFMES-ECT

**Project:** HERMES External Cognitive Tandem  
**Canonical Status:** PILOT / PROOF-OF-CONCEPT EVALUATED  
**Last Updated:** 2026-08-28  

---

## 1. Model Provenance

| Property | Canonical Value | Verification Source |
| :--- | :--- | :--- |
| **Base Model Identity** | `unsloth/Llama-3.2-3B-Instruct` | `TRAINING/QLORA/train_lora.py` |
| **Base Model Family** | Llama 3.2 3B Parameters | Meta Open-Weights / Unsloth Quantized |
| **Quantization Format** | 4-bit NormalFloat (NF4) | `BitsAndBytesConfig` |
| **Model Cache Location** | `D:\Hermes\models\cache` | Environment Override (`HF_HOME`) |
| **LoRA Target Modules** | `q_proj`, `k_proj`, `v_proj`, `o_proj` | `LoraConfig` (r=8, alpha=16, dropout=0.05) |

---

## 2. Dataset Provenance

| Dataset Artifact | Record Count | Split Allocation | Verification Status |
| :--- | :---: | :--- | :--- |
| `TRAINING/DATASET_V0.1.jsonl` | 20 | Pilot V0.1 | Archived |
| `TRAINING/DATASET_V0.2.jsonl` | 50 | 40 Train / 5 Val / 5 Heldout | **VALIDATED** (`validate_dataset.py`) |

---

## 3. Training Run Provenance

- **Run ID:** `qlora-v0.2-20260827`
- **Execution Environment:** Windows 10, PyTorch 2.5.1+cu121, CUDA 12.1, GTX 1050 Ti (4GB VRAM)
- **Optimizer:** `paged_adamw_8bit`
- **Epochs:** 3.0 (15 total steps)
- **Learning Rate:** 2e-4 (cosine decay)
- **Training Duration:** 250.4 seconds
- **Output Adapter Location:** `TRAINING/OUTPUT/hermes-lora-v0.2/adapter_model.safetensors` (8.78 MB)

---

## 4. Ollama Deployment Provenance

- **Ollama Model Name:** `hermes-v0.2` (Aliased tag: `hermes-v0.2:latest`)
- **Ollama Model Digest:** `f372881698b9` (2.0 GB GGUF layer)
- **Profile Integration:** `C:\Users\Fajar\AppData\Local\hermes\profiles\ahfmes\config.yaml` (`local-(localhost:11434)`)

---

## 5. Epistemic Boundary Policy

```text
MODEL HYPOTHESIS
      ↓
TOOL INSPECTION (PHYSICAL FILESYSTEM / SEARCH)
      ↓
OBSERVED EVIDENCE
      ↓
VERIFICATION
      ↓
QUALIFIED CONCLUSION
```

*Rule:* Hermes is strictly forbidden from asserting repository or file state based on internal parametric memory without observed evidence from tool execution.
