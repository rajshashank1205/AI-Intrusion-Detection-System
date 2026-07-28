from detection.behavior.behavior_result import BehaviorResult


class PortScanBehavior:

    def analyze(self, host):

        result = BehaviorResult()

        unique_ports = len(host["destination_ports"])
        syn_count = host["syn_count"]

        # Rule 1
        if unique_ports >= 10:
            result.detected = True
            result.attack = "Port Scan"
            result.raise_score(40)
            result.add_reason(
                f"Contacted {unique_ports} unique destination ports."
            )

        # Rule 2
        if syn_count >= 15:
            result.detected = True
            result.attack = "Port Scan"
            result.raise_score(30)
            result.add_reason(
                f"High SYN count ({syn_count})."
            )

        result.finalize()

        return result