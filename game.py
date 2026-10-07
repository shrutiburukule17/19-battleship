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
            {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)},
        )

        self.player.place_ship(
            "Battleship",
            {(2, 0), (3, 0), (4, 0), (5, 0)},
        )

        self.player.place_ship(
            "Cruiser",
            {(2, 2), (2, 3), (2, 4)},
        )

        self.player.place_ship(
            "Submarine",
            {(4, 2), (4, 3), (4, 4)},
        )

        self.player.place_ship(
            "Destroyer",
            {(1, 5), (2, 5)},
        )

        self.enemy.place_ship(
            "Carrier",
            {(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)},
        )

        self.enemy.place_ship(
            "Battleship",
            {(0, 3), (1, 3), (2, 3), (3, 3)},
        )

        self.enemy.place_ship(
            "Cruiser",
            {(4, 3), (4, 4), (4, 5)},
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
            {(5, 0), (5, 1)},
        )

    def show(self):
        print("\n" + "=" * 40)
        print("BATTLESHIP")
        print("=" * 40)

        print("\nYour shots are entered as row,column.")
        print("Example: 2,3")
        print("Type q to quit.")

        print(
            "\nEnemy ship cells remaining:",
            self.enemy.remaining_cells(),
        )

        print("\nEnemy fleet status:")

        for name, info in self.enemy.ship_status().items():
            if info["sunk"]:
                state = "SUNK"
            else:
                state = f"{info['hits']}/{info['size']} hits"

            print(f"  {name}: {state}")

    def get_player_shot(self):
        raw = input("\nYour shot > ").strip().lower()

        if raw == "q":
            return "quit", None

        try:
            r, c = map(int, raw.split(","))
        except ValueError:
            print("Invalid coordinate. Use row,column, for example 2,3.")
            return "invalid", None

        pos = (r - 1, c - 1)

        if not (
            0 <= pos[0] < Board.SIZE
            and 0 <= pos[1] < Board.SIZE
        ):
            print(
                f"Outside board. Use rows and columns from "
                f"1 to {Board.SIZE}."
            )
            return "invalid", None

        return "valid", pos

    def handle_player_shot(self, pos):
        result = self.enemy.fire(pos)

        if result == "repeat":
            print("Already fired there.")
            return False

        if result == "miss":
            print("MISS!")

        elif result == "hit":
            print("HIT!")

        elif result.startswith("sunk:"):
            ship_name = result.split(":", 1)[1]
            print(f"HIT! You sank the {ship_name}.")

        return True

    def handle_ai_turn(self):
        ai_pos = self.ai.choose()

        if ai_pos is None:
            print("AI has no remaining choices.")
            return False

        row = ai_pos[0] + 1
        column = ai_pos[1] + 1

        print(f"\nAI fired at {row},{column}")

        result = self.player.fire(ai_pos)

        if result == "miss":
            print("AI MISS!")

        elif result == "hit":
            print("AI HIT!")

        elif result.startswith("sunk:"):
            ship_name = result.split(":", 1)[1]
            print(f"AI HIT! It sank your {ship_name}.")

        self.ai.register_result(ai_pos, result)

        return True

    def run(self):
        print("\nWelcome to Battleship!")

        while True:
            self.show()

            status, pos = self.get_player_shot()

            if status == "quit":
                print("Goodbye!")
                return

            if status == "invalid":
                continue

            if not self.handle_player_shot(pos):
                continue

            if self.enemy.all_sunk():
                print("\nYou sank the entire enemy fleet!")
                print("YOU WIN!")
                return

            if not self.handle_ai_turn():
                print("The AI has no legal shots remaining.")
                return

            if self.player.all_sunk():
                print("\nThe AI sank your entire fleet.")
                print("YOU LOSE!")
                return