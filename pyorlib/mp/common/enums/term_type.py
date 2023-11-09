from enum import IntEnum


class TermType(IntEnum):
    """
    An enumeration class representing the types of terms in the context of an optimization model.

    The TermType class provides a set of predefined types that categorize terms according to their behavior.
    """

    CONSTANT = 1
    """ Represents a constant term. """

    VARIABLE = 2
    """ Represents a variable term. """
