from dataclasses import dataclass, asdict
import torch
from enum import Enum

class Action(Enum):
    play_card: str = "play"
    stage_wonder: str = "stage a wonder using"
    discard: str = "discard"
