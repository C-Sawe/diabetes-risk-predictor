import { useEffect, useState } from "react";
import "./app.css";
import {
  fetchDataset, fetchFeatures, fetchFigures, fetchMetrics,
  type DatasetStats, type FeatureSchema, type FiguresDoc, type Metrics,
} from "./api";
import { Analysis } from "./components/Analysis";
import { Hero } from "./components/Hero";
import { Predictor } from "./components/Predictor";
import { Reliability } from "./components/Reliability";

export default function App() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [dataset, setDataset] = useState<DatasetStats | null>(null);
  const [schema, setSchema] = useState<FeatureSchema | null>(null);
  const [figures, setFigures] = useState<FiguresDoc | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    Promise.all([fetchMetrics(), fetchDataset(), fetchFeatures(), fetchFigures()])
      .then(([m, d, s, f]) => {
        if (controller.signal.aborted) return;
        setMetrics(m);
        setDataset(d);
        setSchema(s);
        setFigures(f);
      })
      .catch(() => {
        if (!controller.signal.aborted) {
          setError("Could not load the model. Start the API on port 8000 and run the analysis.");
        }
      });
    return () => controller.abort();
  }, []);

  return (
    <div className="app">
      <Hero metrics={metrics} dataset={dataset} />

      {error && (
        <div className="shell">
          <div className="banner">{error}</div>
        </div>
      )}

      {schema && <Predictor schema={schema} />}
      {metrics && <Reliability metrics={metrics} />}
      {figures && <Analysis figures={figures} />}

      <footer className="footer">
        <div className="shell">
          <p className="footer__note">
            A student project on early-stage diabetes screening.{" "}
            {metrics ? `${metrics.model_name} model` : "Machine-learning model"}, UCI Sylhet
            dataset. For learning, not medical advice.
          </p>
        </div>
      </footer>
    </div>
  );
}
