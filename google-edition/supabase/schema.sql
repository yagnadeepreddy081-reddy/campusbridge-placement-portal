create table if not exists public.portal_state (
 id text primary key,
 payload text not null,
 revision integer not null default 0 check(revision>=0)
);
create table if not exists public.membership (
 id text primary key,
 role text not null check(role in ('admin','student','unassigned')),
 student_id text
);
create table if not exists public.sessions (
 id text primary key,
 user_id text not null,
 role text not null check(role in ('admin','student')),
 student_id text,
 expires bigint not null
);
alter table public.portal_state enable row level security;
alter table public.membership enable row level security;
alter table public.sessions enable row level security;
revoke all on public.portal_state,public.membership,public.sessions from anon,authenticated;
grant all on public.portal_state,public.membership,public.sessions to service_role;
create index if not exists sessions_expiry_idx on public.sessions(expires);
