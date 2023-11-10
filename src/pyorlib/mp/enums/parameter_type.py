from enum import IntEnum


class ParameterType(IntEnum):
    """
    An enumeration class representing the types of parameters in an optimization model.

    Parameters can be categorized as either FIXED, representing parameters under certainty with a single/fixed
    value, or BOUNDED, representing parameters under uncertainty with a lower and upper limit.
    """

    FIXED = 1
    """ Represents parameters under certainty with a single/fixed value. """

    BOUNDED = 2
    """ Represents parameters under uncertainty with a lower and upper limit. """
