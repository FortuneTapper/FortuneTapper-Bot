import unittest
from unittest.mock import patch, MagicMock
from domain.entities.roll_result import AdvantageType, SkillTestResult
from domain.interactors.roll_interactor import expr_with_advantage, plot_roll, PlotDieResultType, skill_test
import domain.interactors.roll_interactor as interactor
import domain.entities.roll_result as entities


class TestRollInteractor(unittest.TestCase):
    def test_no_advantage(self):
        self.assertEqual(expr_with_advantage("2d8", AdvantageType.NONE), "2d8")

    def test_advantage_single_die(self):
        self.assertEqual(expr_with_advantage("1d8", AdvantageType.ADVANTAGE), "2d8kh1")

    def test_advantage_multiple_dice(self):
        self.assertEqual(expr_with_advantage("3d8", AdvantageType.ADVANTAGE), "2d8kh1+2d8")

    def test_disadvantage_single_die(self):
        self.assertEqual(expr_with_advantage("1d8", AdvantageType.DISADVANTAGE), "2d8kl1")

    def test_disadvantage_multiple_dice(self):
        self.assertEqual(expr_with_advantage("3d8", AdvantageType.DISADVANTAGE), "2d8kl1+2d8")

    def test_invalid_format(self):
        with self.assertRaises(AssertionError):
            expr_with_advantage("invalid", AdvantageType.ADVANTAGE)

    @patch('d20.roll')
    def test_plot_roll_complication(self, mock_roll):
        mock_roll.return_value.total = 2
        
        result = plot_roll()
        self.assertEqual(result.type, PlotDieResultType.COMPLICATION)
        self.assertEqual(result.plus, 4)  # 2 * 2

    @patch('d20.roll')
    def test_plot_roll_opportunity(self, mock_roll):
        mock_roll.return_value.total = 5

        result = plot_roll()
        self.assertEqual(result.type, PlotDieResultType.OPPORTUNITY)
        self.assertEqual(result.plus, 0)

    @patch('d20.roll')
    def test_plot_roll_none(self, mock_roll):
        mock_roll.return_value.total = 4

        result = plot_roll()
        self.assertEqual(result.type, PlotDieResultType.NONE)
        self.assertEqual(result.plus, 0)

    def test_no_advantage_no_plot_die(self):
        result = skill_test(expr="1d20", modifier=2)
        
        self.assertIsInstance(result, SkillTestResult)
        self.assertRegex(result.roll_result.result, r'1d20 \(.*?\) \+ 2 = `\d+`')
        self.assertIsNone(result.plot_die_result)

    @patch('domain.interactors.roll_interactor.plot_roll')
    def test_advantage_with_plot_die(self, mock_plot_roll):
        mock_plot_roll.return_value.plus = 4

        result = skill_test(expr="1d20", modifier=3, advantage=AdvantageType.ADVANTAGE, plot_die=True)

        self.assertIsInstance(result, SkillTestResult)
        self.assertRegex(result.roll_result.result, r'2d20kh1 \(.+\) \+ 3 \+ 4 = .+')

    def test_invalid_expr_format(self):
        with self.assertRaises(AssertionError):
            skill_test(expr="invalid")

    @patch('domain.interactors.roll_interactor.skill_test')
    @patch('domain.interactors.roll_interactor.d20.roll')
    def test_basic_attack_roll(self, mock_d20_roll, mock_skill_test):
        mock_skill_test.return_value = MagicMock(
            roll_result=MagicMock(total=20),
            plot_die_result=None
        )
        mock_d20_roll.return_value = MagicMock(total=10)

        result = interactor.attack_roll(damage_expr="2d6", modifier=2)

        self.assertIsInstance(result, entities.AttackResult)
        self.assertEqual(result.hit_result.roll_result.total, 20)
        self.assertEqual(result.damage_result.roll_result.total, 10)
        self.assertEqual(result.damage_result.graze, 8)
        self.assertEqual(result.damage_result.critical, 14)
        self.assertIsNone(result.damage_result.plot_die_result)

    @patch('domain.interactors.roll_interactor.skill_test')
    @patch('domain.interactors.roll_interactor.d20.roll')
    def test_attack_roll_with_advantage(self, mock_d20_roll, mock_skill_test):
        mock_skill_test.return_value = MagicMock(
            roll_result=MagicMock(total=25),
            plot_die_result=None
        )
        mock_d20_roll.return_value = MagicMock(total=12)

        result = interactor.attack_roll(
            damage_expr="2d6",
            modifier=3,
            advantage=entities.AdvantageType.ADVANTAGE,
            damage_advantage=entities.AdvantageType.ADVANTAGE,
        )

        self.assertIsInstance(result, entities.AttackResult)
        self.assertEqual(result.hit_result.roll_result.total, 25)
        self.assertEqual(result.damage_result.roll_result.total, 12)
        self.assertEqual(result.damage_result.graze, 9)
        self.assertEqual(result.damage_result.critical, 15)
        self.assertIsNone(result.damage_result.plot_die_result)


    def test_attack_roll_with_plot_die(self):
        result = interactor.attack_roll(
            damage_expr="2d6",
            modifier=2,
            plot_die=True
        )

        self.assertIsInstance(result, entities.AttackResult)
        self.assertIsNotNone(result.hit_result.plot_die_result)
        self.assertIsNone(result.damage_result.plot_die_result)

    def test_attack_roll_with_plot_die_in_damage(self):
        result = interactor.attack_roll(
            damage_expr="2d6",
            modifier=2,
            plot_die=True,
            plot_die_damage=True
        )
       
        self.assertIsInstance(result, entities.AttackResult)
        self.assertIsNone(result.hit_result.plot_die_result)
        self.assertIsNotNone(result.damage_result.plot_die_result)