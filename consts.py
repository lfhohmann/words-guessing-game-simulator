#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class PositionStatus(Enum):
    """Class representing the status of a position"""

    correct = "c"  # Letter in correct position
    included = "i"  # Letter in position included
    undefined = "_"  # Letter in position is undefined


class LetterStatus(Enum):
    """Class representing the status of a letter"""

    correct = "c"  # Letter in correct position
    included = "i"  # Letter is included
    excluded = "e"  # Letter is excluded
    undefined = "_"  # Letter is undefined


class State(Enum):
    """Class representing the game state"""

    running = "p"  # Game in progress
    loose = "l"  # Game lost
    win = "w"  # Game won


class GuessValidness(Enum):
    """Class representing the guess validness"""

    undefined = "_"  # Guess validness is undefined
    invalid = "i"  # Guess validness is invalid
    valid = "v"  # Guess validness is valid
