"""Utility module to load data."""

class FileDataLoader:
    """
    Load the data from a file containing a plain text sample data of names
    separated by spaces.
    """

    def load(self, file):
        """
        Parameters
        ----------
        file: object
              A file containing plain text sample data of names.
        """
        with open(file, 'r') as f:
            data = f.read().replace('\n', '').lower()
        return data
