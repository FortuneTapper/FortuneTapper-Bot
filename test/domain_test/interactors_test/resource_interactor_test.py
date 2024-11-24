import unittest
from unittest.mock import MagicMock, patch
from domain.entities.character import Character, Resources, Resource, ResourceType
from domain.interactors import resource_interactor

class TestResourceManager(unittest.TestCase):
    @patch("domain.interactors.character_interactor.config.repository.save")
    @patch("domain.interactors.character_interactor.config.repository.get")
    def test_set_resource(self, mock_get, mock_save):
        mock_character : Character = MagicMock()
        mock_character.resources = Resources(
            health=Resource(max=10, current=5),
            focus=Resource(max=5, current=4),
            investiture=Resource(max=3, current=3)
        )
        
        mock_get.return_value = mock_character

        character = resource_interactor.set_current_resource(
            user_id=0,
            guild_id=0,
            resource=ResourceType.HEALTH, 
            amount = 2
        )
        self.assertEqual(character.resources.health.current, 2)
        self.assertEqual(character.resources.health.max, 10)

        character = resource_interactor.set_current_resource(
            user_id=0,
            guild_id=0,
            resource=ResourceType.FOCUS, 
            amount = -1
        )
        self.assertEqual(character.resources.focus.current, 0)
        self.assertEqual(character.resources.focus.max, 5)

        character = resource_interactor.set_current_resource(
            user_id=0,
            guild_id=0,
            resource=ResourceType.INVESTITURE, 
            amount = 4
        )
        self.assertEqual(character.resources.investiture.current, 3)
        self.assertEqual(character.resources.investiture.max, 3)

    @patch("domain.interactors.character_interactor.config.repository.save")
    @patch("domain.interactors.character_interactor.config.repository.get")
    def test_modify_current_resource(self, mock_get, mock_save):
        mock_character : Character = MagicMock()
        mock_character.resources = Resources(
            health=Resource(max=10, current=5),
            focus=Resource(max=5, current=4),
            investiture=Resource(max=3, current=3)
        )
        
        mock_get.return_value = mock_character

        character = resource_interactor.modify_current_resource(
            user_id=0,
            guild_id=0,
            resource=ResourceType.HEALTH, 
            amount = 2
        )
        self.assertEqual(character.resources.health.current, 7)
        self.assertEqual(character.resources.health.max, 10)

        character = resource_interactor.modify_current_resource(
            user_id=0,
            guild_id=0,
            resource=ResourceType.FOCUS, 
            amount = -5
        )
        self.assertEqual(character.resources.focus.current, 0)
        self.assertEqual(character.resources.focus.max, 5)

        character = resource_interactor.modify_current_resource(
            user_id=0,
            guild_id=0,
            resource=ResourceType.INVESTITURE, 
            amount = 1
        )
        self.assertEqual(character.resources.investiture.current, 3)
        self.assertEqual(character.resources.investiture.max, 3)
