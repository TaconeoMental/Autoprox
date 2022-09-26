AST_INDENTATION = 4
AST_LAST = "└" + "─" * (AST_INDENTATION - 1)
AST_MIDDLE = "├" + "─" * (AST_INDENTATION - 1)
AST_LINE = "│" + " " * (AST_INDENTATION - 1)
AST_SPACE = " " * AST_INDENTATION

from src.parser.token import TokenType

def pp_indentation(last):
    if last:
        print(AST_LAST, end="")
        return AST_SPACE
    else:
        print(AST_MIDDLE, end="")
        return AST_LINE


### Nodos ###

class Program:
    def __init__(self):
        self.statements = list()
        self.serve = None

    def pp_tree(self, indent, last):
        print("Program")
        for index, stmt in enumerate(self.statements):
            stmt.pp_tree(indent, index == len(self.statements) - 1)

class StatementList:
    def __init__(self):
        self.statements = list()

    def pp_tree(self, indent, last):
        print(indent, end="")
        indent += pp_indentation(last)

        print("StatementList")
        print(indent + AST_LAST + "Statements")
        for index, stmt in enumerate(self.statements):
            stmt.pp_tree(indent + AST_SPACE, index == len(self.statements) - 1)

class DefineStatement:
    def __init__(self):
        self.token = None
        self.name = None
        self.identifier = None
        self.value = None

    def pp_tree(self, indent, last):
        print(indent, end="")
        indent += pp_indentation(last)

        print("DefineStatement")
        print(indent + AST_MIDDLE + "Name")
        self.identifier.pp_tree(indent + AST_LINE, True)

        print(indent + AST_LAST + "Value")
        self.value.pp_tree(indent + AST_SPACE, True)

class ServeStatement:
    def __init__(self):
        self.token = None
        self.ip = None
        self.port = None

    def pp_tree(self, indent, last):
        print(indent, end="")
        indent += pp_indentation(last)

        print("ServeStatement")
        print(indent + AST_MIDDLE + "IP")
        self.ip.pp_tree(indent + AST_LINE, True)

        print(indent + AST_LAST + "Port")
        self.port.pp_tree(indent + AST_SPACE, True)

class InterceptStatement:
    def __init__(self):
        self.what = list()
        self.condition = None
        self.action = None
        self.body = None

    def pp_tree(self, indent, last):
        print(indent, end="")
        indent += pp_indentation(last)

        print("InterceptStatement")
        print(indent + AST_MIDDLE + "What")
        self.what.pp_tree(indent + AST_LINE, True)

        print(indent + AST_MIDDLE + "Condition")
        self.condition.pp_tree(indent + AST_LINE, True)

        print(indent + AST_MIDDLE + "Action")
        self.action.pp_tree(indent + AST_LINE, True)

        print(indent + AST_LAST + "Body")
        self.body.pp_tree(indent + AST_SPACE, True)

class InterceptStatementWhat:
    def __init__(self):
        self.items = list()

    def add(self, *items):
        for i in items:
            if isinstance(i, InterceptStatementWhat):
                self.items += i.items
            else:
                self.items.append(i)
        return self

    def pp_tree(self, indent, last):
        print(indent, end="")
        indent += pp_indentation(last)
        print("InterceptStatementWhat")
        for index, value in enumerate(self.items):
            value.pp_tree(indent + AST_SPACE, index == len(self.items) - 1)

class InterceptType:
    def __init__(self, value, tok):
        self.token = tok
        self.value = value

    def pp_tree(self, indent, last):
        print(indent, end="")
        indent += pp_indentation(last)

        print("InterceptType")
        print(indent + AST_LAST + self.value)

class InterceptStatementActionSet:
    def __init__(self):
        self.token = None
        self.what = None
        self.value = None

    def pp_tree(self, indent, last):
        print(indent, end="")
        indent += pp_indentation(last)
        print("InterceptStatementActionSet")

        print(indent + AST_MIDDLE + "What")
        self.what.pp_tree(indent + AST_LINE, True)

        print(indent + AST_LAST + "Value")
        self.value.pp_tree(indent + AST_SPACE, True)

class InterceptStatementActionVerb:
    def __init__(self, tok, val):
        self.token = tok
        self.name = val

    def pp_tree(self, indent, last):
        print(indent, end="")
        indent += pp_indentation(last)
        print("InterceptStatementActionVerb")

class Empty:
    def __init__(self):
        pass

    def __bool__(self):
        return False

    def pp_tree(self, indent, last):
        print(indent, end="")
        indent += pp_indentation(last)
        print("Empty")

class Identifier:
    def __init__(self, value, tok):
        self.token = tok
        self.value = value

    def pp_tree(self, indent, last):
        print(indent, end="")
        indent += pp_indentation(last)

        print("Identifier")
        print(indent + AST_LAST + self.value)

class TypeIdentifier:
    def __init__(self, value, tok):
        self.token = tok
        self.value = value

    def pp_tree(self, indent, last):
        print(indent, end="")
        indent += pp_indentation(last)

        print("TypeIdentifier")
        print(indent + AST_LAST + self.value)

class Variable:
    def __init__(self):
        self.type = Empty()
        self.name = Empty()

    def pp_tree(self, indent, last):
        print(indent, end="")
        indent += pp_indentation(last)

        print("Variable")

        print(indent + AST_MIDDLE + "Type")
        self.type.pp_tree(indent + AST_LINE, True)

        print(indent + AST_LAST + "Name")
        self.name.pp_tree(indent + AST_SPACE, True)

class Literal:
    def __init__(self, tok, val):
        self.token = tok
        self.value = val

    def pp_tree(self, indent, last):
        print(indent, end="")
        indent += pp_indentation(last)

        print("Literal")
        if self.token.kind == TokenType.LITERAL_STR:
            val = f'"{self.value}"'
        else:
            val = self.value
        print(indent + AST_LAST + val)

class BinaryOperationExpression:
    def __init__(self, o, l, r):
        self.operator = o
        self.left = l
        self.right = r

    def pp_tree(self, indent, last):
        print(indent, end="")
        indent += pp_indentation(last)

        print("BinaryOperationExpression")

        print(indent + AST_MIDDLE + "Left")
        self.left.pp_tree(indent + AST_LINE, True)

        print(indent + AST_MIDDLE + "Operator")
        print(indent + AST_LINE + AST_LAST + str(self.operator))

        print(indent + AST_LAST + "Right")
        self.right.pp_tree(indent + AST_SPACE, True)

class UnaryOperationExpression:
    def __init__(self, o, v):
        self.operator = o
        self.operand = v

    def pp_tree(self, indent, last):
        print(indent, end="")
        indent += pp_indentation(last)

        print("unaryOperationExpression")

        print(indent + AST_MIDDLE + "Operator")
        print(indent + AST_LINE + str(self.operator))

        print(indent + AST_LAST + "Operand")
        self.operand.pp_tree(indent + AST_SPACE, True)
