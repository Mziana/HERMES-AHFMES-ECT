# QLoRA Training v0.1

## Important
The Ollama `llama3.2:3b` model is not itself the training artifact. Training requires the original Hugging Face Transformers checkpoint (or an equivalent Transformers-format checkpoint) because the Ollama package is a runtime distribution.

Default base model:

`meta-llama/Llama-3.2-3B`

The model may require accepted Meta/Hugging Face licensing and authenticated access.

## Hardware target

Primary target: NVIDIA GTX 1050 Ti 4 GB.

Use 4-bit NF4 QLoRA, batch size 1, gradient accumulation, checkpointing, FP16, and a conservative sequence length. Do not start with 65,536-token training sequences.

The GTX 1050 Ti is Pascal-class. Current bitsandbytes documentation lists Pascal-class NVIDIA GPUs as supported for NF4/FP4 and 8-bit quantization; exact Windows wheel/CUDA compatibility must be validated locally before training. citeturn0search10turn0search11

## Windows setup

Create an isolated environment:

```powershell
python -m venv .venv-hermes-train
.\.venv-hermes-train\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r .\TRAINING\QLORA\requirements.txt
```

Verify CUDA:

```powershell
python -c "import torch; print(torch.__version__); print('cuda=',torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NO CUDA')"
```

Verify bitsandbytes:

```powershell
python -c "import bitsandbytes as bnb; print('bitsandbytes=',bnb.__version__)"
```

If bitsandbytes fails to load on Windows, stop. Do not begin training. Use the current official installation guidance or compile it for the installed CUDA/toolchain. citeturn0search0turn0search14

## Prepare split

```powershell
python .\TRAINING\prepare_dataset_v0_2.py
python .\TRAINING\validate_dataset.py
```

The deterministic seed produces train/validation/held-out partitions. The held-out records must never be passed to the trainer.

## Hugging Face authentication

Set `HERMES_BASE_MODEL` only if using a different compatible Transformers checkpoint. Make sure the account has access to the selected model.

## Smoke training

Start with a tiny run:

```powershell
$env:HERMES_BASE_MODEL="meta-llama/Llama-3.2-3B"
python .\TRAINING\QLORA\train_lora.py --epochs 0.05 --max-seq-length 512
```

A successful smoke run must produce a LoRA adapter without CUDA OOM, NaN loss, or loader errors. Only then consider increasing epochs or sequence length.

## Full first experiment

Do not choose the full run until the corrected blind V0.2 benchmark has been scored and the dataset has been expanded from the 20 seed examples. The 20-example seed is an infrastructure smoke dataset, not a production training corpus.
