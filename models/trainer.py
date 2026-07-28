import os

import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest


def train_model():

    # -----------------------------
    # File Paths
    # -----------------------------

    data_path = os.path.join(
        "data",
        "normal_traffic.csv"
    )

    model_path = os.path.join(
        os.path.dirname(__file__),
        "anomaly_detector.pkl"
    )

    # -----------------------------
    # Load Real Normal Traffic
    # -----------------------------

    print("\nLoading real normal traffic data...")

    if not os.path.exists(data_path):
        raise FileNotFoundError(
            "data/normal_traffic.csv was not found."
        )

    df = pd.read_csv(data_path)

    print(f"Training samples: {len(df)}")
    print(f"Features: {len(df.columns)}")

    # -----------------------------
    # Validate Dataset
    # -----------------------------

    expected_features = [
        "duration",
        "packet_count",
        "byte_count",
        "packets_per_second",
        "bytes_per_second",
        "syn_count",
        "ack_count",
        "unique_destination_ports",
        "recent_packet_count",
    ]

    missing_features = [
        feature
        for feature in expected_features
        if feature not in df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing features: {missing_features}"
        )

    # Keep features in exactly the same order
    # used by the live IDS.
    X = df[expected_features]

    # Remove invalid rows if any exist
    X = X.replace(
        [float("inf"), float("-inf")],
        pd.NA
    )

    X = X.dropna()

    print(
        f"Valid training samples: {len(X)}"
    )

    # -----------------------------
    # Train Isolation Forest
    # -----------------------------

    print("\nTraining Isolation Forest...")

    model = IsolationForest(
        n_estimators=200,

        # Expected percentage of unusual traffic
        contamination=0.03,

        random_state=42,
        n_jobs=-1
    )

    model.fit(X)

    # -----------------------------
    # Save Model
    # -----------------------------

    joblib.dump(
        model,
        model_path
    )

    print("\n✅ AI model trained successfully!")
    print(f"Model saved to: {model_path}")


if __name__ == "__main__":
    train_model()