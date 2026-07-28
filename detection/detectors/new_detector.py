class NewDetector:
    """
    Template for future detectors.
    """

    detector_type = "flow"
    input_type = "packet"

    def detect(self, packet_data):

        return {
            "detected": False,
            "attack": None,
            "severity": "LOW",
            "score": 0,
            "reason": "Template detector"
        }