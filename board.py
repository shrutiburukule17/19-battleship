class Board:
    SIZE = 6

    def __init__(self):
        self.ships = set()
        self.shots = set()

    def place_ship(self, cells):
        self.ships.update(cells)

    def fire(self, pos):
        self.shots.add(pos)
        return pos in self.ships

    def all_sunk(self):
        return self.ships <= self.shots