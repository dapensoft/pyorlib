from pyorlib.core.exceptions import CoreException


class ORToolsException(CoreException):
    """
    An exception class for handling errors related to the OR-Tools library.

    The ORToolsException class is a subclass of the CoreException class and is used to handle
    exceptions specific to the OR-Tools library.
    """

    def __init__(self, message: str = ""):
        super().__init__(message if message else "OR-Tools exception")
