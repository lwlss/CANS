"""Clases for the representation of microbial cultures."""

class Culture:
    """A culture with an amount of cells, nutrients, and signal."""
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
