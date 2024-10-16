from abc import ABC, abstractmethod
from components.symbol_table import SymbolTable

class Node(ABC):
    i = 0  # Atributo estático para IDs únicos

    @staticmethod
    def newId():
        Node.i += 1
        return Node.i

    @abstractmethod
    def Generate(self, symbol_table):
        pass

class BinOp(Node):
    def __init__(self, left, operator, right):
        self.id = Node.newId()
        self.left = left
        self.operator = operator
        self.right = right

    def Generate(self, symbol_table):
        code = ""
        # Código para os operandos
        code += self.left.Generate(symbol_table)
        code += "    PUSH EAX\n"
        code += self.right.Generate(symbol_table)
        code += "    MOV EBX, EAX\n"
        code += "    POP EAX\n"

        if self.operator == 'PLUS':
            code += "    ADD EAX, EBX\n"
            code += "    MOV EBX, EAX\n"
        elif self.operator == 'MINUS':
            code += "    SUB EAX, EBX\n"
            code += "    MOV EBX, EAX\n"
        elif self.operator == 'MULT':
            code += "    IMUL EBX\n"
            code += "    MOV EBX, EAX\n"
        elif self.operator == 'DIV':
            code += "    CDQ\n"
            code += "    IDIV EBX\n"
            code += "    MOV EBX, EAX\n"
        elif self.operator == '<':
            code += "    CMP EAX, EBX\n"
            code += "    CALL binop_jl\n"
            # O resultado estará em EBX
        elif self.operator == '>':
            code += "    CMP EAX, EBX\n"
            code += "    CALL binop_jg\n"
            # O resultado estará em EBX
        elif self.operator == '==':
            code += "    CMP EAX, EBX\n"
            code += "    CALL binop_je\n"
            # O resultado estará em EBX
        else:
            raise ValueError(f"Operador desconhecido '{self.operator}'")

        return code

class UnOp(Node):
    def __init__(self, operator, child):
        self.operator = operator
        self.child = child
        self.id = Node.newId()

    def Generate(self, symbol_table):
        code = ""
        code += self.child.Generate(symbol_table)
        if self.operator == 'MINUS':
            code += "    NEG EAX\n"
        elif self.operator == 'NOT':
            code += "    CMP EAX, 0\n"
            code += "    JE unop_true_{0}\n".format(self.id)
            code += "    MOV EAX, 0\n"
            code += "    JMP unop_exit_{0}\n".format(self.id)
            code += "unop_true_{0}:\n".format(self.id)
            code += "    MOV EAX, 1\n"
            code += "unop_exit_{0}:\n".format(self.id)
            code += "    MOV EBX, EAX\n"
        else:
            raise ValueError(f"Operador unário desconhecido '{self.operator}'")
        return code

class IntVal(Node):
    def __init__(self, value):
        self.value = value
        self.id = Node.newId()

    def Generate(self, symbol_table):
        code = "    MOV EAX, {0}\n".format(self.value)
        return code

class StringVal(Node):
    def __init__(self, value):
        self.value = value
        self.id = Node.newId()
        # Note que lidar com strings em assembly requer manipulação adicional

    def Generate(self, symbol_table):
        # Para simplificar, não implementaremos strings nesta implementação
        raise NotImplementedError("Strings não são suportadas nesta implementação")

class IdentifierNode(Node):
    def __init__(self, name):
        self.name = name
        self.id = Node.newId()

    def Generate(self, symbol_table):
        var_info = symbol_table.get(self.name)
        offset = var_info['offset']
        code = "    MOV EAX, [EBP{0}]\n".format(offset)
        return code

class AssignmentNode(Node):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
        self.id = Node.newId()

    def Generate(self, symbol_table):
        code = ""
        code += self.expression.Generate(symbol_table)
        code += "    MOV EBX, EAX\n"
        code += "    MOV [EBP{0}], EBX ; {1} = ...\n".format(symbol_table.get(self.identifier.name)['offset'], self.identifier.name)
        return code

class VarDec(Node):
    def __init__(self, var_type, declarations):
        self.var_type = var_type
        self.declarations = declarations
        self.id = Node.newId()

    def Generate(self, symbol_table):
        code = ""
        for identifier, expression in self.declarations:
            symbol_table.declare(identifier.name, self.var_type)
            # Gera 'PUSH DWORD 0' para reservar espaço na pilha
            offset = symbol_table.get(identifier.name)['offset']
            code += "    PUSH DWORD 0 ; Dim {0} as Integer [EBP{1}]\n".format(identifier.name, offset)
            if expression:
                code += expression.Generate(symbol_table)
                code += "    MOV [EBP{0}], EAX ; Inicializa {1}\n".format(offset, identifier.name)
        return code

class BlockNode(Node):
    def __init__(self, statements):
        self.statements = statements
        self.id = Node.newId()

    def Generate(self, symbol_table):
        code = ""
        for statement in self.statements:
            code += statement.Generate(symbol_table)
        return code

class PrintNode(Node):
    def __init__(self, expression):
        self.expression = expression
        self.id = Node.newId()

    def Generate(self, symbol_table):
        code = ""
        code += self.expression.Generate(symbol_table)
        code += "    PUSH EAX ; empilha argumento para print\n"
        code += "    CALL print\n"
        code += "    POP EBX ; limpa args\n"
        return code

class IfNode(Node):
    def __init__(self, condition, if_block, else_block=None):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block
        self.id = Node.newId()

    def Generate(self, symbol_table):
        code = ""
        code += self.condition.Generate(symbol_table)
        code += "    CMP EBX, False\n"
        if self.else_block:
            else_label = "ELSE_{0}".format(self.id)
            end_label = "ENDIF_{0}".format(self.id)
            code += "    JE {0}\n".format(else_label)
            code += self.if_block.Generate(symbol_table)
            code += "    JMP {0}\n".format(end_label)
            code += "{0}:\n".format(else_label)
            code += self.else_block.Generate(symbol_table)
            code += "{0}:\n".format(end_label)
        else:
            end_label = "ENDIF_{0}".format(self.id)
            code += "    JE {0}\n".format(end_label)
            code += self.if_block.Generate(symbol_table)
            code += "{0}:\n".format(end_label)
        return code

class WhileNode(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block
        self.id = Node.newId()

    def Generate(self, symbol_table):
        code = ""
        start_label = "LOOP_{0}".format(self.id)
        end_label = "EXIT_{0}".format(self.id)
        code += "{0}:\n".format(start_label)
        code += self.condition.Generate(symbol_table)
        code += "    CMP EBX, False\n"
        code += "    JE {0}\n".format(end_label)
        code += self.block.Generate(symbol_table)
        code += "    JMP {0}\n".format(start_label)
        code += "{0}:\n".format(end_label)
        return code

class InputNode(Node):
    def __init__(self):
        self.id = Node.newId()

    def Generate(self, symbol_table):
        raise NotImplementedError("scanf não é suportado nesta implementação")

class NoOp(Node):
    def __init__(self):
        self.id = Node.newId()

    def Generate(self, symbol_table):
        return ""
