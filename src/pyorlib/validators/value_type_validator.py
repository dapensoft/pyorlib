from math import inf


class ValueTypeValidator:
    """
    This class has two static methods to validate if a
    given "float" or "int" number is a valid binary or
    integer number.
    """

    @staticmethod
    def is_binary(num: float | int) -> bool:
        """
        This method checks if the given float/int number is binary or not.
        :param num: float/int number to be checked
        :return: True if the given float/int number is binary else False
        """
        return num is not None and num in [0, 1]

    @staticmethod
    def is_integer(num: float | int) -> bool:
        """
        This method checks if the given float/int number is a valid integer or not.
        :param num: float/int number to be checked
        :return: True if the given float/int number is an integer else False
        """
        return num is not None and (num == inf or num == -inf or isinstance(num, int) or float(num).is_integer())
