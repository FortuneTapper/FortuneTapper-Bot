from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from enum import Enum
from typing import List, Optional

class ActionCost(Enum):
    REACTION = "r"
    FREE = "0"
    ACTION_1 = "1"
    ACTION_2 = "2"
    ACTION_3 = "3"

    def get_symbol(self):
        symbols = {
            "r": "↶",
            "0": "▷",
            "1": "▶",
            "2": "▶▶",
            "3": "▶▶▶"
        }

        return symbols[self.value]

class ActionType(Enum):
    BASIC = "basic"
    WEAPON = "weapon"


@dataclass_json
@dataclass
class Action:
    name: str = "Unknown"
    description: str = "Unknown"
    type: ActionType = ActionType.BASIC
    cost: ActionCost = ActionCost.FREE
    dice: Optional[str] = None
    focus: Optional[int] = None
    investiture: Optional[int] = None

@dataclass_json
@dataclass
class Actions:
    basic: List[Action] = field(default_factory=list)
    weapon: List[Action] = field(default_factory=list)
    stormlight: List[Action] =field(default_factory=list)


