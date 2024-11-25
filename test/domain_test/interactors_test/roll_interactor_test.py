import unittest
from unittest.mock import patch, MagicMock
from domain.entities.roll_result import AdvantageType, SkillTestResult, PlotDieResultType, AttackResult
from domain.interactors.roll_interactor import RollInteractor
from domain.entities import SkillType
from adapter.gateways.character_repository.caching_character_repository import CachingCharacterRepository


class TestRollInteractor(unittest.TestCase):
    def setUp(self):
        # Mock del repositorio
        self.mock_repository = MagicMock(spec=CachingCharacterRepository)
        self.roll_interactor = RollInteractor(repository=self.mock_repository)

    def test_no_advantage(self):
        self.assertEqual(self.roll_interactor.expr_with_advantage("2d8", AdvantageType.NONE), "2d8")

    def test_advantage_single_die(self):
        self.assertEqual(self.roll_interactor.expr_with_advantage("1d8", AdvantageType.ADVANTAGE), "2d8kh1")

    def test_advantage_multiple_dice(self):
        self.assertEqual(self.roll_interactor.expr_with_advantage("3d8", AdvantageType.ADVANTAGE), "2d8kh1+2d8")

    def test_disadvantage_single_die(self):
        self.assertEqual(self.roll_interactor.expr_with_advantage("1d8", AdvantageType.DISADVANTAGE), "2d8kl1")

    def test_disadvantage_multiple_dice(self):
        self.assertEqual(self.roll_interactor.expr_with_advantage("3d8", AdvantageType.DISADVANTAGE), "2d8kl1+2d8")

    def test_invalid_format(self):
        with self.assertRaises(AssertionError):
            self.roll_interactor.expr_with_advantage("invalid", AdvantageType.ADVANTAGE)

    @patch('d20.roll')
    def test_plot_roll_complication(self, mock_roll):
        mock_roll.return_value.total = 2

        result = self.roll_interactor.plot_roll()
        self.assertEqual(result.type, PlotDieResultType.COMPLICATION)
        self.assertEqual(result.plus, 4)  # 2 * 2

    @patch('d20.roll')
    def test_plot_roll_opportunity(self, mock_roll):
        mock_roll.return_value.total = 5

        result = self.roll_interactor.plot_roll()
        self.assertEqual(result.type, PlotDieResultType.OPPORTUNITY)
        self.assertEqual(result.plus, 0)

    @patch('d20.roll')
    def test_plot_roll_none(self, mock_roll):
        mock_roll.return_value.total = 4

        result = self.roll_interactor.plot_roll()
        self.assertEqual(result.type, PlotDieResultType.NONE)
        self.assertEqual(result.plus, 0)

    @patch('d20.roll')
    def test_skill_test(self, mock_roll):
        self.mock_repository.get.return_value.skills.get_skill_by_type.return_value.modifier = 2
        mock_roll.return_value.result = "1d20 + 2 = 15"

        result = self.roll_interactor.skill_test(
            user_id="user1",
            guild_id="guild1",
            skill=SkillType.ATHLETICS,
            advantage=AdvantageType.NONE,
            plot_die=False
        )

        self.assertIsInstance(result, SkillTestResult)
        self.assertRegex(result.roll_result.result, r'1d20 \+ 2 = .*')
        self.assertIsNone(result.plot_die_result)

    @patch('d20.roll')
    @patch('domain.interactors.roll_interactor.RollInteractor.plot_roll')
    def test_attack_roll(self, mock_plot_roll, mock_roll):
        self.mock_repository.get.return_value.skills.get_skill_by_type.return_value.modifier = 3
        mock_roll.return_value.total = 10
        mock_plot_roll.return_value.plus = 4

        result = self.roll_interactor.attack_roll(
            user_id="user1",
            guild_id="guild1",
            damage_expr="2d6",
            skill=SkillType.HEAVY_WEAPONS,
            advantage=AdvantageType.ADVANTAGE,
            damage_advantage=AdvantageType.ADVANTAGE,
            plot_die=True,
            plot_die_damage=True
        )

        self.assertIsInstance(result, AttackResult)
        self.assertEqual(result.hit_result.roll_result.total, 10)
        self.assertIsNotNone(result.damage_result.plot_die_result)
