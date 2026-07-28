class Evidence:
    """
    Represents one piece of security evidence.
    """

    def __init__(self, source, score, reason, attack=None):

        self.source = source
        self.score = score
        self.reason = reason
        self.attack = attack

    def to_dict(self):

        return {
            "source": self.source,
            "score": self.score,
            "reason": self.reason,
            "attack": self.attack
        }