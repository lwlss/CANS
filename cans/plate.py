"""Classes for the representation of agar plates."""

from culture import Culture


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
        cultures : list[Culture]
            A list of rows*cols Culture objects.
        """
        self.rows = rows
        self.cols = cols
        self.cultures = []
        for culture in range(rows*cols):
            self.cultures.append(Culture())


    def sim_growth(self):
        pass


if __name__ == "__main__":
    plate1 = Plate()
    print(plate1.rows)
    print(plate1.cols)
    print(plate1.cultures)
    print(plate1.cultures[0].cells)
    print(plate1.cultures[0].nutrients)
    print(plate1.cultures[0].signal)
    print(len(plate1.cultures))
