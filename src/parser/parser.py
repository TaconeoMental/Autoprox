import src.parser.ast as ast
from src.parser.token import TokenType, Token, token_string
from src.parser.source_position import SourcePosition
from src.parser.error_collector import CompilationError
from src.logger import LOGGER

def is_value_type(tt):
    valid_types = [
        TokenType.KEY_T_PARAMS,
        TokenType.KEY_T_HEADER,
        TokenType.KEY_T_SCOPE
    ]
    return tt in valid_types

def is_empty_type(tt):
    valid_types = [
        TokenType.KEY_T_METHOD,
        TokenType.KEY_T_SCHEME,
        TokenType.KEY_T_DOMAIN,
        TokenType.KEY_T_PORT,
        TokenType.KEY_T_PATH,
        TokenType.KEY_T_VERSION,
        TokenType.KEY_T_ST_CD,
        TokenType.KEY_T_ST_MSG,
    ]
    return tt in valid_types

class Parser:
    def __init__(self, tokens, error_collector):
        self.tokens = iter(tokens)
        self.error_collector = error_collector

        self.current_token = None
        self.peek_token = None

        self.ast = ast.Program()

        self.push_token()
        self.push_token()

    def push_token(self):
        self.current_token = self.peek_token
        try:
            self.peek_token = next(self.tokens)
        except StopIteration:
            self.peek_token = None

    def current_token_equals(self, tok):
        return self.current_token.kind == tok

    def peek_token_equals(self, tok):
        return self.peek_token.kind == tok

    def add_parse_error(self, tok, msg, *fmt):
        self.error_collector.add_error(
            CompilationError(
                msg.format(*fmt),
                tok.source_position
            )
        )
        self.error_collector.show_errors()

    def consume_peek(self, expect):
        if self.peek_token_equals(expect):
            self.push_token()
            return True

        if self.peek_token_equals(TokenType.EOF):
            tok = self.current_token
        else:
            tok = self.peek_token
        self.add_parse_error(tok,
                             "Expected '{}'. but got '{}' instead.",
                             token_string(expect), self.peek_token)
        self.push_token()
        return False

    def parse(self):
        while self.current_token and not self.current_token_equals(TokenType.EOF):
            statement = self.parse_statement()
            if statement:
                self.ast.statements.append(statement)
            self.push_token()

    def parse_serve_statement(self):
        stmt = ast.ServeStatement()
        stmt.token = self.current_token
        if not self.consume_peek(TokenType.LITERAL_INT):
            return False
        stmt.ip = ast.Literal(self.current_token, self.current_token.value)
        if not self.consume_peek(TokenType.LITERAL_INT):
            return False
        stmt.port = ast.Literal(self.current_token, self.current_token.value)
        return stmt

    def parse_statement(self):
        match self.current_token.kind:
            case TokenType.KEY_DEF:
                return self.parse_define_statement()
            case TokenType.KEY_A_INTERCEPT:
                return self.parse_intercept_statement()
            case TokenType.KEY_A_SERVE:
                return self.parse_serve_statement()
            case _:
                return False

    def parse_define_statement(self):
        stmt = ast.DefineStatement()
        stmt.token = self.current_token
        stmt.type = self.parse_value_type()
        if not self.consume_peek(TokenType.IDENTIFIER):
            return False
        stmt.identifier = ast.Identifier(self.current_token.value,
                                         self.current_token)
        # TODO: Añadir herencia
        if self.peek_token_equals(TokenType.OPERATOR_COLON):
            stmt.value = self.parse_define_value()
        else:
            stmt.value = self.parse_expression()
            if not self.consume_peek(TokenType.KEY_END):
                return False
        return stmt

    def parse_intercept_statement(self):
        stmt = ast.InterceptStatement()
        stmt.token = self.current_token
        stmt.what = self.parse_intercept_what()
        stmt.condition = self.parse_intercept_condition()
        stmt.action = self.parse_intercept_action()
        #stmt.body = self.parse_intercept_body()
        return stmt

    def parse_intercept_what(self):
        what = ast.InterceptStatementWhat()
        kind = self.peek_token.kind
        if kind == TokenType.IDENTIFIER:
            self.push_token()
            iden = ast.Identifier(self.current_token.value, self.current_token)
            what = what.add(iden)
        return what.add(self.parse_intercept_what_2())

    def parse_intercept_what_2(self):
        what = ast.InterceptStatementWhat()
        kind = self.peek_token.kind
        if kind in (TokenType.KEY_REQ, TokenType.KEY_RESP):
            self.push_token()
            node = ast.InterceptType(self.current_token.value,
                                     self.current_token)
            what = what.add(node)
        return what.add(self.parse_intercept_what_3())

    def parse_intercept_what_3(self):
        what = ast.InterceptStatementWhat()
        if self.peek_token_equals(TokenType.LITERAL_NUM):
            self.push_token()
            node = ast.Literal(self.current_token, self.current_token.value)
            what = what.add(node)
        return what

    def parse_intercept_condition(self):
        if self.peek_token_equals(TokenType.KEY_IF):
            self.push_token()
            return self.parse_compare_expression()
        return ast.Empty()

    def parse_intercept_action(self):
        match self.peek_token.kind:
            case TokenType.KEY_A_SET:
                self.push_token()
                return self.parse_intercept_action_set()
            case TokenType.KEY_A_DELETE:
                self.push_token()
                return self.parse_intercept_action_delete()

    def parse_intercept_action_set(self):
        action = ast.InterceptStatementActionSet()
        action.token = self.current_token
        if self.peek_token_equals(TokenType.OPERATOR_OPEN_C):
            action.operand = ast.Empty()
            action.body = self.parse_intercept_body()
            return action
        else:
            return self.parse_intercept_action_set_2(action)

    def parse_intercept_action_set_2(self, action):
        if is_value_type(self.peek_token.kind):
            self.push_token()
            t = ast.TypeIdentifier(self.current_token.value, self.current_token)
            if self.peek_token_equals(TokenType.OPERATOR_OPEN_C):
                action.operand = t
                action.body = self.parse_intercept_body()
            else:
                var = ast.Variable()
                var.type = t
                self.consume_peek(TokenType.IDENTIFIER)
                var.name = ast.Identifier(self.current_token.value,
                                          self.current_token)
                action.operand = var
                self.consume_peek(TokenType.OPERATOR_COLON)
                action.body = self.parse_literal()
        elif is_empty_type(self.peek_token.kind):
            self.push_token()
            action.operand = ast.TypeIdentifier(self.current_token.value)
            self.consume_peek(TokenType.OPERATOR_COLON)
            action.body = self.parse_literal()
        return action

    def parse_intercept_body(self):
        pass

    def parse_value_type(self):
        if is_value_type(self.peek_token.kind):
            self.push_token()
            return ast.TypeIdentifier(self.current_token.value,
                                      self.current_token)
        return False

    def parse_empty_type(self):
        if is_empty_type(self.current_token.kind):
            return ast.TypeIdentifier(self.current_token.value,
                                      self.current_token)
        return False

    def parse_define_value(self):
        if not self.consume_peek(TokenType.OPERATOR_COLON):
            return False
        return self.parse_literal()

    def parse_literal(self):
        if self.peek_token.kind in (TokenType.LITERAL_INT,
                                    TokenType.LITERAL_STR,
                                    TokenType.LITERAL_IP):
            self.push_token()
            return ast.Literal(self.current_token, self.current_token.value)
        self.push_token()
        self.add_parse_error(self.current_token,
                             "'{}' cannot be used as a literal value.",
                             self.current_token)
        return False

    def parse_expression(self):
        return self.parse_boolean_or_expression()

    def parse_boolean_or_expression(self):
        expr = self.parse_boolean_and_expression()
        while self.peek_token_equals(TokenType.OPERATOR_OR):
            self.push_token()
            expr = ast.BinaryOperationExpression(self.current_token,
                                                 expr,
                                                 self.parse_boolean_and_expression())
        return expr

    def parse_boolean_and_expression(self):
        expr = self.parse_primary_expression()
        while self.peek_token_equals(TokenType.OPERATOR_AND):
            self.push_token()
            right = self.parse_primary_expression()
            expr = ast.BinaryOperationExpression(self.current_token, expr, right)
        return expr

    def parse_primary_expression(self):
        if self.peek_token_equals(TokenType.OPERATOR_OPEN_P):
            self.consume_peek(TokenType.OPERATOR_OPEN_P)
            operand = self.parse_expression()
            self.consume_peek(TokenType.OPERATOR_CLOSE_P)
        else:
            operand = self.parse_compare_expression()
        return operand

    def parse_compare_expression(self):
        v = self.parse_operand()
        op = self.parse_compare_operation()
        l = self.parse_literal()
        return ast.BinaryOperationExpression(op, v, l)

    def parse_compare_operation(self):
        match self.peek_token.kind:
            case TokenType.OPERATOR_IS:
                self.push_token()
                if self.peek_token_equals(TokenType.OPERATOR_NOT):
                    self.push_token()
                return self.current_token
            case TokenType.OPERATOR_LIKE:
                self.push_token()
                return self.current_token
            case _:
                self.push_token()
                self.add_parse_error(self.current_token,
                                     "'{}' is not a valid comparison operator.",
                                     self.current_token)
                return False

    def parse_operand(self):
        if is_value_type(self.peek_token.kind):
            v = ast.Variable()
            self.push_token()
            v.type = ast.TypeIdentifier(self.current_token.value, self.current_token)
            if self.peek_token_equals(TokenType.IDENTIFIER):
                self.push_token()
                v.name = ast.Identifier(self.current_token.value, self.current_token)
            return v
        elif is_empty_type(self.peek_token.kind):
            self.push_token()
            return ast.TypeIdentifier(self.current_token.value, self.current_token)
        else:
            return False
