from typing import List, Optional
from domain.entities.character import Character
from adapter.gateways.character_repository import CharacterRepository

class CachingCharacterRepository(CharacterRepository):
    def __init__(self, cache_repo: CharacterRepository, db_repo: CharacterRepository):
        self.cache_repo = cache_repo
        self.db_repo = db_repo

    def save(self, user_id: str, guild_id: str, character: Character):
        self.cache_repo.save(user_id, guild_id, character)
        self.db_repo.save(user_id, guild_id, character)

    def get(self, user_id: str, guild_id: str) -> Optional[Character]:
        character = self.cache_repo.get(user_id, guild_id)
        if not character:
            character = self.db_repo.get(user_id, guild_id)
            if character:
                self.cache_repo.save(user_id, guild_id, character)
        return character

    def get_all(self, user_id: str, guild_id: str) -> List[Character]:
        return self.db_repo.get_all(user_id, guild_id)
