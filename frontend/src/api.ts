const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export interface FeatureImportance {
  feature: string;
  label: string;
  importance: number;
  std: number;
}

export interface Metrics {
  model_name: string;
  accuracy: number;
  precision: number;
  recall: number;
  specificity: number;
  f1: number;
  roc_auc: number;
  confusion_matrix: number[][];
  roc_curve: { fpr: number; tpr: number }[];
  cv_scores: number[];
  cv_mean: number;
  cv_std: number;
  feature_importance: FeatureImportance[];
  test_size: number;
  cv_folds: number;
  n_test: number;
  n_train: number;
}

export interface Prevalence {
  feature: string;
  label: string;
  positive_rate: number;
  negative_rate: number;
  gap: number;
}

export interface AgeBand {
  band: string;
  positive: number;
  negative: number;
  positivity_rate: number;
}

export interface Correlation {
  feature: string;
  label: string;
  corr: number;
}

export interface DatasetStats {
  n_samples: number;
  n_features: number;
  age_min: number;
  age_max: number;
  class_balance: { positive: number; negative: number };
  symptom_prevalence: Prevalence[];
  age_distribution: AgeBand[];
  feature_correlation: Correlation[];
}

export interface BinaryFeature {
  key: string;
  label: string;
}

export interface FeatureSchema {
  numeric: string[];
  gender: string;
  binary: BinaryFeature[];
  labels: Record<string, string>;
}

export interface Prediction {
  probability: number;
  prediction: "Positive" | "Negative";
  risk: { band: string; action: string; tone: "ok" | "warn" | "danger" };
  drivers?: { top_risk?: string; top_reducer?: string };
}

export interface Figure {
  file: string;
  title: string;
  caption: string;
}

export interface FiguresDoc {
  model_name: string;
  figures: Figure[];
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`);
  return res.json() as Promise<T>;
}

export const fetchMetrics = () => get<Metrics>("/metrics");
export const fetchDataset = () => get<DatasetStats>("/dataset");
export const fetchFeatures = () => get<FeatureSchema>("/features");

export const ASSET_BASE = import.meta.env.BASE_URL;

export async function fetchFigures(): Promise<FiguresDoc> {
  const res = await fetch(`${ASSET_BASE}analysis/figures.json`);
  if (!res.ok) throw new Error(`Could not load figures.json: ${res.status}`);
  return res.json() as Promise<FiguresDoc>;
}

export async function predict(payload: Record<string, unknown>): Promise<Prediction> {
  const res = await fetch(`${BASE}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Prediction failed: ${res.status}`);
  return res.json() as Promise<Prediction>;
}
