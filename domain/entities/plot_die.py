from dataclasses import dataclass
from enum import Enum
from typing import Optional
import d20

def roll():
    die_result = d20.roll("1d6").total

    result: PlotDieResult
    if (die_result <= 2):
        result = PlotDieResult(PlotDieResultType.COMPLICATION, die_result*2)
    elif (die_result >= 5):
        result = PlotDieResult(PlotDieResultType.OPPORTUNITY)
    else:
        result = PlotDieResult(PlotDieResultType.NOTHING)

    return result

class PlotDieResultType(Enum):
    OPPORTUNITY = "Opportunity"
    COMPLICATION = "Complication"
    NOTHING = "Nothing"

@dataclass
class PlotDieResult:
    result: PlotDieResultType  # Puede ser OPPORTUNITY, COMPLICATION, o NOTHING
    plus: Optional[int] = 0  # Puede ser None, 2, o 4 en caso de complicación