import { useMemo, useState } from "react";

import { useLiveData } from "@/context/LiveDataContext";


export default function LiveTraffic() {

  const { packets } = useLiveData();

  const [isPaused, setIsPaused] = useState(false);
  const [pausedPackets, setPausedPackets] = useState(packets);

  const [protocolFilter, setProtocolFilter] =
    useState("ALL");

  const [search, setSearch] =
    useState("");


  // Packets shown on screen
  const visiblePackets =
    isPaused ? pausedPackets : packets;


  // Pause / Resume live view
  function togglePause() {

    if (!isPaused) {

      // Take snapshot of current packets
      setPausedPackets(packets);

      setIsPaused(true);

    } else {

      setIsPaused(false);

    }

  }


  // Filter packets
  const filteredPackets = useMemo(() => {

    return visiblePackets.filter((packet) => {

      const matchesProtocol =
        protocolFilter === "ALL" ||
        packet.protocol === protocolFilter;


      const searchValue =
        search.toLowerCase().trim();


      const matchesSearch =
        searchValue === "" ||
        packet.src_ip
          .toLowerCase()
          .includes(searchValue) ||
        packet.dst_ip
          .toLowerCase()
          .includes(searchValue) ||
        String(packet.src_port ?? "")
          .includes(searchValue) ||
        String(packet.dst_port ?? "")
          .includes(searchValue);


      return (
        matchesProtocol &&
        matchesSearch
      );

    });

  }, [
    visiblePackets,
    protocolFilter,
    search,
  ]);


  // Packet statistics
  const tcpCount =
    visiblePackets.filter(
      (packet) =>
        packet.protocol === "TCP"
    ).length;


  const udpCount =
    visiblePackets.filter(
      (packet) =>
        packet.protocol === "UDP"
    ).length;


  function formatTime(timestamp: string) {

    const date =
      new Date(timestamp);

    return date.toLocaleTimeString();

  }


  return (

    <div className="space-y-6">


      {/* Header */}

      <div className="flex items-center justify-between">

        <div>

          <div className="flex items-center gap-3">

            <h1 className="text-4xl font-bold tracking-tight">
              Live Traffic
            </h1>


            <span
              className={`
                rounded-full
                px-3
                py-1
                text-xs
                font-medium
                ${
                  isPaused
                    ? "bg-yellow-500/20 text-yellow-400"
                    : "bg-green-500/20 text-green-400"
                }
              `}
            >

              {isPaused ? "PAUSED" : "LIVE"}

            </span>

          </div>


          <p className="mt-2 text-zinc-500">
            Real-time network packet monitoring.
          </p>

        </div>


        <button
          onClick={togglePause}
          className={`
            rounded-lg
            px-5
            py-2.5
            text-sm
            font-medium
            transition
            ${
              isPaused
                ? "bg-green-600 hover:bg-green-500"
                : "bg-yellow-600 hover:bg-yellow-500"
            }
          `}
        >

          {isPaused
            ? "Resume Live Traffic"
            : "Pause Live Traffic"}

        </button>

      </div>


      {/* Statistics */}

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">


        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">

          <p className="text-sm text-zinc-500">
            Packets Displayed
          </p>

          <p className="mt-2 text-3xl font-bold">
            {visiblePackets.length}
          </p>

        </div>


        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">

          <p className="text-sm text-zinc-500">
            TCP Packets
          </p>

          <p className="mt-2 text-3xl font-bold text-blue-400">
            {tcpCount}
          </p>

        </div>


        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">

          <p className="text-sm text-zinc-500">
            UDP Packets
          </p>

          <p className="mt-2 text-3xl font-bold text-purple-400">
            {udpCount}
          </p>

        </div>

      </div>


      {/* Filters */}

      <div className="flex flex-col gap-4 rounded-xl border border-zinc-800 bg-zinc-900 p-4 md:flex-row">


        <input
          type="text"
          placeholder="Search IP address or port..."
          value={search}
          onChange={(event) =>
            setSearch(event.target.value)
          }
          className="
            flex-1
            rounded-lg
            border
            border-zinc-700
            bg-zinc-950
            px-4
            py-2.5
            text-sm
            outline-none
            transition
            placeholder:text-zinc-600
            focus:border-blue-500
          "
        />


        <select
          value={protocolFilter}
          onChange={(event) =>
            setProtocolFilter(
              event.target.value
            )
          }
          className="
            rounded-lg
            border
            border-zinc-700
            bg-zinc-950
            px-4
            py-2.5
            text-sm
            outline-none
          "
        >

          <option value="ALL">
            All Protocols
          </option>

          <option value="TCP">
            TCP
          </option>

          <option value="UDP">
            UDP
          </option>

          <option value="OTHER">
            Other
          </option>

        </select>

      </div>


      {/* Packet Table */}

      <div className="overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900">


        <div className="flex items-center justify-between border-b border-zinc-800 px-6 py-5">

          <div>

            <h2 className="text-lg font-semibold">
              Packet Stream
            </h2>

            <p className="text-sm text-zinc-500">
              Real-time captured network packets
            </p>

          </div>


          <span className="text-sm text-zinc-500">

            Showing{" "}

            <span className="font-medium text-white">
              {filteredPackets.length}
            </span>

            {" "}packets

          </span>

        </div>


        <div className="max-h-[600px] overflow-auto">


          <table className="w-full text-left text-sm">


            <thead className="sticky top-0 z-10 border-b border-zinc-800 bg-zinc-950 text-zinc-500">

              <tr>

                <th className="px-5 py-4">
                  Time
                </th>

                <th className="px-5 py-4">
                  Protocol
                </th>

                <th className="px-5 py-4">
                  Source
                </th>

                <th className="px-5 py-4">
                  Destination
                </th>

                <th className="px-5 py-4">
                  Size
                </th>

                <th className="px-5 py-4">
                  TTL
                </th>

                <th className="px-5 py-4">
                  Flags
                </th>

              </tr>

            </thead>


            <tbody>

              {filteredPackets.length === 0 ? (

                <tr>

                  <td
                    colSpan={7}
                    className="px-6 py-16 text-center text-zinc-500"
                  >

                    {visiblePackets.length === 0
                      ? "Waiting for live network packets..."
                      : "No packets match the current filters."}

                  </td>

                </tr>

              ) : (

                filteredPackets.map(
                  (packet, index) => (

                    <tr
                      key={`${packet.timestamp}-${index}`}
                      className="
                        border-b
                        border-zinc-800/70
                        transition-colors
                        hover:bg-zinc-800/50
                      "
                    >


                      <td className="whitespace-nowrap px-5 py-4 text-zinc-400">

                        {formatTime(
                          packet.timestamp
                        )}

                      </td>


                      <td className="px-5 py-4">

                        <span
                          className={`
                            rounded-md
                            px-2
                            py-1
                            text-xs
                            font-medium
                            ${
                              packet.protocol === "TCP"
                                ? "bg-blue-500/20 text-blue-400"
                                : packet.protocol === "UDP"
                                ? "bg-purple-500/20 text-purple-400"
                                : "bg-zinc-700 text-zinc-300"
                            }
                          `}
                        >

                          {packet.protocol}

                        </span>

                      </td>


                      <td className="px-5 py-4 font-mono text-xs">

                        {packet.src_ip}

                        {packet.src_port !== null && (

                          <span className="text-zinc-500">

                            :{packet.src_port}

                          </span>

                        )}

                      </td>


                      <td className="px-5 py-4 font-mono text-xs">

                        {packet.dst_ip}

                        {packet.dst_port !== null && (

                          <span className="text-zinc-500">

                            :{packet.dst_port}

                          </span>

                        )}

                      </td>


                      <td className="whitespace-nowrap px-5 py-4 text-zinc-400">

                        {packet.packet_size} B

                      </td>


                      <td className="px-5 py-4 text-zinc-400">

                        {packet.ttl}

                      </td>


                      <td className="px-5 py-4 font-mono text-zinc-400">

                        {packet.flags || "—"}

                      </td>


                    </tr>

                  )
                )

              )}

            </tbody>

          </table>

        </div>

      </div>

    </div>

  );
}