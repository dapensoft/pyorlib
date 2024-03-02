from ..core.exceptions import PyORlibException


class CplexException(PyORlibException):
    """
    An exception class for handling errors related to the IBM ILOG CPLEX optimization library.

    The CplexException class is a subclass of the CoreException class and is used to handle
    exceptions specific to the CPLEX library.
    """

    def __init__(self, message: str = "CPLEX Exception"):
        super().__init__(message)
