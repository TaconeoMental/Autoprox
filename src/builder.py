from src.logger import LOGGER
from src.parser.conf_file import ConfigFile
from src.parser.lexer import Lexer
from src.parser.parser import Parser
from src.parser.optimizer import Optimizer
from src.parser.error_collector import ErrorCollector, CompilerException

class Builder:
    def __init__(self, source):
        self.source = source
        self.print_tokens = False
        self.print_ast = False
        self.printed = False


    # Debug
    def set_print_tokens(self, b=True):
        self.print_token = b
        self.printed = b

    def set_print_ast(self, b=True):
        self.print_ast = b
        self.printed = b

    def run(self):
        conf_file = ConfigFile(self.source)
        err_coll = ErrorCollector(conf_file)

        lexer = Lexer(conf_file, err_coll)
        lexer.run()

        if self.print_tokens:
            lexer.print_tokens()

        if err_coll.has_errors():
            err_coll.show_errors()

        parser = Parser(lexer.tokens, err_coll)
        parser.parse()

        optimizer = Optimizer(parser.ast, err_coll)
        optimizer.run()

        if self.print_ast:
            LOGGER.INFO("AST:")
            optimizer.reduced_ast.pp_tree("", True)

        return optimizer.reduced_ast
