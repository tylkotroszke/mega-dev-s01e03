# S01E03 · what it shows

Prepared from the support KB export dated 2026-10-04. This repository contains only course materials and the local implementation of this review.

## Review artifacts

- Signed review source: `src/routes/kb/incidents/4471-review/+page.svx`.
- Complete rendered DOM and styles from the actual browser view: `rendered/4471-review.html`.
- Browser screenshot of the reconciliation tables: `rendered/4471-review.jpg`.
- Proposed successor decision: `src/routes/kb/decisions/0002-dedupe-by-evidence/+page.svx`.
- GitHub issue bodies: `tickets/01-parser.md`, `tickets/02-form-hint.md` and `tickets/03-temporal.md`.

The KB's original accepted decision, triage page, data, classification logic and components remain unchanged. The new review is found automatically by the KB index. Decision 0002 is a proposal pending desk-owner approval.

## Reproduce the view

Requires Node.js 24 and npm. Run `npm ci --ignore-scripts --no-audit --no-fund`, then `npm run dev`. Open `http://127.0.0.1:5173/kb/incidents/4471-review`. The included Vite shell compiles the original Svelte components and mdsvex pages; it does not replace them with a hand-written rendering.

`npm run build` checks the complete KB bundle. `node scripts/verify.mjs` checks snapshot reconciliation using the supplied classifier. The lockfile pins build dependencies.

The HTML capture is a static snapshot of the real rendered DOM, including computed tables, chart and desk ref. Its explorer controls are illustrative in the capture; run the app for the interactive explorer. The JPEG shows the reconciliation tables. Neither file is a hand-written substitute for the compiled `.svx`.

## Interpretation limits

The supplied classifier produces 379 parser and 33 hint reports, but it ignores report bodies and hides five desk-flagged temporal observations within parser scope. Corrected work items separate parser 374, form hint 33 and temporal five. The scopes cover all 412 distinct reports without overlap. Separating the reported temporal problem does not establish a timezone root cause. All counts describe the export, not the changing live queue. No production fix or live desk change is claimed.

The independent body-evidence view shows parser 370 explicitly swapped date pairs plus four general descriptions, hint 33 explicitly swapped pairs, and five flagged temporal observations exclusively in their own work item. This distinguishes symptom evidence from classifier routing and does not certify production root causes. Ticket links search by title rather than assuming GitHub issue numbers.

## Course handoff

Publishing the repository and creating its GitHub issues prepares the deliverable. The repository must then be submitted to the course and explicitly accepted. The initial two-ticket submission was rejected; the course said one ticket covered two problems. This revision separates the desk-flagged temporal reports into their own investigation. Neither publication nor local checks establish acceptance. The course's solved reply governs the following debrief.
