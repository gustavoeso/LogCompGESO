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
        # Gera o código para o operando esquerdo (resultado em EAX)
        code += self.left.Generate(symbol_table)
        # Salva EAX na pilha
        code += "    PUSH EAX\n"
        # Gera o código para o operando direito (resultado em EAX)
        code += self.right.Generate(symbol_table)
        # Move o resultado do operando direito para EBX
        code += "    MOV EBX, EAX\n"
        # Recupera o operando esquerdo da pilha para EAX
        code += "    POP EAX\n"

        if self.operator == 'PLUS':
            code += "    ADD EAX, EBX\n"
        elif self.operator == 'MINUS':
            code += "    SUB EAX, EBX\n"
        elif self.operator == 'MULT':
            code += "    IMUL EAX, EBX\n"
        elif self.operator == 'DIV':
            code += "    CDQ\n"  # Estende EAX para EDX:EAX
            code += "    IDIV EBX\n"
        elif self.operator == '<':
            code += "    CMP EAX, EBX\n"
            code += f"    CALL binop_jl_{self.id}\n"
        else:
            raise ValueError(f"Operador desconhecido '{self.operator}'")

        return code

class AssignmentNode(Node):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
        self.id = Node.newId()

    def Generate(self, symbol_table):
        code = ""
        # Gera o código para avaliar a expressão e colocar o resultado em EAX
        code += self.expression.Generate(symbol_table)
        # Armazena o valor de EAX na variável usando EBX
        var_info = symbol_table.get(self.identifier.name)
        offset = var_info['offset']
        code += "    MOV EBX, EAX\n"
        code += f"    MOV [EBP{offset}], EBX ; {self.identifier.name} = ...\n"
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
            code += f"    PUSH DWORD 0 ; Dim {identifier.name} as Integer [EBP{symbol_table.get(identifier.name)['offset']}]\n"
            if expression:
                # Gera o código para avaliar a expressão e armazenar na variável
                code += expression.Generate(symbol_table)
                var_info = symbol_table.get(identifier.name)
                offset = var_info['offset']
                code += f"    MOV [EBP{offset}], EAX ; Inicializa {identifier.name}\n"
        return code

# As demais classes permanecem iguais
