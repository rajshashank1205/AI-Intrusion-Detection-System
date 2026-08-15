import time


class BruteForceDetector:
    """
    Detects repeated login attempts from the same source IP.

    Detection rule:
        5 or more POST requests to /login
        from the same IP within 60 seconds.
    """

    detector_type = "flow"
    input_type = "packet"

    MAX_ATTEMPTS = 5
    WINDOW_SECONDS = 60

    def __init__(self):

        # {
        #     "127.0.0.1": [timestamp1, timestamp2, ...]
        # }
        self.login_attempts = {}

    def detect(self, packet_data):

        src_ip = packet_data.get(
            "src_ip",
            "unknown"
        )

        method = packet_data.get(
            "method",
            ""
        )

        path = packet_data.get(
            "path",
            ""
        )

        # -----------------------------------
        # Only inspect POST /login
        # -----------------------------------

        if method.upper() != "POST":
            return self.normal_result()

        if path != "/login":
            return self.normal_result()

        # -----------------------------------
        # Record login attempt
        # -----------------------------------

        current_time = time.time()

        if src_ip not in self.login_attempts:
            self.login_attempts[src_ip] = []

        self.login_attempts[src_ip].append(
            current_time
        )

        # -----------------------------------
        # Remove attempts older than window
        # -----------------------------------

        cutoff = (
            current_time
            - self.WINDOW_SECONDS
        )

        self.login_attempts[src_ip] = [
            timestamp
            for timestamp in self.login_attempts[src_ip]
            if timestamp >= cutoff
        ]

        attempt_count = len(
            self.login_attempts[src_ip]
        )

        # -----------------------------------
        # Brute Force Detection
        # -----------------------------------

        if attempt_count >= self.MAX_ATTEMPTS:

            return {
                "detected": True,

                "attack":
                    "Brute Force Login Attack",

                "severity":
                    "HIGH",

                "score":
                    90,

                "reason":
                    (
                        f"Detected {attempt_count} "
                        f"login attempts from "
                        f"{src_ip} within "
                        f"{self.WINDOW_SECONDS} seconds"
                    )
            }

        return self.normal_result()

    # -----------------------------------
    # Normal Result
    # -----------------------------------

    def normal_result(self):

        return {
            "detected": False,

            "attack": None,

            "severity": "LOW",

            "score": 0,

            "reason":
                "No brute force activity detected"
        }