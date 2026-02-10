import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def load_and_preprocess(path, target, binarize_target=False):
    # -------------------------------
    # LOAD DATA
    # -------------------------------
    df = pd.read_csv(path)

    # Handle kidney dataset missing values
    df.replace("?", np.nan, inplace=True)

    # Separate target
    y = df[target]
    X = df.drop(columns=[target])

    # Optional: binarize target (heart disease)
    if binarize_target:
        y = y.apply(lambda x: 1 if int(x) > 0 else 0)

    # Encode target if categorical
    if y.dtype == "object":
        y = y.astype("category").cat.codes

    # -------------------------------
    # IDENTIFY COLUMN TYPES
    # -------------------------------
    num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()

    # -------------------------------
    # PIPELINES
    # -------------------------------
    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    # -------------------------------
    # COLUMN TRANSFORMER
    # -------------------------------
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, num_cols),
            ("cat", categorical_pipeline, cat_cols)
        ],
        remainder="drop"
    )

    # -------------------------------
    # FIT & TRANSFORM
    # -------------------------------
    X_processed = preprocessor.fit_transform(X)

    # -------------------------------
    # FEATURE NAMES (IMPORTANT)
    # -------------------------------
    feature_names = []

    if num_cols:
        feature_names.extend(num_cols)

    if cat_cols:
        encoded_features = (
            preprocessor.named_transformers_["cat"]
            .named_steps["encoder"]
            .get_feature_names_out(cat_cols)
        )
        feature_names.extend(encoded_features.tolist())

    return X_processed, y, preprocessor, feature_names
