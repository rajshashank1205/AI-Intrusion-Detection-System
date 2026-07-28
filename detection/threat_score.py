class ThreatScorer:
    """
    Calculates a threat score based on
    multiple flow indicators.
    """

    def calculate(self, features, detector_results):

        score = 0
        reasons = []

        # -----------------------------
        # SYN Count
        # -----------------------------
        syn_count = features["syn_count"]

        if syn_count >= 60:
            score += 30
            reasons.append("Very High SYN Count (+30)")

        elif syn_count >= 30:
            score += 20
            reasons.append("High SYN Count (+20)")

        elif syn_count >= 10:
            score += 10
            reasons.append("Moderate SYN Count (+10)")

        # -----------------------------
        # Packet Rate
        # -----------------------------
        pps = features["packets_per_second"]

        if pps >= 500:
            score += 30
            reasons.append("Extremely High Packet Rate (+30)")

        elif pps >= 200:
            score += 20
            reasons.append("High Packet Rate (+20)")

        elif pps >= 50:
            score += 10
            reasons.append("Moderate Packet Rate (+10)")

        # -----------------------------
        # ACK/SYN Ratio
        # -----------------------------
        syn = max(features["syn_count"], 1)
        ack = features["ack_count"]

        ratio = ack / syn

        if ratio < 1:
            score += 20
            reasons.append("Low ACK/SYN Ratio (+20)")

        elif ratio < 3:
            score += 10
            reasons.append("Moderate ACK/SYN Ratio (+10)")

        # -----------------------------
        # Detector Results
        # -----------------------------
        for detector in detector_results:

            if detector["detected"]:

                score += detector["score"]

                reasons.append(
                    f"{detector['attack']} (+{detector['score']})"
                )

        # Cap score at 100
        score = min(score, 100)

        # -----------------------------
        # Severity
        # -----------------------------
        if score <= 20:
            severity = "LOW"

        elif score <= 40:
            severity = "MODERATE"

        elif score <= 60:
            severity = "SUSPICIOUS"

        elif score <= 80:
            severity = "HIGH"

        else:
            severity = "CRITICAL"

        return {
            "score": score,
            "severity": severity,
            "reasons": reasons
        }