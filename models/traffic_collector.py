import csv
import os
import threading


class TrafficCollector:

    def __init__(
        self,
        file_path="data/normal_traffic.csv"
    ):

        self.file_path = file_path
        self.lock = threading.Lock()

        self.headers = [
            "duration",
            "packet_count",
            "byte_count",
            "packets_per_second",
            "bytes_per_second",
            "syn_count",
            "ack_count",
            "unique_destination_ports",
            "recent_packet_count",
        ]

        # Create directory if necessary
        os.makedirs(
            os.path.dirname(self.file_path),
            exist_ok=True
        )

        # Create CSV with headers if it doesn't exist
        if not os.path.exists(self.file_path):

            with open(
                self.file_path,
                "w",
                newline=""
            ) as file:

                writer = csv.writer(file)

                writer.writerow(
                    self.headers
                )


    def collect(self, features):

        row = [
            features.get("duration", 0),
            features.get("packet_count", 0),
            features.get("byte_count", 0),
            features.get("packets_per_second", 0),
            features.get("bytes_per_second", 0),
            features.get("syn_count", 0),
            features.get("ack_count", 0),
            features.get(
                "unique_destination_ports",
                0
            ),
            features.get(
                "recent_packet_count",
                0
            ),
        ]

        with self.lock:

            with open(
                self.file_path,
                "a",
                newline=""
            ) as file:

                writer = csv.writer(file)

                writer.writerow(row)


traffic_collector = TrafficCollector()