import joblib
from ml import data
import pandas as pd

model = joblib.load(data.ARTIFACTS_DIR / "model.joblib")
prep = model.named_steps["prep"]
X = pd.DataFrame([data.load_raw().iloc[0]])
X = data.encode(X)[data.FEATURE_ORDER]

print("X columns:", X.columns.tolist())
X_transformed = prep.transform(X)

print("Feature order:", data.FEATURE_ORDER)
lr = model.named_steps["clf"].named_estimators_["lr"]
coefs = lr.coef_[0]

contributions = X_transformed[0] * coefs
for feat, cont in zip(data.FEATURE_ORDER, contributions):
    print(f"{feat}: {cont:.4f}")

