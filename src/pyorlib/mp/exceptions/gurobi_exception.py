from src.pyorlib.core.exceptions import CoreException


class GurobiException(CoreException):
    """
    An exception class for handling errors related to the Gurobi Optimization library.

    The GurobiException class is a subclass of the CoreException class and is used to handle
    exceptions specific to the Gurobi library.
    """

    def __init__(self, message: str = ""):
        super().__init__(message if message else "Gurobi exception")