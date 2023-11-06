from pyorlib.core.exceptions import CoreException


class CplexException(CoreException):

    def __init__(self, message: str = ""):
        super().__init__(message if message else "Cplex exception")
