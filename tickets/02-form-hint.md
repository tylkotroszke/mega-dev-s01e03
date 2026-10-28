# Booking-v3 hint promises MM/DD but the form reads day-first — 33 reports

**Reports covered: 33 unique reports** in export ticket #4471, received 2026-04-17 through 2026-09-22.

## Problem

The supplied KB specifies that booking-v3 displays MM/DD/YYYY but reads submitted dates in the day-first tenant's order. Following the field's instruction can therefore produce the wrong date.

Example: R-41230, Copper Studio, form: a client arrived on 1 June instead of 6 January. Following MM/DD/YYYY, input 01/06/2026 means 6 January; day-first interpretation instead produces 1 June. This reproduction follows the exported specification; we have not executed the production form.

## Scope and count

Deduplicate reports by ID, filter mergedInto = 4471, and select the hint result from the supplied causeOf rule using tenant configuration and channel. All are form reports from booking-v3: Alder Physio (de-DE), 12; Copper Studio (es-ES), 11; Pale Harbour (pt-PT), 10. The count describes the export, not the live queue. Browser locale and intake tag do not establish the tenant's configuration.

## Fix and acceptance

Make the displayed hint, example and validation agree with the format the form actually accepts for the tenant. Check each affected tenant with an ambiguous date and a day greater than twelve; following the visible instruction must produce the intended stored and invited date.

Sources: src/lib/kb/causes.ts, src/lib/kb/locales.ts, src/lib/data/reports-4471.json and tenant configuration files. Review: src/routes/kb/incidents/4471-review/+page.svx; rendered view: rendered/4471-review.html.
