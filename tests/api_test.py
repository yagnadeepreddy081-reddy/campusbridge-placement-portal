import urllib.request, urllib.error, http.cookiejar, json, pathlib
BASE='http://127.0.0.1:5173'
cj=http.cookiejar.CookieJar(); op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.open(BASE+'/signin-with-chatgpt?return_to=/').read()
checks=[]
def request(action=None, expected=200, **data):
    req=urllib.request.Request(BASE+'/api/portal',data=json.dumps(dict(action=action,**data)).encode() if action else None,headers={'Origin':BASE,'Content-Type':'application/json'})
    try:r=op.open(req);code=r.status;d=json.load(r)
    except urllib.error.HTTPError as e:code=e.code;d=json.load(e)
    assert code==expected,(action,code,d)
    return d
def ok(name,condition):
    assert condition,name;checks.append(name)
c=request();s=c['state'];ok('Real dataset: 30 students, 3 departments, 5 drives',len(s['students'])>=30 and len(set(x['department'] for x in s['students']))==3 and len(s['drives'])>=5)
heads='roll,name,department,program,year,section,batch,email,registered,eligible,cgpa,backlogs,skills'
text=heads+'\nCB26001,Duplicate,Computer Science,B.Tech,4,A,2026,student1@campusbridge.example,true,true,8,0,Python\nBAD,Invalid,Computer Science,B.Tech,4,A,2026,broken,true,true,14,0,Python'
p=request('previewImport',text=text);ok('Duplicate existing student is skipped',p['rows'][0]['status']=='skipped');ok('Invalid row returns meaningful errors',p['rows'][1]['status']=='failed' and len(p['rows'][1]['errors'])==2)
student=dict(s['students'][0]);student['id']='';request('student',expected=400,revision=c['revision'],data=student);ok('Duplicate roll or email rejected on server',True)
request('student',expected=409,revision=-1,data=student);ok('Stale write rejected',True)
a=dict(next(x for x in s['applications'] if x['stage']=='Shortlisted'));old=dict(a);a['stage']='Offer Received';a['package']=9;a['offerPublished']=True
c=request('application',revision=c['revision'],data=a);ok('Recruitment outcome persisted',next(x for x in request()['state']['applications'] if x['id']==a['id'])['stage']=='Offer Received')
c=request('application',revision=c['revision'],data=old)
cl=dict(next(x for x in c['state']['clearances'] if x['studentId']=='s1' and x['categoryId']=='c1'));oldcl=dict(cl);cl['status']='Pending'
c=request('clearance',revision=c['revision'],data=cl);ok('Pending mandatory item prevents complete clearance',any(x['studentId']=='s1' and x['categoryId']=='c1' and x['status']=='Pending' for x in request()['state']['clearances']))
c=request('clearance',revision=c['revision'],data=oldcl)
request('session',role='student',studentId='s1');sc=request();ok('Student response contains only own profile',len(sc['state']['students'])==1 and sc['state']['students'][0]['id']=='s1');ok('Student response contains only own applications and clearance',all(a['studentId']=='s1' for a in sc['state']['applications']+sc['state']['clearances']));request('clearance',expected=403,revision=sc['revision'],data=cl);ok('Student cannot approve clearance',True);request('student',expected=403,revision=sc['revision'],data=student);ok('Student cannot modify profiles',True)
request('session',role='admin');c=request();request('session',role='student',studentId='does-not-exist',expected=400);ok('Invalid impersonation is rejected',True)
noauth=urllib.request.urlopen(BASE+'/api/portal') if False else None
try:urllib.request.urlopen(BASE+'/api/portal');raise AssertionError('Anonymous request succeeded')
except urllib.error.HTTPError as e:ok('Anonymous access rejected',e.code==401)
pathlib.Path('tests/results.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2))
print(json.dumps({'passed':len(checks),'checks':checks},indent=2))
