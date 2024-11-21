from dataclasses import dataclass, field
from typing import List, Optional
from dataclasses_json import dataclass_json
from enum import Enum


@dataclass_json
@dataclass
class Attributes:
    strength: int = 0
    speed: int = 0
    intellect: int = 0
    willpower: int = 0
    awareness: int = 0
    presence: int = 0


@dataclass_json
@dataclass
class Defenses:
    physical: int = 0
    cognitive: int = 0
    spiritual: int = 0
    deflect: int = 0


@dataclass_json
@dataclass
class Resources:
    health: int = 0
    health_max: int = 0
    focus: int = 0
    focus_max: int = 0
    investiture: int = 0
    investiture_max: int = 0
    movement: int = 0
    recovery_die: int = 0
    senses_range: int = 0


@dataclass_json
@dataclass
class Skill:
    proficiency: int = 0
    modifier: int = 0


@dataclass_json
@dataclass
class Skills:
    athletics: Skill = field(default_factory=Skill)
    agility: Skill = field(default_factory=Skill)
    heavy_weapons: Skill = field(default_factory=Skill)
    light_weapons: Skill = field(default_factory=Skill)
    stealth: Skill = field(default_factory=Skill)
    thievery: Skill = field(default_factory=Skill)
    crafting: Skill = field(default_factory=Skill)
    deduction: Skill = field(default_factory=Skill)
    discipline: Skill = field(default_factory=Skill)
    intimidation: Skill = field(default_factory=Skill)
    lore: Skill = field(default_factory=Skill)
    medicine: Skill = field(default_factory=Skill)
    deception: Skill = field(default_factory=Skill)
    insight: Skill = field(default_factory=Skill)
    leadership: Skill = field(default_factory=Skill)
    perception: Skill = field(default_factory=Skill)
    persuasion: Skill = field(default_factory=Skill)
    survival: Skill = field(default_factory=Skill)


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


@dataclass_json
@dataclass
class Character:
    character_id: str = "Unknown"
    avatar: str = "Unknown"
    name: str = "Unknown"
    ancestry: str = "Unknown"
    paths: List[str] = field(default_factory=list)
    attributes: Attributes = field(default_factory=Attributes)
    defenses: Defenses = field(default_factory=Defenses)
    resources: Resources = field(default_factory=Resources)
    skills: Skills = field(default_factory=Skills)
    expertises: List[str] = field(default_factory=list)
    actions: List[Action] = field(default_factory=list)
    equipament: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
