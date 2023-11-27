import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from pathlib import Path

from tqdm import tqdm
from seven_wonders import GameState, RandomChoice, PlayCard, AlexandriaA, AlexandriaB, EphesosA, EphesosB, GizaA, GizaB, RhodesA, RhodesB

# https://github.com/koulanurag/minimal-marl
# https://github.com/seungeunrho/minimalRL

torch.manual_seed(0)

LEARNING_RATE = 0.0002
GAMMA = 0.98

class Policy(nn.Module):
    def __init__(self):
        super().__init__()
        self.input = nn.Sequential(nn.Linear(483, 128), nn.ReLU(), nn.Linear(128, 128), nn.ReLU())
        self.card = nn.Linear(128, 75)
        #self.trade = nn.Linear(128, 14*5)
        self.action = nn.Linear(128, 3)

        self.optimizer = optim.Adam(self.parameters(), lr=LEARNING_RATE)

    def forward(self, input_tensor):
        x = self.input(input_tensor)
        c = self.card(x)
        #t = self.trade(x)
        trade_tensor = torch.ones(14, 5)
        trade_tensor[:, 1:] -= 1000
        a = self.action(x)
        # x = F.softmax(self.fc2(x), dim=0)
        return c, trade_tensor, a

    def train_net(self, probs_card, probs_action, rewards):
        R = 0
        self.optimizer.zero_grad()
        for prob_card, prob_action, reward in zip(probs_card[::-1], probs_action[::-1], rewards[::-1]):
            R = reward + GAMMA * R
            loss = -R * (torch.log(prob_card) + torch.log(prob_action))
            loss.backward()
        self.optimizer.step()

def main():
    alice_wins = 0

    policy = Policy()

    win_percentage = []

    progress_bar = tqdm(range(1, 30001))
    for n in progress_bar:
        Alice = AlexandriaA("Alice", policy)
        Bob = RhodesB("Bob", RandomChoice())
        Charlie = GizaB("Charlie", RandomChoice())

        game = GameState([Alice, Bob, Charlie])
        winner, probs_card, probs_action, rewards = game.play_game()

        Alice.player.train_net(probs_card, probs_action, rewards)

        if winner == "Alice":
            alice_wins += 1

        #if n % 20 == 19:
        progress_bar.set_description(f"Wins AI: {100*alice_wins/n:.01f}%")

        if n > 10:
            win_percentage.append(100*alice_wins/n)

    plt.plot(list(range(10, 30000)), win_percentage)
    plt.xlabel("Step")
    plt.ylabel("Win percentage")
    plt.savefig(Path(__file__).parent / "win_percentage.png")

if __name__ == "__main__":
    main()
