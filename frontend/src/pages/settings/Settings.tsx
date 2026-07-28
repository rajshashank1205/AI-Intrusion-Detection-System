import { useEffect, useState } from "react";


type SettingsState = {
  aiDetection: boolean;
  livePacketStreaming: boolean;
  alertNotifications: boolean;
  soundAlerts: boolean;
  detectionSensitivity: string;
  refreshInterval: string;
};


type BackendSettings = {
  ai_detection: boolean;
  live_packet_streaming: boolean;
  alert_notifications: boolean;
  sound_alerts: boolean;
  detection_sensitivity: string;
  refresh_interval: number;
};


const defaultSettings: SettingsState = {
  aiDetection: true,
  livePacketStreaming: true,
  alertNotifications: true,
  soundAlerts: false,
  detectionSensitivity: "medium",
  refreshInterval: "5",
};


export default function Settings() {

  const [settings, setSettings] =
    useState<SettingsState>(defaultSettings);

  const [saved, setSaved] =
    useState(false);

  const [loading, setLoading] =
    useState(true);

  const [saving, setSaving] =
    useState(false);

  const [error, setError] =
    useState("");


  // -----------------------------------
  // Load Settings From Backend
  // -----------------------------------

  useEffect(() => {

    async function loadSettings() {

      try {

        const response = await fetch(
          "http://127.0.0.1:8000/settings"
        );


        if (!response.ok) {

          throw new Error(
            "Failed to load settings"
          );

        }


        const data: BackendSettings =
          await response.json();


        setSettings({

          aiDetection:
            data.ai_detection,

          livePacketStreaming:
            data.live_packet_streaming,

          alertNotifications:
            data.alert_notifications,

          soundAlerts:
            data.sound_alerts,

          detectionSensitivity:
            data.detection_sensitivity,

          refreshInterval:
            String(
              data.refresh_interval
            ),

        });


        setError("");

      }

      catch (err) {

        console.error(
          "Settings load error:",
          err
        );


        setError(
          "Unable to load settings from the backend."
        );

      }

      finally {

        setLoading(false);

      }

    }


    loadSettings();

  }, []);


  // -----------------------------------
  // Update Local Setting
  // -----------------------------------

  function updateSetting<
    K extends keyof SettingsState
  >(
    key: K,
    value: SettingsState[K]
  ) {

    setSettings(
      (previous) => ({

        ...previous,

        [key]: value,

      })
    );


    setSaved(false);

  }


  // -----------------------------------
  // Save Settings To Backend
  // -----------------------------------

  async function saveSettings() {

    setSaving(true);

    setSaved(false);

    setError("");


    const backendSettings = {

      ai_detection:
        settings.aiDetection,

      live_packet_streaming:
        settings.livePacketStreaming,

      alert_notifications:
        settings.alertNotifications,

      sound_alerts:
        settings.soundAlerts,

      detection_sensitivity:
        settings.detectionSensitivity,

      refresh_interval:
        Number(
          settings.refreshInterval
        ),

    };


    try {

      const response = await fetch(
        "http://127.0.0.1:8000/settings",
        {

          method: "PUT",

          headers: {

            "Content-Type":
              "application/json",

          },

          body: JSON.stringify(
            backendSettings
          ),

        }
      );


      if (!response.ok) {

        throw new Error(
          "Failed to save settings"
        );

      }


      // Keep a browser copy as backup

      localStorage.setItem(
        "ids-settings",
        JSON.stringify(settings)
      );


      setSaved(true);


      setTimeout(() => {

        setSaved(false);

      }, 2500);

    }

    catch (err) {

      console.error(
        "Settings save error:",
        err
      );


      setError(
        "Unable to save settings."
      );

    }

    finally {

      setSaving(false);

    }

  }


  // -----------------------------------
  // Reset Settings
  // -----------------------------------

  function resetSettings() {

    setSettings(
      defaultSettings
    );

    setSaved(false);

    setError("");

  }


  // -----------------------------------
  // Loading
  // -----------------------------------

  if (loading) {

    return (

      <div className="flex h-96 items-center justify-center text-zinc-500">

        Loading IDS settings...

      </div>

    );

  }


  return (

    <div className="space-y-6">


      {/* Header */}

      <div>

        <h1 className="text-4xl font-bold tracking-tight">

          Settings

        </h1>


        <p className="mt-2 text-zinc-500">

          Configure monitoring and detection preferences.

        </p>

      </div>


      {/* Error */}

      {error && (

        <div className="rounded-xl border border-red-900 bg-red-950/30 p-4 text-sm text-red-400">

          {error}

        </div>

      )}


      {/* Detection Engine */}

      <section className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">

        <h2 className="text-lg font-semibold">

          Detection Engine

        </h2>


        <p className="mt-1 text-sm text-zinc-500">

          Configure threat detection preferences.

        </p>


        <div className="mt-6 divide-y divide-zinc-800">


          <SettingToggle
            title="AI Anomaly Detection"
            description="Enable machine-learning based anomaly detection."
            enabled={
              settings.aiDetection
            }
            onChange={(value) =>

              updateSetting(
                "aiDetection",
                value
              )

            }
          />


          <SettingToggle
            title="Live Packet Streaming"
            description="Display captured packets on the Live Traffic page."
            enabled={
              settings.livePacketStreaming
            }
            onChange={(value) =>

              updateSetting(
                "livePacketStreaming",
                value
              )

            }
          />


        </div>


        <div className="mt-6">

          <label className="text-sm font-medium">

            Detection Sensitivity

          </label>


          <p className="mt-1 text-sm text-zinc-500">

            Higher sensitivity may detect more threats
            but can increase false positives.

          </p>


          <select
            value={
              settings.detectionSensitivity
            }
            onChange={(event) =>

              updateSetting(
                "detectionSensitivity",
                event.target.value
              )

            }
            className="
              mt-4
              w-full
              rounded-lg
              border
              border-zinc-700
              bg-zinc-950
              px-4
              py-3
              outline-none
              focus:border-blue-500
            "
          >

            <option value="low">
              Low
            </option>

            <option value="medium">
              Medium
            </option>

            <option value="high">
              High
            </option>

          </select>

        </div>

      </section>


      {/* Notifications */}

      <section className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">

        <h2 className="text-lg font-semibold">

          Notifications

        </h2>


        <p className="mt-1 text-sm text-zinc-500">

          Configure how security alerts are presented.

        </p>


        <div className="mt-6 divide-y divide-zinc-800">


          <SettingToggle
            title="Alert Notifications"
            description="Show notifications when new security threats are detected."
            enabled={
              settings.alertNotifications
            }
            onChange={(value) =>

              updateSetting(
                "alertNotifications",
                value
              )

            }
          />


          <SettingToggle
            title="Sound Alerts"
            description="Play an alert sound for important security events."
            enabled={
              settings.soundAlerts
            }
            onChange={(value) =>

              updateSetting(
                "soundAlerts",
                value
              )

            }
          />


        </div>

      </section>


      {/* Dashboard */}

      <section className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">

        <h2 className="text-lg font-semibold">

          Dashboard

        </h2>


        <p className="mt-1 text-sm text-zinc-500">

          Configure dashboard behaviour.

        </p>


        <div className="mt-6">

          <label className="text-sm font-medium">

            Refresh Interval

          </label>


          <select
            value={
              settings.refreshInterval
            }
            onChange={(event) =>

              updateSetting(
                "refreshInterval",
                event.target.value
              )

            }
            className="
              mt-3
              w-full
              rounded-lg
              border
              border-zinc-700
              bg-zinc-950
              px-4
              py-3
              outline-none
              focus:border-blue-500
            "
          >

            <option value="2">
              Every 2 seconds
            </option>

            <option value="5">
              Every 5 seconds
            </option>

            <option value="10">
              Every 10 seconds
            </option>

            <option value="30">
              Every 30 seconds
            </option>

          </select>

        </div>

      </section>


      {/* Actions */}

      <div className="flex items-center justify-between">


        <button
          onClick={resetSettings}
          className="
            rounded-lg
            border
            border-zinc-700
            px-5
            py-2.5
            text-sm
            text-zinc-300
            transition
            hover:bg-zinc-800
          "
        >

          Reset Defaults

        </button>


        <div className="flex items-center gap-4">


          {saved && (

            <span className="text-sm text-green-400">

              Settings saved successfully

            </span>

          )}


          <button
            onClick={saveSettings}
            disabled={saving}
            className="
              rounded-lg
              bg-blue-600
              px-6
              py-2.5
              text-sm
              font-medium
              text-white
              transition
              hover:bg-blue-500
              disabled:cursor-not-allowed
              disabled:opacity-50
            "
          >

            {
              saving
                ? "Saving..."
                : "Save Settings"
            }

          </button>


        </div>

      </div>

    </div>

  );

}


type SettingToggleProps = {

  title: string;

  description: string;

  enabled: boolean;

  onChange: (
    value: boolean
  ) => void;

};


function SettingToggle({

  title,

  description,

  enabled,

  onChange,

}: SettingToggleProps) {

  return (

    <div className="flex items-center justify-between gap-6 py-5">


      <div>

        <p className="font-medium">

          {title}

        </p>


        <p className="mt-1 text-sm text-zinc-500">

          {description}

        </p>

      </div>


      <button
        type="button"
        onClick={() =>

          onChange(
            !enabled
          )

        }
        className={`
          relative
          h-7
          w-12
          shrink-0
          rounded-full
          transition-colors
          ${
            enabled
              ? "bg-blue-600"
              : "bg-zinc-700"
          }
        `}
      >

        <span
          className={`
            absolute
            top-1
            h-5
            w-5
            rounded-full
            bg-white
            transition-all
            ${
              enabled
                ? "left-6"
                : "left-1"
            }
          `}
        />

      </button>


    </div>

  );

}