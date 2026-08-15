from detection.behavior.classifier import BehaviorClassifier
from detection.behavior.behavior_result import BehaviorResult


class BehaviorAnalyzer:

    def __init__(self):
        self.classifier = BehaviorClassifier()

    def analyze(self, host):

        result = BehaviorResult()

        classification = self.classifier.classify(host)

        result.activity = classification["activity"]
        result.confidence = classification["confidence"]

        # -------------------------
        # Port Scan
        # -------------------------

        if classification["activity"] == "Port Scan":

            result.detected = True
            result.attack = "Port Scan"
            result.raise_score(40)

            result.add_reason(
                f"Contacted {len(host['destination_ports'])} "
                f"unique destination ports."
            )

        # -------------------------
        # Host Sweep
        # -------------------------

        elif classification["activity"] == "Host Sweep":

            result.detected = True
            result.attack = "Host Sweep"
            result.raise_score(50)

            result.add_reason(
                f"Contacted {len(host['destination_ips'])} "
                f"unique destination IPs."
            )

        # -------------------------
        # Connection Burst
        # -------------------------

        elif classification["activity"] == "Connection Burst":

            result.detected = True
            result.attack = "Connection Burst"
            result.raise_score(10)

            result.add_reason(
                "Large number of new outbound connections."
            )

        # -------------------------
        # Normal Traffic
        # -------------------------

        else:

            result.detected = False
            result.attack = None

            result.add_reason(
                "No suspicious behaviour detected."
            )

        # Calculate severity from score
        result.finalize()

        return result