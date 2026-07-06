import type { DatasetStats, Metrics } from "../api";
import { pct } from "../lib/viz";

interface Props {
  metrics: Metrics | null;
  dataset: DatasetStats | null;
}

export function Hero({ metrics, dataset }: Props) {
  const stats = [
    { icon: "✓", label: "accurate", value: metrics ? pct(metrics.accuracy, 0) : "--" },
    { icon: "❤", label: "catches cases", value: metrics ? pct(metrics.recall, 0) : "--" },
    { icon: "⚑", label: "people studied", value: dataset ? String(dataset.n_samples) : "--" },
  ];

  return (
    <header className="hero">
      <div className="shell hero__inner">
        <span className="pill">Early diabetes screening</span>
        <h1 className="hero__title">
          Know your diabetes risk in <span className="hero__hl">a few taps.</span>
        </h1>
        <p className="hero__sub">
          Answer a short symptom checklist and a machine-learning model trained on real
          patient data gives you a friendly risk estimate, plus what to do next. It is a
          gentle heads-up, not a diagnosis.
        </p>

        <div className="hero__stats">
          {stats.map((s) => (
            <div key={s.label} className="hero-stat">
              <span className="hero-stat__icon" aria-hidden>{s.icon}</span>
              <span className="hero-stat__value">{s.value}</span>
              <span className="hero-stat__label">{s.label}</span>
            </div>
          ))}
        </div>
      </div>
    </header>
  );
}
