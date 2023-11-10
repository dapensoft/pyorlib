from src.pyorlib.core.exceptions import CoreException


class CplexException(CoreException):
    """
    An exception class for handling errors related to the IBM ILOG CPLEX optimization library.

    The CplexException class is a subclass of the CoreException class and is used to handle
    exceptions specific to the CPLEX library.
    """

    def __init__(self, message: str = ""):
        super().__init__(message if message else "Cplex exception")