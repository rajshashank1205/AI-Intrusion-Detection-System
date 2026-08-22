import time

from detection.behavior.classifier import BehaviorClassifier
from detection.behavior.behavior_result import BehaviorResult


class BehaviorAnalyzer:

    def __init__(self):

        self.classifier = BehaviorClassifier()

        # Prevent the same host from generating
        # repeated Host Sweep alerts.
        self.host_sweep_alerts = {}

        # Minimum time between Host Sweep alerts
        # for the same host.
        self.host_sweep_cooldown = 30


    def analyze(self, host):

        result = BehaviorResult()

        # -----------------------------------------
        # Classify host behaviour
        # -----------------------------------------

        classification = self.classifier.classify(host)

        result.activity = classification["activity"]
        result.confidence = classification["confidence"]


        # -----------------------------------------
        # Brute Force Login
        # -----------------------------------------

        if classification["activity"] == "Brute Force Login":

            login_attempts = host.get("login_attempts", 0)

            result.detected = True
            result.attack = "Brute Force Login Behavior"

            result.raise_score(60)

            result.add_reason(
                f"Detected {login_attempts} login attempts "
                f"from {host['ip']}."
            )


        # -----------------------------------------
        # Suspicious Login Activity
        # -----------------------------------------

        elif classification["activity"] == "Suspicious Login Activity":

            login_attempts = host.get("login_attempts", 0)

            result.detected = True
            result.attack = "Suspicious Login Activity"

            result.raise_score(30)

            result.add_reason(
                f"Detected {login_attempts} login attempts "
                f"from {host['ip']}."
            )


        # -----------------------------------------
        # Port Scan
        # -----------------------------------------

        elif classification["activity"] == "Port Scan":

            result.detected = True
            result.attack = "Port Scan"

            result.raise_score(40)

            result.add_reason(
                f"Contacted {len(host['destination_ports'])} "
                f"unique destination ports."
            )


        # -----------------------------------------
        # Host Sweep
        # -----------------------------------------

        elif classification["activity"] == "Host Sweep":

            host_ip = host["ip"]
            current_time = time.monotonic()

            last_alert = self.host_sweep_alerts.get(host_ip)

            # Check whether this host already generated
            # a Host Sweep alert recently.
            if (
                last_alert is not None
                and current_time - last_alert < self.host_sweep_cooldown
            ):

                # Suppress duplicate alert.
                result.detected = False
                result.attack = None

                result.raise_score(10)

                result.add_reason(
                    f"Host Sweep already detected recently. "
                    f"Monitoring {len(host['destination_ips'])} "
                    f"unique destination IPs."
                )

            else:

                # Generate a new Host Sweep alert.
                self.host_sweep_alerts[host_ip] = current_time

                result.detected = True
                result.attack = "Host Sweep"

                result.raise_score(50)

                result.add_reason(
                    f"Contacted {len(host['destination_ips'])} "
                    f"unique destination IPs."
                )


        # -----------------------------------------
        # Connection Burst
        # -----------------------------------------

        elif classification["activity"] == "Connection Burst":

            # Connection bursts are suspicious behaviour,
            # but not considered a confirmed attack.

            result.detected = False
            result.attack = None

            result.raise_score(10)

            result.add_reason(
                "Large number of new outbound connections."
            )


        # -----------------------------------------
        # Normal Traffic
        # -----------------------------------------

        else:

            result.detected = False
            result.attack = None

            result.add_reason(
                "No suspicious behaviour detected."
            )


        # -----------------------------------------
        # Calculate severity
        # -----------------------------------------

        result.finalize()

        return result