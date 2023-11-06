from pyorlib.core.exceptions import CoreException


class PuLPException(CoreException):

    def __init__(self, message: str = ""):
        super().__init__(message if message else "PuLP exception")
