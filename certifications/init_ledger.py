import csv, json, datetime
COLS="provider certification_name official_name official_url credential_type exam_code current_status cost currency free_or_paid estimated_hours prerequisites account_required identity_verification proctored open_book ai_allowed exam_required course_required assessment_required passing_score attempt_limit retake_policy expiration renewal_requirement registration_status study_status exam_status result credential_url certificate_file badge_url issued_date expiry_date notes last_checked".split()
rows=[];prov=None
for l in open('targets.txt',encoding='utf-8'):
    l=l.strip()
    if not l: continue
    if l.startswith('['): prov=l[1:-1]; continue
    r=dict.fromkeys(COLS,'');r.update(provider=prov,certification_name=l,current_status='UNVERIFIED',registration_status='NOT_STARTED',study_status='NOT_STARTED',exam_status='NOT_STARTED',result='')
    rows.append(r)
with open('certification_master.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,COLS);w.writeheader();w.writerows(rows)
json.dump({"updated":datetime.date.today().isoformat(),"total":len(rows),"items":{r['certification_name']:{"provider":r['provider'],"status":"UNVERIFIED"} for r in rows}},open('certification_progress.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
open('credentials.csv','w',encoding='utf-8-sig').write("Provider,Official Credential Name,Credential Type,Issue Date,Expiration Date,Credential ID,Credential URL,Certificate File,Badge URL\n")
print(len(rows))
