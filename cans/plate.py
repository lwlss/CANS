"""Classes for the representation of agar plates."""

class Plate:
    """A simple agar plate containing cultures."""
    def __init__(self, rows=3, cols=3):
        """Initialise plate with an array of cultures.

        Parameters
        ----------
        rows : Optional[int]
            Number of rows (default 3)
        cols : Optional[int]
            Number of columns (default 3)
        """
        self.rows = rows
        self.cols = cols
        cultures = []
