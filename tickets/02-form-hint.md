# Booking-v3 promises MM/DD but reads day-first tenant dates — 33 reports

## Problem and scope

The supplied KB specifies that the booking-v3 date field displays `MM/DD/YYYY`, but interprets the submitted date in the day-first tenant's order. Following that instruction can therefore produce the wrong date. This is a form contract mismatch and needs a separate work item from the shared parser issue. We have not executed the production form.

**Reports covered: 33 distinct reports** currently merged into source ticket #4471. Received 2026-04-17 through 2026-09-22. All come through the `form` channel at these three booking-v3 tenants:

- Alder Physio (`alder.physio`, `de-DE`): 12 reports.
- Copper Studio (`copper.studio`, `es-ES`): 11 reports.
- Pale Harbour (`pale.harbour`, `pt-PT`): 10 reports.

These 33 plus 374 reports in the parser ticket and five separately investigated temporal reports account for all 412 unique source reports, with no overlap. Tenant configuration and channel establish the form-hint grouping; intake tags are guesses. Desk-flagged temporal reports are excluded from both mechanism tickets.

All 33 bodies contain explicit swapped day/month pairs. That supports the reported symptom, while the supplied tenant/form/channel specification establishes the proposed mechanism. Neither is a live reproduction. Counts describe the 2026-10-04 export, not the live queue on the review date.

## Evidence and reproduction

- `R-41230`: Copper Studio, form, received 2026-04-17. The report says a client arrived on 1 June instead of 6 January. Intake tagged it `parser`; tenant configuration routes it to the hint problem.
- `R-41241`: Alder Physio, form, received 2026-04-21. The report describes 8 June instead of 6 August.
- With a day-first booking-v3 tenant, follow the field's `MM/DD/YYYY` instruction and type `01/06/2026` for 6 January. Tenant-order parsing instead yields 1 June. Expected: the hint, accepted input and resulting booking all agree. This reproduction is derived from the supplied form/parser specification, not a live production test.
- `src/lib/kb/causes.ts` defines booking-v3's hint and the tenant/channel classifier. `src/lib/kb/locales.ts` reads every tenant JSON; `src/lib/data/reports-4471.json` supplies the report evidence.
- Deduplicate by report ID before counting. The hint group has 18 hint tags and 15 parser tags; grouping on the tag alone gives the wrong scope.

## Proposed fix and acceptance checks

- Align the displayed hint and example with the format the form actually accepts for each tenant, or adopt an unambiguous input that cannot make the promise and interpretation diverge.
- Check all three affected tenant locales and the booking-v3 form route with an ambiguous date and a day greater than twelve.
- Verify the hint, validation, stored date and invite date together; following the hint must produce the user's intended date.
- Confirm that a shared-parser fix alone does not leave the form instruction misleading.
- Refresh reports and historical tenant configuration before moving live reports or claiming live counts. Keep app/email reports from these tenants in the separate shared-parser ticket unless new evidence changes their cause.

This ticket makes visible the second problem hidden by the original “one issue, one fix queued” account. It does not assert that a fix has shipped.

The signed KB review is `src/routes/kb/incidents/4471-review/+page.svx`; its complete rendered capture is `rendered/4471-review.html`, with a browser screenshot at `rendered/4471-review.jpg`.
