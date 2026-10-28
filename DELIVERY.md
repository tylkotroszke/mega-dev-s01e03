# S01E03 · what it shows

Prepared from the support KB export dated 2026-10-04. This repository contains only course materials and the local implementation of this review.

## Review artifacts

- Signed review source: `src/routes/kb/incidents/4471-review/+page.svx`.
- Complete rendered DOM and styles from the actual browser view: `rendered/4471-review.html`.
- Browser screenshot of the top of that page: `rendered/4471-review.jpg`.
- Proposed successor decision: `src/routes/kb/decisions/0002-dedupe-by-evidence/+page.svx`.
- GitHub issue bodies: `tickets/01-parser.md` and `tickets/02-form-hint.md`.

The KB's original accepted decision, triage page, data, classification logic and components remain unchanged. The new review is found automatically by the KB index. Decision 0002 is a proposal pending desk-owner approval.

## Reproduce the view

Requires Node.js 24 and npm. Run `npm ci --ignore-scripts --no-audit --no-fund`, then `npm run dev`. Open `http://127.0.0.1:5173/kb/incidents/4471-review`. The included Vite shell compiles the original Svelte components and mdsvex pages; it does not replace them with a hand-written rendering.

`npm run build` checks the complete KB bundle. `node scripts/verify.mjs` checks snapshot reconciliation using the supplied classifier. The lockfile pins build dependencies.

The HTML capture is a static snapshot of the real rendered DOM, including computed tables, chart and desk ref. Its explorer controls are illustrative in the capture; run the app for the interactive explorer. The JPEG shows the top viewport. Neither file is a hand-written substitute for the compiled `.svx`.

## Interpretation limits

The supplied classifier produces 379 parser and 33 hint reports. Five anomalous temporal observations are retained within parser scope and explicitly require investigation. Neither the classifier nor a reporter's wording establishes a distinct timezone root cause. All counts describe the export, not the changing live queue. No production fix or live desk change is claimed.

The independent body-evidence view finds 370 explicitly swapped date pairs, five flagged temporal observations and four general descriptions in parser routing; hint routing has 33 explicitly swapped pairs. This distinguishes symptom evidence from routing and does not certify production root causes. Ticket links search by title rather than assuming GitHub issue numbers.

## Course handoff

Publishing the repository and creating its GitHub issues prepares the deliverable. The repository must then be submitted to the course in the documented challenge format and explicitly accepted. The course's solved reply governs the following debrief. Repository publication, local checks and this review do not establish acceptance. No final claim has been sent, and the exact claim answer schema still needs confirmation before submission.
