from math import inf


class ValueTypeValidator:
    """
    This class has two static methods to validate if a
    given "float" number is a binary or integer number.
    """

    @staticmethod
    def is_binary(num: float) -> bool:
        """
        This method checks if the given float number is binary or not.
        :param num: float number to be checked
        :return: True if the given float number is binary else False
        """
        return num is not None and num in [0, 1]

    @staticmethod
    def is_integer(num: float) -> bool:
        """
        This method checks if the given float number is an integer or not.
        :param num: float number to be checked
        :return: True if the given float number is an integer else False
        """
        return num is not None and (num == inf or num == -inf or float(num).is_integer())
