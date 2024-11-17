import discord
import d20

from domain.entities.character import Character

class CharacterPresenter:
    interaction: discord.Interaction

    def __init__(self, interaction: discord.Interaction):
        self.interaction = interaction

    async def show(self, character: Character):
        embed = discord.Embed(
            title=f"Datos del Personaje: {character.name}",
            color=discord.Color.gold(),
        )
        embed.set_thumbnail(url=character.avatar)

        # Helper para generar el texto de círculos
        def circle_display(current, maximum):
            filled = '●' * int(current)
            empty = '○' * (int(maximum) - int(current))
            return filled + empty

        # Sección de Atributos
        attributes = (
            f"**Strength**: {character.attributes.strength}\n"
            f"**Speed**: {character.attributes.speed}\n"
            f"**Intellect**: {character.attributes.intellect}\n"
            f"**Willpower**: {character.attributes.willpower}\n"
            f"**Awareness**: {character.attributes.awareness}\n"
            f"**Presence**: {character.attributes.presence}"
        )
        embed.add_field(name="**Atributos**", value=attributes, inline=False)

        # Sección de Habilidades
        skills = "\n".join([
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
        embed.add_field(name="**Skills**", value=skills, inline=False)

        # Sección de Defensas
        defenses = (
            f"**Physical Defense**: {character.defenses.physical}\n"
            f"**Cognitive Defense**: {character.defenses.cognitive}\n"
            f"**Spiritual Defense**: {character.defenses.spiritual}\n"
            f"**Deflect**: {character.defenses.deflect}"
        )
        embed.add_field(name="**Defenses**", value=defenses, inline=False)

        # Sección de Recursos con Círculos para Focus e Investiture
        resources = (
            f"**Health**: {character.resources.health}/{character.resources.health_max}\n"
            f"**Focus**: {circle_display(character.resources.focus, character.resources.focus_max)}\n"
            f"**Investiture**: {circle_display(character.resources.investiture, character.resources.investiture_max)}\n"
            f"**Movement**: {character.resources.movement} ft.\n"
            f"**Recovery Die**: d{character.resources.recovery_die}\n"
            f"**Senses Range**: {character.resources.senses_range} ft."
        )
        embed.add_field(name="**Resources**", value=resources, inline=False)

        await self.interaction.followup.send(embed=embed)

