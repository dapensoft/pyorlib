from pyorlib.core.exceptions import CoreException


class TermException(CoreException):
    """
    An exception class for handling errors related to terms in an optimization model.

    The TermException class is a subclass of the CoreException class and is used to handle
    exceptions specific to terms in a mathematical model, such as validations.
    """

    def __init__(self, message: str = ""):
        super().__init__(message if message else "Term exception")
