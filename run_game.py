from pathlib import Path
from seven_wonders import GameState, RandomChoice, AlexandriaA, AlexandriaB, EphesosA, EphesosB, GizaA, GizaB, RhodesA, RhodesB


if __name__ == "__main__":
    Alice = AlexandriaA("Alice", RandomChoice())
    Bob = RhodesB("Bob", RandomChoice())
    Charlie = GizaB("Charlie", RandomChoice())

    game = GameState([Alice, Bob, Charlie])
    game.play_game()
    game.logger.dump(Path(__file__).parent / "game_log.txt")
