from typing import List


class CoreException(Exception):
    """ Common base class for all domain exceptions """

    def __init__(self, errors: str | List[str] = None):
        """
        Creates a new core exception instance
        :param errors: Error messages
        """
        self.errors: str | List[str] = errors if errors else self.__class__.__name__
        super().__init__(errors)
