import discord
import d20

class RollPresenter:
    interaction: discord.Interaction

    def __init__(self, interaction: discord.Interaction):
        self.interaction = interaction

    async def roll(self, roll_result: d20.RollResult, title : str = "Tapping Fortune 🎲"):
        embed = discord.Embed(
            title=title,
            description=f"**Result:** {roll_result}",
            color=discord.Color.gold()
        )

        await self.interaction.response.send_message(embed=embed)
