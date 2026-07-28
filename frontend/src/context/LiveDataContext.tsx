import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

import type { ReactNode } from "react";


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


const LiveDataContext =
  createContext<LiveDataContextType | null>(
    null
  );


export function LiveDataProvider({
  children,
}: {
  children: ReactNode;
}) {

  const [alerts, setAlerts] =
    useState<Alert[]>([]);

  const [packets, setPackets] =
    useState<LivePacket[]>([]);


  // -------------------------------------------------
  // Add Live Alert
  // -------------------------------------------------

  function addAlert(alert: Alert) {

    setAlerts(
      (prev) =>
        [alert, ...prev].slice(0, 20)
    );

  }


  // -------------------------------------------------
  // Add Live Packet
  // -------------------------------------------------

  function addPacket(packet: LivePacket) {

    setPackets(
      (prev) =>
        [packet, ...prev].slice(0, 100)
    );

  }


  // -------------------------------------------------
  // WebSocket Connection
  // -------------------------------------------------

  useEffect(() => {

    let socket: WebSocket | null = null;

    let reconnectTimer:
      ReturnType<typeof setTimeout> | null =
      null;

    let isUnmounted = false;


    // -----------------------------------------------
    // Connect To IDS Backend
    // -----------------------------------------------

    function connectWebSocket() {

      if (isUnmounted) {
        return;
      }


      console.log(
        "🔌 Connecting to IDS WebSocket..."
      );


      socket = new WebSocket(
        "ws://127.0.0.1:8000/ws"
      );


      // ---------------------------------------------
      // Connection Opened
      // ---------------------------------------------

      socket.onopen = () => {

        console.log(
          "✅ Connected to IDS WebSocket"
        );

      };


      // ---------------------------------------------
      // Receive Message
      // ---------------------------------------------

      socket.onmessage = (event) => {

        try {

          const data =
            JSON.parse(event.data);


          console.log(
            "📡 WebSocket event received:",
            data
          );


          // -----------------------------------------
          // Ignore Backend Heartbeat
          // -----------------------------------------

          if (data.type === "ping") {

            return;

          }


          // -----------------------------------------
          // Live Packet Event
          // -----------------------------------------

          if (data.type === "packet") {

            addPacket(
              data as LivePacket
            );

            return;

          }


          // -----------------------------------------
          // Live Alert Event
          // -----------------------------------------
          //
          // Alert events currently do not contain
          // a "type" field, so identify them using
          // the alert fields sent by the IDS.

          if (
            data.alert_type &&
            data.source_ip &&
            data.severity
          ) {

            addAlert(
              data as Alert
            );

          }


        } catch (error) {

          console.error(
            "❌ Failed to process WebSocket message:",
            error
          );

        }

      };


      // ---------------------------------------------
      // WebSocket Error
      // ---------------------------------------------

      socket.onerror = (error) => {

        console.error(
          "❌ IDS WebSocket error:",
          error
        );

      };


      // ---------------------------------------------
      // Connection Closed
      // ---------------------------------------------

      socket.onclose = () => {

        console.log(
          "⚠️ IDS WebSocket disconnected"
        );


        // Automatically reconnect after 3 seconds.

        if (!isUnmounted) {

          reconnectTimer =
            setTimeout(
              connectWebSocket,
              3000
            );

        }

      };

    }


    // Start WebSocket connection.

    connectWebSocket();


    // -----------------------------------------------
    // Cleanup
    // -----------------------------------------------

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


  // -------------------------------------------------
  // Context Provider
  // -------------------------------------------------

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


// -------------------------------------------------
// Live Data Hook
// -------------------------------------------------

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