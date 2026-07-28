import threading
import time

from capture.capture import (
    start_packet_capture,
    stop_packet_capture
)


def start_threads():
    """
    Starts all background services.
    """

    capture_thread = threading.Thread(
        target=start_packet_capture
    )

    capture_thread.start()

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        print("\n\nShutting down IDS...")

        # Tell Scapy to stop sniffing
        stop_packet_capture()

        # Wait for capture thread to finish
        capture_thread.join()

        print("IDS stopped successfully.")