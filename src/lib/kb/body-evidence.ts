// Describes the reporter's words in this English-language export, not a proven root cause.
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

export type BodyEvidence = 'reported-swap' | 'flagged-time' | 'other-description';

export function bodyEvidence(report: { id: string; body: string }, flaggedIds: readonly string[]): BodyEvidence {
  if (flaggedIds.includes(report.id)) return 'flagged-time';
  const pattern = new RegExp(`(\\d{1,2}) (${MONTHS.join('|')})`, 'g');
  const dates = [...report.body.matchAll(pattern)].map((m) => ({ day: Number(m[1]), month: MONTHS.indexOf(m[2]) + 1 }));
  if (dates.length === 2 && dates[0].day !== dates[0].month && dates[0].day === dates[1].month && dates[0].month === dates[1].day) return 'reported-swap';
  return 'other-description';
}
