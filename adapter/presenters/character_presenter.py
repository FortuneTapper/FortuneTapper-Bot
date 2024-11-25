from typing import List
import discord

from domain.entities import Character

class CharacterPresenter:
    _demiplane_url: str

    def __init__(self, demiplane_url: str):
        self._demiplane_url = demiplane_url

    def circle_display(self, current, maximum):
            filled = '●' * int(current)
            empty = '○' * (int(maximum) - int(current))
            return filled + empty
    

    def display_attributes(self, character: Character) -> str:
        return (
            f"**Strength**: {character.attributes.strength}\n"
            f"**Speed**: {character.attributes.speed}\n"
            f"**Intellect**: {character.attributes.intellect}\n"
            f"**Willpower**: {character.attributes.willpower}\n"
            f"**Awareness**: {character.attributes.awareness}\n"
            f"**Presence**: {character.attributes.presence}"
        )
    

    def display_defenses(self, character: Character) -> str:
         return (
            f"**Physical Defense**: {character.defenses.physical}\n"
            f"**Cognitive Defense**: {character.defenses.cognitive}\n"
            f"**Spiritual Defense**: {character.defenses.spiritual}\n"
            f"**Deflect**: {character.defenses.deflect}"
        )


    def display_resources(self, character: Character) -> str:
        return (
            f"**Health**: {character.resources.health.current}/{character.resources.health.max}\n"
            f"**Focus**: {self.circle_display(character.resources.focus.current, character.resources.focus.max)}\n"
            f"**Investiture**: {self.circle_display(character.resources.investiture.current, character.resources.investiture.max)}\n"
            f"**Movement**: {character.resources.movement} ft.\n"
            f"**Recovery Die**: d{character.resources.recovery_die}\n"
            f"**Senses Range**: {character.resources.senses_range} ft."
        )
    

    def display_skills(self, character: Character) -> str:
        return "\n".join([
            f"**{name}**: +{mod}" for name, mod in [
                ("Athletics", character.skills.athletics.modifier),
                ("Agility", character.skills.agility.modifier),
                ("Heavy Weapons", character.skills.heavy_weapons.modifier),
                ("Light Weapons", character.skills.light_weapons.modifier),
                ("Stealth", character.skills.stealth.modifier),
                ("Thievery", character.skills.thievery.modifier),
                ("Crafting", character.skills.crafting.modifier),
                ("Deduction", character.skills.deduction.modifier),
                ("Discipline", character.skills.discipline.modifier),
                ("Intimidation", character.skills.intimidation.modifier),
                ("Lore", character.skills.lore.modifier),
                ("Medicine", character.skills.medicine.modifier),
                ("Deception", character.skills.deception.modifier),
                ("Insight", character.skills.insight.modifier),
                ("Leadership", character.skills.leadership.modifier),
                ("Perception", character.skills.perception.modifier),
                ("Persuasion", character.skills.persuasion.modifier),
                ("Survival", character.skills.survival.modifier),
            ]
        ])


    async def character(self, interaction: discord.Interaction, character: Character):
        embed = discord.Embed(
            title=f"Datos del Personaje: {character.name}",
            description=f'[Character in Demiplane]({self._demiplane_url}{character.character_id})',
            color=discord.Color.gold(),
        )
        embed.set_thumbnail(url=character.avatar)

        embed.add_field(name="**Atributos**", value=self.display_attributes(character), inline=False)
        embed.add_field(name="**Defenses**", value=self.display_defenses(character), inline=False)
        embed.add_field(name="**Resources**", value=self.display_resources(character), inline=False)

        await interaction.followup.send(embed=embed)


    async def sheet(self, interaction: discord.Interaction, character: Character):
        embed = discord.Embed(
            title=f"Datos del Personaje: {character.name}",
            description=f'[Character in Demiplane]({self._demiplane_url}{character.character_id})',

            color=discord.Color.gold(),
        )
        embed.set_thumbnail(url=character.avatar)

        embed.add_field(name="**Atributos**", value=self.display_attributes(character), inline=False)
        embed.add_field(name="**Defenses**", value=self.display_defenses(character), inline=False)
        embed.add_field(name="**Resources**", value=self.display_resources(character), inline=False)
        embed.add_field(name="**Skills**", value=self.display_skills(character), inline=False)

        await interaction.followup.send(embed=embed)


    async def list(self, interaction: discord.Interaction, characters: List[Character]):
        embed = discord.Embed(
            title=f"Lista de personajes",
            color=discord.Color.gold(),
        )
        for character in characters:
            embed.add_field(name=character.name, value=f'{self._demiplane_url}{character.character_id}', inline=False)
        await interaction.followup.send(embed=embed, ephemeral=True)

