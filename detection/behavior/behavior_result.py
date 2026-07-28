class BehaviorResult:

    def __init__(self):

        self.detected = False
        self.attack = None
        self.score = 0
        self.severity = "LOW"
        self.reasons = []

    def add_reason(self, text):
        self.reasons.append(text)

    def raise_score(self, value):
        self.score += value

        if self.score > 100:
            self.score = 100

    def finalize(self):

        if self.score >= 80:
            self.severity = "CRITICAL"

        elif self.score >= 60:
            self.severity = "HIGH"

        elif self.score >= 40:
            self.severity = "MEDIUM"

        else:
            self.severity = "LOW"