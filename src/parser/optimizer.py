import copy

import src.parser.ast as ast
from src.logger import LOGGER


class Optimizer:
    def __init__(self, or_ast, err_coll):
        self.ast = or_ast
        self.error_collector = err_coll
        self.reduced_ast = ast.Program()

    def recursive_append(self, start, stmts):
        if not stmts:
            self.reduced_ast.statements.append(start)
            return
        for b_stmt in stmts.statements:
            self.recursive_append(b_stmt + start, b_stmt.body)
        self

    def eval_intercept_statement(self, stmt):
        original_stmt = copy.deepcopy(stmt)
        original_stmt.body = ast.Empty()
        self.recursive_append(original_stmt, stmt.body)

    def eval_program(self, program):
        for stmt in program.statements:
            self.eval_node(stmt)

    def eval_node(self, a):
        if isinstance(a, ast.Program):
            return self.eval_program(a)
        elif isinstance(a, ast.DefineStatement) or isinstance(a, ast.ServeStatement):
            return self.reduced_ast.statements.append(a)
        elif isinstance(a, ast.InterceptStatement):
            return self.eval_intercept_statement(a)

    def run(self):
        self.eval_node(self.ast)
