class StdOutColors:
    """ A utility class for defining ANSI escape codes for colored text output in the console. """

    DEFAULT: str = '\033[0m'
    PURPLE: str = '\033[35m'
    YELLOW: str = '\033[33m'
    BLUE: str = '\033[34m'
    RED: str = '\033[31m'
    CYAN: str = '\033[36m'
    GREEN: str = '\033[32m'
    BOLD: str = '\033[1m'
    UNDERLINE: str = '\033[4m'
