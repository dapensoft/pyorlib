from enum import IntEnum


class SolutionStatus(IntEnum):
    """ The SolutionStatus class is an enumeration representing the status of the solution. """

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
