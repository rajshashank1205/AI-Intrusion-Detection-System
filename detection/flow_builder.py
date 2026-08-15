from datetime import datetime

from detection.feature_extractor import extract_features
from detection.detection_manager import DetectionManager
from detection.host_tracker import update_host
from output.console_logger import print_flow_analysis

from database.alert_repository import save_alert


# -------------------------------------------------
# Flow Configuration
# -------------------------------------------------

FLOW_TIMEOUT_SECONDS = 60


# -------------------------------------------------
# Active Flows
# -------------------------------------------------

active_flows = {}


# -------------------------------------------------
# Single Detection Manager
# -------------------------------------------------

manager = DetectionManager()


# -------------------------------------------------
# Remove Expired Flows
# -------------------------------------------------

def cleanup_expired_flows():

    current_time = datetime.now()

    expired_flows = []

    for flow_key, flow in active_flows.items():

        idle_time = (
            current_time
            - flow["last_seen"]
        ).total_seconds()

        if idle_time > FLOW_TIMEOUT_SECONDS:

            expired_flows.append(
                flow_key
            )

    for flow_key in expired_flows:

        del active_flows[
            flow_key
        ]

    if expired_flows:

        print(
            f"🧹 Removed "
            f"{len(expired_flows)} "
            f"expired flow(s)"
        )


# -------------------------------------------------
# Create Flow
# -------------------------------------------------

def create_flow(packet_data):

    current_time = datetime.now()

    flow = {

        "start_time":
            current_time,

        "last_seen":
            current_time,

        "packet_count":
            1,

        "byte_count":
            packet_data["packet_size"],

        "syn_count":
            0,

        "ack_count":
            0,

        "destination_ports":
            set()

    }


    # Add destination port only if available

    if packet_data["dst_port"] is not None:

        flow[
            "destination_ports"
        ].add(
            packet_data["dst_port"]
        )


    # Count TCP flags

    if packet_data["protocol"] == "TCP":

        flags = packet_data.get(
            "flags",
            ""
        )


        # Count ONLY initial SYN packets.
        # SYN-ACK packets are ignored.

        if (
            "S" in flags
            and
            "A" not in flags
        ):

            flow["syn_count"] += 1


        # Count packets containing ACK

        if "A" in flags:

            flow["ack_count"] += 1


    return flow


# -------------------------------------------------
# Update Existing Flow
# -------------------------------------------------

def update_flow(
    flow,
    packet_data
):

    flow["last_seen"] = (
        datetime.now()
    )


    flow["packet_count"] += 1


    flow["byte_count"] += (
        packet_data[
            "packet_size"
        ]
    )


    # Add destination port only
    # when one exists.

    if packet_data["dst_port"] is not None:

        flow[
            "destination_ports"
        ].add(
            packet_data[
                "dst_port"
            ]
        )


    # Count TCP flags

    if packet_data["protocol"] == "TCP":

        flags = packet_data.get(
            "flags",
            ""
        )


        # Count ONLY initial SYN packets.
        # Do not count SYN-ACK packets.

        if (
            "S" in flags
            and
            "A" not in flags
        ):

            flow["syn_count"] += 1


        # Count packets containing ACK

        if "A" in flags:

            flow["ack_count"] += 1


# -------------------------------------------------
# Save Detected Threat
# -------------------------------------------------

def save_detected_threat(
    packet_data,
    analysis
):

    threat = analysis[
        "threat"
    ]


    if threat["score"] <= 0:

        return


    save_alert(

        timestamp=
            datetime.now(),

        source_ip=
            packet_data[
                "src_ip"
            ],

        alert_type=
            threat[
                "attack"
            ],

        severity=
            threat[
                "severity"
            ],

        description=
            ", ".join(
                threat[
                    "reasons"
                ]
            )

    )


# -------------------------------------------------
# Analyze Flow
# -------------------------------------------------

def analyze_flow(
    flow_key,
    packet_data,
    host
):

    flow = active_flows[
        flow_key
    ]


    features = extract_features(
        flow
    )


    analysis = manager.analyze(

        packet_data,

        features,

        host

    )


    print_flow_analysis(

        flow_key,

        features,

        analysis

    )


    save_detected_threat(

        packet_data,

        analysis

    )


