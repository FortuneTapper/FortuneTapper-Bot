import os
import logging
import dotenv

from adapter.gateways.character_repository.character_repository import CharacterRepository
from adapter.gateways.character_repository.caching_character_repository import CachingCharacterRepository
from adapter.gateways.character_repository.redis_character_repository import RedisCharacterRepository
from adapter.gateways.character_repository.sqlalchemy_character_repository import SQLAlchemyCharacterRepository



dotenv.load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', default='')
REDIS_URL = os.getenv('REDIS_URL', default='redis://')
POSTGRES_URL = os.getenv('POSTGRES_URL', default='sqlite:///:memory:')
DEMIPLANE_URL = os.getenv('DEMIPLANE_URL', default = 'https://app.demiplane.com/nexus/cosmererpg/character-sheet/')

repository: CharacterRepository = CachingCharacterRepository(
    RedisCharacterRepository(REDIS_URL), 
    SQLAlchemyCharacterRepository(POSTGRES_URL)
)

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', default='INFO'),  # Nivel de log (puedes cambiar a DEBUG, WARNING, etc.)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger: logging.Logger = logging.getLogger(__name__)