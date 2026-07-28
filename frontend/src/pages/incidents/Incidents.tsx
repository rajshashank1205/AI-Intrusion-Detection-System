import {
  useCallback,
  useEffect,
  useMemo,
  useState,
} from "react";


type Incident = {
  id: number;
  source_ip: string;
  attack_type: string;
  severity: string;
  occurrence_count: number;
  last_seen: string;
  status: string;
};


export default function Incidents() {

  const [incidents, setIncidents] =
    useState<Incident[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [search, setSearch] =
    useState("");

  const [severityFilter, setSeverityFilter] =
    useState("ALL");

  const [updatingIncident, setUpdatingIncident] =
    useState<number | null>(null);


  // -----------------------------------
  // Fetch Incidents
  // -----------------------------------

  const fetchIncidents =
    useCallback(async () => {

      try {

        const response = await fetch(
          "http://127.0.0.1:8000/incidents"
        );


        if (!response.ok) {

          throw new Error(
            "Failed to fetch incidents"
          );

        }


        const data =
          await response.json();


        setIncidents(data);

        setError("");

      }

      catch (err) {

        console.error(
          "Incident fetch error:",
          err
        );


        setError(
          "Unable to load incidents."
        );

      }

      finally {

        setLoading(false);

      }

    }, []);


  // -----------------------------------
  // Initial Load + Live Updates
  // -----------------------------------

  useEffect(() => {

    fetchIncidents();


    function handleDashboardUpdate() {

      fetchIncidents();

    }


    window.addEventListener(
      "dashboard-update",
      handleDashboardUpdate
    );


    return () => {

      window.removeEventListener(
        "dashboard-update",
        handleDashboardUpdate
      );

    };

  }, [fetchIncidents]);


  // -----------------------------------
  // Update Incident Status
  // -----------------------------------

  async function updateStatus(
    incidentId: number,
    newStatus: string
  ) {

    setUpdatingIncident(
      incidentId
    );

    setError("");


    try {

      const response = await fetch(
        `http://127.0.0.1:8000/incidents/${incidentId}/status`,
        {

          method: "PATCH",

          headers: {

            "Content-Type":
              "application/json",

          },

          body: JSON.stringify({

            status: newStatus,

          }),

        }
      );


      if (!response.ok) {

        throw new Error(
          "Failed to update incident status"
        );

      }


      // Update the local UI immediately

      setIncidents(
        (previous) =>

          previous.map(
            (incident) =>

              incident.id === incidentId

                ? {
                    ...incident,
                    status: newStatus,
                  }

                : incident

          )

      );

    }

    catch (err) {

      console.error(
        "Incident status update error:",
        err
      );


      setError(
        "Unable to update incident status."
      );

    }

    finally {

      setUpdatingIncident(
        null
      );

    }

  }


  // -----------------------------------
  // Filter Incidents
  // -----------------------------------

  const filteredIncidents =
    useMemo(() => {

      const searchValue =
        search.toLowerCase().trim();


      return incidents.filter(
        (incident) => {

          const matchesSearch =

            searchValue === ""

            ||

            incident.source_ip
              .toLowerCase()
              .includes(
                searchValue
              )

            ||

            incident.attack_type
              .toLowerCase()
              .includes(
                searchValue
              );


          const matchesSeverity =

            severityFilter === "ALL"

            ||

            incident.severity ===
              severityFilter;


          return (
            matchesSearch
            &&
            matchesSeverity
          );

        }
      );

    }, [
      incidents,
      search,
      severityFilter,
    ]);


  // -----------------------------------
  // Statistics
  // -----------------------------------

  const criticalCount =
    incidents.filter(
      (incident) =>
        incident.severity ===
        "CRITICAL"
    ).length;


  const highCount =
    incidents.filter(
      (incident) =>
        incident.severity ===
        "HIGH"
    ).length;


  // -----------------------------------
  // Severity Styling
  // -----------------------------------

  function getSeverityStyle(
    severity: string
  ) {

    switch (
      severity.toUpperCase()
    ) {

      case "CRITICAL":

        return (
          "bg-red-500/20 text-red-400"
        );


      case "HIGH":

        return (
          "bg-orange-500/20 text-orange-400"
        );


      case "MEDIUM":

        return (
          "bg-yellow-500/20 text-yellow-400"
        );


      default:

        return (
          "bg-green-500/20 text-green-400"
        );

    }

  }


  // -----------------------------------
  // Loading
  // -----------------------------------

  if (loading) {

    return (

      <div className="flex h-96 items-center justify-center text-zinc-500">

        Loading security incidents...

      </div>

    );

  }


  return (

    <div className="space-y-6">


      {/* Header */}

      <div>

        <h1 className="text-4xl font-bold tracking-tight">

          Incidents

        </h1>


        <p className="mt-2 text-zinc-500">

          Grouped security incidents detected
          across monitored network traffic.

        </p>

      </div>


      {/* Error */}

      {error && (

        <div className="rounded-xl border border-red-900 bg-red-950/30 p-4 text-sm text-red-400">

          {error}

        </div>

      )}


      {/* Statistics */}

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">


        <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">

          <p className="text-sm text-zinc-500">

            Total Incidents

          </p>


          <p className="mt-3 text-4xl font-bold">

            {incidents.length}

          </p>

        </div>


        <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">

          <p className="text-sm text-zinc-500">

            Critical Incidents

          </p>


          <p className="mt-3 text-4xl font-bold text-red-400">

            {criticalCount}

          </p>

        </div>


        <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">

          <p className="text-sm text-zinc-500">

            High Severity

          </p>


          <p className="mt-3 text-4xl font-bold text-orange-400">

            {highCount}

          </p>

        </div>


      </div>


      {/* Filters */}

      <div className="flex flex-col gap-4 rounded-xl border border-zinc-800 bg-zinc-900 p-4 md:flex-row">


        <input
          type="text"
          placeholder="Search source IP or attack type..."
          value={search}
          onChange={(event) =>
            setSearch(
              event.target.value
            )
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
            placeholder:text-zinc-600
            focus:border-blue-500
          "
        />


        <select
          value={severityFilter}
          onChange={(event) =>
            setSeverityFilter(
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
            All Severities
          </option>

          <option value="CRITICAL">
            Critical
          </option>

          <option value="HIGH">
            High
          </option>

          <option value="MEDIUM">
            Medium
          </option>

          <option value="LOW">
            Low
          </option>

        </select>


      </div>


      {/* Incident Table */}

      <div className="overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900">


        <div className="flex items-center justify-between border-b border-zinc-800 px-6 py-5">


          <div>

            <h2 className="text-lg font-semibold">

              Security Incidents

            </h2>


            <p className="text-sm text-zinc-500">

              Related alerts grouped by
              source and attack type.

            </p>

          </div>


          <span className="text-sm text-zinc-500">

            Showing{" "}

            <span className="text-white">

              {filteredIncidents.length}

            </span>

          </span>


        </div>


        <div className="max-h-[600px] overflow-auto">


          <table className="w-full text-left text-sm">


            <thead className="sticky top-0 bg-zinc-950 text-zinc-500">

              <tr>

                <th className="px-5 py-4">
                  Incident
                </th>

                <th className="px-5 py-4">
                  Attack Type
                </th>

                <th className="px-5 py-4">
                  Source IP
                </th>

                <th className="px-5 py-4">
                  Severity
                </th>

                <th className="px-5 py-4">
                  Occurrences
                </th>

                <th className="px-5 py-4">
                  Last Seen
                </th>

                <th className="px-5 py-4">
                  Status
                </th>

              </tr>

            </thead>


            <tbody>


              {filteredIncidents.length === 0 ? (

                <tr>

                  <td
                    colSpan={7}
                    className="px-6 py-16 text-center text-zinc-500"
                  >

                    No incidents match
                    the current filters.

                  </td>

                </tr>

              ) : (

                filteredIncidents.map(
                  (incident) => (

                    <tr
                      key={incident.id}
                      className="border-t border-zinc-800/70 hover:bg-zinc-800/50"
                    >


                      {/* Incident ID */}

                      <td className="px-5 py-4 font-mono text-zinc-400">

                        INC-

                        {String(
                          incident.id
                        ).padStart(
                          4,
                          "0"
                        )}

                      </td>


                      {/* Attack Type */}

                      <td className="px-5 py-4 font-medium">

                        {
                          incident.attack_type
                        }

                      </td>


                      {/* Source IP */}

                      <td className="px-5 py-4 font-mono text-xs">

                        {
                          incident.source_ip
                        }

                      </td>


                      {/* Severity */}

                      <td className="px-5 py-4">

                        <span
                          className={`
                            rounded-full
                            px-2.5
                            py-1
                            text-xs
                            font-medium
                            ${getSeverityStyle(
                              incident.severity
                            )}
                          `}
                        >

                          {
                            incident.severity
                          }

                        </span>

                      </td>


                      {/* Occurrences */}

                      <td className="px-5 py-4">

                        {
                          incident.occurrence_count
                        }

                      </td>


                      {/* Last Seen */}

                      <td className="whitespace-nowrap px-5 py-4 text-zinc-400">

                        {new Date(
                          incident.last_seen
                        ).toLocaleString()}

                      </td>


                      {/* Status */}

                      <td className="px-5 py-4">

                        <select
                          value={
                            incident.status
                          }
                          disabled={
                            updatingIncident ===
                            incident.id
                          }
                          onChange={(event) =>
                            updateStatus(
                              incident.id,
                              event.target.value
                            )
                          }
                          className={`
                            rounded-lg
                            border
                            border-zinc-700
                            bg-zinc-950
                            px-3
                            py-2
                            text-xs
                            font-medium
                            outline-none
                            transition
                            focus:border-blue-500
                            disabled:cursor-wait
                            disabled:opacity-50

                            ${
                              incident.status ===
                              "RESOLVED"

                                ? "text-green-400"

                                : incident.status ===
                                  "INVESTIGATING"

                                ? "text-yellow-400"

                                : "text-blue-400"
                            }
                          `}
                        >

                          <option value="OPEN">

                            OPEN

                          </option>


                          <option value="INVESTIGATING">

                            INVESTIGATING

                          </option>


                          <option value="RESOLVED">

                            RESOLVED

                          </option>


                        </select>

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