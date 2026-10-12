# Verification and demonstration

## Automated verification

26 checks passed across the model and local database API tests:

- Seed sizes and coverage; multiple offers do not duplicate student profiles.
- Separate unique-placement and offer counts; derived counts change after recruitment outcomes change.
- Cancelled drives and withdrawn applications excluded from success counts.
- Completed, pending, not-applicable and rejected mandatory clearance behavior.
- Invalid CSV values reported with row-specific errors; comma-containing values parsed correctly.
- Existing student/outcome duplicates skipped without overwriting; duplicate file rows rejected.
- Duplicate roll/email rejected by the server.
- Saved recruitment and clearance changes survive a separate read.
- Student API contains only their own profile, applications and clearances.
- Student mutations/clearance approvals blocked; invalid role sessions blocked.
- Anonymous requests rejected; stale writes rejected; CSV formula injection escaped.

TypeScript and the production build passed after implementation. Browser tests verified sign-in, rendered desktop dashboard, create-student form submission and profile persistence after refreshing.

## Demo sequence

1. Sign in and show in-charge Overview. Explain 9 unique placed students versus 7 offer records in the initial dataset; Aarav has two offers while some selected students have no offer yet.
2. Students → Import Excel/CSV → download template → upload the mixed-validity example → Validate & preview. Show meaningful invalid-row errors and skipped duplicates; import only valid rows.
3. Recruitment → create an Open drive with department/batch, eligibility, deadline and stages.
4. Applications → add an eligible student to that drive → publish the result → progress to Offer Received with a positive package → show updated Overview totals.
5. No-dues → select an incomplete student → update each mandatory category. Keep one Pending and show Incomplete. Then complete it and show Cleared.
6. Open the student’s no-dues statement and print/save as PDF or export CSV.
7. Explore demo roles → Student. Show only that student’s progress, published offers and checklist; administrative edit/approval controls are absent and API checks also block them.
8. Return to in-charge; Reports → select department/batch and student, export student placement and no-dues reports.
9. Refresh/log out and back in. Verify records persist.
10. Present the team’s GitHub repository and actual contributions when the team has connected/created that submission asset.

## Scope notes

The local tests use disposable fictional data. The hosted database is separate and begins with the original 30-student seed. Production is owner-private until an explicit access change is requested. Independent student test credentials and the team’s GitHub history require account/team setup; the prototype does not invent them.
