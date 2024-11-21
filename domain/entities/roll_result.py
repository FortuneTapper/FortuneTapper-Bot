from dataclasses import dataclass
from enum import Enum
from typing import Optional
import d20

class PlotDieResultType(Enum):
    OPPORTUNITY = "Opportunity"
    COMPLICATION = "Complication"
    NONE = "None"

class AdvantageType(Enum):
    ADVANTAGE = "Advantage"
    DISADVANTAGE = "Disadvantage"
    NONE = "None"

@dataclass
class PlotDieResult:
    roll_result: d20.RollResult
    type: PlotDieResultType
    plus: int = 0

@dataclass
class SkillTestResult:
    roll_result: d20.RollResult
    plot_die_result: Optional[PlotDieResult]

@dataclass
class DamageRollResult:
    roll_result: d20.RollResult
    graze: int
    critical: int
    plot_die_result: Optional[PlotDieResult]

@dataclass
class AttackResult:
    hit_result: SkillTestResult
    damage_result: DamageRollResult
