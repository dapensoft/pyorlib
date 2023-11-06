from pyorlib.core.exceptions import CoreException


class ModelException(CoreException):

    def __init__(self, message: str = ""):
        super().__init__(message if message else "Model exception")
