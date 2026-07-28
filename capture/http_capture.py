"""
HTTP Request Capture Module

This module captures HTTP requests from the vulnerable Flask application
and forwards them into the existing IDS detection pipeline.
"""

from detection.flow_builder import process_http_request


def inspect_http_request(request):
    """
    Convert a Flask request into the same packet format used by Scapy.
    """

    payload = request.get_data(as_text=True)

    packet_data = {
        "timestamp": None,
        "src_ip": request.remote_addr or "127.0.0.1",
        "dst_ip": "127.0.0.1",
        "src_port": 0,
        "dst_port": 5000,
        "protocol": "HTTP",
        "packet_size": len(payload.encode()),
        "ttl": 64,
        "flags": "",
        "payload": payload,
        "method": request.method,
        "path": request.path,
        "headers": dict(request.headers),
    }

    print("\n" + "=" * 60)
    print("🌐 HTTP REQUEST CAPTURED")
    print("=" * 60)
    print(f"Method : {request.method}")
    print(f"Path   : {request.path}")
    print(f"Payload: {payload}")
    print("=" * 60)

    # Send request directly into IDS pipeline
    process_http_request(packet_data)