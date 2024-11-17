from typing import List, Optional
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from adapter.gateways.models.sqlalchemy_character import SQLAlchemyCharacter, Base
from domain.entities.character import Character
from adapter.gateways.character_repository import CharacterRepository
from contextlib import contextmanager

class SQLAlchemyCharacterRepository(CharacterRepository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def save(self, user_id: str, guild_id: str, character: Character):
        with self.session_scope() as session:
            session.query(SQLAlchemyCharacter).filter_by(
                user_id=user_id, guild_id=guild_id, is_primary=True
            ).update({"is_primary": False})

            new_character = SQLAlchemyCharacter(
                user_id=user_id,
                guild_id=guild_id,
                character_id=character.character_id,
                character_data=character.to_json(),
                is_primary=True
            )
            session.add(new_character)

    def set_primary(self, user_id: str, guild_id: str, character_id: str):
        with self.session_scope() as session:
            session.query(SQLAlchemyCharacter).filter_by(
                user_id=user_id, guild_id=guild_id, is_primary=True
            ).update({"is_primary": False})

            session.query(SQLAlchemyCharacter).filter_by(
                user_id=user_id,
                guild_id=guild_id,
                character_id=character_id
            ).update({"is_primary": True})

    def get(self, user_id: str, guild_id: str) -> Optional[Character]:
        with self.session_scope() as session:
            result = session.query(SQLAlchemyCharacter).filter_by(
                user_id=user_id, guild_id=guild_id, is_primary=True
            ).first()
            if result:
                return Character.from_json(result.character_data) 
            return None

    def get_all(self, user_id: str, guild_id: str) -> List[Character]:
        with self.session_scope() as session:
            results = session.query(SQLAlchemyCharacter).filter_by(user_id=user_id, guild_id=guild_id).all()
            return [Character.from_json(result.character_data) for result in results if result.guild_id is not None]
