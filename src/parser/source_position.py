class SourcePosition:
    def __init__(self, fn, line, column, line_start):
        self.filename = fn
        self.line = line
        self.column = column
        self.line_start = line_start
