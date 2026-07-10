"""Train the model, evaluate it, and generate the charts."""
from __future__ import annotations

import json

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from ml import data

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier

MODEL_NAME = "Hybrid Ensemble (Voting)"

def make_model():
    lr = LogisticRegression(random_state=42, max_iter=1000)
    rf = RandomForestClassifier(random_state=42, n_estimators=100)
    gb = GradientBoostingClassifier(random_state=42, n_estimators=100)
    return VotingClassifier(
        estimators=[("lr", lr), ("rf", rf), ("gb", gb)],
        voting="soft"
    )


RANDOM_STATE = 42
TEST_SIZE = 0.20
CV_FOLDS = 5

PLOTS_DIR = data.BACKEND_DIR.parent / "frontend" / "public" / "analysis"

GREEN, CORAL, TEAL, INK = "#4aa87a", "#e8896a", "#7bb0c4", "#4a4038"


def build_pipeline() -> Pipeline:
    """Scale Age, pass the 0/1 symptom features through, then the model."""
    prep = ColumnTransformer(
        transformers=[("age", StandardScaler(), data.NUMERIC_FEATURES)],
        remainder="passthrough",
    )
    return Pipeline([("prep", prep), ("clf", make_model())])


def _style() -> None:
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "text.color": INK, "axes.labelcolor": INK,
        "axes.titlecolor": INK, "axes.titleweight": "bold", "xtick.color": INK,
        "ytick.color": INK, "axes.edgecolor": "#d9cfc4", "grid.color": "#ece4d9",
        "figure.dpi": 130,
    })


def _save(fig, name: str) -> None:
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / name, transparent=True, bbox_inches="tight")
    plt.close(fig)


def make_charts(raw, encoded, importance) -> None:
    y = encoded[data.TARGET_COL]
    base_rate = float(y.mean())

    # For each symptom, the share of people reporting it who were diagnosed.
    rates = []
    for feat in data.BINARY_FEATURES:
        have = encoded[encoded[feat] == 1]
        if len(have):
            rates.append((data.FEATURE_LABELS[feat], float(have[data.TARGET_COL].mean())))
    rates.sort(key=lambda t: t[1])
    labels, vals = [r[0] for r in rates], [r[1] for r in rates]
    fig, ax = plt.subplots(figsize=(9, 6.5))
    ax.barh(labels, vals, color=[CORAL if v >= base_rate else TEAL for v in vals])
    ax.axvline(base_rate, color=INK, ls="--", lw=1)
    ax.text(base_rate + 0.01, 0, f"overall {base_rate:.0%}", color=INK, fontsize=9)
    ax.set_xlim(0, 1)
    ax.set_title("Diabetes rate for each symptom")
    ax.set_xlabel("of people reporting the symptom, share who were diagnosed")
    _save(fig, "risk_by_symptom.png")

    # 2. Which symptoms the model leans on most.
    imp = pd.DataFrame(importance).sort_values("importance")
    fig, ax = plt.subplots(figsize=(8.5, 6))
    ax.barh(imp["label"], imp["importance"], color=GREEN)
    ax.set_title("Which symptoms the model weighs most")
    ax.set_xlabel("how much it moves the prediction")
    _save(fig, "feature_importance.png")

    # 3. Basic dataset context: how many were diagnosed, and by age.
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    counts = y.map({1: "Diagnosed", 0: "Not diagnosed"}).value_counts()
    axes[0].bar(counts.index, counts.values, color=[CORAL, TEAL], width=0.6)
    for i, v in enumerate(counts.values):
        axes[0].text(i, v + 4, str(v), ha="center", fontweight="bold")
    axes[0].set_title("How many were diagnosed"); axes[0].set_ylabel("patients")
    for label, code, color in (("Diagnosed", 1, CORAL), ("Not diagnosed", 0, TEAL)):
        sns.kdeplot(raw.loc[y == code, "Age"], ax=axes[1], fill=True, alpha=0.4,
                    color=color, label=label, linewidth=1.5)
    axes[1].set_title("Age by outcome"); axes[1].set_xlabel("age"); axes[1].legend()
    _save(fig, "eda_overview.png")


