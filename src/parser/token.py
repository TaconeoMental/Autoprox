class TokenType:
    EOF              = 0x00
    COMMENT          = 0x01
    IDENTIFIER       = 0x02

    # Literales
    LITERAL_INT      = 0x03
    LITERAL_STR      = 0x04
    LITERAL_IP       = 0x05

    # Keywords
    KEY_DEF          = 0x06
    KEY_END          = 0x07
    KEY_REQ          = 0x08
    KEY_RESP         = 0x09
    KEY_IF           = 0x0A

    KEY_T_METHOD     = 0x0B
    KEY_T_SCHEME     = 0x0C
    KEY_T_DOMAIN     = 0x0D
    KEY_T_PORT       = 0x0E
    KEY_T_PATH       = 0x0F
    KEY_T_PARAMS     = 0x10
    KEY_T_VERSION    = 0x11
    KEY_T_HEADER     = 0x12
    KEY_T_ST_CD      = 0x13
    KEY_T_ST_MSG     = 0x14
    KEY_T_SCOPE      = 0x15

    KEY_A_DELETE     = 0x16
    KEY_A_INTERCEPT  = 0x17
    KEY_A_SERVE      = 0x18
    KEY_A_SET        = 0x19

    OPERATOR_AND     = 0x1A
    OPERATOR_OR      = 0x1B
    OPERATOR_IS      = 0x1C
    OPERATOR_NOT     = 0x1D
    OPERATOR_LIKE    = 0x1E

    OPERATOR_COMMA   = 0x1F
    OPERATOR_COLON   = 0x20
    OPERATOR_OPEN_P  = 0x21
    OPERATOR_CLOSE_P = 0x22
    OPERATOR_OPEN_C  = 0x23
    OPERATOR_CLOSE_C = 0x24

def token_string(token):
    match token:
        case TokenType.EOF:
            return "EOF"
        case TokenType.COMMENT:
            return "COMMENT"
        case TokenType.IDENTIFIER:
            return "IDENTIFIER"
        case TokenType.LITERAL_INT:
            return "LITERAL_INT"
        case TokenType.LITERAL_STR:
            return "LITERAL_STR"
        case TokenType.LITERAL_IP:
            return "LITERAL_IP"
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
            return "OPERATOR_COMMA"
        case TokenType.OPERATOR_COLON:
            return "OPERATOR_COLON"
        case TokenType.OPERATOR_OPEN_P:
            return "OPERATOR_OPEN_P"
        case TokenType.OPERATOR_CLOSE_P:
            return "OPERATOR_CLOSE_P"
        case TokenType.OPERATOR_OPEN_C:
            return "OPERATOR_OPEN_C"
        case TokenType.OPERATOR_CLOSE_C:
            return "OPERATOR_CLOSE_C"
        case _:
            return "Unknown"

class Token:
    def __init__(self, kind, position, value=None):
        self.kind = kind
        self.source_position = position
        self.value = value

    def __str__(self):
        return token_string(self.kind)
