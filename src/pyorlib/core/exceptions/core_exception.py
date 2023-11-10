from typing import List


class CoreException(Exception):
    """
    A common base class for all domain exceptions.

    This class serves as a base class for custom exception classes in a domain-specific application. It provides a
    consistent structure and behavior for handling exceptions in the domain.
    """

    def __init__(self, errors: str | List[str] = None):
        """
        Initializes a new CoreException instance.
        :param errors: Error messages associated with the exception. Defaults to None.
        """
        self.errors: str | List[str] = errors if errors else self.__class__.__name__
        super().__init__(errors)
