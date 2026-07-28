class PortScanDetector:
    """
    Detects port scans using host behaviour.
    """

    detector_type = "host"
    input_type = "host"

    def detect(self, host):

        unique_ports = len(host.get("destination_ports", set()))
        syn_count = host.get("syn_count", 0)
        packet_count = host.get("packet_count", 0)

        syn_ratio = syn_count / packet_count if packet_count else 0

        print("\n========== PORTSCAN DETECTOR ==========")
        print(f"Packet Count : {packet_count}")
        print(f"SYN Count    : {syn_count}")
        print(f"Unique Ports : {unique_ports}")
        print(f"SYN Ratio    : {syn_ratio:.2f}")
        print("=======================================\n")

        # Aggressive scan
        if unique_ports >= 20 and syn_ratio >= 0.70:

            return {
                "detected": True,
                "attack": "Port Scan",
                "severity": "HIGH",
                "score": 80,
                "reason": f"{unique_ports} destination ports with SYN ratio {syn_ratio:.2f}"
            }

        # Moderate scan
        elif unique_ports >= 10 and syn_ratio >= 0.50:

            return {
                "detected": True,
                "attack": "Possible Port Scan",
                "severity": "MEDIUM",
                "score": 60,
                "reason": f"{unique_ports} destination ports with SYN ratio {syn_ratio:.2f}"
            }

        return {
            "detected": False,
            "attack": None,
            "severity": "LOW",
            "score": 0,
            "reason": "No Port Scan Detected"
        }