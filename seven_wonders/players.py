import random
import torch
from abc import ABC, abstractmethod

#random.seed(0)


class Player(ABC):
    @abstractmethod
    def __call__(self, input_tensor: torch.Tensor):
        return NotImplementedError


class RandomChoice(Player):
    def __call__(self, input_tensor: torch.Tensor):
        # 75 different cards
        # 2*7 possible trades, most expensive trade is 4 resources
        return torch.ones(75), torch.ones(14, 5), torch.ones(3)

class PlayCard(Player):
    def __call__(self, input_tensor: torch.Tensor):
        print(input_tensor.shape)
        card_tensor = torch.ones(75)
        trade_tensor = torch.ones(14, 5)
        trade_tensor[:, 1:] /= 1000
        action_tensor = torch.ones(3)
        action_tensor[1:] /= 1000
        return card_tensor, trade_tensor, action_tensor