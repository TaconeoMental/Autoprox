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
        self.errors = dict()
        self.source = source

    def add_error(self, err):
        fn = err.sp.filename
        if fn not in self.errors:
            self.errors[fn] = list()
        self.errors[fn].append(err)

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
        full_line_n = full_line.strip()
        desc = repr(err.desc).strip('"')
        error_string = f"Error: {desc}\n\t{err.sp.line}| {full_line_n}\n\t"
        padding = err.sp.column + n_digits(err.sp.line) + 1 - len(full_line) + len(full_line_n)
        error_string += " " * padding + "^"
        return error_string

    def raise_error(self):
        error_count = 0
        for errors in self.errors.values():
            error_count += len(errors)
        raise CompilerException(f"{error_count} {'errors' if error_count > 1 else 'error'}", "Autoprox")

    def show_errors(self):
        for file in self.errors:
            print(f'File "{file}":')
            for err in self.errors[file]:
                print(f"\t{self.format_error(err)}")
        self.raise_error()
