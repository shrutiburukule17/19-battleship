from board import Board
from ai import AI


class Battleship:
    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI()
        self._setup()

    def _setup(self):
        self.player.place_ship(
            "Carrier",
            {
                (0, 0),
                (0, 1),
                (0, 2),
                (0, 3),
                (0, 4),
            },
        )

        self.player.place_ship(
            "Battleship",
            {
                (2, 0),
                (3, 0),
                (4, 0),
                (5, 0),
            },
        )

        self.player.place_ship(
            "Cruiser",
            {
                (2, 2),
                (2, 3),
                (2, 4),
            },
        )

        self.player.place_ship(
            "Submarine",
            {
                (4, 2),
                (4, 3),
                (4, 4),
            },
        )

        self.player.place_ship(
            "Destroyer",
            {
                (1, 5),
                (2, 5),
            },
        )

        self.enemy.place_ship(
            "Carrier",
            {
                (0, 1),
                (1, 1),
                (2, 1),
                (3, 1),
                (4, 1),
            },
        )

        self.enemy.place_ship(
            "Battleship",
            {
                (0, 3),
                (1, 3),
                (2, 3),
                (3, 3),
            },
        )

        self.enemy.place_ship(
            "Cruiser",
            {
                (4, 3),
                (4, 4),
                (4, 5),
            },
        )

        self.enemy.place_ship(
            "Submarine",
            {
                (1, 5),
                (2, 5),
                (3, 5),
            },
        )

        self.enemy.place_ship(
            "Destroyer",
            {
                (5, 0),
                (5, 1),
            },
        )

    def show(self):
        print("\nYour shots are coordinates like 2,3.")
        print("Enemy ship cells remaining:", self.enemy.remaining_cells())

        print("\nEnemy fleet:")
        for name, info in self.enemy.ship_status().items():
            state = "SUNK" if info["sunk"] else f"{info['hits']}/{info['size']} hit"
            print(f"  {name}: {state}")

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

            result = self.enemy.fire(pos)

            if result == "repeat":
                print("Already fired there.")
                continue

            if result == "miss":
                print("MISS!")

            elif result == "hit":
                print("HIT!")

            elif result.startswith("sunk:"):
                ship_name = result.split(":", 1)[1]
                print(f"HIT! You sank the {ship_name}.")

            if self.enemy.all_sunk():
                print("You sank the entire fleet. You win!")
                return

            ai_pos = self.ai.choose()

            if ai_pos is None:
                print("AI has no remaining choices.")
                return

            print(
                "AI fired at "
                f"{ai_pos[0] + 1},{ai_pos[1] + 1}"
            )

            ai_result = self.player.fire(ai_pos)

            if ai_result == "repeat":
                print("AI attempted a repeated shot.")

            elif ai_result == "miss":
                print("AI missed.")

            elif ai_result == "hit":
                print("AI scored a hit.")

            elif ai_result.startswith("sunk:"):
                ship_name = ai_result.split(":", 1)[1]
                print(f"AI sank your {ship_name}.")

            if self.player.all_sunk():
                print("The AI sank your entire fleet. You lose!")
                return