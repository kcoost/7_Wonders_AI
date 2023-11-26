import random
import torch
from abc import ABC, abstractmethod

random.seed(0)


class Player(ABC):
    @abstractmethod
    def __call__(self, input_tensor: torch.Tensor):
        return NotImplementedError


class RandomChoice(Player):
    def __call__(self, input_tensor: torch.Tensor):
        # 75 different cards
        # 2*7 possible trades, most expensive trade is 4 resources
        return torch.ones(75), torch.ones(14, 5), torch.ones(3)
