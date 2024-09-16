from components.node import Node

class BinOp(Node):
    def __init__(self, left, operator, right):
        super().__init__(operator)
        self.children = [left, right]

    def Evaluate(self, symbol_table):
        if self.value == '+':
            return self.children[0].Evaluate(symbol_table) + self.children[1].Evaluate(symbol_table)
        elif self.value == '-':
            return self.children[0].Evaluate(symbol_table) - self.children[1].Evaluate(symbol_table)
        elif self.value == '*':
            return self.children[0].Evaluate(symbol_table) * self.children[1].Evaluate(symbol_table)
        elif self.value == '/':
            return self.children[0].Evaluate(symbol_table) // self.children[1].Evaluate(symbol_table)

class UnOp(Node):
    def __init__(self, operator, child):
        super().__init__(operator)
        self.children = [child]

    def Evaluate(self, symbol_table):
        if self.value == '+':
            return +self.children[0].Evaluate(symbol_table)
        elif self.value == '-':
            return -self.children[0].Evaluate(symbol_table)
        elif self.value == '!':  # Adicionar suporte para negação lógica
            return not self.children[0].Evaluate(symbol_table)


class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self, symbol_table):
        return self.value

class NoOp(Node):
    def __init__(self):
        super().__init__()

    def Evaluate(self, symbol_table):
        return None

class IdentifierNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def Evaluate(self, symbol_table):
        return symbol_table.get(self.name)  # Usando self.name

class AssignmentNode(Node):
    def __init__(self, identifier, expression):
        super().__init__(identifier)
        self.children = [expression]
        self.name = identifier

    def Evaluate(self, symbol_table):
        value = self.children[0].Evaluate(symbol_table)
        symbol_table.set(self.name, value)  # Usando self.name

class BlockNode(Node):
    def __init__(self, instructions):
        super().__init__()
        self.children = instructions

    def Evaluate(self, symbol_table):
        for instruction in self.children:
            instruction.Evaluate(symbol_table)

class PrintNode(Node):
    def __init__(self, expression):
        super().__init__()
        self.children = [expression]

    def Evaluate(self, symbol_table):
        value = self.children[0].Evaluate(symbol_table)
        print(value)

class RelOp(Node):
    def __init__(self, left, operator, right):
        super().__init__(operator)
        self.children = [left, right]

    def Evaluate(self, symbol_table):
        left_val = self.children[0].Evaluate(symbol_table)
        right_val = self.children[1].Evaluate(symbol_table)
        if self.value == "==":
            return left_val == right_val
        elif self.value == ">":
            return left_val > right_val
        elif self.value == "<":
            return left_val < right_val
        elif self.value == "!=":
            return left_val != right_val

class BoolOp(Node):
    def __init__(self, left, operator, right):
        super().__init__(operator)
        self.children = [left, right]

    def Evaluate(self, symbol_table):
        left_val = self.children[0].Evaluate(symbol_table)
        right_val = self.children[1].Evaluate(symbol_table)
        if self.value == "&&":
            return left_val and right_val
        elif self.value == "||":
            return left_val or right_val

class IfNode(Node):
    def __init__(self, condition, if_block, else_block=None):
        super().__init__()
        self.children = [condition, if_block]
        if else_block:
            self.children.append(else_block)

    def Evaluate(self, symbol_table):
        if self.children[0].Evaluate(symbol_table):
            self.children[1].Evaluate(symbol_table)
        elif len(self.children) == 3:
            self.children[2].Evaluate(symbol_table)

class WhileNode(Node):
    def __init__(self, condition, block):
        super().__init__()
        self.children = [condition, block]

    def Evaluate(self, symbol_table):
        while self.children[0].Evaluate(symbol_table):
            self.children[1].Evaluate(symbol_table)

class InputNode(Node):
    def __init__(self, identifier):
        super().__init__(identifier)

    def Evaluate(self, symbol_table):
        # Solicitar entrada do usuário
        value = int(input(f"Input value for {self.value}: "))
        # Armazenar o valor na tabela de símbolos
        symbol_table.set(self.value, value)
