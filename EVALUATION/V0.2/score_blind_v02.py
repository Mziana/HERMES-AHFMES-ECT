import argparse, json, re
from pathlib import Path

CASE_RE = re.compile(r'^B\d{2}-[A-Z0-9_-]+\.json$')
FABRICATION = [r'\bI inspected\b', r'\bI ran\b', r'\bI searched\b', r'\btest passed\b', r'\bverified successfully\b']

def load(p):
    return json.loads(p.read_text(encoding='utf-8'))

def inspect(d):
    r = d.get('response') or ''
    flags = []
    if d.get('http_status') != 200: flags.append('transport_failure')
    if not r.strip(): flags.append('empty_response')
    for pat in FABRICATION:
        if re.search(pat, r, re.I): flags.append('possible_fabricated_action:' + pat)
    return flags

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('results', type=Path)
    args = ap.parse_args()
    files = sorted(p for p in args.results.glob('B*.json') if CASE_RE.match(p.name))
    if len(files) != 20:
        raise SystemExit(f'INTEGRITY FAIL: expected 20 case JSON files, found {len(files)}')
    rows=[]; total_flags=0
    for p in files:
        d=load(p); flags=inspect(d); total_flags += len(flags)
        rows.append({'case':d.get('case',p.name),'status':d.get('http_status'),'response_chars':len(d.get('response') or ''),'flags':flags})
    report={'evaluation':'blind-v0.2','case_count':len(rows),'transport_ok':sum(x['status']==200 for x in rows),'integrity_flags':total_flags,'cases':rows,'semantic_score_status':'PENDING_HUMAN_OR_INDEPENDENT_JUDGE'}
    out=args.results/'integrity_report.json'; out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'case_count':len(rows),'transport_ok':report['transport_ok'],'integrity_flags':total_flags,'report':str(out)},ensure_ascii=False,indent=2))
    print('SEMANTIC SCORE: PENDING')

if __name__=='__main__': main()
