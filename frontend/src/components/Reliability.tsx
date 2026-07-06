import type { Metrics } from "../api";
import { clinicalRates, pct } from "../lib/viz";

interface Props {
  metrics: Metrics;
}

export function Reliability({ metrics }: Props) {
  const r = clinicalRates(metrics.confusion_matrix);

  const cards = [
    { emoji: "🎯", value: pct(metrics.accuracy, 0), label: "of predictions correct" },
    { emoji: "🔎", value: pct(metrics.recall, 0), label: "of real cases caught" },
    { emoji: "🛡️", value: pct(metrics.specificity, 0), label: "of healthy people cleared" },
    { emoji: "🔁", value: pct(metrics.cv_mean, 0), label: "average across 5 re-tests" },
  ];

  return (
    <section className="section" id="trust">
      <div className="shell">
        <div className="sec-intro">
          <span className="eyebrow">Can you trust it?</span>
          <h2 className="sec-title">How well it does</h2>
          <p className="sec-lede">
            The checker uses a {metrics.model_name} model, tested on {metrics.n_test} patients it
            never saw during training. Here is how it did, in plain terms.
          </p>
        </div>

        <div className="stat-cards">
          {cards.map((c) => (
            <div key={c.label} className="stat-card">
              <span className="stat-card__emoji" aria-hidden>{c.emoji}</span>
              <span className="stat-card__value">{c.value}</span>
              <span className="stat-card__label">{c.label}</span>
            </div>
          ))}
        </div>

        <div className="card block">
          <h3 className="block__title">On {metrics.n_test} test patients</h3>
          <div className="score-line">
            <span className="score-line__big">{r.correct}</span>
            <span className="score-line__small">got right</span>
            <span className="score-line__div">·</span>
            <span className="score-line__big score-line__miss">{r.fp + r.fn}</span>
            <span className="score-line__small">missed</span>
          </div>
          <div className="tally">
            <div className="tally__item tally__item--ok">
              <strong>{r.tp}</strong> correctly flagged at risk
            </div>
            <div className="tally__item tally__item--ok">
              <strong>{r.tn}</strong> correctly cleared
            </div>
            <div className="tally__item tally__item--warn">
              <strong>{r.fp}</strong> flagged but actually fine
            </div>
            <div className="tally__item tally__item--danger">
              <strong>{r.fn}</strong> missed a real case
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
