"""This module contains the business logic to generate random names."""

import random
from project.two_letter_length_strategy import TwoLetterLengthStrategy
from project.three_letter_length_strategy import ThreeLetterLengthStrategy
from project.two_letter_cumulative_strategy import TwoLetterCumulativeStrategy
from project.three_letter_cumulative_strategy import ThreeLetterCumulativeStrategy
from project.cumulative_probability_table import CumulativeProbabilityTable
from project.util.data_loader import FileDataLoader

class RandomNameGenerator:
    """
    Driver class to generate random names.
    """

    generated_names = list()
    pair_pr_table = None
    triplet_pr_table = None
    pair_pr_table_keys = None
    triplet_pr_table_keys = None

    def __init__(self, params):
        # Initialize probability table dependencies
        two_letter_length_strategy = TwoLetterLengthStrategy()
        three_letter_length_strategy = ThreeLetterLengthStrategy()
        two_letter_cumulative_strategy = TwoLetterCumulativeStrategy()
        three_letter_cumulative_strategy = ThreeLetterCumulativeStrategy()
        file_data_loader = FileDataLoader()

        # Initialize pair probability table
        self.pair_pr_table = CumulativeProbabilityTable(
            two_letter_length_strategy, two_letter_cumulative_strategy, file_data_loader)
        self.pair_pr_table.load('media/' + params.get('file') + '.txt')
        self.pair_pr_table_keys = self.pair_pr_table.frequencies.keys()

        # Initialize triplet probability table
        self.triplet_pr_table = CumulativeProbabilityTable(
            three_letter_length_strategy, three_letter_cumulative_strategy, file_data_loader)
        self.triplet_pr_table.load('media/' + params.get('file') + '.txt')
        self.triplet_pr_table_keys = self.triplet_pr_table.frequencies.keys()

    def generate(self):
        """
        Generate a new random name.
        """
        # Start generating name
        name = ' ' + self._get_starting_letter()
        # Since the name already has a starting letter, the total name length will be
        # one more than the selected name_length_distribution selected
        name_length_distribution = [3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 7, 8, 9]
        desired_length = name_length_distribution[random.randint(0, 12)]
        for _ in range(desired_length - 1):
            name += self._get_next_letter(name[len(name) - 2], name[len(name) - 1])
        name += self._get_last_letter(name[len(name) - 2], name[len(name) - 1])
        name = name.strip().capitalize()
        self.generated_names.append(name)

    def _get_starting_letter(self):
        """
        Return the starting letter for a new random name, or alternatively a new random letter
        when we do not have any information from previous letters.
        (i.e. missing pairs in sample data)
        """
        random_number = random.uniform(0, 1)
        starting_letter = sorted({k:v for (k, v) in self.pair_pr_table.frequencies.items()
                                  if k[0] == ' '
                                  and k[1] != ' '
                                  and v >= random_number}.keys())[0][1]
        return starting_letter

    def _get_next_letter(self, second_to_last_letter, last_letter):
        """
        Return the next letter in random name when we have both the first and second letter defined.
        Parameters
        ----------
        second_to_last_letter: char
                               Current second-to-last letter in name.
        last_letter: char
                     Current last letter in name.
        """
        random_number = random.uniform(0, 1)
        next_letter = None
        if any(key[0] == second_to_last_letter and key[1] == last_letter and key[2] != ' '
               for key in self.triplet_pr_table_keys):
            # Determine next letter based on triplets
            next_letter = sorted({k:v for (k, v) in self.triplet_pr_table.frequencies.items()
                                  if k[0] == second_to_last_letter
                                  and k[1] == last_letter
                                  and k[2] != ' '
                                  and v >= random_number}.keys())[0][2]
        elif any(key[0] == last_letter and key[1] != ' ' for key in self.pair_pr_table_keys):
            # Determine next letter based on pairs
            next_letter = sorted({k:v for (k, v) in self.pair_pr_table.frequencies.items()
                                  if k[0] == last_letter
                                  and k[1] != ' '
                                  and v >= random_number}.keys())[0][1]
        else:
            # Generate a random letter
            next_letter = self._get_starting_letter()
        return next_letter

    def _get_last_letter(self, second_to_last_letter, last_letter):
        """
        Return the last letter in random name when all other letters are defined.
        Parameters
        ----------
        second_to_last_letter: char
                               Second-to-last letter in name.
        last_letter: char
                     Last letter in name.
        """
        random_number = random.uniform(0, 1)
        # Try to get last letter using triplets starting with last_letter
        if any(key[0] == last_letter and key[2] == ' '
               for key in self.triplet_pr_table_keys):
            new_last_letter = sorted({k:v for (k, v) in self.triplet_pr_table.frequencies.items()
                                      if k[0] == last_letter
                                      and k[2] == ' '
                                      and v >= random_number}.keys())[0][1]
            return new_last_letter
        # Try to get a triplet that starts with last_letter, has it's second letter be
        # the first letter in space ending triplet and does not end with a space
        valid_letters = map(lambda k: k[0], [key for key in self.triplet_pr_table_keys
                                             if key[2] == ' '])
        if any(key[0] == last_letter and key[1] == letter
               for (key, letter) in zip(self.pair_pr_table_keys, valid_letters)):
            new_last_letter = sorted({k:v for (k, v) in self.pair_pr_table.frequencies.items()
                                      if k[0] == last_letter
                                      and any(k[1] == letter for letter in valid_letters)
                                      and v >= random_number}.keys())[0][1]
            return new_last_letter + self._get_last_letter(new_last_letter, second_to_last_letter)
        # If all else fails, try using regular get_next_letter
        return self._get_next_letter(second_to_last_letter, last_letter)
