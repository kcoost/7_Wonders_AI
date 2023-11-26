from .plays import Play
from .cities import City

LENGTH = 70

def pad_text(text: str, length=LENGTH):
    return f"## {text} " + max(0, length - len(text) - 4)*"#"


class GameLogger:
    def __init__(self):
        self.log_text = ""

    def log(self, texts: list[str]):
        concatenated_text = "\n".join(texts)
        print(concatenated_text)
        self.log_text += concatenated_text

    def start_game(self, cities: list[City]):
        texts = [LENGTH*"#"]
        texts.append(pad_text("Starting Game"))
        texts.append(LENGTH*"#")
        for i, city in enumerate(cities):
            city_name = city.__class__.__name__[:-1]
            texts.append(f"Player {i}: {city.name} playing as {city_name} (side {city.side})")
        texts.append(LENGTH*"#" + "\n")
        self.log(texts)

    def start_age(self, age: str):
        texts = [pad_text(f"Starting Age {age}")]
        texts.append(LENGTH*"#")
        self.log(texts)

    def start_turn(self, turn: int):
        texts = [pad_text(f"Starting turn {turn}")]
        self.log(texts)

    def choose_play(self, name: str, play: Play):
        texts = [f"# {name} chooses to play"]
        texts.append(f"Card: {play.card}")
        texts.append(f"{play.trade}")
        texts.append(play.action.value)
        self.log(texts)

    def military_battle(self, name: str, results: list[int]):
        texts = [f"# Results of {name} military battles"]
        for direction, result in zip(["west", "east"], results):
            if result == -1:
                text = f"Lost battle with {direction} city, losing 1 victory point"
            else:
                text = f"Lost battle with {direction} city, losing {result} victory point"
                if result > 1:
                    text += "s"
            texts.append(text)

        self.log(texts)

    def game_results(self, name: str, score: int):
        self.log([f"{name} scored {score} victory points"])

    def winner(self, name: str):
        self.log([f"{name} won the game!"])

    def dump(self, path):
        with open(path) as file:
            file.write(self.log_text)
