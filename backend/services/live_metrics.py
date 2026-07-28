import threading


class LiveMetrics:

    def __init__(self):

        self._lock = threading.Lock()

        # Live network packet rate
        self._packets_per_second = 0

        # Latest AI anomaly score
        self._ai_score = 0


    # -----------------------------
    # Packet Rate
    # -----------------------------

    def set_packet_rate(self, value: int):

        with self._lock:
            self._packets_per_second = value


    def get_packet_rate(self) -> int:

        with self._lock:
            return self._packets_per_second


    # -----------------------------
    # AI Anomaly Score
    # -----------------------------

    def set_ai_score(self, value: float):

        with self._lock:
            self._ai_score = value


    def get_ai_score(self) -> float:

        with self._lock:
            return self._ai_score


# Single shared metrics instance
live_metrics = LiveMetrics()