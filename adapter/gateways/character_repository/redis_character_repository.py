from typing import List, Optional
import redis
from domain.entities import Character
from adapter.gateways.character_repository.character_repository import CharacterRepository

class RedisCharacterRepository(CharacterRepository):
    def __init__(self, redis_url: str):
        self.redis = redis.Redis.from_url(redis_url)

    def save(self, user_id: str, guild_id: str, character: Character):
        self.redis.set(f"character:{user_id}:{guild_id}", character.to_json())

    def set_primary(self, user_id: str, guild_id: str, character_id: str) -> Optional[Character]:
        raise NotImplementedError()

    def get(self, user_id: str, guild_id: str) -> Optional[Character]:
        character_data = self.redis.get(f"character:{user_id}:{guild_id}")
        if character_data:
            return Character.from_json(character_data)
        return None
    
    def get_by_id(self, user_id: str, guild_id: str, character_id: str) -> Optional[Character]:
        pass

    def get_all(self, user_id: str, guild_id: str) -> List[Character]:
        raise NotImplementedError()