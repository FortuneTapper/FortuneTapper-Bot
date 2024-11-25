from adapter.gateways.character_repository.caching_character_repository import CachingCharacterRepository
from domain.entities import Character, Resource, ResourceType

class ResourceInteractor:

    def __init__(self, repository: CachingCharacterRepository):
        self.repository = repository

    def set_current_resource(self, user_id, guild_id, resource: ResourceType, amount: int) -> Resource:
        character: Character = self.repository.get(user_id, guild_id)

        resource: Resource = character.resources.get_resource_by_type(resource)
        resource.current = amount

        self.repository.save(user_id, guild_id, character)

        return resource

    def modify_current_resource(self, user_id, guild_id, resource: ResourceType, amount: int) -> Resource:
        character: Character = self.repository.get(user_id, guild_id)

        resource: Resource = character.resources.get_resource_by_type(resource)
        resource.current = resource.current + amount

        self.repository.save(user_id, guild_id, character)

        return resource