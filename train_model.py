import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier

# --------------------------------------------------
# CONFIG FOR EACH DISEASE
# --------------------------------------------------
CONFIG = {
    "diabetes": {
        "path": "data/diabetes.csv",
        "target": "Outcome"
    },
    "heart": {
        "path": "data/heart.csv",
        "target": "num"
    },
    "kidney": {
        "path": "data/kidney.csv",
        "target": "classification"
    },
    "liver": {
        "path": "data/liver.csv",
        "target": "Dataset"
    },
    "asthma": {
        "path": "data/asthma.csv",
        "target": "Diagnosis"
    }
}

# --------------------------------------------------
# CREATE MODELS FOLDER AUTOMATICALLY
# --------------------------------------------------
os.makedirs("models", exist_ok=True)

# --------------------------------------------------
# LOAD & PREPROCESS
# --------------------------------------------------
def load_and_preprocess(path, target):
    df = pd.read_csv(path)

    # normalize column names
    df.columns = df.columns.str.strip()

    y = df[target]
    X = df.drop(columns=[target])

    # convert categorical → numeric
    X = pd.get_dummies(X, drop_first=True)

    # handle labels if not numeric
    if y.dtype == "object":
        y = y.astype("category").cat.codes

    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()

    X = imputer.fit_transform(X)
    X = scaler.fit_transform(X)

    return X, y, imputer, scaler, X.shape[1], list(pd.get_dummies(df.drop(columns=[target]), drop_first=True).columns)

# --------------------------------------------------
# TRAIN MODEL
# --------------------------------------------------
def train_model(X_train, y_train):
    scale_pos_weight = (y_train == 0).sum() / max((y_train == 1).sum(), 1)

    model = XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=scale_pos_weight,
        eval_metric="logloss",
        random_state=42,
        use_label_encoder=False
    )

    model.fit(X_train, y_train)
    return model

# --------------------------------------------------
# MAIN TRAINING LOOP
# --------------------------------------------------
for disease, cfg in CONFIG.items():
    try:
        print(f"\n🚀 Training {disease.upper()} model")

        X, y, imputer, scaler, _, features = load_and_preprocess(
            cfg["path"], cfg["target"]
        )

        # Train / Val / Test split
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )

        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
        )

        model = train_model(X_train, y_train)

        print("\n📊 Validation Results:")
        print(classification_report(y_val, model.predict(X_val)))

        print("\n🧪 Test Results:")
        y_test_pred = model.predict(X_test)
        print(classification_report(y_test, y_test_pred))

        # --------------------------------------------------
        # SAVE ACCURACY (THIS FIXES YOUR APP)
        # --------------------------------------------------
        test_accuracy = accuracy_score(y_test, y_test_pred)
        joblib.dump(test_accuracy, f"models/{disease}_accuracy.pkl")

        # --------------------------------------------------
        # SAVE MODEL + PREPROCESSOR
        # --------------------------------------------------
        joblib.dump(model, f"models/{disease}_model.pkl")

        joblib.dump(
            {
                "imputer": imputer,
                "scaler": scaler,
                "features": features
            },
            f"models/{disease}_preprocessor.pkl"
        )

        print(f"✅ Saved {disease}_model.pkl")
        print(f"✅ Saved {disease}_preprocessor.pkl")
        print(f"✅ Saved {disease}_accuracy.pkl → {test_accuracy:.4f}")

    except Exception as e:
        print(f"❌ {disease.upper()} failed: {e}")
