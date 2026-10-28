# Shared month-first parser — 379 routed reports, including unresolved symptoms

## Problem and scope

The supplied KB specifies that the shared parser reads every date month first although the affected tenants write the day first. This mechanism can swap the intended month and day in bookings or calendar invites. We have not executed the production parser.

**Reports covered: 379 distinct reports** currently merged into source ticket #4471. Received 2026-04-01 through 2026-10-04, across 11 tenants. The count follows the supplied tenant-based classifier and includes the five anomalous observations described below; it does not claim that all symptoms have one proven explanation.

An independent inspection of the report bodies finds 370 explicit swapped day/month pairs in this routing group, five flagged temporal observations and four more general descriptions. These are evidence categories, not three confirmed causes. All totals describe the 2026-10-04 export, not the live queue on the review date.

Routing: a day-first tenant, except a `form` report from `booking-v3`. App/email reports at booking-v3 tenants remain in this group. The separate booking-v3 hint issue covers the remaining 33 reports and needs a different fix.

## Evidence and reproduction

- `R-41200`: Harbour Dental, `en-GB`, booking-v2, app, received 2026-04-01. The report says a 7 April reminder went out on 4 July.
- Reproduce that class of error with a day-first tenant: enter `07/04/2026` meaning 7 April through the shared parser; the current month-first interpretation yields 4 July. The expected result is 7 April. This is a reproduction derived from the supplied parser specification, not a live production test.
- Source: `src/lib/kb/causes.ts` (`dayFirst`, `causeOf`, `uniqueById`, `groupByCause`), tenant JSON files, and `src/lib/data/reports-4471.json`.
- Export has 427 rows but 412 unique IDs overall; the 15 repeated rows are identical. Group after deduplication. Neither `meta.intakeTag` nor browser locale establishes tenant configuration. The parser group contains 356 parser tags and 23 hint tags.

## Unresolved temporal symptoms retained in this count

`desk-notes.json` flags five reports: `R-41202`, `R-41209`, `R-41236`, `R-41344`, `R-41620`. Their bodies describe a one-day discrepancy, June-only shifts, an invite preceding the booking, or different calendar days in Lisbon and Toronto. The supplied rule routes all five here, but a parser label is not proof of their root cause.

Preserve and investigate these reports before closing this ticket. Confirm actual event times, timezones, calendar-day conversion, event ordering and the tenant settings at the time. A timezone bug is a hypothesis, not an established diagnosis. Split a third issue only when evidence supports a separate cause, preserving counts and IDs.

## Proposed fix and acceptance checks

- Parse by the tenant's documented format or use an unambiguous date input with explicit validation. Do not infer the tenant's format from the reporter's browser.
- Check app, email, booking-v2 form and app/email at booking-v3 tenants.
- For each route, verify an ambiguous date and a day greater than twelve against the intended date, stored booking and generated invite.
- Reconcile every current report ID using a fresh export before moving live reports. Snapshot counts are not live queue totals.
- Resolve or explicitly split the flagged temporal observations before closure. Keep the misleading booking-v3 hint as a separate fix.

The export ends on 2026-10-04; incoming reports start in April and merges start in July. A July merge spike represents processing older reports, not proof of July onset. “Known” and “fix queued” do not mean a deployed fix.

The signed KB review is `src/routes/kb/incidents/4471-review/+page.svx`; its complete rendered capture is `rendered/4471-review.html`, with a browser screenshot at `rendered/4471-review.jpg`.
