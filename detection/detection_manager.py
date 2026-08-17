import time
import requests

from detection.detector_loader import load_detectors

from detection.behavior.behavior_analyzer import BehaviorAnalyzer
from detection.threat_correlator import ThreatCorrelator
from detection.evidence import Evidence
from detection.sliding_window import SlidingWindow
from detection.timeline import timeline

from models.anomaly_model import AnomalyModel
from models.feature_vector import create_feature_vector
from models.traffic_collector import traffic_collector


# -------------------------------------------------
# Training Data Collection Mode
# -------------------------------------------------

COLLECT_TRAINING_DATA = False


# -------------------------------------------------
# Backend Configuration
# -------------------------------------------------

BACKEND_URL = "http://127.0.0.1:8000"


# -------------------------------------------------
# Settings Cache
# -------------------------------------------------

# The IDS checks the backend for new settings
# at most once every 5 seconds.

SETTINGS_REFRESH_INTERVAL = 5


# -------------------------------------------------
# Default IDS Settings
# -------------------------------------------------

DEFAULT_SETTINGS = {
    "ai_detection": True,
    "live_packet_streaming": True,
    "detection_sensitivity": "medium",
}


# -------------------------------------------------
# AI Sensitivity Thresholds
# -------------------------------------------------

# Higher sensitivity means a lower threshold,
# allowing weaker anomalies to become evidence.

AI_THRESHOLDS = {
    "low": 50,
    "medium": 30,
    "high": 15,
}


