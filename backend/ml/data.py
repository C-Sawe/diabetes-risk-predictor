from __future__ import annotations

from pathlib import Path

import pandas as pd

BACKEND_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BACKEND_DIR / "data" / "brfss.csv"
ARTIFACTS_DIR = BACKEND_DIR / "artifacts"

TARGET_COL = "Diabetes_binary"

NUMERIC_FEATURES = ["Age"]

BINARY_FEATURES = [
    "HighBP",
    "HighChol",
    "Smoker",
    "Stroke",
    "HeartDiseaseorAttack",
    "PhysActivity",
    "HvyAlcoholConsump",
    "DiffWalk"
]

GENDER_FEATURE = "Sex"

# Column order the model expects.
FEATURE_ORDER = NUMERIC_FEATURES + [GENDER_FEATURE] + BINARY_FEATURES

FEATURE_LABELS: dict[str, str] = {
    "Age": "Age Category",
    "Sex": "Male",
    "HighBP": "High Blood Pressure",
    "HighChol": "High Cholesterol",
    "Smoker": "Smoker (100+ cigarettes in life)",
    "Stroke": "History of Stroke",
    "HeartDiseaseorAttack": "Heart Disease or Attack",
    "PhysActivity": "Physical Activity (past 30 days)",
    "HvyAlcoholConsump": "Heavy Alcohol Consumption",
    "DiffWalk": "Difficulty Walking or Climbing Stairs",
}


def encode(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in BINARY_FEATURES + [GENDER_FEATURE]:
        if col in out.columns:
            out[col] = out[col].astype(int)
    if TARGET_COL in out.columns:
        out[TARGET_COL] = out[TARGET_COL].astype(int)
    
    # Map real age to BRFSS 1-13 categories if the input looks like a real age (> 14)
    if "Age" in out.columns and out["Age"].max() > 14:
        out["Age"] = ((out["Age"] - 18) // 5) + 1
        out["Age"] = out["Age"].clip(lower=1, upper=13)
        
    return out


def load_raw() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def load_xy() -> tuple[pd.DataFrame, pd.Series]:
    encoded = encode(load_raw())
    return encoded[FEATURE_ORDER], encoded[TARGET_COL]
