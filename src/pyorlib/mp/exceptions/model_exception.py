from src.pyorlib.core.exceptions import PyORlibException


class ModelException(PyORlibException):
    """
    An exception class for handling errors related to the execution
    or handling of an optimization model.
    """

    def __init__(self, message: str = ""):
        super().__init__(message if message else "Model exception")
