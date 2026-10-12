import {NextRequest,NextResponse} from 'next/server';
import {authClient} from '../../../lib/supabase/server';
export const dynamic='force-dynamic';
export async function GET(req:NextRequest){
 const origin=process.env.SITE_URL;if(!origin)return new Response('Authentication setup is pending.',{status:503});
 const code=req.nextUrl.searchParams.get('code');
 if(code){const {error}=await (await authClient()).auth.exchangeCodeForSession(code);if(!error)return NextResponse.redirect(new URL('/',origin),{headers:{'Cache-Control':'no-store'}})}
 return NextResponse.redirect(new URL('/?login_error=google',origin),{headers:{'Cache-Control':'no-store'}});
}
