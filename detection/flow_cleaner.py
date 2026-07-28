from datetime import datetime, timedelta


FLOW_TIMEOUT = 10  # seconds


def get_expired_flows(active_flows):
    """
    Returns flows that have been inactive
    for more than FLOW_TIMEOUT seconds.
    """

    expired = []

    now = datetime.now()

    for flow_key, flow in active_flows.items():

        if now - flow["last_seen"] > timedelta(seconds=FLOW_TIMEOUT):
            expired.append(flow_key)

    return expired