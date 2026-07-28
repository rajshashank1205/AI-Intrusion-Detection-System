import os

import joblib
import pandas as pd


class AnomalyModel:
    """
    Loads the trained Isolation Forest model
    and analyzes live network traffic.
    """

    def __init__(self):

        self.model = None

        model_path = os.path.join(
            os.path.dirname(__file__),
            "anomaly_detector.pkl"
        )

        if os.path.exists(model_path):

            self.model = joblib.load(
                model_path
            )

            print(
                "✅ AI anomaly model loaded."
            )

        else:

            print(
                "⚠️ AI anomaly model not found."
            )


    def predict(
        self,
        feature_vector
    ):

        if self.model is None:

            return {
                "detected": False,
                "score": 0,
                "reason":
                    "AI model not trained yet."
            }


        # -----------------------------------------
        # Prepare Model Input
        # -----------------------------------------

        # Use the exact feature names that were
        # used when the Isolation Forest was trained.

        feature_names = [

            "duration",

            "packet_count",

            "byte_count",

            "packets_per_second",

            "bytes_per_second",

            "syn_count",

            "ack_count",

            "unique_destination_ports",

            "recent_packet_count"

        ]


        # Create a DataFrame instead of a NumPy
        # array so sklearn receives feature names.

        X = pd.DataFrame(
            [
                feature_vector
            ],
            columns=feature_names,
            dtype=float
        )


        # -----------------------------------------
        # Isolation Forest Prediction
        # -----------------------------------------

        #  1 = normal
        # -1 = anomaly

        prediction = (
            self.model.predict(X)[0]
        )


        # -----------------------------------------
        # Raw Decision Score
        # -----------------------------------------

        decision_score = (
            self.model.decision_function(
                X
            )[0]
        )


        # -----------------------------------------
        # Convert To 0-100 Anomaly Score
        # -----------------------------------------

        if decision_score < 0:

            anomaly_score = min(
                100,
                max(
                    1,
                    int(
                        abs(
                            decision_score
                        ) * 500
                    )
                )
            )

        else:

            # Normal traffic receives a small
            # anomaly-confidence value.

            anomaly_score = max(
                0,
                min(
                    29,
                    int(
                        (
                            0.1
                            - decision_score
                        )
                        * 290
                    )
                )
            )


        # -----------------------------------------
        # Anomaly Result
        # -----------------------------------------

        if prediction == -1:

            return {

                "detected":
                    True,

                "score":
                    anomaly_score,

                "reason": (
                    "AI detected anomalous traffic "
                    f"(model score: "
                    f"{decision_score:.4f})."
                )

            }


        # -----------------------------------------
        # Normal Result
        # -----------------------------------------

        return {

            "detected":
                False,

            "score":
                anomaly_score,

            "reason": (
                "Traffic appears normal "
                f"(model score: "
                f"{decision_score:.4f})."
            )

        }