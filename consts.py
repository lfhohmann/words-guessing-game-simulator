#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


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
