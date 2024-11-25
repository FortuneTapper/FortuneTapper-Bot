from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from enum import Enum

class SkillType(Enum):
    ATHLETICS = "athletics"
    AGILITY = "agility"
    HEAVY_WEAPONS = "heavy_weapons"
    LIGHT_WEAPONS = "light_weapons"
    STEALTH = "stealth"
    THIEVERY = "thievery"
    CRAFTING = "crafting"
    DEDUCTION = "deduction"
    DISCIPLINE = "discipline"
    INTIMIDATION = "intimidation"
    LORE = "lore"
    MEDICINE = "medicine"
    DECEPTION = "deception"
    INSIGHT = "insight"
    LEADERSHIP = "leadership"
    PERCEPTION = "perception"
    PERSUASION = "persuasion"
    SURVIVAL = "survival"

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

    def get_skill_by_type(self, skill_type: SkillType) -> Skill:
            return getattr(self, skill_type.value)