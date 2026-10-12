import urllib.request,urllib.error,http.cookiejar,json,concurrent.futures,time,pathlib
base='http://127.0.0.1:5173';j=http.cookiejar.CookieJar();o=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(j));o.open(base+'/signin-with-chatgpt?return_to=/');o.open(urllib.request.Request(base+'/api/portal',data=b'{"action":"session","role":"admin"}',headers={'Origin':base,'Content-Type':'application/json'}));cookie='; '.join(c.name+'='+c.value for c in j)
def call(body=None):
 t=time.monotonic();q=urllib.request.Request(base+'/api/portal',headers={'Cookie':cookie,'Origin':base,'Content-Type':'application/json'},data=json.dumps(body).encode() if body else None)
 try:r=urllib.request.urlopen(q);code=r.status;d=json.load(r)
 except urllib.error.HTTPError as e:code=e.code;d=json.load(e)
 return {'status':code,'ms':round((time.monotonic()-t)*1000),'data':d}
c=call()['data'];b={'action':'student','revision':c['revision'],'data':c['state']['students'][0]}
with concurrent.futures.ThreadPoolExecutor(2) as pool:r=list(pool.map(call,[b,b]))
assert sorted(x['status'] for x in r)==[200,409],r
with concurrent.futures.ThreadPoolExecutor(4) as pool:reads=list(pool.map(lambda _:call(),range(20)))
assert all(x['status']==200 for x in reads)
result={'scope':'local application copy only','concurrentWriteStatuses':[x['status'] for x in r],'readRequests':len(reads),'allReadsSuccessful':True,'readMsMin':min(x['ms'] for x in reads),'readMsMax':max(x['ms'] for x in reads)};pathlib.Path('work/qa/concurrency-results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
