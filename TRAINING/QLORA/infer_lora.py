"""
Inference script for Hermes QLoRA v0.2 fine-tuned model.
Loads base model unsloth/Llama-3.2-3B-Instruct and applies adapter from TRAINING/OUTPUT/hermes-lora-v0.2.
Runs inference on heldout cases to evaluate performance improvements.
"""

import os
os.environ['HF_HOME'] = r'D:\Hermes\models\cache'
os.environ['HF_HUB_CACHE'] = r'D:\Hermes\models\cache'

import argparse
import json
import torch
from datasets import load_dataset
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base-model', default='unsloth/Llama-3.2-3B-Instruct')
    ap.add_argument('--adapter', default='TRAINING/OUTPUT/hermes-lora-v0.2')
    ap.add_argument('--data', default='TRAINING/DATASET_V0.2.jsonl')
    ap.add_argument('--output', default='EVALUATION/V0.2/HELDOUT_RESULTS_V0.2.json')
    args = ap.parse_args()

    print(f"Loading base model '{args.base_model}' with adapter '{args.adapter}'...")
    tokenizer = AutoTokenizer.from_pretrained(args.base_model, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    bnb = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type='nf4',
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16,
    )
    base_model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        quantization_config=bnb,
        device_map='auto',
        torch_dtype=torch.float16,
    )

    model = PeftModel.from_pretrained(base_model, args.adapter)
    model.eval()

    ds = load_dataset('json', data_files=args.data)['train']
    heldout = ds.filter(lambda x: x['split'] == 'heldout')

    results = []
    print(f"Running inference on {len(heldout)} heldout test cases...")
    for idx, example in enumerate(heldout):
        prompt = f"### Instruction\n{example['instruction']}\n\n### Context\n{example['context']}\n\n### Response\n"
        inputs = tokenizer(prompt, return_tensors='pt').to('cuda')

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.2,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
            )

        gen_text = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)

        results.append({
            "id": example.get("id", f"heldout_{idx}"),
            "instruction": example["instruction"],
            "expected_response": example["response"],
            "generated_response": gen_text.strip(),
        })
        print(f"Completed heldout case {idx + 1}/{len(heldout)}: {example.get('id', idx)}")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"HELDOUT RESULTS SAVED: {args.output}")


if __name__ == '__main__':
    main()
