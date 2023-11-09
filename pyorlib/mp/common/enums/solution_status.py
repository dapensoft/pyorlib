from enum import IntEnum


class SolutionStatus(IntEnum):
    """
    Enumerates the possible solution statuses for an optimization model.

    The SolutionStatus class provides a set of predefined statuses that describe the outcome of an
    optimization model. These statuses can be used to determine the quality and feasibility of
    the obtained solution.
    """

    OPTIMAL = 1
    """ The model has been solved to optimality. """

    FEASIBLE = 2
    """ The model has been solved but may not be optimal. """

    INFEASIBLE = 3
    """ The model has been proven to be infeasible. """

    NOT_SOLVED = 4
    """ The model has not been solved yet. """

    ERROR = 5
    """ The solver terminated abnormally with some errors. """
