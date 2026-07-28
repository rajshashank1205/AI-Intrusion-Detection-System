from collections import defaultdict, deque
from datetime import datetime


class SlidingWindow:

    def __init__(self, window_seconds=2):

        self.window_seconds = window_seconds
        self.events = defaultdict(deque)

    def add_event(self, key):

        now = datetime.now()

        queue = self.events[key]

        queue.append(now)

        self._cleanup(queue, now)

    def count(self, key):

        now = datetime.now()

        queue = self.events[key]

        self._cleanup(queue, now)

        return len(queue)

    def _cleanup(self, queue, now):

        while queue:

            age = (now - queue[0]).total_seconds()

            if age > self.window_seconds:
                queue.popleft()
            else:
                break