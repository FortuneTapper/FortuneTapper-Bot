import discord
from domain.entities import Resource, ResourceType

class ResourcePresenter:

    def circle_display(self, current, maximum):
            filled = '●' * int(current)
            empty = '○' * (int(maximum) - int(current))
            return filled + empty

    async def resource(self, interaction: discord.Interaction, resource : Resource, resource_type : ResourceType):
        embed = discord.Embed(
            title=f"Modifying {resource_type.value}",
            description=f"{resource.current}/{resource.max}",
            color=discord.Color.gold()
        )
        embed.add_field(name="", value=self.circle_display(resource.current, resource.max))

        await interaction.followup.send(embed=embed)