import argparse, os
os.environ['HF_HOME'] = os.getenv('HF_HOME', r'D:\Hermes\models\cache')
os.environ['HF_HUB_CACHE'] = os.getenv('HF_HUB_CACHE', r'D:\Hermes\models\cache')
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig
import torch

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--model',default=os.getenv('HERMES_BASE_MODEL','meta-llama/Llama-3.2-3B'))
    ap.add_argument('--data',default='TRAINING/DATASET_V0.2.jsonl')
    ap.add_argument('--output',default='TRAINING/OUTPUT/hermes-lora-v0.1')
    ap.add_argument('--max-seq-length',type=int,default=1024)
    ap.add_argument('--epochs',type=float,default=1.0)
    ap.add_argument('--lr',type=float,default=2e-4)
    args=ap.parse_args()
    if not torch.cuda.is_available(): raise SystemExit('CUDA GPU not detected; aborting GPU QLoRA training.')
    ds=load_dataset('json',data_files=args.data)['train']
    ds=ds.filter(lambda x:x['split'] in ('train','validation'))
    train=ds.filter(lambda x:x['split']=='train'); val=ds.filter(lambda x:x['split']=='validation')
    tokenizer=AutoTokenizer.from_pretrained(args.model,use_fast=True)
    if tokenizer.pad_token is None: tokenizer.pad_token=tokenizer.eos_token
    def fmt(x): return f"### Instruction\n{x['instruction']}\n\n### Context\n{x['context']}\n\n### Response\n{x['response']}"
    bnb=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
    model=AutoModelForCausalLM.from_pretrained(args.model,quantization_config=bnb,device_map='auto',torch_dtype=torch.float16)
    model=prepare_model_for_kbit_training(model)
    lora=LoraConfig(r=8,lora_alpha=16,lora_dropout=.05,target_modules=['q_proj','k_proj','v_proj','o_proj'],bias='none',task_type='CAUSAL_LM')
    for p in model.parameters():
        if p.requires_grad: p.data = p.data.to(torch.float16)
    cfg=SFTConfig(output_dir=args.output,num_train_epochs=args.epochs,learning_rate=args.lr,per_device_train_batch_size=1,per_device_eval_batch_size=1,gradient_accumulation_steps=8,gradient_checkpointing=True,fp16=False,bf16=False,optim='paged_adamw_8bit',logging_steps=1,save_strategy='epoch',eval_strategy='epoch',report_to='none',max_length=args.max_seq_length,packing=False)
    trainer=SFTTrainer(model=model,processing_class=tokenizer,train_dataset=train,eval_dataset=val if len(val) else None,peft_config=lora,args=cfg,formatting_func=fmt)
    trainer.train(); trainer.save_model(args.output); tokenizer.save_pretrained(args.output)
    print(f'ADAPTER SAVED: {args.output}')

if __name__=='__main__': main()
