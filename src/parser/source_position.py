class SourcePosition:
    def __init__(self, fn, line, column, line_start):
        self.filename = fn
        self.line = line
        self.column = column
        self.line_start = line_start

    def __repr__(self):
        return f"{self.filename}(L={self.line}, C={self.column}, LS={self.line_start})"
