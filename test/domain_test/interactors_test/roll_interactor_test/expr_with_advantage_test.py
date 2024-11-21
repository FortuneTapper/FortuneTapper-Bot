import unittest
from domain.entities.roll_result import AdvantageType
from domain.interactors.roll_interactor import expr_with_advantage


class TestExprWithAdvantage(unittest.TestCase):
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