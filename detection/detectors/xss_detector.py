import re
from urllib.parse import unquote_plus


class XSSDetector:
    """
    Detects possible Cross-Site Scripting (XSS)
    attempts in likely HTTP traffic.
    """

    detector_type = "flow"
    input_type = "packet"


    def detect(self, packet_data):

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
        # Strong XSS Patterns
        # -----------------------------------

        patterns = [

            # Script tag

            (
                r"<\s*script\b[^>]*>",

                "Script tag injection"
            ),


            # JavaScript URI

            (
                r"javascript\s*:",

                "JavaScript URI injection"
            ),


            # Event handler with executable value

            (
                r"\bon(?:error|load|click|mouseover|focus)"
                r"\s*=\s*['\"]?[^>]+",

                "JavaScript event-handler injection"
            ),


            # Image tag combined with an event handler

            (
                r"<\s*img\b[^>]*\bonerror\s*=",

                "Image-based XSS injection"
            ),


            # SVG with an event handler

            (
                r"<\s*svg\b[^>]*\bonload\s*=",

                "SVG-based XSS injection"
            ),


            # Common JavaScript execution functions

            (
                r"\b(?:alert|prompt|confirm)\s*\(",

                "Suspicious JavaScript execution"
            ),


            # Cookie access

            (
                r"\bdocument\s*\.\s*cookie\b",

                "Browser cookie access"
            ),

        ]


        # -----------------------------------
        # Detect Patterns
        # -----------------------------------

        for pattern, description in patterns:

            if re.search(
                pattern,
                normalized_payload,
                re.IGNORECASE
            ):

                return {

                    "detected":
                        True,

                    "attack":
                        "Cross Site Scripting (XSS)",

                    "severity":
                        "HIGH",

                    "score":
                        85,

                    "reason":
                        description

                }


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
                "No XSS detected"

        }