from detection.detectors.base_detector import BaseDetector


class SYNDetector(BaseDetector):
    """
    Detects possible SYN Flood attacks using
    multiple traffic indicators.
    """

    detector_type = "flow"
    input_type = "features"

    # Minimum number of SYN packets observed
    SYN_THRESHOLD = 100

    # Minimum packet rate required before
    # considering the traffic flood-like
    PACKET_RATE_THRESHOLD = 50

    # Recent traffic burst threshold
    RECENT_PACKET_THRESHOLD = 40


    def detect(self, features):

        recent_syn_count = features.get(
            "recent_syn_count",
            0
        )

        # Sliding window = 2 seconds
        syn_per_second = (
            recent_syn_count / 2.0
        )

        print("\n========== SYN FLOOD DETECTOR ==========")
        print(
            f"Recent SYN Count : {recent_syn_count}"
        )
        print(
            f"Estimated SYN/sec: {syn_per_second:.1f}"
        )
        print("=========================================\n")


        # -----------------------------------
        # Strong SYN Flood
        # -----------------------------------

        if (
            recent_syn_count >= 100
            and
            syn_per_second >= 50
        ):

            return {
                "detected": True,
                "attack": "Possible SYN Flood",
                "severity": "CRITICAL",
                "score": 95,
                "reason": (
                    f"High SYN activity detected: "
                    f"{recent_syn_count} SYN packets "
                    f"in the last 2 seconds "
                    f"({syn_per_second:.1f} SYN/sec)"
                )
            }


        # -----------------------------------
        # Suspicious SYN Activity
        # -----------------------------------

        if recent_syn_count >= 50:

            return {
                "detected": True,
                "attack": "Suspicious SYN Activity",
                "severity": "MEDIUM",
                "score": 55,
                "reason": (
                    f"Elevated SYN activity detected: "
                    f"{recent_syn_count} SYN packets "
                    f"in the last 2 seconds"
                )
            }


        # -----------------------------------
        # Normal Traffic
        # -----------------------------------

        return {
            "detected": False,
            "attack": None,
            "severity": "LOW",
            "score": 0,
            "reason": "Normal SYN activity"
        }