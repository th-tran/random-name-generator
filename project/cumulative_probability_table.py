"""Module for CumulativeProbabilityTable. Extends ProbabilityTable."""

from project.probability_table import ProbabilityTable

class CumulativeProbabilityTable(ProbabilityTable):
    """
    In a cumulative table, the probability percentages for keys starting with the same letter are
    cumulative with the last key of the group having a probability of 1.0.
    """

    cumulative_strategy = None

    def __init__(self, letter_length_strategy, cumulative_strategy, input_loader):
        super().__init__(letter_length_strategy, input_loader)
        self.cumulative_strategy = cumulative_strategy

    def load(self, data_name):
        super().load(data_name)
        self.cumulative_strategy.execute(self.frequencies)
