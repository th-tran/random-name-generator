"""This module implements the two letter cumulative strategy for cumulative pair probablity tables."""

from project.util.cumulative_roundoff import roundoff

class TwoLetterCumulativeStrategy:
    """
    This class transforms given frequencies (generated by the two letter length strategy) into
    cumulative frequencies.
    """

    @classmethod
    def execute(cls, frequencies):
        """
        Will transform a non-cumulative probability table using two-letter pairs into a
        cumulative probability table using pairs. In a cumulative table, the probability percentages
        for keys starting with the same letter are cumulative with the last key of the group
        having a probability of 1.0.
        """

        last_key_read = ""
        cumulative_value = 0.0

        regular_keys = sorted(list({k:v for (k, v) in frequencies.items() if k[1] != ' '}.keys()))
        # Do this for all keys except those ending with a space
        for key in regular_keys:
            if last_key_read and last_key_read[0] != key[0]:
                cumulative_value = 0.0
            cumulative_value += frequencies[key]
            cumulative_value = roundoff(cumulative_value)
            frequencies[key] = cumulative_value
            last_key_read = key
        # Now treat the keys ending with a space as a special case
        cumulative_value = 0.0
        word_ending_keys = sorted(list({k:v for (k, v) in frequencies.items() if k[1] == ' '}.keys()))
        for key in word_ending_keys:
            cumulative_value += frequencies[key]
            cumulative_value = roundoff(cumulative_value)
            frequencies[key] = cumulative_value
