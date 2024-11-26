from adapter.gateways.character_repository.caching_character_repository import CachingCharacterRepository
from domain.entities import Action

class ActionInteractor:
    def __init__(self, repository: CachingCharacterRepository):
        self.repository = repository

    def get_action(self, user_id, guild_id, action_name: str) -> Action:
        for action in self.repository.get(user_id, guild_id).actions.basic:
            if action.name.lower() == action_name.lower():
                return action
        
        return None