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

        syn_count = features.get(
            "syn_count",
            0
        )

        packets_per_second = features.get(
            "packets_per_second",
            0
        )

        recent_packet_count = features.get(
            "recent_packet_count",
            0
        )


        # -----------------------------------
        # Strong SYN Flood
        # -----------------------------------

        if (
            syn_count >= self.SYN_THRESHOLD
            and
            packets_per_second >=
            self.PACKET_RATE_THRESHOLD
            and
            recent_packet_count >=
            self.RECENT_PACKET_THRESHOLD
        ):

            return {
                "detected": True,
                "attack": "Possible SYN Flood",
                "severity": "CRITICAL",
                "score": 95,
                "reason": (
                    f"High SYN activity detected: "
                    f"{syn_count} SYN packets, "
                    f"{packets_per_second:.1f} packets/sec, "
                    f"{recent_packet_count} recent packets"
                )
            }


        # -----------------------------------
        # Suspicious SYN Activity
        # -----------------------------------

        if (
            syn_count >= self.SYN_THRESHOLD
            and
            (
                packets_per_second >=
                self.PACKET_RATE_THRESHOLD
                or
                recent_packet_count >=
                self.RECENT_PACKET_THRESHOLD
            )
        ):

            return {
                "detected": True,
                "attack": "Suspicious SYN Activity",
                "severity": "MEDIUM",
                "score": 55,
                "reason": (
                    f"Elevated SYN activity detected "
                    f"({syn_count} SYN packets)"
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