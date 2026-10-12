import 'server-only';
import {createServerClient} from '@supabase/ssr';
import {cookies} from 'next/headers';
export function authConfigured(){return !!(process.env.NEXT_PUBLIC_SUPABASE_URL&&process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY)}
export async function authClient(){
 if(!authConfigured())throw Error('Google sign-in setup is pending: configure the Supabase project and enable its Google provider.');
 const jar=await cookies();
 return createServerClient(process.env.NEXT_PUBLIC_SUPABASE_URL!,process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,{
  cookieOptions:{httpOnly:true,sameSite:'lax',secure:process.env.NODE_ENV==='production',path:'/'},
  cookies:{getAll(){return jar.getAll()},setAll(items){for(const {name,value,options} of items)jar.set(name,value,options)}}
 });
}
export async function verifiedIdentity(){
 const client=await authClient();const {data:{user},error}=await client.auth.getUser();
 if(error||!user||!user.email_confirmed_at||!user.identities?.some(i=>i.provider==='google'))throw Error('AUTH');
 return {id:user.id,email:user.email!.toLowerCase()};
}
