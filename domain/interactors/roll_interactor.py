import d20
from domain.entities import plot_die

def roll(expr: str):
    return d20.roll(expr)

def plot_roll():
    return plot_die.roll()