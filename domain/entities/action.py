from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
from typing import Optional

class ActionCost(Enum):
    REACTION = "r"
    FREE = "0"
    ACTION_1 = "1"
    ACTION_2 = "2"
    ACTION_3 = "3"
    # REACTION = "↶"
    # FREE = "▷"
    # ACTION_1 = "▶"
    # ACTION_2 = "▶▶"
    # ACTION_3 = "▶▶▶"


class ActionType(Enum):
    BASIC = "Basic"
    WEAPON = "Weapon"


@dataclass_json
@dataclass
class Action:
    name: str = "Unknown"
    description: str = "Unknown"
    type: Optional[ActionType] = None
    cost: Optional[ActionCost] = None
    focus: int = 0
    investiture: int = 0