export type Problem = 'parser' | 'hint' | 'temporal' | 'unplaced';

// A routing label is not a diagnosis. Keep desk-flagged temporal symptoms out of the parser work item.
export function problemOf(report: { id: string }, legacyCause: 'parser' | 'hint' | null, temporalIds: readonly string[]): Problem {
  if (temporalIds.includes(report.id)) return 'temporal';
  return legacyCause ?? 'unplaced';
}
