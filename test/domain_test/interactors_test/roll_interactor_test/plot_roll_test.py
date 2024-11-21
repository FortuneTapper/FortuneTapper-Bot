import unittest
from unittest.mock import patch
from domain.interactors.roll_interactor import plot_roll, PlotDieResultType

class TestPlotRoll(unittest.TestCase):

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