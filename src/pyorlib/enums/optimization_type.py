from enum import IntEnum


class OptimizationType(IntEnum):
    """
    An enumeration class representing the type of optimization to be performed.

    This class extends the `IntEnum` class and provides two options for
    optimization types: MINIMIZE and MAXIMIZE.
    """

    MINIMIZE = 1
    """ Represents a minimization problem. """

    MAXIMIZE = 2
    """ Represents a maximization problem. """
