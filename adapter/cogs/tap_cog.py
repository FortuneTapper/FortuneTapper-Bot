from typing import Any
import discord
from discord.ext import commands
from discord import app_commands
from domain.entities.character import Character
from domain.entities.roll_result import AdvantageType
from domain.interactors import roll_interactor, character_interactor
from adapter.presenters.roll_presenter import RollPresenter
import adapter.config as config
from domain.interactors.exceptions import NoCharacterError

class TapCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @app_commands.command(
        name="roll", 
        description="Make a generic roll"
    )
    @app_commands.describe(
        dice="Dice expression format, like 1d20 or 2d6"
    )
    async def roll(self, interaction: discord.Interaction, dice: str):
        config.logger.info({
            'event': 'roll',
            'user': str(interaction.user),
            'user_id': interaction.user.id,
            'guild': interaction.guild.name if interaction.guild else "DM",
            'guild_id': interaction.guild.id if interaction.guild else None,
            'channel': interaction.channel.name if interaction.channel else "Unknown",
            'channel_id': interaction.channel.id if interaction.channel else None,
            'dice': dice
        })

        try:
            await interaction.response.defer()

            await RollPresenter(interaction).roll(roll_interactor.roll(dice))
        except NoCharacterError as e:
            config.logger.error(f"NoCharacterError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except Exception as e:
            config.logger.error(f"Unexpected error: {e}", exc_info=True)
            await interaction.followup.send("Unexpected error occurred.", ephemeral=True)
        


    @app_commands.command(name="tap", description="Makes a skill test roll")
    @app_commands.describe(
        stat="Which skill to use",
        advantage="Advantage/Disadvantage on skill test",
        plot_die="Whether to use plot dice or not",
        plot_advantage="Advantage/Disadvantage on plot die"
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
            app_commands.Choice(name="Advantage", value=roll_interactor.AdvantageType.ADVANTAGE.value),
            app_commands.Choice(name="Disadvantage", value=roll_interactor.AdvantageType.DISADVANTAGE.value),
        ],
        plot_advantage = [
            app_commands.Choice(name="Advantage", value=roll_interactor.AdvantageType.ADVANTAGE.value),
            app_commands.Choice(name="Disadvantage", value=roll_interactor.AdvantageType.DISADVANTAGE.value),
        ]
    )
    async def tap(
        self, 
        interaction: discord.Interaction, 
        stat: app_commands.Choice[str], 
        advantage: str = roll_interactor.AdvantageType.NONE.value, 
        plot_die: bool = False, 
        plot_advantage: str = roll_interactor.AdvantageType.NONE.value
    ):
        config.logger.info({
            'event': 'tap',
            'user': str(interaction.user),
            'user_id': interaction.user.id,
            'guild': interaction.guild.name if interaction.guild else "DM",
            'guild_id': interaction.guild.id if interaction.guild else None,
            'channel': interaction.channel.name if interaction.channel else "Unknown",
            'channel_id': interaction.channel.id if interaction.channel else None,
        })

        try:
            await interaction.response.defer()

            await RollPresenter(interaction).skill_test(
                roll_interactor.skill_test(
                    modifier = character_interactor.get_character(
                        str(interaction.user.id), 
                        str(interaction.guild.id)
                    ).skills.__dict__[stat.value].modifier,
                    advantage = AdvantageType(advantage),
                    plot_die = plot_die,
                    plot_advantage = AdvantageType(plot_advantage)
                ), 
                skill = stat.name
            )
        except NoCharacterError as e:
            config.logger.error(f"NoCharacterError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except Exception as e:
            config.logger.error(f"Unexpected error: {e}", exc_info=True)
            await interaction.followup.send("Unexpected error occurred.", ephemeral=True)
        

    @app_commands.command(name="attack", description="Makes an attack roll")
    @app_commands.describe(
        damage_dice = "Dice to roll damage", 
        weapon_type = "What type of weapon to use: heavy, light or unarmed",
        advantage = "If to give advantage/disadvantage to the hit roll",
        damage_advantage = "If to give advantage/disadvantage to the damage roll",
        plot_die = "If to use plot die",
        plot_advantage = "If to have advantage/disadvantage in the plot die roll",
        plot_die_damage = "If to apply plot to damage roll",
        weapon_name = "Name of the weapon to use"
    )
    @app_commands.choices(
        weapon_type = [
            app_commands.Choice(name="Heavy Weapon", value="heavy_weapons"),
            app_commands.Choice(name="Light Weapon", value="light_weapons"),
            app_commands.Choice(name="Unarmed", value="athletics"),
        ],
        advantage = [
            app_commands.Choice(name="Advantage", value=roll_interactor.AdvantageType.ADVANTAGE.value),
            app_commands.Choice(name="Disadvantage", value=roll_interactor.AdvantageType.DISADVANTAGE.value),
        ],
        damage_advantage = [
            app_commands.Choice(name="Advantage", value=roll_interactor.AdvantageType.ADVANTAGE.value),
            app_commands.Choice(name="Disadvantage", value=roll_interactor.AdvantageType.DISADVANTAGE.value),
        ],
        plot_advantage = [
            app_commands.Choice(name="Advantage", value=roll_interactor.AdvantageType.ADVANTAGE.value),
            app_commands.Choice(name="Disadvantage", value=roll_interactor.AdvantageType.DISADVANTAGE.value),
        ]
    )
    async def attack(
        self, 
        interaction: discord.Interaction, 
        damage_dice: str, 
        weapon_type: app_commands.Choice[str],
        advantage: str = roll_interactor.AdvantageType.NONE.value, 
        damage_advantage: str =  roll_interactor.AdvantageType.NONE.value,
        plot_die: bool = False, 
        plot_advantage: str = roll_interactor.AdvantageType.NONE.value,
        plot_die_damage: bool = False,
        weapon_name: str = 'Unknown'
    ):
        config.logger.info({
            'event': 'tap',
            'user': str(interaction.user),
            'user_id': interaction.user.id,
            'guild': interaction.guild.name if interaction.guild else "DM",
            'guild_id': interaction.guild.id if interaction.guild else None,
            'channel': interaction.channel.name if interaction.channel else "Unknown",
            'channel_id': interaction.channel.id if interaction.channel else None,
        })

        try:
            await interaction.response.defer()

            await RollPresenter(interaction).attack(
                roll_interactor.attack_roll(
                    damage_expr = damage_dice,
                    modifier = character_interactor.get_character(
                        str(interaction.user.id), 
                        str(interaction.guild.id)
                    ).skills.__dict__[weapon_type.value].modifier if weapon_type else 0,
                    advantage = AdvantageType(advantage),
                    damage_advantage = AdvantageType(damage_advantage),
                    plot_die = plot_die,
                    plot_advantage = AdvantageType(plot_advantage),
                    plot_die_damage = plot_die_damage
                ), 
                weapon = weapon_name
            )
        except NoCharacterError as e:
            config.logger.error(f"NoCharacterError: {e}", exc_info=True)
            await interaction.followup.send(str(e), ephemeral=True)
        except Exception as e:
            config.logger.error(f"Unexpected error: {e}", exc_info=True)
            await interaction.followup.send("Unexpected error occurred.", ephemeral=True)
    


async def setup(bot):
    await bot.add_cog(TapCommand(bot))
