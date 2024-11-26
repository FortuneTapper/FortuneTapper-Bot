from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from enum import Enum

class ResourceType(Enum):
    HEALTH = "health"
    FOCUS = "focus"
    INVESTITURE = "investiture"

@dataclass_json
@dataclass
class Resource:
    max: int = 0,
    current: int = 0


@dataclass_json
@dataclass
class Resources:
    health: Resource = field(default_factory=Resource)
    focus: Resource = field(default_factory=Resource)
    investiture: Resource = field(default_factory=Resource)
    movement: int = 0
    recovery_die: int = 0
    senses_range: int = 0

    def get_resource_by_type(self, resource_type: ResourceType) -> Resource:
        return getattr(self, resource_type.value)