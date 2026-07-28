from datetime import datetime, timedelta


class AttackMemory:

    def __init__(self):
        self.memory = {}

    def add(self, ip, attack, severity):
        self.memory[ip] = {
            "attack": attack,
            "severity": severity,
            "time": datetime.now()
        }

    def recent(self, ip, seconds=30):

        if ip not in self.memory:
            return None

        event = self.memory[ip]

        if datetime.now() - event["time"] <= timedelta(seconds=seconds):
            return event

        del self.memory[ip]
        return None


attack_memory = AttackMemory()