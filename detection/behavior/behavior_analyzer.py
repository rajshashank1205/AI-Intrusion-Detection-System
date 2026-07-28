from detection.behavior.classifier import BehaviorClassifier


class BehaviorResult:

    def __init__(self):

        self.detected = False
        self.attack = None
        self.score = 0
        self.severity = "LOW"
        self.reasons = []
        self.activity = "Normal Traffic"
        self.confidence = "HIGH"


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
            result.score = 40
            result.severity = "MEDIUM"
            result.reasons.append(
                f"Contacted {len(host['destination_ports'])} unique destination ports."
            )

        # -------------------------
        # Host Sweep
        # -------------------------

        elif classification["activity"] == "Host Sweep":

            result.detected = True
            result.attack = "Host Sweep"
            result.score = 50
            result.severity = "MEDIUM"
            result.reasons.append(
                f"Contacted {len(host['destination_ips'])} unique destination IPs."
            )

        # -------------------------
        # Connection Burst
        # -------------------------

        elif classification["activity"] == "Connection Burst":

            result.detected = False
            result.attack = None
            result.score = 10
            result.severity = "LOW"
            result.reasons.append(
                "Large number of new outbound connections."
            )

        else:

            result.reasons.append(
                "No suspicious behaviour detected."
            )

        return result