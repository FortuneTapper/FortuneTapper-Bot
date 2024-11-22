from sqlalchemy import Column, String, JSON, Boolean, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SQLAlchemyCharacter(Base):
    __tablename__ = 'characters'

    user_id = Column(String, primary_key=True)
    guild_id = Column(String, primary_key=True)
    character_id = Column(String, primary_key=True)
    character_data = Column(JSON, nullable=False)
    is_primary = Column(Boolean, default=False)

    def __init__(self, user_id, guild_id, character_id, character_data, is_primary=False):
        self.user_id = user_id
        self.guild_id = guild_id
        self.character_id = character_id
        self.character_data = character_data
        self.is_primary = is_primary
