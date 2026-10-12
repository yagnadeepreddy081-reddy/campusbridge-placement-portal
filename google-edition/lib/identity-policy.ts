import type {State} from './model';
export function resolveMembership(email:string,state:State,options:{demoAdmin:boolean;adminEmails:string[]}){
 const normalized=email.trim().toLowerCase();const student=state.students.find(s=>s.email.trim().toLowerCase()===normalized);
 const admin=options.demoAdmin||options.adminEmails.some(e=>e.trim().toLowerCase()===normalized);
 return {role:admin?'admin':student?'student':'unassigned',studentId:student?.id??null};
}
