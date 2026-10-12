# CampusBridge — Direct Google Login

This is the portable Google-only login edition of CampusBridge. It runs on ordinary Next.js hosting such as Vercel, with Supabase Auth and PostgreSQL. It does not redirect users through ChatGPT.

## Delivery status

The Google sign-in button, PKCE OAuth flow, callback/code exchange, verified server-side identity, session refresh, sign-out, role policy and persistent database integration are implemented. TypeScript, the production build and isolated business/role tests can run without credentials.

Live activation and a complete Google round-trip require a connected Supabase project, a configured Google OAuth client, and a hosting deployment. These are not configured in the delivered source. The existing Sites-hosted portal is unchanged. This edition starts a separate demo database; do not switch real users over without migrating their current records.

## Activate

1. Connect Supabase and Vercel to the current chat, or create projects in their dashboards.
2. Apply `supabase/schema.sql` in the Supabase SQL editor. Only the backend service role can access portal tables; browser users have no direct table permissions.
3. In Google Cloud, create an OAuth Web application for CampusBridge. Use only `openid`, email and profile scopes. Configure the consent audience and test users if Google keeps the app in testing mode.
4. In Supabase Authentication → Sign In / Providers → Google, enable Google and enter the OAuth client ID and client secret. Register the callback URL shown there (`https://YOUR_PROJECT.supabase.co/auth/v1/callback`) as an authorized Google redirect URI. Keep the secret in the provider settings, not in source or chat.
5. Create a Vercel project from this directory. Configure its environment variables using `.env.example` as a list of names. `SUPABASE_SERVICE_ROLE_KEY` is server-only and must be stored as a secret. Never prefix it with `NEXT_PUBLIC_`.
6. Set `SITE_URL` to the final application origin, such as your Vercel domain. Set the same URL as the Supabase Site URL and allow `https://YOUR_APP/auth/callback` as a redirect URL.
7. As requested for this fictional-data demo, set `ALLOW_DEMO_ADMIN=true` to permit any verified Google account to enter the in-charge workspace and explore student demo sessions. For a university installation, set it to false and set `IN_CHARGE_EMAILS` to explicit in-charge addresses. Other verified Google users then receive only their matching student profile or an unassigned-account screen.
8. Deploy, sign in with Google, test an outcome update, switch to the student demo role, check clearance restrictions, refresh, and sign out/in again.

Google OAuth documentation: https://supabase.com/docs/guides/auth/social-login/auth-google
Supabase server session documentation: https://supabase.com/docs/guides/auth/server-side/creating-a-client?framework=nextjs

## Local development

Node >=22.13.0. Run `npm ci`, create an ignored `.env.local` using the key names in `.env.example`, then `npm run dev`. Register the local application origin and `/auth/callback` in Supabase's redirect configuration when testing locally.

`npm run typecheck` checks types. `npm test` runs 13 placement, clearance and import checks. `node --experimental-strip-types tests/identity_test.mjs` runs six Google-role policy checks. `npm run build` creates the production build.

## Security and roles

Every data request obtains a server-verified Google identity through Supabase `getUser()`. Browser-supplied identity headers from the previous host are ignored. An email alone is never accepted as authentication. Callback code exchange uses Supabase's PKCE verifier and request cookies. Tokens refresh through the Next.js proxy. Admin roles come from the server's configured demo mode or exact email allowlist, not user-submitted fields. Demo student sessions are HttpOnly, tied to their authenticated in-charge, and checked on each request.

The data layer retains optimistic revisions, duplicate detection, import validation, published-only student results, offer visibility controls and mandatory-checklist rules. The server-only Supabase key is used after authentication and role authorization; no service key is bundled into browser code.

## Portal features

Student profiles and Excel/CSV imports; company and drive management; applications, selections and multiple offers; dynamic statistics; configurable no-dues requirements; department/batch summaries; placement and clearance reports; CSV exports and printable statements. The sample set includes 30 students, three departments, five drives and mixed recruitment/clearance statuses.
