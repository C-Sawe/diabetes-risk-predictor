export const pct = (v: number, digits = 0): string => `${(v * 100).toFixed(digits)}%`;

export function shortLabel(label: string): string {
  return label.replace(/\s*\(.*\)/, "");
}

export interface ClinicalRates {
  sensitivity: number;
  specificity: number;
  tn: number;
  fp: number;
  fn: number;
  tp: number;
  correct: number;
}

export function clinicalRates(matrix: number[][]): ClinicalRates {
  const [[tn, fp], [fn, tp]] = matrix;
  const safe = (num: number, den: number) => (den === 0 ? 0 : num / den);
  return {
    tn,
    fp,
    fn,
    tp,
    correct: tn + tp,
    sensitivity: safe(tp, tp + fn),
    specificity: safe(tn, tn + fp),
  };
}
