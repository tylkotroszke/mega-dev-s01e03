# Shared month-first parser misreads day-first dates — 379 reports

**Reports covered: 379 unique reports** in export ticket #4471, received 2026-04-01 through 2026-10-04 across 11 tenants.

## Problem

The supplied KB specifies that the shared parser reads dates month first, while the affected tenant locales write the day first. An ambiguous input can therefore produce a different calendar date.

Example: R-41200, Harbour Dental, en-GB, app: a reminder intended for 7 April went out on 4 July. For that tenant, input 07/04/2026 should mean 7 April, not 4 July. This reproduction follows the exported specification; we have not executed the production parser.

## Scope and count

Deduplicate reports by ID, filter mergedInto = 4471, and select the parser result from the supplied causeOf rule using tenant configuration and channel. This includes app/email routes and booking-v2 forms, including app/email at booking-v3 tenants. The count describes the export, not the live queue. Report-level qualifications are preserved in the signed KB review.

## Fix and acceptance

Interpret dates according to the documented tenant format, or require unambiguous input. Check affected routes with an ambiguous date and a day greater than twelve; the intended date, stored booking and generated invite must agree.

Sources: src/lib/kb/causes.ts, src/lib/kb/locales.ts, src/lib/data/reports-4471.json and tenant configuration files. Review: src/routes/kb/incidents/4471-review/+page.svx; rendered view: rendered/4471-review.html.
