# One-day shifts and temporal inconsistencies — 5 reports

## One reported problem and scope

Bookings or invites do not preserve the reported calendar day or event ordering. **Reports covered: 5 distinct reports**, received 2026-04-02 through 2026-10-04 across five tenants, from source ticket #4471. These reports need an independent temporal investigation rather than being closed with the shared month/day parser fix.

The exported tenant classifier puts them under parser without reading their bodies. The desk's oneDayMove list identifies exactly these five IDs. This work item removes them from the parser ticket's count; the scopes are now parser 374, form hint 33, temporal five, totaling 412 distinct reports without overlap.

## Evidence: preserve each observation

- R-41202, Kettle Books, email, 2026-04-02: "Invite says Tuesday 12 May. Calendar says Monday 11 May. My client turned up on the Monday. We had coffee."
- R-41209, Alder Physio, app, 2026-04-06: "Every booking in June is one day off. Only June. Why only June."
- R-41236, Nine Lanterns, app, 2026-04-20: "The invite arrived before I made the booking. I would like to know how."
- R-41344, Pale Harbour, email, 2026-06-12: "Client in Lisbon got Tuesday. Client in Toronto got Monday. Same meeting. We held it twice."
- R-41620, Lantern Row, email, 2026-10-04: "Tuesday 6 October showed as Monday. I moved it myself. I have stopped reporting these but my colleague says it helps you."

None of these bodies establishes a swapped month/day pair. A timezone conversion error, a date-boundary error or event-order handling may be involved; no production root cause has been demonstrated. Grouping these desk-flagged observations for investigation does not prove one implementation defect explains them all. Refine the scope if reproduction separates them further, retaining report IDs and counts.

## Investigation and acceptance checks

- Obtain intended date/time, stored timestamp, timezone, offset and calendar/invite payload for each case, including the tenant configuration at that time.
- Reproduce the same meeting in Lisbon and Toronto and determine whether different local days are expected or violate the intended calendar-day behavior. The reporter's location comparison alone is not proof of a timezone defect.
- Check the June-only claim and the invite-before-booking claim against actual event timestamps and ordering. Do not silently reinterpret them as month/day swaps.
- Verify intended calendar days and event ordering through storage and invite generation before closure. An unknown cause is a reason to investigate this separate work item, not to bury it in parser routing.
- Keep the five IDs excluded from the parser and hint tickets, and reconcile against a fresh export before acting on the live desk.

Sources: src/lib/data/desk-notes.json, src/lib/data/reports-4471.json, tenant JSON files and src/lib/kb/triage.ts. Counts cover the export ending 2026-10-04. The signed review is src/routes/kb/incidents/4471-review/+page.svx and its rendered capture is rendered/4471-review.html.
