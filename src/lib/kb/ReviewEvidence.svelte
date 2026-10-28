<script lang="ts">
  import raw from '#lib/data/reports-4471.json';
  import notes from '#lib/data/desk-notes.json';
  import { uniqueById, groupByCause, causeOf, type Report } from '#lib/kb/causes';
  import { tenantOf } from '#lib/kb/locales';
  import { bodyEvidence } from '#lib/kb/body-evidence';

  const reports = uniqueById(raw as Report[]).filter((r) => r.mergedInto === 4471);
  const groups = groupByCause(reports, tenantOf);
  const misTagged = reports.filter((r) => r.meta.intakeTag !== causeOf(r, tenantOf(r)));
  const oneDay = reports.filter((r) => notes.oneDayMove.includes(r.id));
  const months = [...new Set(reports.map((r) => r.receivedAt.slice(0, 7)))].sort();
  const receivedDays = reports.map((r) => r.receivedAt.slice(0, 10)).sort();
  const mergedDays = reports.flatMap((r) => r.mergedAt ? [r.mergedAt.slice(0, 10)] : []).sort();
  const examples = ['R-41200', 'R-41230', ...notes.oneDayMove].map((id) => reports.find((r) => r.id === id)!);
  const evidenceCount = (rs: Report[], kind: string) => rs.filter((r) => bodyEvidence(r, notes.oneDayMove) === kind).length;
  const tickets: Record<string, { label: string; href: string }> = {
    parser: { label: 'Find parser ticket', href: 'https://github.com/tylkotroszke/mega-dev-s01e03/issues?q=is%3Aissue%20in%3Atitle%20%22Shared%20month-first%20parser%22' },
    hint: { label: 'Find form hint ticket', href: 'https://github.com/tylkotroszke/mega-dev-s01e03/issues?q=is%3Aissue%20in%3Atitle%20%22Booking-v3%20hint%20promises%22' },
  };
</script>

<h2>Reconciled report counts</h2>
<p>{raw.length} exported rows − {raw.length - reports.length} repeated rows = <strong>{reports.length} unique reports</strong> in #4471. Repeated IDs have identical payloads in this snapshot.</p>
<table>
  <thead><tr><th>Separate work item / ticket search</th><th>Distinct reports</th><th>Period received</th><th>Scope</th></tr></thead>
  <tbody>
    {#each groups as g (g.cause)}
      <tr>
        <td><a href={tickets[g.cause]?.href}>{tickets[g.cause]?.label ?? g.cause}</a></td>
        <td><strong>{g.reports.length}</strong></td>
        <td>{g.firstSeen} → {g.lastSeen}</td>
        <td>{g.tenants} tenants</td>
      </tr>
    {/each}
  </tbody>
</table>
<h2>What the report bodies support</h2>
<table>
  <thead><tr><th>Routing</th><th>Reported swapped date pair</th><th>Flagged temporal symptom</th><th>Other description</th></tr></thead>
  <tbody>
    {#each groups as g (g.cause)}
      <tr><td>{g.cause}</td><td>{evidenceCount(g.reports, 'reported-swap')}</td><td>{evidenceCount(g.reports, 'flagged-time')}</td><td>{evidenceCount(g.reports, 'other-description')}</td></tr>
    {/each}
  </tbody>
</table>
<p>This second table reads explicit English date pairs in the bodies and flags from desk notes. It describes reported symptoms independently of tenant-based routing; it neither reproduces the product nor confirms a root cause. A description without a swapped pair is not evidence that no formatting problem occurred.</p>
<p><strong>{oneDay.length}</strong> reports have desk-noted temporal observations and remain counted once in the <code>parser</code> scope, as the supplied <code>readAs</code> convention specifies. They are preserved below as qualified observations, not evidence of a proven additional mechanism. Intake labels disagree with the tenant classifier for <strong>{misTagged.length}</strong> reports; a label and an exact count do not certify every underlying cause.</p>

<h2>Received is different from merged</h2>
<p>Reports were received from <strong>{receivedDays[0]}</strong> through <strong>{receivedDays.at(-1)}</strong>. Merges run from <strong>{mergedDays[0] ?? 'none recorded'}</strong> through <strong>{mergedDays.at(-1) ?? 'none recorded'}</strong>. These are different events in the report history.</p>
<table>
  <thead><tr><th>Month</th><th>Reports received</th><th>Reports merged</th></tr></thead>
  <tbody>
    {#each months as month (month)}
      <tr><td>{month}</td><td>{reports.filter((r) => r.receivedAt.startsWith(month)).length}</td><td>{reports.filter((r) => r.mergedAt?.startsWith(month)).length}</td></tr>
    {/each}
  </tbody>
</table>

<h2>Traceable examples and unresolved symptoms</h2>
{#each examples as r (r.id)}
  <section class="report">
    <h3>{r.id} · {notes.oneDayMove.includes(r.id) ? 'unresolved temporal symptom' : causeOf(r, tenantOf(r))}</h3>
    <p><code>{r.tenant}</code> · {tenantOf(r)?.locale} · {tenantOf(r)?.form} · {r.channel} · received {r.receivedAt.slice(0, 10)}</p>
    <blockquote>{r.body}</blockquote>
  </section>
{/each}

<style>
  .report { margin: 1.25rem 0; padding: 0 0 0.5rem; border-bottom: 1px solid var(--line); }
  h3 { font-size: 1rem; margin-bottom: 0.25rem; }
  .report p { color: var(--muted); font-size: 0.85rem; margin-top: 0; }
  blockquote { margin: 0.5rem 0; border-left: 3px solid var(--line); padding-left: 1rem; }
</style>
