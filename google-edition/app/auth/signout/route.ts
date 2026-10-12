import {NextRequest,NextResponse} from 'next/server';
import {authClient} from '../../../lib/supabase/server';
export async function GET(req:NextRequest){await (await authClient()).auth.signOut();const r=NextResponse.redirect(new URL('/',process.env.SITE_URL||req.url));r.cookies.set('cb_session','',{maxAge:0,path:'/',httpOnly:true,sameSite:'lax'});r.headers.set('Cache-Control','no-store');return r}
