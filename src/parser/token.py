class TokenType:
    EOF              = 0x00
    COMMENT          = 0x01
    IDENTIFIER       = 0x02

    # Literales
    LITERAL_INT      = 0x03
    LITERAL_STR      = 0x04
    LITERAL_IP       = 0x05
    LITERAL_NUM      = 0x06

    # Keywords
    KEY_DEF          = 0x07
    KEY_END          = 0x08
    KEY_REQ          = 0x09
    KEY_RESP         = 0x0A
    KEY_IF           = 0x0B

    KEY_T_METHOD     = 0x0C
    KEY_T_SCHEME     = 0x0D
    KEY_T_DOMAIN     = 0x0E
    KEY_T_PORT       = 0x0F
    KEY_T_PATH       = 0x10
    KEY_T_PARAMS     = 0x11
    KEY_T_VERSION    = 0x12
    KEY_T_HEADER     = 0x13
    KEY_T_ST_CD      = 0x14
    KEY_T_ST_MSG     = 0x15
    KEY_T_SCOPE      = 0x16

    KEY_A_DELETE     = 0x17
    KEY_A_INTERCEPT  = 0x18
    KEY_A_SERVE      = 0x19
    KEY_A_SET        = 0x1A

    OPERATOR_AND     = 0x1B
    OPERATOR_OR      = 0x1C
    OPERATOR_IS      = 0x1D
    OPERATOR_NOT     = 0x1E
    OPERATOR_LIKE    = 0x1F

    OPERATOR_COMMA   = 0x20
    OPERATOR_COLON   = 0x21
    OPERATOR_OPEN_P  = 0x22
    OPERATOR_CLOSE_P = 0x23
    OPERATOR_OPEN_C  = 0x24
    OPERATOR_CLOSE_C = 0x25

def token_string(token):
    match token:
        case TokenType.EOF:
            return "EOF"
        case TokenType.COMMENT:
            return "COMMENT"
        case TokenType.IDENTIFIER:
            return "IDENTIFIER"
        case TokenType.LITERAL_INT:
            return "int"
        case TokenType.LITERAL_STR:
            return "string"
        case TokenType.LITERAL_IP:
            return "IP"
        case TokenType.LITERAL_NUM:
            return "NUM"
        case TokenType.KEY_DEF:
            return "def"
        case TokenType.KEY_END:
            return "end"
        case TokenType.KEY_REQ:
            return "req"
        case TokenType.KEY_RESP:
            return "resp"
        case TokenType.KEY_IF:
            return "if"
        case TokenType.KEY_T_METHOD:
            return "METHOD"
        case TokenType.KEY_T_SCHEME:
            return "SCHEME"
        case TokenType.KEY_T_DOMAIN:
            return "DOMAIN"
        case TokenType.KEY_T_PORT:
            return "PORT"
        case TokenType.KEY_T_PATH:
            return "PATH"
        case TokenType.KEY_T_PARAMS:
            return "PARAMETERS"
        case TokenType.KEY_T_VERSION:
            return "VERSION"
        case TokenType.KEY_T_HEADER:
            return "HEADER"
        case TokenType.KEY_T_ST_CD:
            return "STATUS_CODE"
        case TokenType.KEY_T_ST_MSG:
            return "STATUS_MESSAGE"
        case TokenType.KEY_T_SCOPE:
            return "SCOPE"
        case TokenType.KEY_A_DELETE:
            return "delete"
        case TokenType.KEY_A_INTERCEPT:
            return "intercept"
        case TokenType.KEY_A_SERVE:
            return "serve"
        case TokenType.KEY_A_SET:
            return "set"
        case TokenType.OPERATOR_AND:
            return "&"
        case TokenType.OPERATOR_OR:
            return "|"
        case TokenType.OPERATOR_IS:
            return "is"
        case TokenType.OPERATOR_NOT:
            return "not"
        case TokenType.OPERATOR_LIKE:
            return "like"
        case TokenType.OPERATOR_COMMA:
            return ","
        case TokenType.OPERATOR_COLON:
            return ":"
        case TokenType.OPERATOR_OPEN_P:
            return "("
        case TokenType.OPERATOR_CLOSE_P:
            return ")"
        case TokenType.OPERATOR_OPEN_C:
            return "{"
        case TokenType.OPERATOR_CLOSE_C:
            return "}"
        case _:
            return "Unknown"

class Token:
    def __init__(self, kind, position, value=None):
        self.kind = kind
        self.source_position = position
        self.value = value

    def __str__(self):
        return token_string(self.kind)

    def __repr__(self):
        return str(self)
