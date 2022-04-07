#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the core simulator for games like Wordle, Quordle, Octordle, Term.ooo and etc...
"""

from consts import *

# TODO: Return a list of letters and their status (excluded, included, correct or unknown), for each attempt
# TODO: Implement 'Hard Mode'
# TODO: Return 'player_guess'?


__author__ = "Lucas Hohmann"
__email__ = "lfhohmann@gmail.com"
__user__ = "@lfhohmann"

__date__ = "2022/04/07"
__status__ = "Production"
__version__ = "1.0.0"
__license__ = "MIT"


class GameCore:
    """This is the main class for the Game Core"""

    def __init__(
        self,
        solution: str,
        hard_mode: bool,
        max_attempts: int,
        valid_guesses: list,
        valid_answers: list,
    ) -> None:

        """
        Wordle game constructor

        ARGUMENTS:
        -----------

        solution: str (required)
            A word for the game's solution

        hard_mode: bool (required)
            Wether or not to enable 'Hard Mode'

        max_attempts: int (required)
            The maximum number of attempts the player can make

        valid_guesses: list (required)
            Valid guesses for the game

        valid_answers: list (required)
            Valid answers for the game

        RETURNS:
        --------

        output: None
        """

        # Store arguments
        self.solution = solution
        self.hard_mode = hard_mode
        self.max_attempts = max_attempts
        self.valid_guesses = valid_guesses
        self.valid_answers = valid_answers

        # Store length of solution in a variable, so we won't have to call len() every time
        self.words_length = len(self.solution)

        # Init guess validness and game state
        self.guess_validness = GuessValidness.undefined
        self.state = State.running

        # Init attempt counter
        self.attempt = 0

    def __response(self) -> dict:
        """
        Standardize the response of the game

        RETURNS:
        --------

        output: dict
            The values that need to be returned by the 'play()' method
        """

        # letters = {
        #     "keys": list(self.letters.keys()),
        #     "values": [value.value for value in self.letters.values()],
        # }

        return {
            "state": self.state.value,
            "guess_validness": self.guess_validness.value,
            "attempt": self.attempt,
            "positions": [position.value for position in self.positions],
            # "letters": list(zip(letters["keys"], letters["values"])),
        }

    def play(self, player_guess: str) -> dict:
        """
        Execute an attempt at guessing the correct solution

        ARGUMENTS:
        -----------

        player_guess: str (required)
            The word guessed by the player

        RETURNS:
        --------

        output: dict
            Returns the value returned by the '__response()' method
        """

        # Init 'positions'
        self.positions = [PositionStatus.undefined for _ in range(self.words_length)]

        # Check whether game is over
        if self.state != State.running:
            self.guess_validness = GuessValidness.undefined

            return self.__response()

        # Check whether "player_guess" is valid
        elif player_guess not in self.valid_guesses + self.valid_answers:
            self.guess_validness = GuessValidness.invalid

            return self.__response()

        # Player guess is valid, increment attempt counter
        self.guess_validness = GuessValidness.valid
        self.attempt += 1

        # Pre fill positions
        for i in range(self.words_length):
            if player_guess[i] == self.solution[i]:
                self.positions[i] = PositionStatus.correct

            elif player_guess[i] in self.solution:
                self.positions[i] = PositionStatus.included

            else:
                self.positions[i] = PositionStatus.undefined

        #! Refactor this
        # Count number of element occurances in solution's word
        chars = {}
        for char in self.solution:
            if char not in chars:
                chars[char] = self.solution.count(char)

        #! Refactor this
        # Remove extra occurrances of elements from positions - part 1
        for i in range(self.words_length):
            if self.positions[i] == PositionStatus.correct:
                chars[player_guess[i]] -= 1

        #! Refactor this
        # Remove extra occurrances of elements from positions - part 2
        for i in range(self.words_length):
            if self.positions[i] == PositionStatus.included:
                chars[player_guess[i]] -= 1

                if chars[player_guess[i]] < 0:
                    self.positions[i] = PositionStatus.undefined

        # Check if the number of attempts is over
        if self.attempt >= self.max_attempts:
            self.state = State.loose

        # Check if the correct word was guessed
        if self.positions == [PositionStatus.correct for _ in range(self.words_length)]:
            self.state = State.win

        # Standard response for when the guess is valid
        return self.__response()
