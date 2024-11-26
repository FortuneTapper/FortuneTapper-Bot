import unittest
from unittest.mock import MagicMock, patch
from domain.entities import Character, Resources, Resource, ResourceType
from adapter.gateways.character_repository.caching_character_repository import CachingCharacterRepository
from domain.interactors import ResourceInteractor

class TestResourceManager(unittest.TestCase):
    def setUp(self):
        # Mock del repositorio
        self.mock_repository = MagicMock(spec=CachingCharacterRepository)
        self.resource_interactor = ResourceInteractor(repository=self.mock_repository)

    def test_set_resource(self):
        mock_character : Character = MagicMock()
        mock_character.resources = Resources(
            health=Resource(max=10, current=5),
            focus=Resource(max=5, current=4),
            investiture=Resource(max=3, current=3)
        )
        
        self.mock_repository.get.return_value = mock_character

        resource: Resource = self.resource_interactor.set_current_resource(
            user_id=0,
            guild_id=0,
            resource=ResourceType.HEALTH, 
            amount = 2
        )
        self.assertEqual(resource.current, 2)
        self.assertEqual(resource.max, 10)

        resource: Resource  = self.resource_interactor.set_current_resource(
            user_id=0,
            guild_id=0,
            resource=ResourceType.FOCUS, 
            amount = -1
        )
        self.assertEqual(resource.current, 0)
        self.assertEqual(resource.max, 5)

        resource: Resource  = self.resource_interactor.set_current_resource(
            user_id=0,
            guild_id=0,
            resource=ResourceType.INVESTITURE, 
            amount = 4
        )
        self.assertEqual(resource.current, 3)
        self.assertEqual(resource.max, 3)


    def test_modify_current_resource(self):
        mock_character : Character = MagicMock()
        mock_character.resources = Resources(
            health=Resource(max=10, current=5),
            focus=Resource(max=5, current=4),
            investiture=Resource(max=3, current=3)
        )
        
        self.mock_repository.get.return_value = mock_character

        resource: Resource = self.resource_interactor.modify_current_resource(
            user_id=0,
            guild_id=0,
            resource=ResourceType.HEALTH, 
            amount = 2
        )
        self.assertEqual(resource.current, 7)
        self.assertEqual(resource.max, 10)

        resource: Resource = self.resource_interactor.modify_current_resource(
            user_id=0,
            guild_id=0,
            resource=ResourceType.FOCUS, 
            amount = -5
        )
        self.assertEqual(resource.current, 0)
        self.assertEqual(resource.max, 5)

        resource: Resource = self.resource_interactor.modify_current_resource(
            user_id=0,
            guild_id=0,
            resource=ResourceType.INVESTITURE, 
            amount = 1
        )
        self.assertEqual(resource.current, 3)
        self.assertEqual(resource.max, 3)
