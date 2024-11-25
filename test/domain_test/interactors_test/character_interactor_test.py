import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from domain.interactors.character_interactor import CharacterInteractor
from domain.entities import Character
from domain.interactors import exceptions
from adapter.gateways.character_repository.caching_character_repository import CachingCharacterRepository
import os

class TestCharacterInteractor(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Mock del repositorio
        self.mock_repository = MagicMock(spec=CachingCharacterRepository)
        self.character_interactor = CharacterInteractor(
            repository=self.mock_repository,
            demiplane_url="http://example.com/character/"
        )

    @patch("domain.interactors.character_interactor.async_playwright")
    async def test_import_character_from_html(self, mock_playwright):
        with open(os.path.join(os.path.dirname(__file__), "character_test.html"), "r", encoding="utf-8") as f:
            html_content = f.read()

        mock_browser = AsyncMock()
        mock_page = AsyncMock()
        mock_browser.new_page.return_value = mock_page
        mock_playwright.return_value.__aenter__.return_value.chromium.launch.return_value = mock_browser
        mock_page.content.return_value = html_content

        result = await self.character_interactor.import_character(
            "http://example.com/character/123", "user1", "guild1"
        )

        self.assertIsInstance(result, Character)
        self.assertEqual(result.name, "Yazbk")
        self.mock_repository.save.assert_called_once_with("user1", "guild1", result)

    async def test_update_character(self):
        mock_character = MagicMock()
        mock_character.character_id = "123"
        mock_character.name = "Updated Character"

        self.mock_repository.get.return_value = mock_character
        self.character_interactor.import_character = AsyncMock(return_value=mock_character)

        result = await self.character_interactor.update_character("user1", "guild1")

        self.assertEqual(result.name, "Updated Character")
        self.mock_repository.get.assert_called_once_with("user1", "guild1")
        self.character_interactor.import_character.assert_called_once()

    def test_get_character(self):
        mock_character = MagicMock()
        mock_character.name = "Test Character"

        self.mock_repository.get.return_value = mock_character

        result = self.character_interactor.get_character("user1", "guild1")

        self.assertEqual(result.name, "Test Character")
        self.mock_repository.get.assert_called_once_with("user1", "guild1")

    def test_get_character_raises_exception(self):
        self.mock_repository.get.return_value = None

        with self.assertRaises(exceptions.CharacterImportError):
            self.character_interactor.get_character("user1", "guild1")

    def test_get_character_list(self):
        mock_characters = [MagicMock(name="Character 1"), MagicMock(name="Character 2")]
        self.mock_repository.get_all.return_value = mock_characters

        result = self.character_interactor.get_character_list("user1", "guild1")

        self.assertEqual(len(result), 2)
        self.mock_repository.get_all.assert_called_once_with("user1", "guild1")

    def test_select_character(self):
        mock_character = MagicMock()
        mock_character.name = "Primary Character"
        self.mock_repository.set_primary.return_value = mock_character

        result = self.character_interactor.select_character("user1", "guild1", "char_id")

        self.assertEqual(result.name, "Primary Character")
        self.mock_repository.set_primary.assert_called_once_with("user1", "guild1", "char_id")

    def test_select_character_raises_exception(self):
        self.mock_repository.set_primary.return_value = None

        with self.assertRaises(exceptions.CharacterImportError):
            self.character_interactor.select_character("user1", "guild1", "char_id")
