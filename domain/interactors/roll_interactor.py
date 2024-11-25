import d20
import re
from domain.entities.roll_result import PlotDieResult, PlotDieResultType, AdvantageType, SkillTestResult, AttackResult, DamageRollResult
from domain.entities import SkillType, Character
from adapter.gateways.character_repository.caching_character_repository import CachingCharacterRepository

class RollInteractor:
    def __init__(self, repository: CachingCharacterRepository):
        self.repository = repository

    def roll(self, expr: str) -> d20.RollResult:
        return d20.roll(expr)

    def expr_with_advantage(self, expr: str, advantage: AdvantageType) -> str:
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

    def plot_roll(self, advantage: AdvantageType = AdvantageType.NONE) -> PlotDieResult:
        die_result = d20.roll(self.expr_with_advantage('1d6', advantage))

        if (die_result.total <= 2):
            return PlotDieResult(die_result, PlotDieResultType.COMPLICATION, die_result.total*2)
        elif (die_result.total >= 5):
            return PlotDieResult(die_result, PlotDieResultType.OPPORTUNITY)
        else:
            return PlotDieResult(die_result, PlotDieResultType.NONE)

    def roll_test(self, 
            expr: str = '1d20',
            modifier: int = 0, 
            advantage: AdvantageType = AdvantageType.NONE, 
            plot_die: bool = False, 
            plot_advantage: AdvantageType = AdvantageType.NONE
    ) -> SkillTestResult:

        skill_expr = f'{self.expr_with_advantage(expr, advantage)}+{modifier}'

        plot_result = None
        if (plot_die):
            plot_result = self.plot_roll(advantage=plot_advantage)
            skill_expr = f'{skill_expr}+{plot_result.plus}'

        return SkillTestResult(
            roll_result = d20.roll(skill_expr),
            plot_die_result = plot_result
        )

    def skill_test(
        self, 
        user_id, 
        guild_id, 
        skill: SkillType, 
        advantage: AdvantageType = AdvantageType.NONE, 
        plot_die: bool = False, 
        plot_advantage: AdvantageType = AdvantageType.NONE
    ) -> SkillTestResult:
        return self.roll_test(
            modifier = self.repository.get(user_id, guild_id).skills.get_skill_by_type(skill).modifier,
            advantage = advantage,
            plot_die = plot_die,
            plot_advantage = plot_advantage
        )
        

    def attack_roll(self, user_id, guild_id,
            damage_expr: str, 
            skill: SkillType, 
            advantage: AdvantageType = AdvantageType.NONE,
            damage_advantage: AdvantageType = AdvantageType.NONE, 
            plot_die: bool = False, 
            plot_advantage: AdvantageType = AdvantageType.NONE,
            plot_die_damage = False,
    ) -> AttackResult:
        assert re.fullmatch(r'\d+d\d+', damage_expr) # Format XdY
        
        addition = self.repository.get(user_id, guild_id).skills.get_skill_by_type(skill).modifier
        damage_expr_with_modifiers  = f'{self.expr_with_advantage(damage_expr, damage_advantage)}+{addition}'

        plot_result = None
        if (plot_die and plot_die_damage):
            plot_result = self.plot_roll(advantage=plot_advantage)
            damage_expr_with_modifiers  = f'{damage_expr_with_modifiers}+{plot_result.plus}'
            addition = addition + plot_result.plus

        damage_result = d20.roll(damage_expr_with_modifiers)

        return AttackResult(
            hit_result = self.skill_test(
                user_id=user_id, 
                guild_id=guild_id,
                skill=skill, 
                advantage=advantage, 
                plot_die=plot_die and not plot_die_damage, 
                plot_advantage=plot_advantage
            ),
            damage_result = DamageRollResult(
                roll_result = damage_result,
                graze = damage_result.total - addition,
                critical = int(damage_expr.split('d')[0]) * int(damage_expr.split('d')[1]) + addition, 
                plot_die_result = plot_result
            )
        )
