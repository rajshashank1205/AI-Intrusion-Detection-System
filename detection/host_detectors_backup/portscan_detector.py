class PortScanDetector:
    """
    Detects port scanning using host behaviour.
    """

    detector_type = "host"

    def detect(self, host):

        unique_ports = len(host["destination_ports"])
        syn_count = host["syn_count"]

        # -----------------------------
        # DEBUG OUTPUT
        # -----------------------------
        print("\n========== PORT SCAN DEBUG ==========")
        print("Host Data:")
        print(host)
        print("-------------------------------------")
        print(f"Unique Destination Ports : {unique_ports}")
        print(f"SYN Count                : {syn_count}")
        print("=====================================\n")

        # -----------------------------
        # Port Scan Detection
        # -----------------------------
        if unique_ports >= 10 and syn_count >= 10:

            return {
                "detected": True,
                "attack": "Port Scan",
                "severity": "HIGH",
                "score": 70,
                "reason": (
                    f"Contacted {unique_ports} destination ports "
                    f"with {syn_count} SYN packets."
                )
            }

        return {
            "detected": False,
            "attack": None,
            "severity": "LOW",
            "score": 0,
            "reason": "No Port Scan Detected"
        }