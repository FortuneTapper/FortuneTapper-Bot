import discord
from discord.ext import commands
from discord import app_commands
from adapter.presenters import ActionPresenter
from domain.interactors import CharacterInteractor, NoCharacterError, ActionInteractor
from adapter import config as config

class ActionCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.presenter = ActionPresenter()
        self.action_interactor = ActionInteractor(repository=config.repository)
        self.character_interactor = CharacterInteractor(repository=config.repository, demiplane_url=config.DEMIPLANE_URL)


    @app_commands.command(name="actions", description="List the available actions")
    async def actions(
        self, 
        interaction: discord.Interaction,
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
        
        try:
            await interaction.response.defer()

            await self.presenter.list_actions(interaction, self.character_interactor.get_character(str(interaction.user.id), str(interaction.guild.id)))
        except NoCharacterError as e:
            config.logger.error(f"NoCharacterError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except Exception as e:
            config.logger.error(f"Unexpected error: {e}", exc_info=True)
            await interaction.followup.send("Unexpected error occurred.", ephemeral=True)

    @app_commands.command(name="action_show", description="List the available actions")
    async def action_show(
        self, 
        interaction: discord.Interaction,
        action: str
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
        
        try:
            await interaction.response.defer()

            await self.presenter.show_action(interaction, self.action_interactor.get_action(str(interaction.user.id), str(interaction.guild.id), action))
        except NoCharacterError as e:
            config.logger.error(f"NoCharacterError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except Exception as e:
            config.logger.error(f"Unexpected error: {e}", exc_info=True)
            await interaction.followup.send("Unexpected error occurred.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ActionCommand(bot))
