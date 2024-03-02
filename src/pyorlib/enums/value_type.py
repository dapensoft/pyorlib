from enum import IntEnum


class ValueType(IntEnum):
    """
    An enumeration class representing the type of value that a parameter or term can take in the context of
    an optimization model.

    The ValueType class provides a set of predefined types that categorize the values that a parameter
    or term can have. These types help describe the nature of the values and guide the optimization
    algorithm or mathematical modeling techniques.
    """

    BINARY = 1
    """ Represents a binary value (0 or 1). """

    INTEGER = 2
    """ Represents an integer value. """

    CONTINUOUS = 3
    """ Represents a continuous value. """
