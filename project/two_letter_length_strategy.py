"""This module implements the two letter length strategy for pair probability tables."""

from collections import defaultdict
import json

class TwoLetterLengthStrategy:
    """
    This class implements the two letter length strategy to generate frequencies from given data
    to load into probability tables.
    """

    @classmethod
    def create_frequencies(cls, data):
        """
        Create a dictionary that contains each pair of characters in the data and
        the frequency of this single pair of characters against all other pairs
        of characters starting with the same letter.

        Parameters
        ----------
        data: string
              A string containing the characters from which to build a probability table.
        """
        occurrences = cls.count_occurrences(data)
        #print(occurrences)

        regular_occurrences = {k:v for (k, v) in occurrences.items() if k[1] != ' '}
        word_ending_occurrences = {k:v for (k, v) in occurrences.items() if k[1] == ' '}

        frequencies = dict()
        frequencies = defaultdict(lambda: 0, frequencies)

        # Fill frequencies with all the keys contained in occurrences and
        # values being {value_in_occurrences_for_this_pair /
        # value_in_occurrences_for_all_pairs_starting_with_same_letter}
        if occurrences:
            # Do this for all pairs except those ending with a space
            for key, value in regular_occurrences.items():
                same_start_occurrences = {k:v for (k, v) in regular_occurrences.items()
                                          if k[0] == key[0]}
                #print(same_start_occurrences)
                frequencies[key] = value / sum(same_start_occurrences.values())
            # Now treat the pairs ending with a space as a special case
            for key, value in word_ending_occurrences.items():
                frequencies[key] = value / sum(word_ending_occurrences.values())
        #print(frequencies)
        #print("TWO LETTER")
        #print(json.dumps(frequencies, sort_keys=True, indent=4))
        return frequencies

    @classmethod
    def count_occurrences(cls, data):
        """
        Creates a dictionary that contains the count of how many times each pair of characters
        occur in the data.

        Parameters
        ----------
        data: string
              A string containing the characters from which to build a probability table.
        """
        occurrences = dict()
        occurrences = defaultdict(lambda: 0, occurrences)

        last_char_read = None
        for char in data:
            if last_char_read is not None:
                #print(last_char_read + char)
                occurrences[last_char_read + char] += 1
            last_char_read = char

        return occurrences
