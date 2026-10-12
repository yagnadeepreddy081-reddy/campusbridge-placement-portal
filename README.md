# CampusBridge

University Placement and Department No-Dues Portal — Pixel to Product 2026, problem statement 2.

## Status

Hackathon prototype with a working hosted database. The latest audit found outstanding import-validation, skill-matching, statement-export, mobile sign-out and keyboard issues. Read [the full QA report](docs/QA-REPORT.md) before treating it as production-ready.

The root contains the currently hosted Sites/Vinext edition. [google-edition](google-edition/README.md) contains the separate Next.js + Supabase edition with direct Google OAuth code; it still needs provider configuration and deployment. No Google secrets or database service keys are included.

The original hosted Site is private. This public repository publishes source code, not access to that Site or its database. `.openai/hosting.example.json` documents the hosting configuration; provision your own project before deploying.

## Features

- Responsive in-charge and student dashboards; live database-derived counts and working department, batch, company and drive-status filters.
- Student CRUD, registration/eligibility, year/section, CGPA/backlogs and skills.
- Excel `.xlsx` and CSV student imports with template, preview, validation, duplicate detection, explicit skipped/failed/successful totals and no silent overwrites.
- Company/drive CRUD, eligibility criteria, published/draft visibility, stages, deadlines, package/location and lifecycle statuses.
- Student-company application CRUD, stage tracking, multiple offers, per-application result and offer publishing.
- Excel/CSV placement-outcome imports with validation and duplicate skipping.
- Analytics distinguish unique placed students from offers, exclude cancelled drives/withdrawn records, summarize valid offer packages and show batch comparisons.
- Configurable mandatory/optional no-dues categories; remarks, reviewer and timestamps; automatic overall status.
- Reports: department statistics, company outcomes, student placement history, unplaced students, pending clearances, student statements and batch summaries.
- CSV exports and print/PDF via browser printing. Student history/no-dues reports can be narrowed to one student.
- 30 fictional students, 3 departments, 5 drives, mixed recruitment outcomes, multiple offers, 180 clearance entries and activity log.
- Platform-owned authentication, HttpOnly demo sessions, server-side role checks, CSRF origin checks and optimistic concurrency protection.

## Architecture

React/TypeScript, Vinext (Next.js App Router API), Cloudflare Workers, Cloudflare D1, Drizzle migrations, Lucide icons, SheetJS workbook parsing. Hosted through Sites.

`lib/model.ts` owns the seed dataset, business rules, CSV parsing/escaping and import validation. `app/api/portal/route.ts` owns trusted authorization and data operations. `app/portal.tsx` provides the application UI. `db/schema.ts` defines persisted state, identity memberships and demo sessions.

The demonstration uses one versioned state document in D1. Updates compare revisions and reject stale writes to prevent lost updates. This is suitable for the hackathon-scale dataset; a production university deployment should normalize records and add pagination and operational audit retention.

## Run locally

Use Node >=22.13.0. Run `npm ci`, `npm run db:generate` only when the schema changes, and `npm run build`.

Apply the existing migration once:

```
node --import ./scripts/sites-env.mjs ./node_modules/wrangler/bin/wrangler.js d1 execute DB --local --config dist/server/wrangler.json --persist-to .wrangler/state --file drizzle/0000_marvelous_spyke.sql
```

Run `npm run dev` and open the printed loopback URL. Local sign-in uses the starter's loopback-only simulated identity `seedy@sites.test`. Production does not include this authentication simulation.

The first authenticated visitor to this owner-private demo is provisioned as the in-charge. Only an existing in-charge can open demo student sessions. Later real signed-in students must match the university email stored in their profile; unknown accounts receive an unassigned-account screen. They cannot promote themselves.

## Try both roles

1. Sign in using the platform’s sign-in flow.
2. Open **Explore demo roles**.
3. Select **Student**, then select a fictional profile; Aarav Sharma demonstrates two offers and a completed checklist.
4. Use **Explore demo roles** again to return to Placement In-Charge.

These are server-enforced evaluator demo sessions tied to the signed-in owner. They are not independent password-based test accounts. An actual public multi-user university submission needs separate student identities and an explicit approved access policy. Do not present the demo switch as proof of independent student credentials.

## Calculation definitions

- Placed: a unique student with a Selected, Offer Received or Joined application on a non-cancelled drive.
- Offers: individual Offer Received or Joined applications on non-cancelled drives.
- Department placement percentage: unique eligible, registered students placed divided by all eligible, registered students in that department/batch view.
- Unplaced dashboard count: registered students without qualifying placements in the current filtered application view.
- Package summaries: positive packages from offer records only, in INR lakhs per annum.
- Fully cleared: every mandatory category has an explicit Cleared or Not Applicable record. Missing, Pending or Rejected mandatory records keep the status incomplete. Optional categories do not block overall clearance.
- Student result data is returned only for their own published applications. Unpublished offer amounts are omitted.

## Imports

Use the in-app template or `samples/student-template.csv`. Excel workbooks are parsed from their first worksheet. Maximum file size is 5 MB and maximum import size is 2,000 rows.

Student required headings: roll, name, department, program, year, section, batch, email, registered, eligible, cgpa, backlogs, skills. Skills may be empty. Boolean fields use true/false. Batch is a four-digit year; CGPA is 0–10; backlogs is a non-negative integer. Departments use the configured demo departments: Computer Science, Electronics, Mechanical.

Placement headings: roll, company, job_role, stage, package, published, offer_published, remarks. Company and job_role match an existing drive. A duplicate student-drive outcome is skipped; update existing outcomes explicitly in Applications.

## Tests

- `npx tsc --noEmit`
- `node --experimental-strip-types tests/model_test.mjs`
- Start local preview, then `python3 tests/api_test.py`

See [the latest QA report](docs/QA-REPORT.md) for current passing checks, reproduced bugs and verification limits. `TESTING.md` contains the earlier demonstration sequence.

## Submission items requiring the team

- Genuine team branches/issues/PRs and meaningful human contribution history. This source export does not fabricate team activity.
- Team name, member names, roll numbers and actual responsibilities.
- Public evaluator access and independently usable role accounts. The delivered Site starts owner-private under the hosting platform’s default policy.
- Confirm university-specific eligibility definitions, departments and certificate wording before using real student records.

No private student records, passwords, API keys or privileged database credentials are included.
