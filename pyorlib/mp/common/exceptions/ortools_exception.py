from pyorlib.core.exceptions import CoreException


class ORToolsException(CoreException):

    def __init__(self, message: str = ""):
        super().__init__(message if message else "OR-Tools exception")