# -------------------------------------------------
# Process Packet Flow
# -------------------------------------------------

def process_flow(packet_data):

    # ----------------------------------
    # Clean Up Old Flows
    # ----------------------------------

    cleanup_expired_flows()


    # ----------------------------------
    # Update Host Profile
    # ----------------------------------

    host = update_host(
        packet_data
    )


    # ----------------------------------
    # Flow Keys
    # ----------------------------------

    flow_key = (

        packet_data["src_ip"],

        packet_data["dst_ip"],

        packet_data["src_port"],

        packet_data["dst_port"],

        packet_data["protocol"]

    )


    reverse_flow_key = (

        packet_data["dst_ip"],

        packet_data["src_ip"],

        packet_data["dst_port"],

        packet_data["src_port"],

        packet_data["protocol"]

    )


    # ----------------------------------
    # Existing Forward Flow
    # ----------------------------------

    if flow_key in active_flows:

        update_flow(

            active_flows[
                flow_key
            ],

            packet_data

        )


        print(
            "\n🔵 Existing Flow Updated"
        )

        print(
            flow_key
        )


        analyze_flow(

            flow_key,

            packet_data,

            host

        )


    # ----------------------------------
    # Existing Reverse Flow
    # ----------------------------------

    elif reverse_flow_key in active_flows:

        update_flow(

            active_flows[
                reverse_flow_key
            ],

            packet_data

        )


        print(
            "\n🔵 Existing Flow Updated"
        )

        print(
            reverse_flow_key
        )


        analyze_flow(

            reverse_flow_key,

            packet_data,

            host

        )


    # ----------------------------------
    # New Flow
    # ----------------------------------

    else:

        active_flows[
            flow_key
        ] = create_flow(
            packet_data
        )


        print(
            "\n🟢 New Flow Created"
        )

        print(
            flow_key
        )


        # IMPORTANT:
        #
        # Analyze the first packet of a new flow
        # immediately.
        #
        # This allows host-level detectors such
        # as the PortScanDetector to analyze every
        # new connection attempt made by a host.

        analyze_flow(

            flow_key,

            packet_data,

            host

        )
# -------------------------------------------------
# Process HTTP Request
# -------------------------------------------------

def process_http_request(packet_data):
    """
    Process an HTTP request using the existing IDS flow pipeline.

    HTTP requests are grouped into the same flow so that
    repeated requests contribute to packet_count, byte_count,
    and recent traffic statistics.
    """

    cleanup_expired_flows()

    host = update_host(packet_data)

    flow_key = (
        packet_data["src_ip"],
        packet_data["dst_ip"],
        packet_data["src_port"],
        packet_data["dst_port"],
        packet_data["protocol"]
    )

    # ----------------------------------
    # Existing HTTP Flow
    # ----------------------------------

    if flow_key in active_flows:

        update_flow(
            active_flows[flow_key],
            packet_data
        )

        print("\n🔵 Existing HTTP Flow Updated")
        print(flow_key)

    # ----------------------------------
    # New HTTP Flow
    # ----------------------------------

    else:

        active_flows[flow_key] = create_flow(
            packet_data
        )

        print("\n🟢 New HTTP Flow Created")
        print(flow_key)

    # ----------------------------------
    # Extract Aggregated Features
    # ----------------------------------

    flow = active_flows[flow_key]

    features = extract_features(flow)

    # ----------------------------------
    # Recent HTTP Requests
    # ----------------------------------

    features["recent_packet_count"] = min(
        flow["packet_count"],
        10
    )

    # ----------------------------------
    # Run Detection Pipeline
    # ----------------------------------

    analysis = manager.analyze(
        packet_data,
        features,
        host
    )

    # ----------------------------------
    # Display Results
    # ----------------------------------

    print_flow_analysis(
        flow_key,
        features,
        analysis
    )

    # ----------------------------------
    # Save Threat
    # ----------------------------------

    save_detected_threat(
        packet_data,
        analysis
    )