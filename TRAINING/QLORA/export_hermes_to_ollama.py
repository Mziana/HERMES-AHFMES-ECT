"""
Export Hermes QLoRA v0.2 model to Ollama so it can be selected directly inside Hermes Agent.

Steps:
1. Load base model unsloth/Llama-3.2-3B-Instruct and adapter TRAINING/OUTPUT/hermes-lora-v0.2.
2. Merge adapter into base model weights.
3. Save merged 16-bit model to D:\Hermes\models\hermes-v0.2-merged.
4. Convert merged model to GGUF or build Ollama model 'hermes-v0.2'.
"""

import os
import sys
import subprocess
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ['HF_HOME'] = r'D:\Hermes\models\cache'
os.environ['HF_HUB_CACHE'] = r'D:\Hermes\models\cache'

SYSTEM_PROMPT = """You are Hermes, an independent External Cognitive Tandem and engineering consultant for AHFMES-ARE. You adhere strictly to evidence-based reasoning, clear uncertainty calibration, non-destructive action safety, and trade-off precision. You distinguish clearly between facts, hypotheses, and unknowns. You answer directly, concisely, and accurately."""


def main():
    base_model_path = "unsloth/Llama-3.2-3B-Instruct"
    adapter_path = "TRAINING/OUTPUT/hermes-lora-v0.2"
    merged_output_dir = r"D:\Hermes\models\hermes-v0.2-merged"

    print("=" * 65)
    print(" EXPORTING HERMES QLORA V0.2 TO OLLAMA (FOR HERMES AGENT)")
    print("=" * 65)

    print(f"\n[1/4] Loading base model '{base_model_path}' and adapter '{adapter_path}'...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_path, use_fast=True)

    # Load base model in float16 on CUDA for fast merging
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        torch_dtype=torch.float16,
        device_map="cuda",
    )

    print("[2/4] Merging LoRA adapter into base model weights...")
    model = PeftModel.from_pretrained(base_model, adapter_path)
    merged_model = model.merge_and_unload()

    print(f"[3/4] Saving merged model to '{merged_output_dir}'...")
    os.makedirs(merged_output_dir, exist_ok=True)
    merged_model.save_pretrained(merged_output_dir, max_shard_size="4GB")
    tokenizer.save_pretrained(merged_output_dir)

    print(f"[4/4] Creating Ollama Modelfile for 'hermes-v0.2'...")
    modelfile_path = os.path.join(merged_output_dir, "Modelfile")
    with open(modelfile_path, "w", encoding="utf-8") as f:
        f.write(f'FROM "{merged_output_dir}"\n')
        f.write(f'SYSTEM """{SYSTEM_PROMPT}"""\n')
        f.write('PARAMETER temperature 0.3\n')
        f.write('PARAMETER top_p 0.9\n')
        f.write('PARAMETER num_ctx 65536\n')

    print(f"Modelfile created at {modelfile_path}")
    print("Running 'ollama create hermes-v0.2 -f Modelfile'...")

    res = subprocess.run(["ollama", "create", "hermes-v0.2", "-f", modelfile_path], capture_output=True, text=True)
    print(res.stdout)
    if res.returncode == 0:
        print("\nSUCCESS! Ollama model 'hermes-v0.2' created successfully!")
        print("You can now run 'hermes' or select model 'hermes-v0.2' inside Hermes Agent!")
    else:
        print(f"\nOllama creation failed:\n{res.stderr}")


if __name__ == '__main__':
    main()
