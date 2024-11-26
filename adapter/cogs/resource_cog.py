import discord
from discord.ext import commands
from discord import app_commands
from domain.entities import ResourceType
from adapter.presenters import ResourcePresenter
from domain.interactors import ResourceInteractor, NoCharacterError
from adapter import config as config

class ResourceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.presenter = ResourcePresenter()
        self.interactor = ResourceInteractor(repository=config.repository)

    async def _resource(
        self, 
        interaction: discord.Interaction, 
        resource: ResourceType, 
        value: str
    ):
        try:
            await interaction.response.defer()

            if value.startswith(('+', '-')):
                result = self.interactor.modify_current_resource(
                    user_id=str(interaction.user.id),
                    guild_id=str(interaction.guild.id),
                    resource=resource,
                    amount=int(value)
                )
            else:
                result = self.interactor.set_current_resource(
                    user_id=str(interaction.user.id),
                    guild_id=str(interaction.guild.id),
                    resource=resource,
                    amount=int(value)
                )

            await self.presenter.resource(
                interaction=interaction,
                resource=result,
                resource_type=resource
            )
        except NoCharacterError as e:
            config.logger.error(f"NoCharacterError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except Exception as e:
            config.logger.error(f"Unexpected error: {e}", exc_info=True)
            await interaction.followup.send("Unexpected error occurred.", ephemeral=True)


    @app_commands.command(name="health", description="Manages health")
    @app_commands.describe(
        value = "Value to set or modify. Use +X or -X to modify, or X to set."
    )
    async def health(
        self, 
        interaction: discord.Interaction, 
        value: str
    ):
        config.logger.info({
            'event': 'health',
            'user': str(interaction.user),
            'user_id': interaction.user.id,
            'guild': interaction.guild.name if interaction.guild else "DM",
            'guild_id': interaction.guild.id if interaction.guild else None,
            'channel': interaction.channel.name if interaction.channel else "Unknown",
            'channel_id': interaction.channel.id if interaction.channel else None,
        })
        
        await self._resource(interaction, ResourceType.HEALTH, value)

    @app_commands.command(name="focus", description="Manages focus")
    @app_commands.describe(
        value = "Value to set or modify. Use +X or -X to modify, or X to set."
    )
    async def focus(
        self, 
        interaction: discord.Interaction, 
        value: str
    ):
        config.logger.info({
            'event': 'focus',
            'user': str(interaction.user),
            'user_id': interaction.user.id,
            'guild': interaction.guild.name if interaction.guild else "DM",
            'guild_id': interaction.guild.id if interaction.guild else None,
            'channel': interaction.channel.name if interaction.channel else "Unknown",
            'channel_id': interaction.channel.id if interaction.channel else None,
        })
        
        await self._resource(interaction, ResourceType.FOCUS, value)

    @app_commands.command(name="investiture", description="Manages investiture")
    @app_commands.describe(
        value = "Value to set or modify. Use +X or -X to modify, or X to set."
    )
    async def investiture(
        self, 
        interaction: discord.Interaction, 
        value: str
    ):
        config.logger.info({
            'event': 'investiture',
            'user': str(interaction.user),
            'user_id': interaction.user.id,
            'guild': interaction.guild.name if interaction.guild else "DM",
            'guild_id': interaction.guild.id if interaction.guild else None,
            'channel': interaction.channel.name if interaction.channel else "Unknown",
            'channel_id': interaction.channel.id if interaction.channel else None,
        })
        
        await self._resource(interaction, ResourceType.INVESTITURE, value)

async def setup(bot):
    await bot.add_cog(ResourceCommand(bot))
