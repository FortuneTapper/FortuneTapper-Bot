import unittest
from unittest.mock import patch
import domain.interactors.roll_interactor as interactor
import domain.entities.roll_result as entities



class TestAttackRoll(unittest.TestCase):
    @patch('domain.interactors.roll_interactor.skill_test')
    def test_basic_attack_roll(self, mock_skill_test):
        mock_skill_test.return_value.roll_result.total = 20
        mock_skill_test.return_value.plot_die_result = None

        result = interactor.attack_roll(damage_expr="2d6", modifier=2)

        self.assertIsInstance(result, entities.AttackResult)
        self.assertEqual(result.hit_result.roll_result.total, 20)
        self.assertEqual(result.damage_result.roll_result.total, 20)

    @patch('domain.interactors.roll_interactor.skill_test')
    def test_attack_roll_with_advantage(self, mock_skill_test):
        mock_skill_test.return_value.roll_result.total = 25
        mock_skill_test.return_value.plot_die_result = None

        result = interactor.attack_roll(
            damage_expr="2d6",
            modifier=3,
            advantage=entities.AdvantageType.ADVANTAGE,
            damage_advantage=entities.AdvantageType.ADVANTAGE,
        )

        self.assertIsInstance(result, entities.AttackResult)
        self.assertEqual(result.hit_result.roll_result.total, 25)
        self.assertEqual(result.damage_result.roll_result.total, 25)

    @patch('domain.interactors.roll_interactor.skill_test')
    def test_attack_roll_with_plot_die(self, mock_skill_test):
        mock_skill_test.return_value.roll_result.total = 22
        mock_skill_test.return_value.plot_die_result = None

        result = interactor.attack_roll(damage_expr="2d6", modifier=2, plot_die=True)

        self.assertIsInstance(result, entities.AttackResult)
        self.assertEqual(result.hit_result.roll_result.total, 22)
        self.assertEqual(result.damage_result.roll_result.total, 22)
