from enum import IntEnum


class ParameterType(IntEnum):
    """  An enumeration that represents the types of parameters in a model. """

    FIXED = 1
    """ Parameters that consider a single/fixed value """

    BOUNDED = 2
    """ Parameters that consider a lower and upper limit """
