import math

class CompilerException(Exception):
    def __init__(self, msg, prefix="Error"):
        self.message = f"{prefix}: {msg}"
    def __str__(self):
        return self.message

class CompilationError:
    def __init__(self, desc, sp):
        self.desc = desc
        self.sp = sp

def n_digits(n):
    return math.ceil(math.log10(n + 1))

class ErrorCollector:
    def __init__(self, source):
        self.errors = list()
        self.source = source

    def add_error(self, err):
        self.errors.append(err)

    def has_errors(self):
        return len(self.errors) != 0

    def get_full_line(self, sp):
        line = str()
        line_start = sp.line_start
        file = self.source.source
        while file[line_start] and file[line_start] != "\n":
            line += file[line_start]
            line_start += 1
        return line

    def format_error(self, err):
        full_line = self.get_full_line(err.sp)
        desc = repr(err.desc).strip('"')
        error_string = f"Error: {desc}\n\t{err.sp.line}| {full_line}\n\t"
        error_string += " " * (err.sp.column + n_digits(err.sp.line) + 1) + "^"
        return error_string

    def show_errors(self):
        for err in self.errors:
            print(err.sp.filename)
            print(f"\t{self.format_error(err)}")

        l = len(self.errors)
        raise CompilerException(f"{l} {'errors' if l > 1 else 'error'}", "Autoprox")