class DetectionManager:

    def __init__(self):

        self.window = SlidingWindow(
            window_seconds=2

        )
        self.syn_window = SlidingWindow(
            window_seconds = 2
        )

        # Automatically load every detector

        all_detectors = load_detectors(
            "detection/detectors"
        )

        print("\n" + "=" * 60)
        print("LOADED DETECTORS")
        print("=" * 60)

        for detector in all_detectors:
            print(f"✅ {detector.__class__.__name__}")

        print("=" * 60 + "\n")
        self.flow_detectors = [
            detector
            for detector in all_detectors
            if getattr(
                detector,
                "detector_type",
                "flow"
            ) == "flow"
        ]

        self.host_detectors = [
            detector
            for detector in all_detectors
            if getattr(
                detector,
                "detector_type",
                "host"
            ) == "host"
        ]

        self.behavior = BehaviorAnalyzer()

        self.correlator = ThreatCorrelator()

        # AI Model

        self.ai_model = AnomalyModel()

        # Last successfully loaded settings

        self.settings = (
            DEFAULT_SETTINGS.copy()
        )

        # Time when settings were last checked

        self.last_settings_fetch = 0


    # -------------------------------------------------
    # Fetch Current Settings
    # -------------------------------------------------

    def get_settings(self):

        current_time = time.monotonic()


        # -----------------------------------------
        # Return Cached Settings
        # -----------------------------------------

        if (
            current_time
            - self.last_settings_fetch
            <
            SETTINGS_REFRESH_INTERVAL
        ):

            return self.settings


        # Record the attempt time so an unavailable
        # backend is not hammered on every packet.

        self.last_settings_fetch = (
            current_time
        )


        # -----------------------------------------
        # Fetch Fresh Settings
        # -----------------------------------------

        try:

            response = requests.get(
                f"{BACKEND_URL}/settings",
                timeout=0.5
            )

            response.raise_for_status()

            backend_settings = (
                response.json()
            )

            self.settings.update(
                backend_settings
            )

        except requests.RequestException:

            # Continue using the last known
            # settings if the backend is offline.

            pass


        return self.settings


    # -------------------------------------------------
    # Analyze Traffic
    # -------------------------------------------------

    def analyze(
        self,
        packet_data,
        features,
        host
    ):

        # -----------------------------------------
        # Get Cached IDS Settings
        # -----------------------------------------

        settings = self.get_settings()


        ai_enabled = settings.get(
            "ai_detection",
            True
        )


        sensitivity = settings.get(
            "detection_sensitivity",
            "medium"
        )


        ai_threshold = AI_THRESHOLDS.get(
            sensitivity,
            30
        )


        # ---------------- Sliding Window ----------------

        self.window.add_event(
            packet_data["src_ip"]
        )
        if (
            packet_data.get("protocol") == "TCP"
        and "S" in packet_data.get("flags","")
        and "A" not in packet_data.get("flags","")
        ):
            self.syn_window.add_event(
                packet_data["src_ip"]
            )


        features["recent_packet_count"] = (
            self.window.count(
                packet_data["src_ip"]
            )
        )
        features["recent_syn_count"] = (
            self.syn_window.count(
                packet_data["src_ip"]
            )
        )


        # -----------------------------------------
        # Collect Normal Traffic Training Data
        # -----------------------------------------

        if COLLECT_TRAINING_DATA:

            traffic_collector.collect(
                features
            )


        evidences = []

        flow_results = []

        host_results = []


        # ---------------- Flow Detectors ----------------

        for detector in self.flow_detectors:

            detector_name = (
                detector.__class__.__name__
            )


            if detector_name in [
                "SQLInjectionDetector",
                "XSSDetector",
                "BruteForceDetector",
                "NewDetector"
            ]:

                result = detector.detect(
                    packet_data
                )

            else:

                result = detector.detect(
                    features
                )


            flow_results.append(
                result
            )


            if result["detected"]:

                evidences.append(
                    Evidence(
                        source="Flow Detector",
                        score=result["score"],
                        reason=result["reason"],
                        attack=result["attack"]
                    )
                )


                timeline.add_event(
                    source="Flow Detector",
                    event=result["reason"],
                    severity=result["severity"]
                )


        # ---------------- Host Detectors ----------------

        for detector in self.host_detectors:

            result = detector.detect(
                host
            )


            host_results.append(
                result
            )


            if result["detected"]:

                evidences.append(
                    Evidence(
                        source="Host Detector",
                        score=result["score"],
                        reason=result["reason"],
                        attack=result["attack"]
                    )
                )


                timeline.add_event(
                    source="Host Detector",
                    event=result["reason"],
                    severity=result["severity"]
                )


        # ---------------- Behavior ----------------

        behavior = self.behavior.analyze(
            host
        )


        if behavior.detected:

            evidences.append(
                Evidence(
                    source="Behavior Analyzer",
                    score=behavior.score,
                    reason=", ".join(
                        behavior.reasons
                    ),
                    attack=behavior.attack
                )
            )


            timeline.add_event(
                source="Behavior Analyzer",
                event=", ".join(
                    behavior.reasons
                ),
                severity=behavior.severity
            )


        # ---------------- AI Detection ----------------

        if ai_enabled:

            feature_vector = (
                create_feature_vector(
                    features
                )
            )


            ai_result = (
                self.ai_model.predict(
                    feature_vector
                )
            )


            # -----------------------------------------
            # Send AI Score To Dashboard
            # -----------------------------------------

            try:

                requests.post(
                    f"{BACKEND_URL}/internal/ai-score",
                    json={
                        "ai_score":
                            ai_result["score"]
                    },
                    timeout=0.5
                )

            except requests.RequestException:

                pass


            # -----------------------------------------
            # Add Strong AI Anomalies As Evidence
            # -----------------------------------------

            if (
                ai_result["detected"]
                and
                ai_result["score"]
                >= ai_threshold
            ):

                evidences.append(
                    Evidence(
                        source="AI Engine",
                        score=ai_result["score"],
                        reason=ai_result["reason"],
                        attack="AI Anomaly"
                    )
                )


                timeline.add_event(
                    source="AI Engine",
                    event=ai_result["reason"],
                    severity="HIGH"
                )


        else:

            # AI engine disabled from dashboard

            ai_result = {
                "detected": False,
                "score": 0,
                "reason":
                    "AI anomaly detection disabled"
            }


        # ---------------- Final Threat ----------------

        final_result = (
            self.correlator.correlate(
                evidences
            )
        )


        if final_result["score"] > 0:

            timeline.add_event(
                source="Threat Correlator",
                event=(
                    f"{final_result['attack']} "
                    f"({final_result['score']})"
                ),
                severity=(
                    final_result["severity"]
                )
            )


        # ---------------- Return Analysis ----------------

        return {

            "flow_detectors":
                flow_results,

            "host_detectors":
                host_results,

            "behavior":
                behavior,

            "ai":
                ai_result,

            "threat":
                final_result,

        }