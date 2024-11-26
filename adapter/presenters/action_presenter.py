import discord
from domain.entities import Character, Action

class ActionPresenter:

    async def list_actions(self, interaction: discord.Interaction, character: Character):
        embed = discord.Embed(
            title=f"Available actions for {character.name}",
            description=f"",
            color=discord.Color.gold()
        )
        if len(character.actions.basic) > 0:
            embed.add_field(name=f"**Basic Actions**", value="", inline=False)
            for action in character.actions.basic:
                embed.add_field(name="", value=f"{action.name} {action.cost.get_symbol()}")

        await interaction.followup.send(embed=embed)

    async def show_action(self, interaction: discord.Interaction, action: Action):
        embed = discord.Embed(
            title=f"Action {action.name} {action.cost.get_symbol()}",
            description=f"{action.description}",
            color=discord.Color.gold()
        )
        embed.add_field(name="Dice", value=f"{action.dice}")
        embed.add_field(name="Focus Cost", value=f"{action.focus}")
        embed.add_field(name="Investiture Cost", value=f"{action.investiture}")

        await interaction.followup.send(embed=embed)