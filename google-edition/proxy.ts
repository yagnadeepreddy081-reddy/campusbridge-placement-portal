import {createServerClient} from '@supabase/ssr';
import {NextResponse,type NextRequest} from 'next/server';
export async function proxy(req:NextRequest){
 if(!process.env.NEXT_PUBLIC_SUPABASE_URL||!process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY)return NextResponse.next();
 let response=NextResponse.next({request:req});
 const client=createServerClient(process.env.NEXT_PUBLIC_SUPABASE_URL,process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY,{
 cookieOptions:{httpOnly:true,sameSite:'lax',secure:process.env.NODE_ENV==='production',path:'/'},
 cookies:{getAll(){return req.cookies.getAll()},setAll(values){values.forEach(({name,value})=>req.cookies.set(name,value));response=NextResponse.next({request:req});values.forEach(({name,value,options})=>response.cookies.set(name,value,options))}}
 });
 await client.auth.getClaims();response.headers.set('Cache-Control','private, no-store');return response;
}
export const config={matcher:['/api/:path*','/auth/:path*']};
