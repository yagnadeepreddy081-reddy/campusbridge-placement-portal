import {NextResponse} from 'next/server';
import {authClient} from '../../../lib/supabase/server';
export const dynamic='force-dynamic';
export async function GET(){
 try{
  const origin=process.env.SITE_URL;if(!origin)throw Error('Google sign-in setup is pending: set the portal URL.');
  const {data,error}=await (await authClient()).auth.signInWithOAuth({provider:'google',options:{redirectTo:new URL('/auth/callback',origin).toString(),queryParams:{prompt:'select_account'},skipBrowserRedirect:true}});
  if(error||!data.url)throw Error('Google sign-in is unavailable. Enable the Google provider in the Supabase project.');
  return NextResponse.redirect(data.url,{headers:{'Cache-Control':'no-store'}});
 }catch(e:any){return new Response(e.message,{status:503,headers:{'Content-Type':'text/plain; charset=utf-8','Cache-Control':'no-store'}})}
}
