#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the core simulator for games like Wordle, Quordle, Octordle, Term.ooo and etc...
"""

from enum import Enum


__author__ = "Lucas Hohmann"
__email__ = "lfhohmann@gmail.com"
__user__ = "@lfhohmann"

__date__ = "2022/04/14"
__status__ = "Production"
__version__ = "2.1.0"
__license__ = "MIT"


class Hit(Enum):
    """Class representing the status of a hit"""

    CORRECT = "c"  # Letter is correct
    MISPLACED = "m"  # Letter is misplaced
    INCORRECT = "_"  # Letter is incorrect


class GameState(Enum):
    """Class representing the game state"""

    RUNNING = "r"  # Game running
    LOST = "l"  # Game lost
    WON = "w"  # Game won


class AttemptValidness(Enum):
    """Class representing the attempt validness"""

    INVALID = "i"  # Attempt is invalid
    VALID = "v"  # Attempt is valid


class GameCore:
    """This is the main class for the Game Core"""

    def __init__(
        self,
        max_attempts: int,
        game_solution: str,
        valid_guesses: list,
        valid_answers: list,
    ) -> None:

        """
        Wordle game constructor

        ARGUMENTS:
        -----------

        max_attempts: int (required)
            The maximum number of attempts the player can make

        game_solution: str (required)
            A word for the game's solution

        valid_guesses: list (required)
            Valid guesses for the game

        valid_answers: list (required)
            Valid answers for the game

        RETURNS:
        --------

        output: None
        """

        # Store arguments
        self.max_attempts = max_attempts
        self.game_solution = game_solution
        self.valid_guesses = valid_guesses
        self.valid_answers = valid_answers

        # Store length of the game solution in a variable, so we won't have to call len() every time
        self.words_length = len(self.game_solution)

        # Init attempt validness and game state
        self.attempt_validness = AttemptValidness.INVALID
        self.game_state = GameState.RUNNING

        # Init attempt counter
        self.attempt_number = 0

    def __response(self) -> dict:
        """
        Standardize the response of the game

        RETURNS:
        --------

        output: dict
            The values that need to be returned by the 'play()' method
        """

        return {
            "game_state": self.game_state.value,
            "attempt_validness": self.attempt_validness.value,
            "attempt_number": self.attempt_number,
            "attempt_hits": [hit.value for hit in self.attempt_hits],
        }

    def play(self, attempt_guess: str) -> dict:
        """
        Execute an attempt at guessing the correct solution

        ARGUMENTS:
        -----------

        attempt_guess: str (required)
            The word guessed by the player

        RETURNS:
        --------

        output: dict
            Returns the value returned by the '__response()' method
        """

        # Init attempt hits
        self.attempt_hits = [Hit.INCORRECT for _ in range(self.words_length)]

        # Check whether game is over or attempt guess is invalid
        if (
            self.game_state != GameState.RUNNING
            or attempt_guess not in self.valid_guesses + self.valid_answers
        ):
            self.attempt_validness = AttemptValidness.INVALID

            return self.__response()

        # The attempt guess is valid, increment attempt counter
        self.attempt_validness = AttemptValidness.VALID
        self.attempt_number += 1

        # Init letters counter
        counter = {}
        for letter in set(attempt_guess):
            counter[letter] = self.game_solution.count(letter)

        # Compute attempt hits
        for i in range(self.words_length):

            if attempt_guess[i] == self.game_solution[i]:
                self.attempt_hits[i] = Hit.CORRECT
                counter[attempt_guess[i]] -= 1

            elif counter[attempt_guess[i]] > 0:
                self.attempt_hits[i] = Hit.MISPLACED
                counter[attempt_guess[i]] -= 1

        # Check if the number of attempts is over
        if self.attempt_number >= self.max_attempts:

            self.game_state = GameState.LOST
            return self.__response()

        # Check if the correct word was guessed
        if self.attempt_hits == [Hit.CORRECT for _ in range(self.words_length)]:

            self.game_state = GameState.WON
            return self.__response()

        # Standard response for when the guess is valid
        return self.__response()
