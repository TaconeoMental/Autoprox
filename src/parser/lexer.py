from src.parser.token import TokenType, Token
from src.parser.source_position import SourcePosition
from src.parser.error_collector import CompilationError
from src.logger import LOGGER

keywords = {
    "def": TokenType.KEY_DEF,
    "end": TokenType.KEY_END,
    "req": TokenType.KEY_REQ,
    "resp": TokenType.KEY_RESP,
    "if": TokenType.KEY_IF,
    "METHOD": TokenType.KEY_T_METHOD,
    "SCHEME": TokenType.KEY_T_SCHEME,
    "DOMAIN": TokenType.KEY_T_DOMAIN,
    "PORT": TokenType.KEY_T_PORT,
    "PATH": TokenType.KEY_T_PATH,
    "PARAMETERS": TokenType.KEY_T_PARAMS,
    "VERSION": TokenType.KEY_T_VERSION,
    "HEADER": TokenType.KEY_T_HEADER,
    "STATUS_CODE": TokenType.KEY_T_ST_CD,
    "STATUS_MESSAGE": TokenType.KEY_T_ST_MSG,
    "SCOPE": TokenType.KEY_T_SCOPE,
    "delete": TokenType.KEY_A_DELETE,
    "intercept": TokenType.KEY_A_INTERCEPT,
    "serve": TokenType.KEY_A_SERVE,
    "set": TokenType.KEY_A_SET,
    "is": TokenType.OPERATOR_IS,
    "not": TokenType.OPERATOR_NOT,
    "like": TokenType.OPERATOR_LIKE
}

def is_valid_first_id_char(c):
    return c.isalpha() or c == "_"

def is_valid_id_char(c):
    return c.isalnum() or c == "_"

def is_keyword(k):
    return k in keywords

class Lexer:
    def __init__(self, source, error_collector):
        self.source = source
        self.error_collector = error_collector

        self.tokens = list()

        self.line_number = 1
        self.column_number = 0
        self.line_column = 0

        self.current_char = str()
        self.peek_char = self.source[self.column_number]

    def push_char(self):
        self.current_char = self.peek_char
        self.column_number += 1
        self.line_column += 1
        self.peek_char = self.source[self.column_number]
        if self.current_char == "\n":
            self.line_number += 1
            self.line_column = 0
            self.source.push_line_index(self.column_number)
        return self.current_char

    def read_until(self, c):
        res = str()
        while self.current_char != c:
            res += self.current_char
            self.push_char()
        return res

    def check_literal(self):
        lit = str()
        if self.current_char == '"':
            tt = TokenType.LITERAL_STR
            self.push_char()
            while self.current_char != '"':
                lit += self.current_char
                if self.peek_char == "\n":
                    self.add_syntax_error("Unexpected EOL reading string literal")
                    self.push_char()
                    return False
                self.push_char()
            self.add_token(tt, lit)
            return True
        elif self.current_char.isdigit():
            tt = TokenType.LITERAL_INT
            lit += self.current_char
            while self.peek_char.isdigit():
                self.push_char()
                lit += self.current_char
            if self.peek_char == ".":
                lit += self.peek_char
                self.push_char()
                for i in range(2):
                    if not self.peek_char.isdigit():
                        self.add_syntax_error("Invalid char '{}' in IP literal", self.peek_char)
                        self.push_char()
                        return False
                    while self.peek_char.isdigit():
                        self.push_char()
                        lit += self.current_char
                    if self.peek_char == ".":
                        lit += self.peek_char
                        self.push_char()
                    else:
                        self.push_char()
                        self.add_syntax_error("Invalid char '{}' in IP literal", self.current_char)
                        return False

                if not self.peek_char.isdigit():
                    self.add_syntax_error("Invalid char '{}' in IP literal", self.peek_char)
                    return False
                while self.peek_char.isdigit():
                    self.push_char()
                    lit += self.current_char
            self.add_token(tt, lit)
            return True
        return False

    def check_operator(self):
        tt = -1
        match self.current_char:
            case "&":
                tt = TokenType.OPERATOR_AND
            case "|":
                tt = TokenType.OPERATOR_OR
            case ":":
                tt = TokenType.OPERATOR_COLON
            case "{":
                tt = TokenType.OPERATOR_OPEN_C
            case "}":
                tt = TokenType.OPERATOR_CLOSE_C
            case _:
                return False
        self.push_char()
        self.add_token(tt)

    def check_comment(self):
        if self.current_char == "/" and self.peek_char == "/":
            self.read_until("\n")
            return True
        return False

    def check_word(self):
        word = str()
        if is_valid_first_id_char(self.current_char):
            tt = -1
            word += self.current_char
            while is_valid_id_char(self.peek_char):
                self.push_char()
                word += self.current_char

            if is_keyword(word):
                tt = keywords[word]
            else:
                tt = TokenType.IDENTIFIER

            self.add_token(tt, word)
            return True
        return False

    def add_token(self, tt, value=None):
        self.tokens.append(
            Token(
                tt,
                SourcePosition(
                    self.source.get_filename(),
                    self.line_number,
                    self.line_column,
                    self.source.line_indexes[-1]
                ),
                value
            )
        )

    def add_syntax_error(self, msg, *fmt):
        self.error_collector.add_error(
            CompilationError(
                msg.format(*fmt),
                SourcePosition(
                    self.source.get_filename(),
                    self.line_number,
                    self.line_column,
                    self.source.line_indexes[-1]
                )
            )
        )

    def run(self):
        while self.push_char():
            if self.check_word() or self.check_comment() or self.check_operator() or self.check_literal():
                continue
            else:
                if not self.current_char.isspace():
                    self.add_syntax_error("Unknown char '{}'", self.current_char)
                continue
        self.add_token(TokenType.EOF)
