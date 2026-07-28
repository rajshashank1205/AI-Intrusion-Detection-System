let socket: WebSocket | null = null;

export function connectWebSocket(
  onMessage: (data: any) => void
) {
  socket = new WebSocket("ws://127.0.0.1:8000/ws");

  socket.onopen = () => {
    console.log("✅ WebSocket Connected");
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (err) {
      console.error("WebSocket message error:", err);
    }
  };

  socket.onclose = () => {
    console.log("❌ WebSocket Disconnected");
  };

  socket.onerror = (error) => {
    console.error("WebSocket Error:", error);
  };

  return socket;
}

export function getSocket() {
  return socket;
}