def dataset_stats(raw, encoded) -> dict:
    y = encoded[data.TARGET_COL]
    prevalence = []
    for feat in data.BINARY_FEATURES + [data.GENDER_FEATURE]:
        prevalence.append({
            "feature": feat, "label": data.FEATURE_LABELS[feat],
            "positive_rate": round(float(encoded.loc[y == 1, feat].mean()), 3),
            "negative_rate": round(float(encoded.loc[y == 0, feat].mean()), 3),
            "gap": round(float(encoded.loc[y == 1, feat].mean() - encoded.loc[y == 0, feat].mean()), 3),
        })
    prevalence.sort(key=lambda d: abs(d["gap"]), reverse=True)

    bins = list(range(10, 100, 10))
    labels = [f"{b}-{b + 9}" for b in bins[:-1]]
    age_binned = pd.cut(raw["Age"], bins=bins, labels=labels, right=False)
    age_dist = []
    for lbl in labels:
        mask = age_binned == lbl
        pos, neg = int(((y == 1) & mask).sum()), int(((y == 0) & mask).sum())
        total = pos + neg
        age_dist.append({"band": lbl, "positive": pos, "negative": neg,
                         "positivity_rate": round(pos / total, 3) if total else 0.0})

    return {
        "n_samples": int(len(raw)), "n_features": len(data.FEATURE_ORDER),
        "age_min": int(raw["Age"].min()), "age_max": int(raw["Age"].max()),
        "class_balance": {"positive": int((y == 1).sum()), "negative": int((y == 0).sum())},
        "symptom_prevalence": prevalence, "age_distribution": age_dist,
    }


def main() -> None:
    _style()
    data.ARTIFACTS_DIR.mkdir(exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    raw = data.load_raw()
    if len(raw) > 1000:
        raw = raw.sample(n=1000, random_state=RANDOM_STATE)
    encoded = data.encode(raw)
    X, y = encoded[data.FEATURE_ORDER], encoded[data.TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE
    )
    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)

    model = build_pipeline()
    
    print("Evaluating individual models for comparison...")
    for name, clf in model.named_steps["clf"].estimators:
        clf_pipe = Pipeline([("prep", model.named_steps["prep"]), ("clf", clf)])
        clf_cv = cross_val_score(clf_pipe, X_train, y_train, cv=cv, scoring="roc_auc")
        print(f"  {name.upper()}: CV AUC = {clf_cv.mean():.3f}±{clf_cv.std():.3f}")
        
    print("Evaluating hybrid ensemble...")
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="roc_auc")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

    X_test_samp = X_test.sample(n=min(5000, len(X_test)), random_state=RANDOM_STATE)
    y_test_samp = y_test.loc[X_test_samp.index]
    perm = permutation_importance(model, X_test_samp, y_test_samp, n_repeats=10,
                                  random_state=RANDOM_STATE, scoring="roc_auc")
    importance = sorted(
        ({"feature": f, "label": data.FEATURE_LABELS[f],
          "importance": round(float(m), 4), "std": round(float(s), 4)}
         for f, m, s in zip(data.FEATURE_ORDER, perm.importances_mean, perm.importances_std)),
        key=lambda d: d["importance"], reverse=True,
    )

    make_charts(raw, encoded, importance)

    # Deploy: retrain on ALL data and save.
    final = build_pipeline()
    final.fit(X, y)
    joblib.dump(final, data.ARTIFACTS_DIR / "model.joblib")

    metrics = {
        "model_name": MODEL_NAME,
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "specificity": round(tn / (tn + fp), 4) if (tn + fp) else 0.0,
        "f1": round(f1_score(y_test, y_pred), 4),
        "roc_auc": round(roc_auc_score(y_test, y_proba), 4),
        "confusion_matrix": [[int(tn), int(fp)], [int(fn), int(tp)]],
        "cv_scores": [round(float(s), 4) for s in cv_scores],
        "cv_mean": round(float(cv_scores.mean()), 4),
        "cv_std": round(float(cv_scores.std()), 4),
        "feature_importance": importance,
        "test_size": TEST_SIZE, "cv_folds": CV_FOLDS,
        "n_test": int(len(y_test)), "n_train": int(len(y_train)),
    }

    figures = {
        "model_name": MODEL_NAME,
        "figures": [
            {"file": "risk_by_symptom.png", "title": "Diabetes rate for each symptom",
             "caption": "Of the people who reported a symptom, the share who turned out diabetic. "
                        "Bars past the dashed line are red flags: that symptom means above-average risk."},
            {"file": "feature_importance.png", "title": "Which symptoms matter most",
             "caption": "How much each symptom moves the model's estimate. The bigger the bar, the "
                        "more that symptom pushes your risk up or down."},
            {"file": "eda_overview.png", "title": "Who is in the data",
             "caption": f"How many of the {len(raw)} people were diagnosed, and how age spreads across outcomes."},
        ],
    }

    (data.ARTIFACTS_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2))
    (data.ARTIFACTS_DIR / "dataset_stats.json").write_text(json.dumps(dataset_stats(raw, encoded), indent=2))
    (PLOTS_DIR / "figures.json").write_text(json.dumps(figures, indent=2))

    print(f"Model: {MODEL_NAME}")
    print(f"  accuracy={metrics['accuracy']:.3f}  f1={metrics['f1']:.3f}  "
          f"auc={metrics['roc_auc']:.3f}  cv={metrics['cv_mean']:.3f}±{metrics['cv_std']:.3f}")
    print(f"  saved model + metrics to {data.ARTIFACTS_DIR}")
    print(f"  saved 3 charts to {PLOTS_DIR}")


if __name__ == "__main__":
    main()
