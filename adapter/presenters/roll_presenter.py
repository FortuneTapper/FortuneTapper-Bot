import discord
import d20
from domain.entities.roll_result import SkillTestResult, AttackResult, PlotDieResultType

class RollPresenter:

    async def roll(self, interaction: discord.Interaction, roll_result: d20.RollResult, title : str = "Tapping Fortune 🎲"):
        embed = discord.Embed(
            title=title,
            description=f"**Result:** {roll_result}",
            color=discord.Color.gold()
        )

        await interaction.followup.send(embed=embed)

    async def skill_test(self, interaction: discord.Interaction, skill_result: SkillTestResult, skill : str = "Fortune"):
        color = discord.Color.gold()
        if skill_result.plot_die_result:
            if skill_result.plot_die_result.type == PlotDieResultType.OPPORTUNITY:
                color = discord.Color.blue()
            elif skill_result.plot_die_result.type == PlotDieResultType.COMPLICATION:
                color = discord.Color.red()

        embed = discord.Embed(
            title=f"Tapping {skill} 🎲",
            description=f"**Result:** {skill_result.roll_result}",
            color=color
        )
        if skill_result.plot_die_result:
            embed.add_field(name=f'Plot die: {skill_result.plot_die_result.type.value}', value=skill_result.plot_die_result.roll_result.result, inline = False)

        await interaction.followup.send(embed=embed)

    async def attack(self, interaction: discord.Interaction, attack_result: AttackResult, weapon : str = "Unknown"):
        color = discord.Color.gold()

        if attack_result.hit_result.plot_die_result:
            if attack_result.hit_result.plot_die_result.type == PlotDieResultType.OPPORTUNITY:
                color = discord.Color.blue()
            elif attack_result.hit_result.plot_die_result.type == PlotDieResultType.COMPLICATION:
                color = discord.Color.red()
        elif attack_result.damage_result.plot_die_result:
            if attack_result.damage_result.plot_die_result.type == PlotDieResultType.OPPORTUNITY:
                color = discord.Color.blue()
            elif attack_result.damage_result.plot_die_result.type == PlotDieResultType.COMPLICATION:
                color = discord.Color.red()

        embed = discord.Embed(
            title=f"Attack ({weapon}) 🎲",
            description=f"**To hit:** {attack_result.hit_result.roll_result}",
            color=color
        )
        embed.add_field(name=f'Damage', value=f'{attack_result.damage_result.roll_result}')
        embed.add_field(name=f'Graze', value=f'{attack_result.damage_result.graze}')
        embed.add_field(name=f'Critical', value=f'{attack_result.damage_result.critical}')
        if attack_result.hit_result.plot_die_result:
             embed.add_field(
                name=f'Plot die (attack): {attack_result.hit_result.plot_die_result.type.value}', 
                value=attack_result.hit_result.plot_die_result.roll_result.result, inline = False
            )
        elif attack_result.damage_result.plot_die_result:
            embed.add_field(
                name=f'Plot die (damage): {attack_result.damage_result.plot_die_result.type.value}', 
                value=attack_result.damage_result.plot_die_result.roll_result.result, inline = False
            )

        await interaction.followup.send(embed=embed)
