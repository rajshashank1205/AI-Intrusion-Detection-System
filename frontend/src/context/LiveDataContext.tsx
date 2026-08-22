import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

import type { ReactNode } from "react";


// =====================================================
// TYPES
// =====================================================

export type Alert = {
  timestamp: string;
  source_ip: string;
  alert_type: string;
  severity: string;
  description: string;
};


export type LivePacket = {
  type: "packet";
  timestamp: string;
  src_ip: string;
  dst_ip: string;
  src_port: number | null;
  dst_port: number | null;
  protocol: string;
  packet_size: number;
  ttl: number;
  flags: string;
};


type LiveDataContextType = {
  alerts: Alert[];
  packets: LivePacket[];

  addAlert: (alert: Alert) => void;
  addPacket: (packet: LivePacket) => void;
};


// =====================================================
// CONTEXT
// =====================================================

const LiveDataContext =
  createContext<LiveDataContextType | null>(null);


// =====================================================
// PROVIDER
// =====================================================

export function LiveDataProvider({
  children,
}: {
  children: ReactNode;
}) {

  const [alerts, setAlerts] =
    useState<Alert[]>([]);

  const [packets, setPackets] =
    useState<LivePacket[]>([]);


  // ===================================================
  // ADD LIVE ALERT
  // ===================================================

  function addAlert(alert: Alert) {

    setAlerts((prev) => {

      const updatedAlerts =
        [alert, ...prev].slice(0, 20);

      return updatedAlerts;

    });


    // Tell dashboard cards that new data arrived
    window.dispatchEvent(
      new CustomEvent("dashboard-update")
    );

  }


  // ===================================================
  // ADD LIVE PACKET
  // ===================================================

  function addPacket(packet: LivePacket) {

    setPackets((prev) =>
      [packet, ...prev].slice(0, 100)
    );

  }


  // ===================================================
  // WEBSOCKET CONNECTION
  // ===================================================

  useEffect(() => {

    let socket: WebSocket | null = null;

    let reconnectTimer:
      ReturnType<typeof setTimeout> | null =
      null;

    let isUnmounted = false;


    // -------------------------------------------------
    // CONNECT
    // -------------------------------------------------

    function connectWebSocket() {

      if (isUnmounted) {
        return;
      }


      console.log(
        "🔌 Connecting to IDS WebSocket..."
      );


      socket = new WebSocket(
        `${(import.meta.env.VITE_API_URL || "http://127.0.0.1:8000")
          .replace(/^http:/, "ws:")
          .replace(/^https:/, "wss:")}/ws`
      );


      // ------------------------------------------------
      // CONNECTION OPEN
      // ------------------------------------------------

      socket.onopen = () => {

        console.log(
          "✅ Connected to IDS WebSocket"
        );

      };


      // ------------------------------------------------
      // RECEIVE MESSAGE
      // ------------------------------------------------

      socket.onmessage = (event) => {

        try {

          const data =
            JSON.parse(event.data);


          console.log(
            "📡 WebSocket event received:",
            data
          );


          // --------------------------------------------
          // HEARTBEAT
          // --------------------------------------------

          if (data.type === "ping") {

            return;

          }


          // --------------------------------------------
          // LIVE PACKET
          // --------------------------------------------

          if (data.type === "packet") {

            addPacket(
              data as LivePacket
            );

            return;

          }


          // --------------------------------------------
          // LIVE ALERT
          // --------------------------------------------

          if (
            data.alert_type &&
            data.source_ip &&
            data.severity
          ) {

            addAlert(
              data as Alert
            );

            return;

          }


          console.log(
            "ℹ️ Unknown WebSocket event:",
            data
          );

        } catch (error) {

          console.error(
            "❌ Failed to parse WebSocket message:",
            error
          );

        }

      };


      // ------------------------------------------------
      // CONNECTION CLOSED
      // ------------------------------------------------

      socket.onclose = () => {

        console.log(
          "⚠️ IDS WebSocket disconnected"
        );


        if (!isUnmounted) {

          console.log(
            "🔄 Reconnecting in 3 seconds..."
          );


          reconnectTimer =
            setTimeout(
              connectWebSocket,
              3000
            );

        }

      };


      // ------------------------------------------------
      // CONNECTION ERROR
      // ------------------------------------------------

      socket.onerror = (error) => {

        console.error(
          "❌ IDS WebSocket error:",
          error
        );

      };

    }


    // =================================================
    // START CONNECTION
    // =================================================

    connectWebSocket();


    // =================================================
    // CLEANUP
    // =================================================

    return () => {

      isUnmounted = true;


      if (reconnectTimer) {

        clearTimeout(
          reconnectTimer
        );

      }


      if (socket) {

        socket.close();

      }

    };

  }, []);


  // ===================================================
  // CONTEXT PROVIDER
  // ===================================================

  return (

    <LiveDataContext.Provider
      value={{
        alerts,
        packets,
        addAlert,
        addPacket,
      }}
    >

      {children}

    </LiveDataContext.Provider>

  );

}


// =====================================================
// LIVE DATA HOOK
// =====================================================

export function useLiveData() {

  const context =
    useContext(LiveDataContext);


  if (!context) {

    throw new Error(
      "useLiveData must be used inside LiveDataProvider"
    );

  }


  return context;

}