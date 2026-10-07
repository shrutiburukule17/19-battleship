from board import Board
from ai import AI


class Battleship:
    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI()
        self._setup()

    def _setup(self):
        self.player.place_ship({(1, 1), (1, 2), (1, 3)})
        self.enemy.place_ship({(2, 2), (2, 3), (2, 4)})

    def show(self):
        print("\nYour shots are coordinates like 2,3.")
        print(
            "Enemy ship cells remaining:",
            len(self.enemy.ships - self.enemy.shots)
        )

    def run(self):
        print("Battleship")

        while True:
            self.show()

            raw = input("> ").strip().lower()

            if raw == "q":
                print("Goodbye!")
                return

            try:
                r, c = map(int, raw.split(","))
                pos = (r - 1, c - 1)
            except ValueError:
                print("Use row,col.")
                continue

            if not (
                0 <= pos[0] < Board.SIZE
                and 0 <= pos[1] < Board.SIZE
            ):
                print("Outside board.")
                continue

            if pos in self.enemy.shots:
                print("Already fired there.")
                continue

            hit = self.enemy.fire(pos)

            if hit:
                print("HIT!")
            else:
                print("MISS!")

            if self.enemy.all_sunk():
                print("You sank the fleet.")
                return

            ai_pos = self.ai.choose()

            if ai_pos is None:
                print("AI has no remaining choices.")
                return

            print(
                "AI fired at "
                f"{ai_pos[0] + 1},{ai_pos[1] + 1}"
            )

            ai_hit = self.player.fire(ai_pos)

            if ai_hit:
                print("AI scored a hit.")
            else:
                print("AI missed.")