from enum import IntEnum


class OptimizationType(IntEnum):
    """  The OptimizationType class is an enumeration representing the type of optimization to be performed. """

    MINIMIZE = 1
    """ Represents a minimization problem. """

    MAXIMIZE = 2
    """ Represents a maximization problem. """
