"""This module implements the three letter length strategy for triplet probability tables."""

from collections import defaultdict
import json

class ThreeLetterLengthStrategy:
    """
    This class implements the three letter length strategy to generate frequencies from given data
    to load into probability tables.
    """

    def create_frequencies(self, data):
        """
        Create a dictionary that contains triplet of characters in the data and
        the frequency of this single triplet of characters against all other triplets
        of characters starting with the same first two letters.

        Parameters
        ----------
        data: string
              A string containing the characters from which to build a probability table.
        """
        occurrences = self.count_occurrences(data)
        occurrences = {k:v for (k, v) in occurrences.items() if k[1] != ' '}

        regular_occurrences = {k:v for (k, v) in occurrences.items() if k[2] != ' '}
        word_ending_occurrences = {k:v for (k, v) in occurrences.items() if k[2] == ' '}

        frequencies = dict()
        frequencies = defaultdict(lambda: 0, frequencies)

        # Fill frequencies with all the keys contained in occurrences and
        # values being {value_in_occurrences_for_this_triplet /
        # value_in_occurrences_for_all_triplets_starting_with_same_two_letters}
        if occurrences:
            # Do this for all triplets except those ending with a space
            for key, value in regular_occurrences.items():
                same_start_occurrences = {k:v for (k, v) in regular_occurrences.items()
                                          if k[0] == key[0] and k[1] == key[1]}
                #print(same_start_occurrences)
                frequencies[key] = value / sum(same_start_occurrences.values())
            # Now treat the pairs ending with a space as a special case
            for key, value in word_ending_occurrences.items():
                same_first_letter_occurrences = {k:v for (k, v) in word_ending_occurrences.items()
                                                 if k[0] == key[0]}
                frequencies[key] = value / sum(same_first_letter_occurrences.values())

        #print("THREE LETTER")
        #print(json.dumps(frequencies, sort_keys=True, indent=4))
        return frequencies

    @staticmethod
    def count_occurrences(data):
        """
        Creates a dictionary that contains the count of how many times each pair of character
        occurs in the data.

        Parameters
        ----------
        data: string
              A string containing the characters from which to build a probability table.
        """
        occurrences = dict()
        occurrences = defaultdict(lambda: 0, occurrences)

        last_char_read = None
        second_to_last_char_read = None
        for char in data:
            if None not in (last_char_read, second_to_last_char_read):
                #print(last_char_read + char)
                occurrences[second_to_last_char_read + last_char_read + char] += 1
            second_to_last_char_read = last_char_read
            last_char_read = char

        return occurrences
