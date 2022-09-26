import os
from  src.logger import LOGGER

from src.parser.error_collector import CompilerException

class ConfigFile:
    def __init__(self, path):
        if not os.path.exists(path):
            LOGGER.ERROR("Error: File '{}' doesn't exist", path)
            raise CompilerException("1 error", "Autoprox")

        self.path = path
        self.line_indexes = [0]
        with open(path, "r") as f:
            self.source = f.read()

    def get_filename(self):
        return os.path.basename(self.path)

    def get_path(self):
        return os.path.abspath(self.path)


    def push_line_index(self, index):
        self.line_indexes.append(index)

    def __getitem__(self, index):
        if index >= len(self.source):
            return ""
        return self.source[index]

    def len(self):
        return len(self.source)
