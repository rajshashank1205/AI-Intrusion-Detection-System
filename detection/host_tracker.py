from datetime import datetime

hosts = {}


def update_host(packet_data):
    """
    Maintains behavioural statistics for each source host.

    Only outbound connection attempts (initial SYN packets)
    contribute towards Port Scan statistics.
    """

    src_ip = packet_data["src_ip"]

    if src_ip not in hosts:

        hosts[src_ip] = {
            "ip" : src_ip,
            "first_seen": datetime.now(),
            "last_seen": datetime.now(),
            "packet_count": 0,
            "byte_count": 0,
            "syn_count": 0,
            "destination_ips": set(),
            "destination_ports": set(),
            "login_attempts": 0
        }

    host = hosts[src_ip]

    host["last_seen"] = datetime.now()
    host["packet_count"] += 1
    host["byte_count"] += packet_data["packet_size"]

    # -------------------------------
    # Count ONLY initial TCP SYN packets
    # -------------------------------

    if packet_data["protocol"] == "TCP":

        flags = packet_data.get("flags", "")

        # Initial SYN only (ignore SYN-ACK)
        if "S" in flags and "A" not in flags:

            host["syn_count"] += 1

            host["destination_ips"].add(
                packet_data["dst_ip"]
            )

            host["destination_ports"].add(
                packet_data["dst_port"]
            )
    if(
        packet_data.get("protocol") == "HTTP"
        and packet_data.get("method") == "POST"
        and packet_data.get("path") == "/login"
    ):
        host["login_attempts"] += 1

    return host