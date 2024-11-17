import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import sessionmaker
from adapter.gateways.sqlalchemy_repository import SQLAlchemyCharacterRepository
from adapter.gateways.models.sqlalchemy_character import SQLAlchemyCharacter
from domain.entities.character import Character


class TestSQLAlchemyCharacterRepository(unittest.TestCase):
    def setUp(self):
        self.db_url = "sqlite:///:memory:"
        self.repository = SQLAlchemyCharacterRepository(self.db_url)

        # Mocking the session
        self.mock_session = MagicMock()
        self.repository.Session = MagicMock(return_value=self.mock_session)

        # Example Character
        self.character = Character(
            character_id="12345",
            name="Test Character",
            attributes={"strength": 10, "dexterity": 12}
        )

    @patch("adapter.gateways.sqlalchemy_repository.SQLAlchemyCharacter")
    def test_save(self, mock_sqlalchemy_character):
        # Arrange
        self.mock_session.query.return_value.filter_by.return_value.update.return_value = None
        self.mock_session.add.return_value = None

        # Act
        with self.repository.session_scope() as session:
            self.repository.save("user123", "guild123", self.character)

        # Assert
        self.mock_session.query.assert_called_with(mock_sqlalchemy_character)
        self.mock_session.query.return_value.filter_by.assert_called_with(
            user_id="user123", guild_id="guild123", is_primary=True
        )
        self.mock_session.add.assert_called_once()
        mock_sqlalchemy_character.assert_called_with(
            user_id="user123",
            guild_id="guild123",
            character_id="12345",
            character_data=self.character.to_json(),
            is_primary=True
        )

    @patch("adapter.gateways.sqlalchemy_repository.SQLAlchemyCharacter")
    def test_get(self, mock_sqlalchemy_character):
        # Arrange
        mock_character_data = """{"character_id": "12345", "name": "Test Character", "attributes": {"strength": 10}}"""
        mock_result = MagicMock()
        mock_result.character_data = mock_character_data

        # Act
        with self.repository.session_scope() as session:
            session.query.return_value.filter_by.return_value.first.return_value = mock_result
            result = self.repository.get("user123", "guild123")

        # Assert
        self.mock_session.query.assert_called_with(mock_sqlalchemy_character)
        self.mock_session.query.return_value.filter_by.assert_called_with(
            user_id="user123", guild_id="guild123", is_primary=True
        )
        self.assertEqual(result.character_id, "12345")
        self.assertEqual(result.name, "Test Character")

    @patch("adapter.gateways.sqlalchemy_repository.SQLAlchemyCharacter")
    def test_get_all(self, mock_sqlalchemy_character):
        # Arrange
        mock_character_data = [
            """{"character_id": "12345", "name": "Test Character 1", "attributes": {"strength": 10}}""",
            """{"character_id": "67890", "name": "Test Character 2", "attributes": {"dexterity": 12}}"""
        ]
        mock_results = [MagicMock(character_data=data, guild_id="guild123") for data in mock_character_data]

        # Act
        with self.repository.session_scope() as session:
            session.query.return_value.filter_by.return_value.all.return_value = mock_results
            result = self.repository.get_all("user123", "guild123")

        # Assert
        self.mock_session.query.assert_called_with(mock_sqlalchemy_character)
        self.mock_session.query.return_value.filter_by.assert_called_with(
            user_id="user123", guild_id="guild123"
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].character_id, "12345")
        self.assertEqual(result[1].character_id, "67890")

    @patch("adapter.gateways.sqlalchemy_repository.SQLAlchemyCharacter")
    def test_set_primary(self, mock_sqlalchemy_character):
        # Arrange
        self.mock_session.query.return_value.filter_by.return_value.update.return_value = None

        # Act
        with self.repository.session_scope() as session:
            self.repository.set_primary("user123", "guild123", "12345")

        # Assert
        self.mock_session.query.assert_called_with(mock_sqlalchemy_character)
        self.mock_session.query.return_value.filter_by.assert_any_call(
            user_id="user123", guild_id="guild123", is_primary=True
        )
        self.mock_session.query.return_value.filter_by.assert_any_call(
            user_id="user123", guild_id="guild123", character_id="12345"
        )


if __name__ == "__main__":
    unittest.main()
