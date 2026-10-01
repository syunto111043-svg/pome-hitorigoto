import csv, json, glob, datetime
rows=list(csv.DictReader(open('certification_master.csv',encoding='utf-8-sig')))
cols=list(rows[0].keys())
res={}
for f in glob.glob('_research/*.json'):
    d=json.load(open(f,encoding='utf-8'))
    if isinstance(d,dict): d=d.get('items') or d.get('certifications') or list(d.values())
    for o in d:
        if isinstance(o,dict) and o.get('certification_name'): res[o['certification_name']]=o
def s(v): return '' if v is None else str(v)
hit=0
for r in rows:
    o=res.get(r['certification_name'])
    if not o: continue
    hit+=1
    for k,v in o.items():
        if k in cols and k not in('certification_name','current_status'): r[k]=s(v)
    av=s(o.get('availability')).upper()
    r['current_status']={'AVAILABLE':'VERIFIED','RENAMED':'VERIFIED','DISCONTINUED':'DISCONTINUED','NOT_FOUND':'NOT_AVAILABLE'}.get(av,'UNVERIFIED')
    if r['current_status']=='NOT_AVAILABLE': r['notes']=('[公式未確認: 提供終了とは未確定] '+r['notes'])[:300]
    r['last_checked']=datetime.date.today().isoformat()
with open('certification_master.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,cols);w.writeheader();w.writerows(rows)
from collections import Counter
print(hit,Counter(r['current_status'] for r in rows))
