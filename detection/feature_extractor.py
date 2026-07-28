def extract_features(flow):
    """
    Extract useful features from a network flow.

    Very new flows do not have enough timing information
    to calculate reliable packet/byte rates.
    """

    duration = (
        flow["last_seen"] - flow["start_time"]
    ).total_seconds()

    packet_count = flow["packet_count"]
    byte_count = flow["byte_count"]

    # -------------------------------------------------
    # Calculate Safe Traffic Rates
    # -------------------------------------------------
    #
    # A brand-new flow may have a duration extremely
    # close to zero. Dividing by values such as 0.001
    # creates unrealistic rates like 1000 packets/sec.
    #
    # Until enough time has passed, use zero for the
    # rate-based features.

    if duration < 1.0:

        packets_per_second = 0.0
        bytes_per_second = 0.0

    else:

        packets_per_second = (
            packet_count / duration
        )

        bytes_per_second = (
            byte_count / duration
        )

    # -------------------------------------------------
    # Build Feature Dictionary
    # -------------------------------------------------

    features = {

        "duration": duration,

        "packet_count": packet_count,

        "byte_count": byte_count,

        "packets_per_second":
            packets_per_second,

        "bytes_per_second":
            bytes_per_second,

        "syn_count":
            flow["syn_count"],

        "ack_count":
            flow["ack_count"],

        "unique_destination_ports":
            len(
                flow["destination_ports"]
            )

    }

    return features