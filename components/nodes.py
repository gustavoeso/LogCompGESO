from abc import ABC, abstractmethod

class Node(ABC):
    @abstractmethod
    def Evaluate(self, symbol_table):
        pass

class BinOp(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def Evaluate(self, symbol_table):
        left_val = self.left.Evaluate(symbol_table)
        right_val = self.right.Evaluate(symbol_table)
        if self.operator == 'PLUS':
            return left_val + right_val
        elif self.operator == 'MINUS':
            return left_val - right_val
        elif self.operator == 'MULT':
            return left_val * right_val
        elif self.operator == 'DIV':
            return left_val // right_val

class UnOp(Node):
    def __init__(self, operator, child):
        self.operator = operator
        self.child = child

    def Evaluate(self, symbol_table):
        val = self.child.Evaluate(symbol_table)
        if self.operator == 'PLUS':
            return +val
        elif self.operator == 'MINUS':
            return -val
        elif self.operator == 'NOT':
            return int(not val)

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self, symbol_table):
        return self.value

class NoOp(Node):
    def Evaluate(self, symbol_table):
        pass

class IdentifierNode(Node):
    def __init__(self, name):
        self.name = name

    def Evaluate(self, symbol_table):
        return symbol_table.get(self.name)

class AssignmentNode(Node):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def Evaluate(self, symbol_table):
        value = self.expression.Evaluate(symbol_table)
        symbol_table.set(self.identifier.name, value)

class BlockNode(Node):
    def __init__(self, statements):
        self.statements = statements

    def Evaluate(self, symbol_table):
        for statement in self.statements:
            statement.Evaluate(symbol_table)

class PrintNode(Node):
    def __init__(self, expression):
        self.expression = expression

    def Evaluate(self, symbol_table):
        value = self.expression.Evaluate(symbol_table)
        print(value)

class RelOp(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def Evaluate(self, symbol_table):
        left_val = self.left.Evaluate(symbol_table)
        right_val = self.right.Evaluate(symbol_table)
        if self.operator == '==':
            return int(left_val == right_val)
        elif self.operator == '>':
            return int(left_val > right_val)
        elif self.operator == '<':
            return int(left_val < right_val)
        elif self.operator == '!=':
            return int(left_val != right_val)

class BoolOp(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def Evaluate(self, symbol_table):
        left_val = self.left.Evaluate(symbol_table)
        right_val = self.right.Evaluate(symbol_table)
        if self.operator == '&&':
            return int(left_val and right_val)
        elif self.operator == '||':
            return int(left_val or right_val)

class IfNode(Node):
    def __init__(self, condition, if_block, else_block=None):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block

    def Evaluate(self, symbol_table):
        if self.condition.Evaluate(symbol_table):
            self.if_block.Evaluate(symbol_table)
        elif self.else_block:
            self.else_block.Evaluate(symbol_table)

class WhileNode(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def Evaluate(self, symbol_table):
        while self.condition.Evaluate(symbol_table):
            self.block.Evaluate(symbol_table)

class InputNode(Node):
    def Evaluate(self, symbol_table):
        value = int(input())
        return value