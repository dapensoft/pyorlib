from pyorlib.core.exceptions import CoreException


class TermException(CoreException):

    def __init__(self, message: str = ""):
        super().__init__(message if message else "Term exception")
