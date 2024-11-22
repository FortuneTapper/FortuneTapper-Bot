# import_cog.py

import discord
from discord.ext import commands
from discord import app_commands
from adapter.presenters.character_presenter import CharacterPresenter
from domain.interactors import character_interactor
from adapter import config as config
from domain.interactors.exceptions import NoCharacterError, CharacterImportError

class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="import", description="Imports a character from Demiplane URL")
    async def import_character(self, interaction: discord.Interaction, url: str):
        config.logger.info({
            'event': 'func',
            'user': str(interaction.user), 
            'user_id': interaction.user.id,
            'guild': interaction.guild.name if interaction.guild else "DM",
            'guild_id': interaction.guild.id if interaction.guild else None,
            'channel': interaction.channel.name if interaction.channel else "Unknown",
            'channel_id': interaction.channel.id if interaction.channel else None,
        })

        try:
            await interaction.response.defer()

            await CharacterPresenter(interaction).character(
                await character_interactor.import_character(
                    url, 
                    str(interaction.user.id), 
                    str(interaction.guild.id)
                )
            )
        except CharacterImportError as e:
            config.logger.error(f"CharacterImportError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except NoCharacterError as e:
            config.logger.error(f"NoCharacterError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except Exception as e:
            config.logger.error(f"Unexpected error: {e}", exc_info=True)
            await interaction.followup.send("Unexpected error occurred.", ephemeral=True)
        


    @app_commands.command(name="update", description="Updates a character from Demiplane sheet")
    async def update(self, interaction: discord.Interaction):
        config.logger.info({
            'event': 'update',
            'user': str(interaction.user),
            'user_id': interaction.user.id,
            'guild': interaction.guild.name if interaction.guild else "DM",
            'guild_id': interaction.guild.id if interaction.guild else None,
            'channel': interaction.channel.name if interaction.channel else "Unknown",
            'channel_id': interaction.channel.id if interaction.channel else None,
        })

        try:
            await interaction.response.defer()

            await CharacterPresenter(interaction).character(
                await character_interactor.update_character(
                    str(interaction.user.id), 
                    str(interaction.guild.id)
                )
            )
        except CharacterImportError as e:
            config.logger.error(f"CharacterImportError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except NoCharacterError as e:
            config.logger.error(f"NoCharacterError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except Exception as e:
            config.logger.error(f"Unexpected error: {e}", exc_info=True)
            await interaction.followup.send("Unexpected error occurred.", ephemeral=True)

        


    @app_commands.command(name="chararacter", description="Shows summary of a character")
    async def character(self, interaction: discord.Interaction):
        config.logger.info({
            'event': 'character',
            'user': str(interaction.user),
            'user_id': interaction.user.id,
            'guild': interaction.guild.name if interaction.guild else "DM",
            'guild_id': interaction.guild.id if interaction.guild else None,
            'channel': interaction.channel.name if interaction.channel else "Unknown",
            'channel_id': interaction.channel.id if interaction.channel else None,
        })

        try:
            await interaction.response.defer()

            await CharacterPresenter(interaction).character(
                character_interactor.get_character(
                    str(interaction.user.id), 
                    str(interaction.guild.id)
                )
            )
        except CharacterImportError as e:
            config.logger.error(f"CharacterImportError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except NoCharacterError as e:
            config.logger.error(f"NoCharacterError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except Exception as e:
            config.logger.error(f"Unexpected error: {e}", exc_info=True)
            await interaction.followup.send("Unexpected error occurred.", ephemeral=True)

        


    @app_commands.command(name="sheet", description="Shows whole sheet of a character")
    async def sheet(self, interaction: discord.Interaction):
        config.logger.info({
            'event': 'sheet',
            'user': str(interaction.user),
            'user_id': interaction.user.id,
            'guild': interaction.guild.name if interaction.guild else "DM",
            'guild_id': interaction.guild.id if interaction.guild else None,
            'channel': interaction.channel.name if interaction.channel else "Unknown",
            'channel_id': interaction.channel.id if interaction.channel else None,
        })

        try:
            await interaction.response.defer()

            await CharacterPresenter(interaction).sheet(
                character_interactor.get_character(
                    str(interaction.user.id), 
                    str(interaction.guild.id)
                )
            )
        except CharacterImportError as e:
            config.logger.error(f"CharacterImportError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except NoCharacterError as e:
            config.logger.error(f"NoCharacterError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except Exception as e:
            config.logger.error(f"Unexpected error: {e}", exc_info=True)
            await interaction.followup.send("Unexpected error occurred.", ephemeral=True)

        


    @app_commands.command(name="list", description="Shows the list of characters imported")
    async def list_characters(self, interaction: discord.Interaction):
        config.logger.info({
            'event': 'list',
            'user': str(interaction.user),
            'user_id': interaction.user.id,
            'guild': interaction.guild.name if interaction.guild else "DM",
            'guild_id': interaction.guild.id if interaction.guild else None,
            'channel': interaction.channel.name if interaction.channel else "Unknown",
            'channel_id': interaction.channel.id if interaction.channel else None,
        })

        try:
            await interaction.response.defer()

            await CharacterPresenter(interaction).list(
                character_interactor.get_character_list(
                    str(interaction.user.id), 
                    str(interaction.guild.id)
                )
            )
        except CharacterImportError as e:
            config.logger.error(f"CharacterImportError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except NoCharacterError as e:
            config.logger.error(f"NoCharacterError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except Exception as e:
            config.logger.error(f"Unexpected error: {e}", exc_info=True)
            await interaction.followup.send("Unexpected error occurred.", ephemeral=True)
        
        

    @app_commands.command(name="select", description="Selects one character from the list of available characters")
    async def select(self, interaction: discord.Interaction, character_id: str):
        config.logger.info({
            'event': 'select',
            'user': str(interaction.user),
            'user_id': interaction.user.id,
            'guild': interaction.guild.name if interaction.guild else "DM",
            'guild_id': interaction.guild.id if interaction.guild else None,
            'channel': interaction.channel.name if interaction.channel else "Unknown",
            'channel_id': interaction.channel.id if interaction.channel else None,
        })

        try:
            await interaction.response.defer()

            await CharacterPresenter(interaction).character(
                character_interactor.select_character(
                    str(interaction.user.id), 
                    str(interaction.guild.id),
                    character_id
                )
            )
        except CharacterImportError as e:
            config.logger.error(f"CharacterImportError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except NoCharacterError as e:
            config.logger.error(f"NoCharacterError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except Exception as e:
            config.logger.error(f"Unexpected error: {e}", exc_info=True)
            await interaction.followup.send("Unexpected error occurred.", ephemeral=True)
            
        



async def setup(bot):
    await bot.add_cog(Character(bot))
