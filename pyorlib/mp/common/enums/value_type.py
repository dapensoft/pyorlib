from enum import IntEnum


class ValueType(IntEnum):
    """ The ValueType class is an enumeration representing the type of value that a parameter can take. """

    BINARY = 1
    """ Represents a binary value. """

    INTEGER = 2
    """ Represents an integer value. """

    CONTINUOUS = 3
    """ Represents a continuous value. """
