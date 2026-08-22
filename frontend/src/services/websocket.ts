let socket: WebSocket | null = null;

export function connectWebSocket(
  onMessage: (data: any) => void
) {
  const apiUrl =
    import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

  // Convert HTTP/HTTPS API URL to WS/WSS
  const wsUrl = apiUrl
    .replace(/^http:/, "ws:")
    .replace(/^https:/, "wss:");

  socket = new WebSocket(`${wsUrl}/ws`);

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
    console.error("WebSocket error:", error);
  };
}

export function disconnectWebSocket() {
  if (socket) {
    socket.close();
    socket = null;
  }
}