from ..core.exceptions import PyORlibException


class PuLPException(PyORlibException):
    """
    An exception class for handling errors related to the PuLP library.

    The PuLPException class is a subclass of the CoreException class and is used to handle
    exceptions specific to the PuLP library.
    """

    def __init__(self, message: str = "PuLP exception"):
        super().__init__(message)
