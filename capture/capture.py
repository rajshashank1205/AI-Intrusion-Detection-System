import threading
import time

import requests
from scapy.all import sniff

from capture.parser import parse_packet


# -------------------------------------------------
# Capture Configuration
# -------------------------------------------------

WIFI_INTERFACE = (
    r"\Device\NPF_{71C99036-6247-441A-9CC1-47C37DD5D0DA}"
)

LOOPBACK_INTERFACE = (
    r"\Device\NPF_Loopback"
)

CAPTURE_FILTER = "tcp"


# -------------------------------------------------
# Global Stop Event
# -------------------------------------------------

stop_event = threading.Event()


# -------------------------------------------------
# Packet Counter
# -------------------------------------------------

packet_count = 0

packet_count_lock = threading.Lock()


# -------------------------------------------------
# Packet Handler
# -------------------------------------------------

def packet_handler(packet):

    global packet_count

    # -------------------------------------------------
    # DEBUG: Detect Flask Traffic (Port 5000)
    # -------------------------------------------------

    if packet.haslayer("TCP"):

        tcp_layer = packet["TCP"]

        if (
            tcp_layer.sport == 5000
            or
            tcp_layer.dport == 5000
        ):

            print("\n🔥 FLASK PACKET DETECTED 🔥")
            print(packet.summary())

    # -------------------------------------------------
    # Count Captured Packet
    # -------------------------------------------------

    with packet_count_lock:

        packet_count += 1

    # -------------------------------------------------
    # Send Packet Through IDS Pipeline
    # -------------------------------------------------

    try:

        parse_packet(packet)

    except Exception as error:

        print(
            f"\n❌ Packet processing error: {error}"
        )


# -------------------------------------------------
# Capture Single Interface
# -------------------------------------------------

def capture_interface(
    interface,
    interface_name
):

    print(
        f"✅ Capture thread started: "
        f"{interface_name}"
    )

    try:

        sniff(

            iface=interface,

            filter=CAPTURE_FILTER,

            prn=packet_handler,

            store=False,

            stop_filter=lambda packet:
                stop_event.is_set()

        )

    except Exception as error:

        print(
            f"\n❌ Capture error on "
            f"{interface_name}:"
        )

        print(error)


# -------------------------------------------------
# Packet Rate Reporter
# -------------------------------------------------

def send_packet_rate():

    global packet_count

    while not stop_event.is_set():

        time.sleep(1)

        with packet_count_lock:

            packets_per_second = packet_count

            packet_count = 0

        try:

            requests.post(

                "http://127.0.0.1:8000/internal/packet-rate",

                json={
                    "packets_per_second":
                        packets_per_second
                },

                timeout=1

            )

        except requests.RequestException:

            pass


# -------------------------------------------------
# Start Packet Capture
# -------------------------------------------------

def start_packet_capture():

    stop_event.clear()

    print(
        "\nListening for network packets..."
    )

    print(
        "Monitoring interfaces:"
    )

    print(
        "  • Intel(R) Wi-Fi 6 AX101"
    )

    print(
        "  • Software Loopback Interface"
    )

    print(
        "Capture filter:"
    )

    print(
        "  • All IP traffic"
    )

    print()

    # -----------------------------------------
    # Wi-Fi Capture Thread
    # -----------------------------------------

    wifi_thread = threading.Thread(

        target=capture_interface,

        args=(

            WIFI_INTERFACE,

            "Wi-Fi"

        ),

        daemon=True

    )

    # -----------------------------------------
    # Loopback Capture Thread
    # -----------------------------------------

    loopback_thread = threading.Thread(

        target=capture_interface,

        args=(

            LOOPBACK_INTERFACE,

            "Loopback"

        ),

        daemon=True

    )

    # -----------------------------------------
    # Packet Rate Thread
    # -----------------------------------------

    rate_thread = threading.Thread(

        target=send_packet_rate,

        daemon=True

    )

    # Start all threads

    wifi_thread.start()
    loopback_thread.start()
    rate_thread.start()

    # -----------------------------------------
    # Keep Capture Function Alive
    # -----------------------------------------

    try:

        while not stop_event.is_set():

            time.sleep(0.5)

    except KeyboardInterrupt:

        stop_event.set()


# -------------------------------------------------
# Stop Packet Capture
# -------------------------------------------------

def stop_packet_capture():

    stop_event.set()

if __name__ == "__main__":
    start_packet_capture()