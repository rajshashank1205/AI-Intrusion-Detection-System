class ThreatCorrelator:
    """
    Combines evidence from multiple detection engines.
    """

    def correlate(self, evidences):

        total_score = 0
        reasons = []
        attacks = []

        for evidence in evidences:

            total_score += evidence.score
            reasons.append(evidence.reason)

            if evidence.attack:
                attacks.append(evidence.attack)

        total_score = min(total_score, 100)

        if total_score >= 80:
            severity = "CRITICAL"

        elif total_score >= 60:
            severity = "HIGH"

        elif total_score >= 40:
            severity = "MEDIUM"

        else:
            severity = "LOW"

        attack = None

        if attacks:
            attack = max(set(attacks), key=attacks.count)

        return {
            "score": total_score,
            "severity": severity,
            "attack": attack,
            "reasons": reasons
        }