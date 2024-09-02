from components.node import Node

class BinOp(Node):
    def __init__(self, left, operator, right):
        super().__init__(operator)
        self.children = [left, right]

    def Evaluate(self):
        if self.value == '+':
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        elif self.value == '-':
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        elif self.value == '*':
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        elif self.value == '/':
            return self.children[0].Evaluate() // self.children[1].Evaluate()

class UnOp(Node):
    def __init__(self, operator, child):
        super().__init__(operator)
        self.children = [child]

    def Evaluate(self):
        if self.value == '+':
            return +self.children[0].Evaluate()
        elif self.value == '-':
            return -self.children[0].Evaluate()

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self):
        return self.value

class NoOp(Node):
    def __init__(self):
        super().__init__()

    def Evaluate(self):
        return None
