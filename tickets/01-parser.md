# Shared month-first parser — 374 reports

## Problem and scope

The supplied KB specifies that the shared parser reads every date month first although the affected tenants write the day first. This mechanism can swap the intended month and day in bookings or calendar invites. We have not executed the production parser.

**Reports covered: 374 distinct reports** from source ticket #4471. Received 2026-04-01 through 2026-10-04, across 11 tenants. This scope excludes all five desk-flagged temporal reports, which have their own work item. It covers the month/day parser problem alone; a routing label does not prove every report's root cause.

An independent inspection of the report bodies finds 370 explicit swapped day/month pairs and four more general descriptions in this scope. All totals describe the 2026-10-04 export, not the live queue on the review date.

Scope: a day-first tenant, except a `form` report from `booking-v3`; then exclude every ID in desk-notes.json's oneDayMove list. App/email reports at booking-v3 tenants remain here. The separate form-hint and temporal work items cover 33 and five reports respectively. The three scopes are disjoint and cover all 412 distinct source reports.

## Evidence and reproduction

- `R-41200`: Harbour Dental, `en-GB`, booking-v2, app, received 2026-04-01. The report says a 7 April reminder went out on 4 July.
- Reproduce that class of error with a day-first tenant: enter `07/04/2026` meaning 7 April through the shared parser; the current month-first interpretation yields 4 July. The expected result is 7 April. This is a reproduction derived from the supplied parser specification, not a live production test.
- Source: `src/lib/kb/causes.ts` (`dayFirst`, `causeOf`, `uniqueById`, `groupByCause`), tenant JSON files, and `src/lib/data/reports-4471.json`.
- Export has 427 rows but 412 unique IDs overall; the 15 repeated rows are identical. Group after deduplication. Neither `meta.intakeTag` nor browser locale establishes tenant configuration. This parser scope contains 351 parser tags and 23 hint tags. The explicit exclusions are implemented in src/lib/kb/triage.ts.

## Separate temporal work item: excluded from this count

`R-41202`, `R-41209`, `R-41236`, `R-41344` and `R-41620` belong exclusively to the separate temporal work item. They are not included in this ticket's 374 reports.

Do not close that work item on the basis of a month/day parser fix. Its reported behavior needs independent investigation even before its implementation root cause is known.

## Proposed fix and acceptance checks

- Parse by the tenant's documented format or use an unambiguous date input with explicit validation. Do not infer the tenant's format from the reporter's browser.
- Check app, email, booking-v2 form and app/email at booking-v3 tenants.
- For each route, verify an ambiguous date and a day greater than twelve against the intended date, stored booking and generated invite.
- Reconcile every current report ID using a fresh export before moving live reports. Snapshot counts are not live queue totals.
- Keep the temporal work item and the misleading booking-v3 hint as separate investigations/fixes, without counting their report IDs here.

The export ends on 2026-10-04; incoming reports start in April and merges start in July. A July merge spike represents processing older reports, not proof of July onset. “Known” and “fix queued” do not mean a deployed fix.

The signed KB review is `src/routes/kb/incidents/4471-review/+page.svx`; its complete rendered capture is `rendered/4471-review.html`, with a browser screenshot at `rendered/4471-review.jpg`.
