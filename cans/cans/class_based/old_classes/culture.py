"""Clases for the representation of microbial cultures."""
import random


class Culture:
    """A culture with an amount of cells, nutrients, and signal."""
    def __init__(self, cells=0.1, nutrients=1.0, signal=0.0,
                 r=1, b=0.1, a=0.1):
        """Initialise culture.

        Parameters
        ----------
        cells : Optional[float]
            Initial amount of cells (default 0.1)
        nutrients : Optional[float]
            Initial amount of cells (default 1.0)
        signal : Optional[float]
            Initial amount of signal (default 0.0)
        """
        self.cells = cells
        self.nutrients = nutrients
        self.signal = signal
        self.r = r    # Growth rate constant
        self.b = b    # Signal on cells effect constant
        self.a = a    # Signal secretion constant


class RandomCulture(Culture):
    """A culture with random parameter values r, b, and a."""
    def __init__(self, cells=0.1, nutrients=1.0, signal=0.0):
        """Initialise culture.

        Parameters
        ----------
        cells : Optional[float]
            Initial amount of cells (default 0.1)
        nutrients : Optional[float]
            Initial amount of cells (default 1.0)
        signal : Optional[float]
            Initial amount of signal (default 0.0)
        """
        self.cells = cells
        self.nutrients = nutrients
        self.signal = signal
        self.r = max(0.0, random.gauss(1.0, 1.0))   # Growth rate constant
        self.b = 0.05   # Signal on cells effect constant
        self.a = 0.05    # Signal secretion constant


if __name__ == '__main__':
    culture1 = Culture()
    rand_culture = RandomCulture()