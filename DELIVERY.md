# S01E03 · what it shows

Prepared from the support KB export dated 2026-10-04. This repository contains only course materials and the local implementation of this review.

## Review artifacts

- Signed review source: `src/routes/kb/incidents/4471-review/+page.svx`.
- Complete rendered DOM and styles from the actual browser view: `rendered/4471-review.html`.
- Browser screenshot of the reconciliation tables: `rendered/4471-review.jpg`.
- Saved KB index and linked pages: `rendered/index.html` and the other local HTML files.
- Captured control-state reference: `rendered/snapshot-state.json`.
- Proposed successor decision: `src/routes/kb/decisions/0002-dedupe-by-evidence/+page.svx`.
- Proposed active GitHub issue bodies: `tickets/01-parser.md` and `tickets/02-form-hint.md`.

The KB's original accepted decision, triage page, data, classification logic and components remain unchanged. The new review is found automatically by the KB index. Decision 0002 is a proposal pending desk-owner approval.

## Reproduce the view

Requires Node.js 24 and npm. Run `npm ci --ignore-scripts --no-audit --no-fund`, then `npm run dev`. Open `http://127.0.0.1:5173/kb/incidents/4471-review`. The included Vite shell compiles the original Svelte components and mdsvex pages; it does not replace them with a hand-written rendering.

`npm run build` checks the complete KB bundle. `node scripts/verify.mjs` checks snapshot reconciliation using the supplied classifier. The lockfile pins build dependencies.

The saved HTML pages retain the real rendered text, computed tables, SVG charts and desk ref. Their select and input values are serialized from properties read in the live browser. Controls are explicitly read-only in the saved view, and internal KB links point to the other saved HTML files in the same folder. Run the source app for the interactive explorer. The JPEG shows the live source page's reconciliation tables.

Export tooling: `scripts/export_snapshots.py` takes a JSON capture of the live pages' DOM, styles and control properties. `scripts/verify_snapshots.py` checks the resulting saved files against that capture: control values, read-only state, visible text, unchanged SVG and existence of every local link target. Checks of saved files use a local parser; a successful build alone is not evidence that export state is correct.

## Interpretation limits

The supplied KB specifies two mechanisms, producing 379 parser and 33 hint reports after deduplication. Its readAs convention says to count desk-noted observations in their assigned group with a footnote. The two scopes cover all 412 distinct IDs without overlap. Counts and observed symptoms do not certify every production root cause. All totals describe the export, not the changing live queue; no production fix is claimed.

The body-evidence view retains parser's 370 explicitly swapped date pairs, five desk-noted temporal observations and four general descriptions; hint has 33 explicitly swapped pairs. The five observations are preserved verbatim and counted once. They are not automatically promoted to a third cause. Ticket links search by title rather than assuming GitHub issue numbers.

## Course handoff

This is a local draft of a further correction after two rejected submissions. It proposes two narrow issue scopes and retaining the five observations in a KB footnote. The hypothesis that the first rejection concerned the breadth of an issue body is unconfirmed; the course did not identify the exact problem pair. No new submission or acceptance is implied. Future publication and a new course claim require the owner's separate decision.
