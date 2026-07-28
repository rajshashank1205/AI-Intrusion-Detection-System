import re
from urllib.parse import unquote_plus


class SQLInjectionDetector:
    """
    Detects possible SQL Injection attempts
    in likely HTTP traffic using stronger
    SQL injection patterns.
    """

    detector_type = "flow"
    input_type = "packet"

    def detect(self, packet_data):

        # -----------------------------------
        # Basic Packet Information
        # -----------------------------------

        payload = packet_data.get(
            "payload",
            ""
        )

        src_port = packet_data.get(
            "src_port"
        )

        dst_port = packet_data.get(
            "dst_port"
        )

        # -----------------------------------
        # DEBUG OUTPUT
        # -----------------------------------

        print("\n========== SQL DETECTOR ==========")
        print(f"Source Port      : {src_port}")
        print(f"Destination Port : {dst_port}")
        print("Payload received:")
        print(repr(payload))
        print("=================================\n")

        # -----------------------------------
        # Ignore Empty Payloads
        # -----------------------------------

        if not payload:

            return self.normal_result()

        # -----------------------------------
        # Only Inspect Likely HTTP Traffic
        # -----------------------------------

        http_ports = {
            80,
            8080,
            8000,
            3000,
            5000
        }

        if (
            src_port not in http_ports
            and
            dst_port not in http_ports
        ):

            return self.normal_result()

        # -----------------------------------
        # Normalize Payload
        # -----------------------------------

        try:

            normalized_payload = (
                unquote_plus(
                    payload
                )
                .lower()
            )

        except Exception:

            normalized_payload = (
                payload.lower()
            )

        # -----------------------------------
        # DEBUG NORMALIZED PAYLOAD
        # -----------------------------------

        print("Normalized Payload:")
        print(repr(normalized_payload))
        print("=================================\n")

        # -----------------------------------
        # Strong SQL Injection Patterns
        # -----------------------------------

        patterns = [

            # Authentication bypass
            (
                r"['\"]\s*or\s*['\"]?\d+['\"]?"
                r"\s*=\s*['\"]?\d+",

                "SQL authentication bypass"
            ),

            # UNION based SQL injection
            (
                r"\bunion\s+(all\s+)?select\b",

                "UNION SELECT injection"
            ),

            # DROP TABLE
            (
                r"\bdrop\s+table\b",

                "DROP TABLE statement"
            ),

            # Database schema discovery
            (
                r"\binformation_schema\b",

                "Database schema enumeration"
            ),

            # Time-based SQL injection
            (
                r"\bsleep\s*\(",

                "Time-based SQL injection"
            ),

            # MySQL benchmark attack
            (
                r"\bbenchmark\s*\(",

                "SQL benchmark injection"
            ),

            # Boolean-based injection
            (
                r"\bor\s+\d+\s*=\s*\d+",

                "Boolean-based SQL injection"
            ),

            # SQL statement followed by comment
            (
                r"['\";]\s*--(?:\s|&|$)",

                "SQL comment injection"
            ),
            (
                r"['\"]\s*--",

                "SQL comment injection"
            ),

        ]

        # -----------------------------------
        # Detect Patterns
        # -----------------------------------

        for pattern, description in patterns:

            print(f"Checking Pattern: {pattern}")

            if re.search(
                pattern,
                normalized_payload,
                re.IGNORECASE
            ):

                print(f"✅ MATCH FOUND -> {description}")

                return {

                    "detected":
                        True,

                    "attack":
                        "SQL Injection",

                    "severity":
                        "HIGH",

                    "score":
                        85,

                    "reason":
                        description

                }

        print("❌ No SQL Injection Pattern Matched")

        return self.normal_result()

    # -----------------------------------
    # Normal Result
    # -----------------------------------

    def normal_result(self):

        return {

            "detected":
                False,

            "attack":
                None,

            "severity":
                "LOW",

            "score":
                0,

            "reason":
                "No SQL Injection detected"

        }