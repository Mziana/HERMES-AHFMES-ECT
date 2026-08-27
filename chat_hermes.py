"""
Interactive Chat Interface for Hermes ECT (Llama-3.2-3B QLoRA v0.2)

Allows chatting naturally with the fine-tuned Hermes model directly in terminal or Hermes Agent.
Features conversation memory, streaming-style response delivery, and command controls.
"""

import os
import sys

# Ensure models cache is set to Drive D
os.environ['HF_HOME'] = r'D:\Hermes\models\cache'
os.environ['HF_HUB_CACHE'] = r'D:\Hermes\models\cache'

import warnings
warnings.filterwarnings('ignore')
import logging as py_logging
py_logging.getLogger("transformers").setLevel(py_logging.ERROR)

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, logging
logging.set_verbosity_error()


SYSTEM_PROMPT = """You are Hermes, an independent External Cognitive Tandem and engineering consultant for AHFMES-ARE.
You adhere strictly to evidence-based reasoning, clear uncertainty calibration, non-destructive action safety, and trade-off precision.
You distinguish clearly between facts, hypotheses, and unknowns.
You answer directly, concisely, and accurately."""


def main():
    base_model_path = "unsloth/Llama-3.2-3B-Instruct"
    adapter_path = "TRAINING/OUTPUT/hermes-lora-v0.2"

    print("=" * 65)
    print(" 🚀 HERMES EXTERNAL COGNITIVE TANDEM (v0.2 QLoRA) — CHAT INTERFACE")
    print("=" * 65)
    print(f" Base Model : {base_model_path}")
    print(f" Adapter    : {adapter_path}")
    print(f" Cache Path : {os.environ['HF_HOME']}")
    print("-" * 65)
    print(" Controls: Type 'exit' or 'quit' to end session. Type 'reset' to clear chat history.")
    print("=" * 65)
    print("\n[System] Loading model onto GTX 1050 Ti GPU... Please wait.")

    try:
        tokenizer = AutoTokenizer.from_pretrained(base_model_path, use_fast=True)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        bnb = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.float16,
        )

        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_path,
            quantization_config=bnb,
            device_map='auto',
            torch_dtype=torch.float16,
        )

        model = PeftModel.from_pretrained(base_model, adapter_path)
        model.eval()
        print("[System] Model and LoRA Adapter loaded successfully! Ready to chat.\n")
    except Exception as e:
        print(f"\n❌ Error loading model: {e}")
        sys.exit(1)

    conversation_history = []

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n[Hermes] Session ended. Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("\n[Hermes] Ending chat session. See you next time!")
            break

        if user_input.lower() == "reset":
            conversation_history.clear()
            print("\n[System] Chat history reset.")
            continue

        # Build prompt using Llama-3 / Chat template formatting
        prompt = f"### System\n{SYSTEM_PROMPT}\n\n"
        for user_msg, assistant_msg in conversation_history:
            prompt += f"### Instruction\n{user_msg}\n\n### Response\n{assistant_msg}\n\n"
        prompt += f"### Instruction\n{user_input}\n\n### Response\n"

        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.3,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
            )

        gen_text = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
        print(f"Hermes: {gen_text}")

        # Store in history (keep last 5 turns to stay within context)
        conversation_history.append((user_input, gen_text))
        if len(conversation_history) > 5:
            conversation_history.pop(0)


if __name__ == "__main__":
    main()
