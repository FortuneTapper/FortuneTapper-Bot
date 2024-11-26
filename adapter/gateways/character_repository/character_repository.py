from abc import ABC, abstractmethod, update_abstractmethods
from domain.entities import Character
from typing import List, Optional

class CharacterRepository(ABC):

    @abstractmethod
    def save(self, user_id: str, guild_id: str, character: Character):
        pass

    @abstractmethod
    def set_primary(self, user_id: str, guild_id: str, character_id: str) -> Optional[Character]:
        pass

    @abstractmethod
    def get(self, user_id: str, guild_id: str) -> Optional[Character]:
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: str, guild_id: str, character_id: str) -> Optional[Character]:
        pass

    @abstractmethod
    def get_all(self, user_id: str, guild_id: str) -> List[Character]:
        pass

update_abstractmethods(CharacterRepository)