import json
from typing import List, Optional
from domain.entities.character import Character
from adapter.gateways.character_repository import CharacterRepository

class InMemoryCharacterRepository(CharacterRepository):
    def __init__(self):
        self.data = {}

    def save(self, user_id: str, guild_id: str, character: Character):
        key = (user_id, guild_id)
        self.data[key] = character.to_dict()  # Serializa el objeto a diccionario

    def get(self, user_id: str, guild_id: str) -> Optional[Character]:
        key = (user_id, guild_id)
        character_data = self.data.get(key)
        return Character.from_dict(character_data) if character_data else None

    def get_all_by_user(self, user_id: str) -> List[Character]:
        return [
            Character.from_dict(data)
            for (u_id, _), data in self.data.items()
            if u_id == user_id
        ]
