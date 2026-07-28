class BehaviorClassifier:
    """
    Converts host behaviour into a high-level activity.
    """

    def classify(self, host):

        syn = host["syn_count"]
        dst_ips = len(host["destination_ips"])
        dst_ports = len(host["destination_ports"])

        # ----------------------------
        # Port Scan
        # ----------------------------

        if dst_ports >= 15:
            return {
                "activity": "Port Scan",
                "confidence": "HIGH"
            }

        # ----------------------------
        # Host Sweep
        # ----------------------------

        if dst_ips >= 15:
            return {
                "activity": "Host Sweep",
                "confidence": "HIGH"
            }

        # ----------------------------
        # Connection Burst
        # ----------------------------

        if syn >= 15 and dst_ports <= 2:
            return {
                "activity": "Connection Burst",
                "confidence": "MEDIUM"
            }

        # ----------------------------
        # Normal Browsing
        # ----------------------------

        return {
            "activity": "Normal Traffic",
            "confidence": "HIGH"
        }