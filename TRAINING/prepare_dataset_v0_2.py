import argparse, json, random
from pathlib import Path

FIELDS={'id','source','competencies','instruction','context','response','verification','split','version'}

def load(path):
    rows=[]
    for n,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
        if not line.strip(): continue
        d=json.loads(line)
        missing=FIELDS-set(d)
        if missing: raise ValueError(f'line {n}: missing {sorted(missing)}')
        if d['split']!='train': raise ValueError(f'line {n}: seed dataset must start as train-only')
        rows.append(d)
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',default='TRAINING/DATASET_V0.1.jsonl')
    ap.add_argument('--output',default='TRAINING/DATASET_V0.2.jsonl')
    ap.add_argument('--seed',type=int,default=20260827)
    ap.add_argument('--validation-ratio',type=float,default=.10)
    ap.add_argument('--heldout-ratio',type=float,default=.10)
    args=ap.parse_args()
    rows=load(Path(args.input))
    if len(rows)<10: raise SystemExit('Need at least 10 records before creating splits')
    rng=random.Random(args.seed); rng.shuffle(rows)
    hv=max(1,round(len(rows)*args.heldout_ratio)); vv=max(1,round(len(rows)*args.validation_ratio)); tr=len(rows)-hv-vv
    if tr<1: raise SystemExit('Split leaves no training records')
    for i,d in enumerate(rows): d['split']='train' if i<tr else ('validation' if i<tr+vv else 'heldout'); d['version']='0.2'
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text('\n'.join(json.dumps(x,ensure_ascii=False,separators=(',',':')) for x in rows)+'\n',encoding='utf-8')
    print(f'records={len(rows)} train={tr} validation={vv} heldout={hv}')
    print(out)

if __name__=='__main__': main()
