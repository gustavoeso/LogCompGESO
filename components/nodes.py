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
