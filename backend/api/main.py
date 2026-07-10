from __future__ import annotations

import json

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from api.risk import classify_risk
from ml import data

ARTIFACTS = data.ARTIFACTS_DIR

app = FastAPI(title="Diabetes Risk API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Loaded once at startup.
_model = joblib.load(ARTIFACTS / "model.joblib")
_metrics = json.loads((ARTIFACTS / "metrics.json").read_text())
_dataset = json.loads((ARTIFACTS / "dataset_stats.json").read_text())


class PatientInput(BaseModel):
    Age: int = Field(..., ge=1, le=120)
    Gender: str = Field(..., pattern="^(Male|Female)$")
    HighBP: bool
    HighChol: bool
    Smoker: bool
    Stroke: bool
    HeartDiseaseorAttack: bool
    PhysActivity: bool
    HvyAlcoholConsump: bool
    DiffWalk: bool

    model_config = {"populate_by_name": True}


def _to_feature_row(p: PatientInput) -> pd.DataFrame:
    raw = p.model_dump(by_alias=True)
    row = {"Age": raw["Age"], "Sex": 1 if raw["Gender"] == "Male" else 0}
    for feat in data.BINARY_FEATURES:
        row[feat] = 1 if raw[feat] else 0
    return pd.DataFrame([row])[data.FEATURE_ORDER]


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> dict:
    return _metrics


@app.get("/dataset")
def dataset() -> dict:
    return _dataset


@app.get("/features")
def features() -> dict:
    return {
        "numeric": data.NUMERIC_FEATURES,
        "gender": data.GENDER_FEATURE,
        "binary": [{"key": f, "label": data.FEATURE_LABELS[f]} for f in data.BINARY_FEATURES],
        "labels": data.FEATURE_LABELS,
    }


@app.post("/predict")
def predict(patient: PatientInput) -> dict:
    try:
        X = _to_feature_row(patient)
        probability = float(_model.predict_proba(X)[0, 1])

        # Calculate interpretability drivers from Logistic Regression base model
        X_scaled = _model.named_steps["prep"].transform(X)
        lr_coefs = _model.named_steps["clf"].named_estimators_["lr"].coef_[0]
        contributions = X_scaled[0] * lr_coefs
        
        feature_contributions = [
            {"label": data.FEATURE_LABELS[f], "contribution": float(c)}
            for f, c in zip(data.FEATURE_ORDER, contributions)
        ]
        feature_contributions.sort(key=lambda x: x["contribution"], reverse=True)
        
        top_risk = feature_contributions[0]["label"] if feature_contributions[0]["contribution"] > 0 else None
        top_reducer = feature_contributions[-1]["label"] if feature_contributions[-1]["contribution"] < 0 else None

        drivers = {}
        if top_risk: drivers["top_risk"] = top_risk
        if top_reducer: drivers["top_reducer"] = top_reducer
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Inference failed: {exc}") from exc

    return {
        "probability": round(probability, 4),
        "prediction": "Positive" if probability >= 0.5 else "Negative",
        "risk": classify_risk(probability),
        "drivers": drivers,
    }
