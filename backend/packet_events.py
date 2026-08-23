import requests

from backend.config import BACKEND_URL


def broadcast_packet(packet_data: dict):
    """
    Send captured packet metadata from the IDS process
    to the FastAPI backend.
    """

    packet_event = {
        "type": "packet",
        "timestamp": str(packet_data["timestamp"]),
        "src_ip": packet_data["src_ip"],
        "dst_ip": packet_data["dst_ip"],
        "src_port": packet_data["src_port"],
        "dst_port": packet_data["dst_port"],
        "protocol": packet_data["protocol"],
        "packet_size": packet_data["packet_size"],
        "ttl": packet_data["ttl"],
        "flags": packet_data["flags"],
    }

    try:
        requests.post(
            f"{BACKEND_URL}/internal/broadcast-packet",
            json=packet_event,
            timeout=1,
        )

    except requests.RequestException:
        # Packet capture must continue even if
        # the dashboard backend is unavailable.
        pass