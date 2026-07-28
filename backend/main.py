from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router
from backend.websocket_manager import manager
from backend.services.live_metrics import live_metrics


app = FastAPI(
    title="AI Intrusion Detection API",
    version="1.0.0"
)


# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# REST API Routes
# --------------------------------------------------

app.include_router(router)


# --------------------------------------------------
# WebSocket Endpoint
# --------------------------------------------------

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    print("✅ Dashboard connected to WebSocket")

    try:

        while True:

            # Wait for messages from the browser.
            # This immediately detects disconnects when the
            # browser closes or refreshes.
            await websocket.receive_text()

    except WebSocketDisconnect:

        print("❌ Dashboard disconnected")

        manager.disconnect(websocket)

    except Exception as e:

        print(f"❌ WebSocket error: {e}")

        manager.disconnect(websocket)


# --------------------------------------------------
# IDS Alert Broadcast Endpoint
# --------------------------------------------------

@app.post("/internal/broadcast-alert")
async def broadcast_alert_endpoint(alert: dict):

    print("📡 Backend received alert from IDS:")
    print(alert)

    await manager.broadcast(alert)

    return {
        "status": "broadcasted"
    }


# --------------------------------------------------
# Live Packet Broadcast Endpoint
# --------------------------------------------------

@app.post("/internal/broadcast-packet")
async def broadcast_packet_endpoint(packet: dict):
    """
    Receives captured packet metadata from the IDS
    and broadcasts it to connected dashboard clients.
    """

    await manager.broadcast(packet)

    return {
        "status": "broadcasted"
    }


# --------------------------------------------------
# Live Packet Rate Endpoint
# --------------------------------------------------

@app.post("/internal/packet-rate")
async def update_packet_rate(data: dict):

    packets_per_second = data.get(
        "packets_per_second",
        0
    )

    live_metrics.set_packet_rate(
        int(packets_per_second)
    )

    return {
        "status": "updated",
        "packets_per_second": packets_per_second
    }


# --------------------------------------------------
# Live AI Score Endpoint
# --------------------------------------------------

@app.post("/internal/ai-score")
async def update_ai_score(data: dict):

    ai_score = data.get(
        "ai_score",
        0
    )

    live_metrics.set_ai_score(
        float(ai_score)
    )

    return {
        "status": "updated",
        "ai_score": ai_score
    }


# --------------------------------------------------
# Health Routes
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "AI Intrusion Detection System API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }