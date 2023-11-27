from .plays import Play
from .cities import City

LENGTH = 70
VERBOSITY = 0 #1

def pad_text(text: str, length=LENGTH):
    return f"## {text} " + max(0, length - len(text) - 4)*"#"

class GameLogger:
    def __init__(self):
        self.log_text = ""

    def log(self, texts: list[str]):
        concatenated_text = "\n".join(texts)
        if VERBOSITY > 1:
            print(concatenated_text)
        self.log_text += concatenated_text

    def start_game(self, cities: list[City]):
        texts = [LENGTH*"#"]
        texts.append(pad_text("Starting Game"))
        texts.append(LENGTH*"#")
        for i, city in enumerate(cities):
            city_name = city.__class__.__name__[:-1]
            texts.append(f"Player {i+1}: {city.name} playing as {city_name} (side {city.side})")
        texts.append(LENGTH*"#" + "\n")
        self.log(texts)

    def start_age(self, age: str):
        texts = [pad_text(f"Starting Age {age}")]
        texts.append(LENGTH*"#")
        self.log(texts)

    def start_turn(self, turn: int):
        texts = [pad_text(f"Starting Turn {turn}")]
        self.log(texts)

    def choose_play(self, name: str, play: Play):
        texts = [f"# {name} chooses to {play.action.value} {play.card}"]
        if play.spent_coins < 0:
            texts.append(f"at the cost of {-play.spent_coins} coins")
        else:
            texts.append(f"gaining {play.spent_coins}")
        texts.append(f"West trade: {play.trade_west}")
        texts.append(f"East trade: {play.trade_east}")
        self.log(texts)

    def military_battle(self, name: str, results: list[int]):
        texts = [f"# Results of {name} military battles"]
        for direction, result in zip(["west", "east"], results):
            if result == -1:
                text = f"Lost battle with {direction} city, losing 1 victory point"
            elif result > 0:
                text = f"Won battle with {direction} city, gaining {result} victory point"
                if result > 1:
                    text += "s"
            else:
                text = f"Drew battle with {direction} city, not gaining or losing any victory points"

            texts.append(text)

        self.log(texts)

    def game_results(self, name: str, score: int):
        self.log([f"{name} scored {score} victory points"])

    def winner(self, name: str, score: int):
        if VERBOSITY > 0:
            print(f"{name} won the game, having scored {score} victory points!")
        else:
            self.log([f"{name} won the game, having scored {score} victory points!"])

    def dump(self, path):
        with open(path, "w") as file:
            file.write(self.log_text)
