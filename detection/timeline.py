from datetime import datetime


class Timeline:

    def __init__(self):
        self.events = []

    def add_event(self, source, event, severity="INFO"):

        self.events.append({
            "time": datetime.now(),
            "source": source,
            "event": event,
            "severity": severity
        })

    def get_events(self):
        return self.events

    def clear(self):
        self.events.clear()


# Global timeline instance
timeline = Timeline()