(
    LEVEL_OFF,
    LEVEL_GOOD,
    LEVEL_ERROR,
    LEVEL_WARN,
    LEVEL_INFO,
    LEVEL_DEBUG
) = range(6)

class Colour:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    ENDC = '\033[0m'

class Logger:
    def __init__(self):
        self.set_level(LEVEL_DEBUG)

    def quiet(self):
        self.set_level(LEVEL_OFF)

    def set_level(self, verbose_level):
        if LEVEL_OFF <= verbose_level <= LEVEL_DEBUG:
            self.level = verbose_level

    def _print(self, level, level_name, fmt, *args):
        if level <= self.level:
            print(f"{level_name} {fmt}{Colour.ENDC}".format(*args))

    def DEBUG(self, fmt, *args):
        self._print(LEVEL_DEBUG, "[D]", fmt, *args)

    def INFO(self, fmt, *args):
        self._print(LEVEL_INFO, f"{Colour.BOLD}[*]", fmt, *args)

    def WARN(self, fmt, *args):
        self._print(LEVEL_WARN, f"{Colour.YELLOW}[!]", fmt, *args)

    def ERROR(self, fmt, *args):
        self._print(LEVEL_ERROR, f"{Colour.RED}[-]", fmt, *args)

    def GOOD(self, fmt, *args):
        self._print(LEVEL_GOOD, f"{Colour.GREEN}[+]", fmt, *args)

LOGGER = Logger()
