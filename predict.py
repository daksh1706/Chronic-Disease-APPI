# src/predict.py

import joblib
import pandas as pd

def predict_disease(disease, user_input):
    """
    disease: diabetes / heart / asthma
    user_input: dict from question_engine
    returns: (risk_percent, accuracy_percent or None)
    """

    # -------------------------------
    # LOAD MODEL + PREPROCESSOR
    # -------------------------------
    model = joblib.load(f"models/{disease}_model.pkl")
    preprocessor = joblib.load(f"models/{disease}_preprocessor.pkl")

    # Load accuracy if available
    try:
        accuracy = joblib.load(f"models/{disease}_accuracy.pkl")
        accuracy_percent = round(accuracy * 100, 2)
    except FileNotFoundError:
        accuracy_percent = None

    imputer = preprocessor["imputer"]
    scaler = preprocessor["scaler"]
    features = preprocessor["features"]

    # -------------------------------
    # ALIGN INPUT FEATURES
    # -------------------------------
    X = pd.DataFrame([user_input])

    for f in features:
        if f not in X.columns:
            X[f] = 0

    X = X[features]

    X = imputer.transform(X)
    X = scaler.transform(X)

    # -------------------------------
    # PREDICTION
    # -------------------------------
    prob = model.predict_proba(X)[0][1]
    risk_percent = round(prob * 100, 2)

    return risk_percent, accuracy_percent
