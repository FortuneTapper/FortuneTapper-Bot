import discord
from discord import app_commands
from domain.entities.character import Character
from domain.interactors import roll_interactor
from presenters.roll_presenter import RollPresenter
import adapter.config as config

class TapCommand(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="roll", 
        description="Realiza una tirada de dados."
    )
    @app_commands.describe(
        dice="El formato de dados, como 1d20 o 2d6"
    )
    async def roll(self, interaction: discord.Interaction, dice: str):
        await RollPresenter(interaction).roll(roll_interactor.roll(dice))

    @app_commands.command(
        name="plot", 
        description="Makes a plot dice roll"
    )
    async def plot(self, interaction: discord.Interaction):
        await RollPresenter(interaction).roll(roll_interactor.plot_roll(), title = "Plot dice roll!")

    @app_commands.command(name="tap", description="Realiza una tirada usando un atributo o habilidad.")
    @app_commands.describe(
        stat="Which skill to use",
        advantage="Advantage/Disadvantage",
        plot="Whether to use plot dice or not"
    )
    @app_commands.choices(
        stat=[
            app_commands.Choice(name="Athletics", value="athletics"),
            app_commands.Choice(name="Agility", value="agility"),
            app_commands.Choice(name="Heavy Weapons", value="heavy_weapons"),
            app_commands.Choice(name="Light Weapons", value="light_weapons"),
            app_commands.Choice(name="Stealth", value="stealth"),
            app_commands.Choice(name="Thievery", value="thievery"),
            app_commands.Choice(name="Crafting", value="crafting"),
            app_commands.Choice(name="Deduction", value="deduction"),
            app_commands.Choice(name="Discipline", value="discipline"),
            app_commands.Choice(name="Intimidation", value="intimidation"),
            app_commands.Choice(name="Lore", value="lore"),
            app_commands.Choice(name="Medicine", value="medicine"),
            app_commands.Choice(name="Deception", value="deception"),
            app_commands.Choice(name="Insight", value="insight"),
            app_commands.Choice(name="Leadership", value="leadership"),
            app_commands.Choice(name="Perception", value="perception"),
            app_commands.Choice(name="Persuasion", value="persuasion"),
            app_commands.Choice(name="Survival", value="survival"),
        ],
        advantage = [
            app_commands.Choice(name="Advantage", value="adv"),
            app_commands.Choice(name="Disadvantage", value="dis"),
        ]
    )
    async def tap(self, interaction: discord.Interaction, stat: app_commands.Choice[str], advantage: str = None, plot: bool = False):
        """Realiza una tirada de dados usando un atributo o habilidad del personaje activo."""

        try:
            # Obtener el personaje activo del usuario en el servidor actual
            character = config.repository.get(str(interaction.user.id), str(interaction.guild.id))

            if character:
                await RollPresenter(interaction).roll(roll_interactor.roll(f"{(
                    '2d20kl1' if advantage == 'dis'
                    else '2d20kh1' if advantage == 'adv'
                    else '1d20'
                )}+{character.skills.__dict__[stat.value].modifier}"), title = f"Tapping {stat.name} 🎲")
            else:
                await interaction.response.send_message(
                    "No tienes un personaje activo en este servidor.",
                    ephemeral=True
                )

        except Exception as e:
            await interaction.response.send_message(
                "Ha ocurrido un error inesperado. Inténtalo de nuevo más tarde.",
                ephemeral=True
            )
            print(f"Error inesperado: {e}")


async def setup(bot):
    await bot.add_cog(TapCommand(bot))
