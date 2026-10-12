import assert from 'node:assert/strict';
import {seed,cleared,successful,hasOffer,csv,previewImport,previewPlacementImport,IMPORT_HEADERS,PLACEMENT_HEADERS} from '../lib/model.ts';
const s=seed();const checks=[];function ok(name,v){assert.ok(v,name);checks.push(name)}
const placed=()=>new Set(s.applications.filter(a=>successful(a,s)).map(a=>a.studentId)).size;
const offers=()=>s.applications.filter(a=>hasOffer(a,s)).length;
ok('A student can have two offers without a duplicate profile',s.students.filter(x=>x.id==='s1').length===1&&s.applications.filter(a=>a.studentId==='s1'&&hasOffer(a,s)).length===2);
ok('Offers and unique placements are separate measures',offers()===7&&placed()===9);
const a=s.applications.find(a=>a.stage==='Shortlisted');a.stage='Offer Received';ok('Outcome updates immediately change derived totals',offers()===8&&placed()===10);a.stage='Withdrawn';ok('Withdrawn applications do not count as placements',offers()===7&&placed()===9);
s.drives.find(d=>d.id==='d1').status='Cancelled';ok('Cancelled drives are excluded from offer and placement totals',offers()===4&&placed()===7);
ok('Initially completed mandatory checklist is cleared',cleared('s1',s));s.clearances.find(c=>c.studentId==='s1'&&c.categoryId==='c1').status='Pending';ok('One pending mandatory item blocks clearance',!cleared('s1',s));s.clearances.find(c=>c.studentId==='s1'&&c.categoryId==='c1').status='Not Applicable';ok('Not Applicable satisfies a mandatory category',cleared('s1',s));s.clearances.find(c=>c.studentId==='s1'&&c.categoryId==='c1').status='Rejected / Further Action Required';ok('One rejected mandatory item blocks clearance',!cleared('s1',s));
const row=['CB26031','Test Student','Computer Science','B.Tech','4','A','2026','new@campus.example','true','true',8,0,'Python, SQL'];const preview=previewImport(csv([IMPORT_HEADERS,row,row]),s);ok('File duplicates are reported',preview[0].status==='ready'&&preview[1].status==='failed');ok('CSV preserves comma-containing skills',preview[0].data.skills==='Python, SQL');
const px=previewPlacementImport(csv([PLACEMENT_HEADERS,['CB26001','Microsoft','Graduate Engineer','Offer Received',20,'true','true','']]),s);ok('Existing placement outcomes are skipped instead of overwritten',px[0].status==='skipped');
ok('Formula-like CSV values are escaped',csv([['=1+1']]).includes("'=1+1"));
console.log(JSON.stringify({passed:checks.length,checks},null,2));
