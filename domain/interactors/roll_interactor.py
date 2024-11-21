import d20
import re
from domain.entities.roll_result import PlotDieResult, PlotDieResultType, AdvantageType, SkillTestResult, AttackResult, DamageRollResult


def roll(expr: str) -> d20.RollResult:
    return d20.roll(expr)

def expr_with_advantage(expr: str, advantage: AdvantageType) -> str:
    assert re.fullmatch(r'\d+d\d+', expr) # Format XdY

    dice_sides = int(expr.split("d")[1])
    dice_number = int(expr.split("d")[0])

    if advantage == AdvantageType.ADVANTAGE:
        if (dice_number > 1):
            return f'2d{dice_sides}kh1+{dice_number-1}d{dice_sides}'
        else:
            return f'2d{dice_sides}kh1'
    elif advantage == AdvantageType.DISADVANTAGE:
        if (dice_number > 1):
            return f'2d{dice_sides}kl1+{dice_number-1}d{dice_sides}'
        else:
            return f'2d{dice_sides}kl1'
    else:
        return expr

def plot_roll(advantage: AdvantageType = AdvantageType.NONE) -> PlotDieResult:
    die_result = d20.roll(expr_with_advantage('1d6', advantage))

    if (die_result.total <= 2):
        return PlotDieResult(die_result, PlotDieResultType.COMPLICATION, die_result.total*2)
    elif (die_result.total >= 5):
        return PlotDieResult(die_result, PlotDieResultType.OPPORTUNITY)
    else:
        return PlotDieResult(die_result, PlotDieResultType.NONE)


def skill_test(
        expr: str = '1d20',
        modifier: int = 0, 
        advantage: AdvantageType = AdvantageType.NONE, 
        plot_die: bool = False, 
        plot_advantage: AdvantageType = AdvantageType.NONE
) -> SkillTestResult:

    skill_expr = f'{expr_with_advantage(expr, advantage)}+{modifier}'

    plot_result = None
    if (plot_die):
        plot_result = plot_roll(advantage=plot_advantage)
        skill_expr = f'{skill_expr}+{plot_result.plus}'

    return SkillTestResult(
        roll_result = d20.roll(skill_expr),
        plot_die_result = plot_result
    )
    

def attack_roll(
        damage_expr: str, 
        modifier: int = 0, 
        advantage: AdvantageType = AdvantageType.NONE,
        damage_advantage: AdvantageType = AdvantageType.NONE, 
        plot_die: bool = False, 
        plot_advantage: AdvantageType = AdvantageType.NONE,
        plot_die_damage = False,
) -> AttackResult:
    assert re.fullmatch(r'\d+d\d+', damage_expr) # Format XdY
    
    addition = modifier
    damage_expr_with_modifiers  = f'{expr_with_advantage(damage_expr, damage_advantage)}+{modifier}'

    plot_result = None
    if (plot_die and plot_die_damage):
        plot_result = plot_roll(advantage=plot_advantage)
        damage_expr_with_modifiers  = f'{damage_expr_with_modifiers}+{plot_result.plus}'
        addition = addition + plot_result.plus

    damage_result = d20.roll(damage_expr_with_modifiers)

    return AttackResult(
        hit_result = skill_test(modifier=modifier, advantage=advantage, plot_die=plot_die and not plot_die_damage, plot_advantage=plot_advantage),
        damage_result = DamageRollResult(
            roll_result = damage_result,
            graze = damage_result.total - addition,
            critical = int(damage_expr.split('d')[0]) * int(damage_expr.split('d')[1]) + addition, 
            plot_die_result = plot_result
        )
    )
