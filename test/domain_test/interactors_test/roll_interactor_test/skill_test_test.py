import unittest
from unittest.mock import patch
from domain.interactors.roll_interactor import skill_test, plot_roll
from domain.entities.roll_result import AdvantageType, SkillTestResult


class TestSkillTest(unittest.TestCase):

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
