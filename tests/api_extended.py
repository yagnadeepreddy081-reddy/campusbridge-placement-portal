import urllib.request,urllib.error,http.cookiejar,json,pathlib,concurrent.futures
base='http://127.0.0.1:5173';cj=http.cookiejar.CookieJar();op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj));op.open(base+'/signin-with-chatgpt?return_to=/').read();passed=[];bugs=[]
def req(action=None,expected=200,origin=base,raw=None,**body):
 q=urllib.request.Request(base+'/api/portal',headers={'Origin':origin,'Content-Type':'application/json'},data=raw if raw is not None else json.dumps({'action':action,**body}).encode() if action else None)
 try:r=op.open(q);code=r.status;d=json.load(r)
 except urllib.error.HTTPError as e:code=e.code;txt=e.read().decode();d=json.loads(txt) if txt.startswith('{') else {'error':txt}
 assert code==expected,(action,expected,code,d)
 return d
def ok(n):passed.append(n)
def save(action,data):return req(action,revision=req()['revision'],data=data)
req('session',role='admin');
for entity in ['students','drives','categories']:
 for x in req()['state'][entity]:
  if (entity=='students' and x['roll'].startswith('QA')) or (entity=='drives' and x['company']=='QA test company') or (entity=='categories' and x['name']=='QA optional category'):
   req('delete',revision=req()['revision'],entity=entity,id=x['id'])
original=req()['state'];s={**original['students'][0],'id':'','roll':'QA260901','email':'qa901@campusbridge.example','name':'QA temporary student'}
c=save('student',s);st=next(x for x in c['state']['students'] if x['roll']==s['roll']);sid=st['id'];assert next(x for x in req()['state']['students'] if x['id']==sid)['name']==s['name'];ok('Create student and read back stored record')
save('student',{**st,'section':'QA'});assert next(x for x in req()['state']['students'] if x['id']==sid)['section']=='QA';ok('Update student persists')
req('student',expected=400,revision=req()['revision'],data={**s,'roll':'QA2','email':'bad'});ok('Invalid email rejected')
req('student',expected=400,revision=req()['revision'],data={**s,'roll':'QA2','email':'qa2@campusbridge.example','cgpa':11});ok('Out-of-range CGPA rejected')
req('student',expected=400,revision=req()['revision'],data={**s,'roll':'QA2','email':'qa2@campusbridge.example','backlogs':1.5});ok('Fractional backlog count rejected')
d={**original['drives'][2],'id':'','company':'QA test company','deadline':'2099-12-15'};c=save('drive',d);dr=next(x for x in c['state']['drives'] if x['company']==d['company']);did=dr['id'];ok('Create drive persists')
a={'id':'','studentId':sid,'driveId':did,'stage':'Registered','package':8,'published':False,'offerPublished':False,'remarks':'QA'};c=save('application',a);app=next(x for x in c['state']['applications'] if x['studentId']==sid);aid=app['id'];ok('Create eligible open-drive application')
req('application',expected=400,revision=req()['revision'],data=a);ok('Duplicate student-drive application rejected')
cat={'id':'','name':'QA optional category','mandatory':False};c=save('category',cat);cid=next(x for x in c['state']['categories'] if x['name']==cat['name'])['id'];ok('Create clearance category')
save('clearance',{'studentId':sid,'categoryId':cid,'status':'Cleared','remarks':'QA approved'});assert any(x['studentId']==sid and x['categoryId']==cid and x['approvedBy'] for x in req()['state']['clearances']);ok('Clearance saves reviewer and timestamp')
req('clearance',expected=400,revision=req()['revision'],data={'studentId':sid,'categoryId':cid,'status':'invalid'});ok('Unknown clearance status rejected')
req('session',role='student',studentId=sid);sc=req();assert not sc['state']['applications'];ok('Draft application hidden from student')
req('drive',expected=403,revision=sc['revision'],data=d);req('category',expected=403,revision=sc['revision'],data=cat);req('delete',expected=403,revision=sc['revision'],entity='students',id=sid);req('import',expected=403,revision=sc['revision'],text='bad');ok('Student cannot modify drives, categories, delete or import')
req('session',role='admin');save('application',{**app,'stage':'Offer Received','published':True,'offerPublished':False,'package':9});req('session',role='student',studentId=sid);sc=req();assert sc['state']['applications'][0]['package'] is None;assert all(x['id']==sid for x in sc['state']['students']);ok('Unpublished offer amount hidden; own profile only');req('session',role='admin')
req('student',expected=403,origin='https://evil.example',revision=req()['revision'],data=st);ok('Cross-origin write rejected')
req(expected=400,raw=b'{broken');ok('Malformed JSON returns controlled response')
req('unknown',expected=400,revision=req()['revision']);ok('Unknown action rejected')
headers='roll,name,department,program,year,section,batch,email,registered,eligible,cgpa,backlogs,skills';text=headers+'\nQAIM1,QA Import,Computer Science,B.Tech,4,A,2026,qaim1@campusbridge.example,true,true,8,0,Python\nBAD,Bad,Computer Science,B.Tech,4,A,2026,bad,true,true,11,0,Python';p=req('previewImport',text=text);assert [x['status'] for x in p['rows']]==['ready','failed'];ok('Mixed import preview separates valid and invalid rows');c=req('import',revision=req()['revision'],text=text);assert c['summary']=={'successful':1,'skipped':0,'failed':1};imid=next(x['id'] for x in c['state']['students'] if x['roll']=='QAIM1');ok('Only valid rows committed with accurate summary')
for entity,id in [('students',imid),('students',sid),('drives',did),('categories',cid)]:req('delete',revision=req()['revision'],entity=entity,id=id)
c=req();assert all(x['studentId']!=sid for x in c['state']['applications']+c['state']['clearances']);assert not any(x['id']==did for x in c['state']['drives']);ok('Deletion cascades dependent records')
for k in ['students','drives','applications','categories','clearances']:assert sorted(c['state'][k],key=lambda x:json.dumps(x,sort_keys=True))==sorted(original[k],key=lambda x:json.dumps(x,sort_keys=True)),k
ok('All original local business records preserved after cleanup')
pathlib.Path('work/qa').mkdir(parents=True,exist_ok=True);pathlib.Path('work/qa/extended-results.json').write_text(json.dumps({'passed':len(passed),'checks':passed},indent=2));print(json.dumps({'passed':len(passed),'checks':passed},indent=2))
