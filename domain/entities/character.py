from dataclasses import dataclass, field
from typing import List
from dataclasses_json import dataclass_json
from domain.entities.resource import Resources
from domain.entities.skill import Skills
from domain.entities.action import Actions


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
    actions: Actions = field(default_factory=list)
    equipament: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
