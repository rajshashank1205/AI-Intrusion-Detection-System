from typing import List


def create_feature_vector(features: dict) -> List[float]:
    """
    Converts extracted flow features into
    a numerical vector for AI models.
    """

    return [

        float(features.get("duration", 0)),
        float(features.get("packet_count", 0)),
        float(features.get("byte_count", 0)),
        float(features.get("packets_per_second", 0)),
        float(features.get("bytes_per_second", 0)),
        float(features.get("syn_count", 0)),
        float(features.get("ack_count", 0)),
        float(features.get("unique_destination_ports", 0)),
        float(features.get("recent_packet_count", 0))

    ]