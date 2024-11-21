import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from domain.interactors.character_interactor import (
    import_character,
    update_character,
    get_character,
    get_character_list,
    select_character
)
from domain.entities.character import Character, Attributes, Skills, Skill, Defenses, Resources, Action
from domain.interactors import exceptions
import os
import adapter.config as config

class TestCharacterInteractor(unittest.IsolatedAsyncioTestCase):

    @patch("domain.interactors.character_interactor.config.repository.save")
    @patch("domain.interactors.character_interactor.async_playwright")
    async def test_import_character_from_html(self, mock_playwright, mock_save):
        with open(os.path.join(os.path.dirname(__file__), "character_test.html"), "r", encoding="utf-8") as f:
            html_content = f.read()

        mock_browser = AsyncMock()
        mock_page = AsyncMock()
        mock_browser.new_page.return_value = mock_page
        mock_context = AsyncMock()
        mock_playwright.return_value.__aenter__.return_value.chromium.launch.return_value = mock_browser
        mock_page.content.return_value = html_content

        result = await import_character("http://example.com/character/123", "user1", "guild1")

        self.assertIsInstance(result, Character)
        self.assertEqual(result.name, "Yazbk")
        mock_save.assert_called_once_with("user1", "guild1", result)

    @patch("domain.interactors.character_interactor.config.repository.get")
    @patch("domain.interactors.character_interactor.import_character")
    async def test_update_character(self, mock_import_character, mock_get):
        mock_character = MagicMock()
        mock_character.character_id = "123"
        mock_character.name = "Updated Character"
        
        mock_get.return_value = mock_character
        mock_import_character.return_value = mock_character

        result = await update_character("user1", "guild1")

        self.assertEqual(result.name, "Updated Character")
        mock_get.assert_called_once_with("user1", "guild1")
        mock_import_character.assert_called_once_with(f"{config.DEMIPLANE_URL}123", "user1", "guild1")

    @patch("domain.interactors.character_interactor.config.repository.get")
    def test_get_character(self, mock_get):
        mock_character = MagicMock()
        mock_character.name = "Test Character"

        mock_get.return_value = mock_character

        result = get_character("user1", "guild1")

        self.assertEqual(result.name, "Test Character")
        mock_get.assert_called_once_with("user1", "guild1")

    @patch("domain.interactors.character_interactor.config.repository.get")
    def test_get_character_raises_exception(self, mock_get):
        mock_get.return_value = None

        with self.assertRaises(exceptions.CharacterImportError):
            get_character("user1", "guild1")

    @patch("domain.interactors.character_interactor.config.repository.get_all")
    def test_get_character_list(self, mock_get_all):
        mock_characters = [MagicMock(name="Character 1"), MagicMock(name="Character 2")]
        mock_get_all.return_value = mock_characters

        result = get_character_list("user1", "guild1")

        self.assertEqual(len(result), 2)
        mock_get_all.assert_called_once_with("user1", "guild1")

    @patch("domain.interactors.character_interactor.config.repository.set_primary")
    def test_select_character(self, mock_set_primary):
        mock_character = MagicMock()
        mock_character.name = "Primary Character"
        mock_set_primary.return_value = mock_character

        result = select_character("user1", "guild1", "char_id")

        self.assertEqual(result.name, "Primary Character")
        mock_set_primary.assert_called_once_with("user1", "guild1", "char_id")

    @patch("domain.interactors.character_interactor.config.repository.set_primary")
    def test_select_character_raises_exception(self, mock_set_primary):
        mock_set_primary.return_value = None

        with self.assertRaises(exceptions.CharacterImportError):
            select_character("user1", "guild1", "char_id")
