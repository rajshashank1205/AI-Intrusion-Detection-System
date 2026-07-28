import time
import requests

from scapy.layers.inet import IP, TCP, UDP
from scapy.packet import Raw
from datetime import datetime

from database.packet_repository import save_packet
from detection.flow_builder import process_flow

from backend.packet_events import broadcast_packet


# -------------------------------------------------
# Backend Settings Configuration
# -------------------------------------------------

BACKEND_URL = "http://127.0.0.1:8000"

SETTINGS_REFRESH_INTERVAL = 5

# Default value used if backend is unavailable
live_packet_streaming_enabled = True

last_settings_fetch = 0


# -------------------------------------------------
# Check Live Packet Streaming Setting
# -------------------------------------------------

def is_live_streaming_enabled():

    global live_packet_streaming_enabled
    global last_settings_fetch

    current_time = time.monotonic()

    # Use cached setting for 5 seconds
    if (
        current_time
        - last_settings_fetch
        <
        SETTINGS_REFRESH_INTERVAL
    ):

        return live_packet_streaming_enabled

    # Record the settings check attempt
    last_settings_fetch = current_time

    try:

        response = requests.get(
            f"{BACKEND_URL}/settings",
            timeout=0.5
        )

        response.raise_for_status()

        settings = response.json()

        live_packet_streaming_enabled = (
            settings.get(
                "live_packet_streaming",
                True
            )
        )

    except requests.RequestException:

        # Continue using the last known value
        # if the backend is unavailable.
        pass

    return live_packet_streaming_enabled


# -------------------------------------------------
# Packet Parser
# -------------------------------------------------

def parse_packet(packet):
    """
    Extract important information from a network packet,
    display it, and forward it to the IDS pipeline.
    """

    # Ignore packets without an IP layer
    if not packet.haslayer(IP):
        return

    # -------------------------------
    # Basic Packet Information
    # -------------------------------

    timestamp = datetime.now()

    src_ip = packet[IP].src
    dst_ip = packet[IP].dst

    ttl = packet[IP].ttl
    packet_size = len(packet)

    protocol_name = "OTHER"

    src_port = None
    dst_port = None

    tcp_flags = ""

    # -------------------------------
    # TCP
    # -------------------------------

    if packet.haslayer(TCP):

        protocol_name = "TCP"

        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport

        tcp_flags = str(packet[TCP].flags)

    # -------------------------------
    # UDP
    # -------------------------------

    elif packet.haslayer(UDP):

        protocol_name = "UDP"

        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport

    # -------------------------------
    # Extract Payload
    # -------------------------------

    payload = ""
    print("Has Raw Layer:", packet.haslayer(Raw))

    if packet.haslayer(Raw):

        try:

            payload = bytes(
                packet[Raw].load
            ).decode(
                "utf-8",
                errors="ignore"
            )

            # =====================================================
            # DEBUG SECTION
            # =====================================================

            print("\n========== RAW PAYLOAD ==========")

            if payload.strip():
                print(payload)
            else:
                print("[Payload is empty]")

            print("=================================\n")

        except Exception as e:

            print("\n========== RAW PAYLOAD ==========")
            print(f"Payload Decode Error: {e}")
            print("=================================\n")

            payload = ""

    # -------------------------------
    # Packet Dictionary
    # -------------------------------

    packet_data = {

        "timestamp": timestamp,
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": src_port,
        "dst_port": dst_port,
        "protocol": protocol_name,
        "packet_size": packet_size,
        "ttl": ttl,
        "flags": tcp_flags,
        "payload": payload

    }

    # -----------------------------------------
    # Send Packet To Live Dashboard
    # -----------------------------------------

    if is_live_streaming_enabled():

        broadcast_packet(packet_data)

    # -------------------------------
    # IDS Pipeline
    # -------------------------------

    process_flow(packet_data)

    # -------------------------------
    # Console Output
    # -------------------------------

    print("=" * 60)

    print(
        f"Time        : "
        f"{timestamp.strftime('%H:%M:%S')}"
    )

    print(
        f"Protocol    : {protocol_name}"
    )

    print(
        f"Source IP   : {src_ip}"
    )

    print(
        f"Source Port : {src_port}"
    )

    print(
        f"Destination : {dst_ip}"
    )

    print(
        f"Dest Port   : {dst_port}"
    )

    print(
        f"Packet Size : "
        f"{packet_size} Bytes"
    )

    print(
        f"TTL         : {ttl}"
    )

    if protocol_name == "TCP":

        print(
            f"TCP Flags   : "
            f"{tcp_flags}"
        )

    # -----------------------------------------
    # Informational SYN Packet Logging
    # -----------------------------------------

    if (
        protocol_name == "TCP"
        and
        tcp_flags == "S"
    ):

        print(
            "🔵 TCP SYN Packet Observed"
        )

    print("=" * 60)

    # -------------------------------
    # Save Packet
    # -------------------------------

    save_packet(packet_data)