import 'server-only';
import {createClient} from '@supabase/supabase-js';
import {State} from '../model';
export function portalStore(){
 if(!process.env.SUPABASE_SERVICE_ROLE_KEY)throw Error('Database setup is pending.');
 const db=createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!,process.env.SUPABASE_SERVICE_ROLE_KEY,{auth:{persistSession:false,autoRefreshToken:false}});
 const check=(error:any)=>{if(error)throw Error('Database operation failed. Check the database setup and server logs.')};
 return {
 async load(initial:State){const {error}=await db.from('portal_state').upsert({id:'main',payload:JSON.stringify(initial),revision:0},{onConflict:'id',ignoreDuplicates:true});check(error);const r=await db.from('portal_state').select('*').eq('id','main').single();check(r.error);return r.data!},
 async membership(id:string){const r=await db.from('membership').select('*').eq('id',id).maybeSingle();check(r.error);return r.data},
 async assign(id:string,role:string,studentId:string|null){const r=await db.from('membership').upsert({id,role,student_id:studentId},{onConflict:'id'}).select('*').single();check(r.error);return r.data!},
 async session(id:string,user:string){const r=await db.from('sessions').select('*').eq('id',id).eq('user_id',user).gt('expires',Date.now()).maybeSingle();check(r.error);return r.data},
 async createSession(id:string,user:string,role:string,studentId:string|null,expires:number){const r=await db.from('sessions').insert({id,user_id:user,role,student_id:studentId,expires});check(r.error)},
 async save(state:State,revision:number){const r=await db.from('portal_state').update({payload:JSON.stringify(state),revision:revision+1}).eq('id','main').eq('revision',revision).select('id');check(r.error);return !!r.data?.length}
 };
}
