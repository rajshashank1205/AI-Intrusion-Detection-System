import requests
from backend.config import BACKEND_URL


def broadcast_alert(alert: dict):
    """
    Send a newly detected alert to the FastAPI backend.

    The FastAPI backend will then broadcast it
    to all connected WebSocket clients.
    """

    try:
        response = requests.post(
            f"{BACKEND_URL}/internal/broadcast-alert",
            json=alert,
            timeout=2
        )

        if response.status_code == 200:
            print("📡 Alert sent to WebSocket server.")
        else:
            print(
                f"⚠️ WebSocket broadcast failed: "
                f"{response.status_code}"
            )

    except requests.RequestException as error:
        print(
            f"⚠️ Could not send alert to WebSocket server: "
            f"{error}"
        )