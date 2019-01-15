"""Module for ProbabilityTable."""

class ProbabilityTable:
    """
    Represents the probability of a group of letters composed of 1..* letters being followed by
    another letter N.
    """

    frequencies = None
    _letter_length_strategy = None
    _data_loader = None

    def __init__(self, letter_length_strategy, data_loader):
        self.frequencies = dict()
        self._letter_length_strategy = letter_length_strategy
        self._data_loader = data_loader

    def empty(self):
        """
        Helper method to check if the table is empty.
        """
        if self.frequencies is None:
            return None
        return len(self.frequencies) == 0

    def load(self, data_name):
        """
        Helper method to load from a file that follows the expected format of data loader.
        """
        data = self._data_loader.load(data_name)
        self.frequencies = self._letter_length_strategy.create_frequencies(data)
