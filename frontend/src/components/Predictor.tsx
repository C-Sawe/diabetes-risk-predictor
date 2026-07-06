import { useState } from "react";
import { predict, type FeatureSchema, type Prediction } from "../api";
import { RiskRing } from "./RiskRing";

interface Props {
  schema: FeatureSchema;
}

type FormState = {
  Age: number;
  Gender: "Male" | "Female";
  symptoms: Record<string, boolean>;
};

const HIGH_RISK = new Set([
  "HighBP", "HighChol", "Smoker", "HeartDiseaseorAttack", "DiffWalk"
]);

function initialSymptoms(schema: FeatureSchema, on?: Set<string>): Record<string, boolean> {
  return Object.fromEntries(schema.binary.map((f) => [f.key, on?.has(f.key) ?? false]));
}

export function Predictor({ schema }: Props) {
  const [form, setForm] = useState<FormState>({
    Age: 45,
    Gender: "Male",
    symptoms: initialSymptoms(schema),
  });
  const [result, setResult] = useState<Prediction | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const setSymptom = (key: string, val: boolean) =>
    setForm((f) => ({ ...f, symptoms: { ...f.symptoms, [key]: val } }));

  const loadPreset = (kind: "high" | "low") => {
    setForm({
      Age: kind === "high" ? 52 : 28,
      Gender: kind === "high" ? "Male" : "Female",
      symptoms: initialSymptoms(schema, kind === "high" ? HIGH_RISK : undefined),
    });
    setResult(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const payload = { Age: form.Age, Gender: form.Gender, ...form.symptoms };
      setResult(await predict(payload));
    } catch {
      setError("Could not reach the model. Is the API running on port 8000?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="section" id="check">
      <div className="shell">
        <div className="sec-intro">
          <span className="eyebrow">Try it yourself</span>
          <h2 className="sec-title">Check a risk estimate</h2>
          <p className="sec-lede">
            Fill in a few details and tap the symptoms that apply. You will get an instant,
            easy-to-read estimate.
          </p>
        </div>

        <div className="check">
          <form className="card check__form" onSubmit={handleSubmit}>
            <div className="check__presets">
              <span className="check__presets-label">Quick fill</span>
              <button type="button" className="soft-chip" onClick={() => loadPreset("high")}>
                higher risk
              </button>
              <button type="button" className="soft-chip" onClick={() => loadPreset("low")}>
                lower risk
              </button>
            </div>

            <div className="check__row">
              <label className="soft-field soft-field--age">
                <span className="soft-field__label">Age</span>
                <input type="number" min={1} max={120} value={form.Age}
                  onChange={(e) => setForm((f) => ({ ...f, Age: Number(e.target.value) }))} />
              </label>
              <div className="soft-field">
                <span className="soft-field__label">Gender</span>
                <div className="toggle-group" role="radiogroup" aria-label="Gender">
                  {(["Male", "Female"] as const).map((g) => (
                    <button key={g} type="button" role="radio" aria-checked={form.Gender === g}
                      className={`toggle-group__opt ${form.Gender === g ? "is-active" : ""}`}
                      onClick={() => setForm((f) => ({ ...f, Gender: g }))}>
                      {g}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <fieldset className="check__symptoms">
              <legend className="soft-field__label">Which symptoms do you have?</legend>
              <div className="chip-grid">
                {schema.binary.map((f) => (
                  <button key={f.key} type="button" aria-pressed={form.symptoms[f.key]}
                    className={`symptom-chip ${form.symptoms[f.key] ? "is-on" : ""}`}
                    onClick={() => setSymptom(f.key, !form.symptoms[f.key])}>
                    {f.label}
                  </button>
                ))}
              </div>
            </fieldset>

            <button type="submit" className="big-btn" disabled={loading}>
              {loading ? "Checking..." : "Check my risk"}
            </button>
          </form>

          <div className="card check__result">
            {error && <p className="check__error">{error}</p>}
            {!result && !error && (
              <div className="check__empty">
                <span className="check__empty-emoji" aria-hidden>🩺</span>
                <p>Your estimate will appear here once you check.</p>
              </div>
            )}
            {result && (
              <div className="check__body">
                <RiskRing value={result.probability} tone={result.risk.tone} />
                <span className={`risk-badge risk-badge--${result.risk.tone}`}>
                  {result.risk.band} risk
                </span>
                <p className="check__advice">{result.risk.action}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
