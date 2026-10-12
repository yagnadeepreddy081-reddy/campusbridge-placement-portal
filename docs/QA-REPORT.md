# CampusBridge application test report

Tested live site: https://campusbridge-placement-2026.chicgoose64.chatgpt.site/

**Result: the application runs and the live database saves correctly, but several confirmed bugs and unfinished login setup prevent a full release approval.**

This report separates tests performed on the live website from tests performed on the matching local application. No application fixes were deployed during this audit.

## Database result

The live Cloudflare D1 database is connected. The Sites database viewer returned the expected `DB` binding and `portal_state`, `membership`, and `sessions` tables. I changed one demo student's skills, saved, completely reloaded the browser page, and opened the record again. The changed value was still present. I then restored the original skills and verified them again. The live database revision advanced from 0 to 1 for the test save and to 2 for the restoration.

This proves the live read/write connection and persistence for that workflow. It does not prove unlimited reliability, backups, or performance under heavy production traffic. The import uniqueness bug below concerns data quality, not a disconnected database.

The database viewer limits long values, so its shortened JSON payload was not used to claim a complete row-content comparison. The reload-and-reopen browser check supplied the persistence evidence.

## Confirmed problems

| Priority | Problem in simple words | Where verified | How to reproduce / effect |
|---|---|---|---|
| High | Two new students with the same email can both pass import validation. | Live CSV preview and local model | Upload `duplicate-email-input.csv` from the evidence folder. Both rows display Ready. The import checks existing emails but does not track duplicate emails between new rows in the same file. This can make student-account matching ambiguous. I did not commit these rows on the live site. |
| High | Importing applications can bypass registration eligibility and drive-status checks. | Local model tests and server code | A new Registered application for an ineligible student, or a completed drive, is marked Ready. The normal Add application endpoint enforces an eligible student, an Open drive and an active deadline; the import path does not apply the same registration checks. |
| High | A no-dues statement can download an empty CSV because a different student was selected earlier. | Live browser and downloaded files | In Reports select Diya Patel. Go to No-dues, open Aarav Sharma's checklist and Download CSV from his statement. The on-screen certificate is correct, but the CSV has its header and zero data rows. Without that earlier report selection it has all six clearance rows. The statement export incorrectly inherits the report-student filter. |
| Medium | Skill matching can give the wrong eligibility result. | Local model test | Require Java in a drive and give the student only JavaScript. The current substring check returns Eligible. Skill names need an intentional exact-match or alias policy. |
| Medium | The Sign out button disappears on phones and smaller screens. | Live 390-pixel browser and CSS review | The sidebar profile, containing the only Sign out link, is hidden below 850 pixels. No replacement appears. The phone layout itself fits the viewport. |
| Low | Escape does not close application dialogs. | Live keyboard test | Open Explore demo roles and press Escape from the Role control. The dialog remains open. Close and Cancel buttons work. |
| Low | The server accepts impossible calendar dates. | Local API | Submit a drive deadline of `2026-02-30`. It is accepted because the server checks the date's text shape but not whether the calendar date exists. The normal browser date field reduces exposure, but direct requests still need validation. |

## Login and access setup still unfinished

- Direct Google-only login is **not active on this live URL**. The separate Google/Supabase edition has prepared code, but has not been configured and deployed. Actual Google account selection, callback, cancellation and session expiry cannot be passed as live tests yet.
- The current live Site is owner-private: its access policy allows only the owner and has no external visitors. A general student/evaluator cannot currently use it just by having any Google email. This is the current access configuration, not a database error. I preserved it.

## Live website checks

