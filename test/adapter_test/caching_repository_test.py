import unittest
from unittest.mock import MagicMock
from adapter.gateways.caching_character_repository import CachingCharacterRepository
from domain.entities.character import Character


class TestCachingCharacterRepository(unittest.TestCase):
    def setUp(self):
        # Mocking the cache and DB repositories
        self.mock_cache_repo = MagicMock()
        self.mock_db_repo = MagicMock()
        self.repository = CachingCharacterRepository(self.mock_cache_repo, self.mock_db_repo)

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
        self.mock_cache_repo.save.assert_called_once_with("user123", "guild123", self.character)
        self.mock_db_repo.save.assert_called_once_with("user123", "guild123", self.character)

    def test_get_found_in_cache(self):
        # Arrange
        self.mock_cache_repo.get.return_value = self.character

        # Act
        result = self.repository.get("user123", "guild123")

        # Assert
        self.mock_cache_repo.get.assert_called_once_with("user123", "guild123")
        self.mock_db_repo.get.assert_not_called()  # DB should not be queried
        self.assertEqual(result.character_id, self.character.character_id)
        self.assertEqual(result.name, self.character.name)

    def test_get_found_in_db(self):
        # Arrange
        self.mock_cache_repo.get.return_value = None
        self.mock_db_repo.get.return_value = self.character

        # Act
        result = self.repository.get("user123", "guild123")

        # Assert
        self.mock_cache_repo.get.assert_called_once_with("user123", "guild123")
        self.mock_db_repo.get.assert_called_once_with("user123", "guild123")
        self.mock_cache_repo.save.assert_called_once_with("user123", "guild123", self.character)
        self.assertEqual(result.character_id, self.character.character_id)
        self.assertEqual(result.name, self.character.name)

    def test_get_not_found(self):
        # Arrange
        self.mock_cache_repo.get.return_value = None
        self.mock_db_repo.get.return_value = None

        # Act
        result = self.repository.get("user123", "guild123")

        # Assert
        self.mock_cache_repo.get.assert_called_once_with("user123", "guild123")
        self.mock_db_repo.get.assert_called_once_with("user123", "guild123")
        self.mock_cache_repo.save.assert_not_called()  # Nothing to save if not found
        self.assertIsNone(result)

    def test_get_all(self):
        # Arrange
        all_characters = [self.character]
        self.mock_db_repo.get_all.return_value = all_characters

        # Act
        result = self.repository.get_all("user123", "guild123")

        # Assert
        self.mock_db_repo.get_all.assert_called_once_with("user123", "guild123")
        self.assertEqual(result, all_characters)


if __name__ == "__main__":
    unittest.main()
