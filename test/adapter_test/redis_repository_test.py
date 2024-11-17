import unittest
from unittest.mock import MagicMock, patch
from adapter.gateways.redis_character_repository import RedisCharacterRepository
from domain.entities.character import Character


class TestRedisCharacterRepository(unittest.TestCase):
    def setUp(self):
        self.redis_url = "redis://localhost:6379/0"
        self.repository = RedisCharacterRepository(self.redis_url)

        # Mocking the Redis client
        self.mock_redis = MagicMock()
        self.repository.redis = self.mock_redis

        # Example Character
        self.character = Character(
            character_id="12345",
            name="Test Character",
            attributes={"strength": 10, "dexterity": 12}
        )

    def test_save(self):
        # Act
        self.repository.save("user123", "guild123", self.character)

        # Assert
        self.mock_redis.set.assert_called_once_with(
            "character:user123:guild123",
            self.character.to_json()
        )

    def test_get_found(self):
        # Arrange
        character_data = self.character.to_json()
        self.mock_redis.get.return_value = character_data

        # Act
        result = self.repository.get("user123", "guild123")

        # Assert
        self.mock_redis.get.assert_called_once_with("character:user123:guild123")
        self.assertEqual(result.character_id, self.character.character_id)
        self.assertEqual(result.name, self.character.name)

    def test_get_not_found(self):
        # Arrange
        self.mock_redis.get.return_value = None

        # Act
        result = self.repository.get("user123", "guild123")

        # Assert
        self.mock_redis.get.assert_called_once_with("character:user123:guild123")
        self.assertIsNone(result)

    def test_get_all_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.repository.get_all("user123", "guild123")


if __name__ == "__main__":
    unittest.main()
