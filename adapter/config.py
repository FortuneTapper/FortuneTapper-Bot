import os
import logging
import dotenv

from adapter.gateways.character_repository import CharacterRepository
from adapter.gateways.caching_character_repository import CachingCharacterRepository
from adapter.gateways.redis_character_repository import RedisCharacterRepository
from adapter.gateways.sqlalchemy_repository import SQLAlchemyCharacterRepository



dotenv.load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
REDIS_URL = os.getenv('REDIS_URL')
POSTGRES_URL = os.getenv('POSTGRES_URL')

repository: CharacterRepository = CachingCharacterRepository(
    RedisCharacterRepository(REDIS_URL), 
    SQLAlchemyCharacterRepository(POSTGRES_URL)
)

logging.basicConfig(
    level=logging.INFO,  # Nivel de log (puedes cambiar a DEBUG, WARNING, etc.)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger: logging.Logger = logging.getLogger(__name__)