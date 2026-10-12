import assert from 'node:assert/strict';
import {seed} from '../lib/model.ts';
import {resolveMembership} from '../lib/identity-policy.ts';
const state=seed();let n=0;
function test(name,value,expected){assert.deepEqual(value,expected,name);n++;console.log('PASS '+name)}
test('Any email can enter the explicitly enabled demo',resolveMembership('any@gmail.com',state,{demoAdmin:true,adminEmails:[]}).role,'admin');
test('New Google users are not automatically administrators outside the demo',resolveMembership('new@gmail.com',state,{demoAdmin:false,adminEmails:[]}).role,'unassigned');
test('Allowlisted in-charge has admin access',resolveMembership('OFFICER@gmail.com',state,{demoAdmin:false,adminEmails:['officer@gmail.com']}).role,'admin');
test('Email substring does not grant admin access',resolveMembership('attacker-officer@gmail.com',state,{demoAdmin:false,adminEmails:['officer@gmail.com']}).role,'unassigned');
test('Known university email maps to its own student',resolveMembership('STUDENT1@campusbridge.example',state,{demoAdmin:false,adminEmails:[]}),{role:'student',studentId:'s1'});
test('Demo accounts can explore existing student profiles',resolveMembership('student1@campusbridge.example',state,{demoAdmin:true,adminEmails:[]}),{role:'admin',studentId:'s1'});
console.log(n+' identity policy checks passed');
