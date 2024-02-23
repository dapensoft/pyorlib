from ..core.exceptions import PyORlibException


class ORToolsException(PyORlibException):
    """
    An exception class for handling errors related to the OR-Tools library.

    The ORToolsException class is a subclass of the CoreException class and is used to handle
    exceptions specific to the OR-Tools library.
    """

    def __init__(self, message: str = "OR-Tools exception"):
        super().__init__(message)
