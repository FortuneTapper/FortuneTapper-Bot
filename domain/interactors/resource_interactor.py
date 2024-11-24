from domain.entities.character import Character, Resource, ResourceType
from adapter import config


def set_current_resource(user_id, guild_id, resource: ResourceType, amount: int):
    character: Character = config.repository.get(user_id, guild_id)

    resource : Resource = getattr(character.resources, resource.value, Resource())

    resource.current = min(max(amount, 0), resource.max)

    config.repository.save(user_id, guild_id, character)

    return character

def modify_current_resource(user_id, guild_id, resource: ResourceType, amount: int):
    character: Character = config.repository.get(user_id, guild_id)

    resource : Resource = getattr(character.resources, resource.value, Resource())

    resource.current = min(max(resource.current + amount, 0), resource.max)

    config.repository.save(user_id, guild_id, character)

    return character