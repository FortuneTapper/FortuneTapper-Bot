import discord
from domain.entities import ResourceType

class ResourcePresenter:

    def circle_display(self, current, maximum):
            filled = '●' * int(current)
            empty = '○' * (int(maximum) - int(current))
            return filled + empty

    async def resource(self, interaction: discord.Interaction, resource : ResourceType):
        embed = discord.Embed(
            title=f"Modifying {resource.value}",
            description=self.circle_display(resource.current, resource.max),
            color=discord.Color.gold()
        )

        await interaction.followup.send(embed=embed)