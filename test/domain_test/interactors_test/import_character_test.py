import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from domain.interactors.character_interactor import import_character
from domain.entities.character import Character
from lxml import etree

class TestImportCharacterData(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Cargar el contenido de character_test.html
        with open("test/domain_test/interactors_test/character_test.html", "r", encoding="utf-8") as file:
            self.mock_html_content = file.read()

    @patch("domain.interactors.import_character.get_rendered_html", new_callable=AsyncMock)
    @patch("adapter.config.repository.save")
    async def test_import_character_data(self, mock_save, mock_get_rendered_html):
        # Arrange
        url = "https://example.com/character/12345"
        user_id = "user123"
        guild_id = "guild123"

        mock_get_rendered_html.return_value = self.mock_html_content

        # Act
        character = await import_character(url, user_id, guild_id)

        # Assert
        mock_get_rendered_html.assert_called_once_with(url)
        mock_save.assert_called_once_with(user_id, guild_id, character)

        # Verificar datos del personaje
        self.assertIsInstance(character, Character)
        self.assertEqual(character.character_id, "12345")
        self.assertEqual(character.name, "Yazbk")
        self.assertEqual(character.attributes.strength, 1)
        self.assertEqual(character.attributes.speed, 2)
        self.assertEqual(character.attributes.intellect, 3)
        self.assertEqual(character.attributes.willpower, 3)
        self.assertEqual(character.attributes.awareness, 2)
        self.assertEqual(character.attributes.presence, 1)
        self.assertEqual(character.defenses.physical, 13)
        self.assertEqual(character.defenses.cognitive, 16)
        self.assertEqual(character.defenses.spiritual, 13)
        self.assertEqual(character.defenses.deflect, 0)
        self.assertEqual(character.resources.health, 11)
        self.assertEqual(character.resources.focus, 5)
        self.assertEqual(character.resources.investiture, 0)
        self.assertEqual(character.resources.movement, 25)
        self.assertEqual(character.resources.recovery_die, 8)
        self.assertEqual(character.resources.senses_range, 10)

if __name__ == "__main__":
    unittest.main()
