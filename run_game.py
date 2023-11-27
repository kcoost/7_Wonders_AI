from pathlib import Path
from seven_wonders import GameState, RandomChoice, PlayCard, AlexandriaA, AlexandriaB, EphesosA, EphesosB, GizaA, GizaB, RhodesA, RhodesB

# https://github.com/koulanurag/minimal-marl
# https://github.com/seungeunrho/minimalRL

if __name__ == "__main__":
    alice_wins = 0
    bob_wins = 0
    charlie_wins = 0
    for i in range(1, 10000):
        Alice = AlexandriaA("Alice", PlayCard())
        Bob = RhodesB("Bob", RandomChoice())
        Charlie = GizaB("Charlie", RandomChoice())

        game = GameState([Alice, Bob, Charlie])
        winner = game.play_game()
        # game.logger.dump(Path(__file__).parent / "game_log.txt")

        if winner == "Alice":
            alice_wins += 1
        if winner == "Bob":
            bob_wins += 1
        if winner == "Charlie":
            charlie_wins += 1

        if i % 100 == 99:
            print(f"Wins: Alice {100*alice_wins/i:.01f}, Bob {100*bob_wins/i:.01f}, Charlie {100*charlie_wins/i:.01f}")
