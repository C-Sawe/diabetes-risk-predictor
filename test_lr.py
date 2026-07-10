import joblib
from ml import data
import pandas as pd
model = joblib.load(data.ARTIFACTS_DIR / "model.joblib")
prep = model.named_steps["prep"]
X = pd.DataFrame([data.load_raw().iloc[0]])
X = data.encode(X)[data.FEATURE_ORDER]
print("X columns:", X.columns.tolist())
X_transformed = prep.transform(X)
print("transformed shape:", X_transformed.shape)
lr = model.named_steps["clf"].named_estimators_["lr"]
print("LR coefs shape:", lr.coef_.shape)
