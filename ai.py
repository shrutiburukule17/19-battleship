import random


class AI:
    def __init__(self, size=6):
        self.size = size
        self.tried = set()
        self.target_queue = []

    def _valid(self, pos):
        r, c = pos

        return (
            0 <= r < self.size
            and 0 <= c < self.size
            and pos not in self.tried
        )

    def _neighbors(self, pos):
        r, c = pos

        return [
            (r - 1, c),
            (r + 1, c),
            (r, c - 1),
            (r, c + 1),
        ]

    def register_result(self, pos, result):
        if result == "hit":
            for neighbor in self._neighbors(pos):
                if self._valid(neighbor):
                    if neighbor not in self.target_queue:
                        self.target_queue.append(neighbor)

        elif result.startswith("sunk:"):
            self.target_queue.clear()

    def choose(self):
        while self.target_queue:
            pos = self.target_queue.pop(0)

            if self._valid(pos):
                self.tried.add(pos)
                return pos

        options = [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if (r, c) not in self.tried
        ]

        if not options:
            return None

        pos = random.choice(options)
        self.tried.add(pos)

        return pos