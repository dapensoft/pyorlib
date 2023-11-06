from enum import IntEnum


class TermType(IntEnum):
    """
    The TermType class is an enumeration representing the type of term
    that a parameter, variable or constant can be.
    """

    CONSTANT = 1
    """ Represents a constant term. """

    VARIABLE = 2
    """ Represents a variable term. """
