# import_cog.py

import discord
from discord.ext import commands
from discord import app_commands
from adapter.presenters.character_presenter import CharacterPresenter
from domain.interactors import import_character
import adapter.config as config
import traceback

class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="import", description="Importa un personaje desde Demiplane con la URL de su hoja.")
    async def import_character(self, interaction: discord.Interaction, url: str):
        """Comando de Discord para importar un personaje desde Demiplane."""
        await interaction.response.defer()
        
        # Importa y guarda el personaje en el repositorio
        try: 
            character = await import_character.import_character_data(url, str(interaction.user.id), str(interaction.guild.id))
        
            # Muestra el personaje usando el presentador
            await CharacterPresenter(interaction).show(character)
        except Exception as e:
            await interaction.followup.send("Ha ocurrido un error inesperado. Inténtalo de nuevo más tarde.", ephemeral=True)
            print(f"Error inesperado: {e}")
            print(traceback.format_exc())

    @app_commands.command(name="show", description="Muestra la información del personaje activo.")
    async def show_character(self, interaction: discord.Interaction):
        """Comando de Discord para mostrar el personaje activo del usuario en el servidor."""
        await interaction.response.defer()

        user_id = str(interaction.user.id)
        guild_id = str(interaction.guild.id)

        try:
            # Recuperar el personaje activo desde el repositorio
            character = config.repository.get(user_id, guild_id)
            
            if character:
                await CharacterPresenter(interaction).show(character)
            else:
                await interaction.followup.send("No tienes un personaje activo en este servidor.", ephemeral=True)
        
        except Exception as e:
            await interaction.followup.send("Ha ocurrido un error inesperado. Inténtalo de nuevo más tarde.", ephemeral=True)
            print(f"Error inesperado: {e}")
            print(traceback.format_exc())

# Configuración para añadir el cog al bot
async def setup(bot):
    await bot.add_cog(Character(bot))
