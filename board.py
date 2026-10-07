class Board:
    SIZE = 6

    def __init__(self):
        self.ships = {}
        self.shots = set()

    def place_ship(self, name, cells):
        cells = set(cells)

        if not cells:
            raise ValueError("A ship must contain at least one cell.")

        if any(
            not (0 <= r < self.SIZE and 0 <= c < self.SIZE)
            for r, c in cells
        ):
            raise ValueError("Ship contains a cell outside the board.")

        occupied = set().union(*self.ships.values()) if self.ships else set()

        if occupied & cells:
            raise ValueError("Ships cannot overlap.")

        self.ships[name] = cells

    def fire(self, pos):
        if pos in self.shots:
            return "repeat"

        self.shots.add(pos)

        for name, cells in self.ships.items():
            if pos in cells:
                if cells <= self.shots:
                    return f"sunk:{name}"

                return "hit"

        return "miss"

    def ship_status(self):
        status = {}

        for name, cells in self.ships.items():
            hits = cells & self.shots
            status[name] = {
                "size": len(cells),
                "hits": len(hits),
                "sunk": cells <= self.shots,
            }

        return status

    def all_sunk(self):
        return bool(self.ships) and all(
            cells <= self.shots
            for cells in self.ships.values()
        )

    def remaining_cells(self):
        occupied = set().union(*self.ships.values())
        return len(occupied - self.shots)