| Area / buttons | Result |
|---|---|
| Overview, Students, Recruitment, Applications, No-dues, Reports navigation | All six sections open. |
| Refresh data | Reloads stored data without an observed error. |
| Dashboard shortcuts: Export reports, View department report, All drives, Review clearances | Each opens the intended section. |
| Student name search | Correctly reduces the directory to Aarav's record. |
| Department, batch, registration and year filters; Reset | Expected counts and empty states; Reset restores the view. Computer Science has 10 students; its 2025 batch has 2. |
| Add student; Edit record; Save changes; Cancel; Close dialog | Forms open. Empty required fields are blocked. Duplicate roll is rejected by the live server. A reversible edit saves and survives reload. Original skills restored. |
| Student Delete record and Keep record | Confirmation opens and Keep record closes it. Final live deletion deliberately not executed. |
| Recruitment company and status filters | Company filtering works; Cancelled produces an empty state. |
| New drive, edit drive, View recruitment stages | Correct forms/details open. Empty required fields prevent saving. Cancel works. |
| Application search, Add application, edit application | Correct student records and forms open. Application changes and validation were exercised comprehensively on the local copy. |
| Configure checklist, edit category, Add category | Controls open expected forms; empty category name is blocked. |
| Open checklist, Back to students, Update Library | Correct checklist and update form open; Cancel works. |
| No-dues statement and Download CSV | Certificate displays and download occurs. Cross-page empty-export bug reproduced separately. |
| All nine report tabs | Student placement, Department statistics, Company outcomes, Student placement history, Unplaced students, No-dues, Pending no-dues, Student no-dues statement and Batch summary all render. |
| Student-specific report selector | Selected student's placement and clearance rows appear. Its state incorrectly affects later statement export, as reported above. |
| Report Export CSV | Download confirmed and inspected. Batch summary contains three department rows. |
| Print report | Invoked the print flow; Escape returned to the application. Actual printed/PDF pagination and physical printing were not verified. |
| Student CSV upload; Excel `.xlsx` upload; Validate & preview | Both formats produce previews. Excel's first load took noticeably longer and has no clear parsing progress indication; it eventually completed. |
| Download student and placement sample templates | Both template downloads confirmed. |
| Invalid CSV missing columns | Clear missing-column error appears. Dismiss error works. |
| Import valid rows | Preview availability checked live; actual commits and valid/invalid summary counts tested locally to avoid adding fake students to the live workspace. |
| Explore demo roles and Open dashboard | Switched to Aarav's student view and restored Placement In-Charge afterward. |
| Student dashboard, My applications, Recruitment, No-dues, Reports | Only the selected student's personal records appear. No profile/drive edit or clearance approval controls are displayed. Recruitment-stage details remain available. |
| Phone width 390 pixels | Student dashboard, recruitment, applications and reports fit without whole-page horizontal overflow. Tables scroll inside their containers. Mobile Sign out is missing. |
| Browser console / recent server logs | No browser errors/warnings or Worker crash outcomes observed during the collected checks. Controlled 400 validation and 401 authentication responses were expected. |

## Local automated checks

These run against the local copy of the deployed application, not against the live production database.

- 13 business-model checks passed: distinct offers vs students placed, recruitment updates, cancelled/withdrawn exclusions, mandatory clearance rules, imports and CSV formula escaping.
- 13 baseline API checks passed: seeded data, duplicate validation, stale revisions, persisted outcomes, own-student response isolation, forbidden writes, invalid impersonation and anonymous rejection.
- 21 additional API checks passed: create/update student, numeric/email validation, drive/application/category creation, duplicate application rejection, clearance reviewer recording, draft/private offer restrictions, student write restrictions, cross-origin protection, malformed requests, valid-only imports, accurate import counts, cascade deletion and cleanup.
- Concurrent writes to the same revision returned one success and one conflict, protecting against silent overwrite.
- 20 read requests, with four running at a time, all succeeded locally. This is a small smoke test, not a production load test.
- TypeScript checking passed.
- Four extra model edge cases failed, identifying duplicate-email imports, skill substring matching and the two application-import registration bypass examples above.
- A separate local API test reproduced the impossible-date acceptance.

All local temporary business records used by the CRUD tests were removed. The live workspace retains its 30 students, 5 drives and existing demo records. Two live audit entries record the test edit and restoration; editing reorders that student's directory position because the current save logic appends the updated record.

## Verification limits

A real tester cannot honestly certify every possible condition in one session. This audit covers the main button families, data workflows, validation, role views, server checks and one phone width. The following remain unverified:

- Live final permanent deletion and live import commits; their operations were tested on the local database instead.
- Actual sign-out/re-login with a separate student account; the current Site is private. I did not log the user out of their existing session.
- Direct Google OAuth, real Supabase connection and the new deployment: not yet activated.
- Actual saved PDF/physical print layout, Safari/Firefox/Edge differences, real-device touch behavior and assistive-technology testing.
- Large-user production load, long-running sessions, database backup/restore, outage recovery and a full security penetration test.

## Recommended repair order

1. Fix duplicate-email imports and apply the same registration rules to imports and forms.
2. Make statement export use the student whose statement is open, independently of report filters.
3. Fix exact skill matching and server calendar-date validation.
4. Add a visible Sign out control on mobile and keyboard support for dialogs.
5. Configure and deploy the direct Google edition, then test both real account roles and evaluator access.
6. Repeat the failing cases and run multi-browser/print testing before using real university data.

## Evidence

- `CampusBridge-QA-duplicate-preview.jpg`: live preview marks both duplicate-email rows Ready.
- `CampusBridge-QA-mobile.jpg`: mobile layout, with no visible Sign out control.
- `CampusBridge-QA-overview.jpg`: final application view.
- `CampusBridge-QA-evidence/`: input CSV, correct and empty statement downloads, and local machine-readable test results.
