from datetime import datetime

from database.alert_repository import save_alert

syn_counter = {}
last_severity = {}


def calculate_severity(syn_count):
    """
    Determine attack severity based on the number of SYN packets.
    """

    if syn_count >= 50:
        return "CRITICAL"

    elif syn_count >= 20:
        return "HIGH"

    elif syn_count >= 10:
        return "MEDIUM"

    else:
        return "LOW"


def process_syn_packet(source_ip):
    """
    Count SYN packets from each source IP and
    generate alerts whenever the severity increases.
    """

    syn_counter[source_ip] = syn_counter.get(source_ip, 0) + 1

    count = syn_counter[source_ip]

    severity = calculate_severity(count)

    print(f"🛡️ {source_ip} -> SYN Count: {count} | Severity: {severity}")

    previous = last_severity.get(source_ip)

    # Only save a new alert if the severity changes
    if severity != previous:

        save_alert(
            timestamp=datetime.now(),
            source_ip=source_ip,
            alert_type="Possible SYN Flood",
            severity=severity,
            description=f"{count} SYN packets detected from {source_ip}."
        )

        print(f"🚨 {severity} ALERT GENERATED")

        last_severity[source_ip] = severity