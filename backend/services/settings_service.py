from threading import Lock


class IDSSettings:

    def __init__(self):

        self._lock = Lock()

        self._settings = {
            "ai_detection": True,
            "live_packet_streaming": True,
            "detection_sensitivity": "medium",
            "alert_notifications": True,
            "sound_alerts": False,
            "refresh_interval": 5,
        }


    def get_settings(self):

        with self._lock:

            return self._settings.copy()


    def update_settings(self, new_settings):

        with self._lock:

            for key in self._settings:

                if key in new_settings:

                    self._settings[key] = (
                        new_settings[key]
                    )

            return self._settings.copy()


    def is_ai_enabled(self):

        with self._lock:

            return self._settings[
                "ai_detection"
            ]


    def is_packet_streaming_enabled(self):

        with self._lock:

            return self._settings[
                "live_packet_streaming"
            ]


    def get_detection_sensitivity(self):

        with self._lock:

            return self._settings[
                "detection_sensitivity"
            ]


ids_settings = IDSSettings()