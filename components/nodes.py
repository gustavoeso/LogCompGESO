from abc import ABC, abstractmethod
from components.symbol_table import SymbolTable

class Node(ABC):
    i = 0  # Atributo estatico para IDs unicos

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
        # Gera o codigo para o operando esquerdo (resultado em EAX)
        code += self.left.Generate(symbol_table)
        # Salva EAX na pilha
        code += "    PUSH EAX\n"
        # Gera o codigo para o operando direito (resultado em EAX)
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
            code += "    IMUL EBX\n"
        elif self.operator == 'DIV':
            code += "    CDQ\n"  # Estende EAX para EDX:EAX
            code += "    IDIV EBX\n"
        elif self.operator == '<':
            code += "    CMP EAX, EBX\n"
            code += "    CALL binop_jl\n"
        elif self.operator == '>':
            code += "    CMP EAX, EBX\n"
            code += "    CALL binop_jg\n"
        elif self.operator == '==':
            code += "    CMP EAX, EBX\n"
            code += "    CALL binop_je\n"
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
        else:
            raise ValueError(f"Operador unario desconhecido '{self.operator}'")
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
        # Note que lidar com strings em assembly requer manipulacao adicional

    def Generate(self, symbol_table):
        # Para simplificar, nao implementaremos strings nesta implementacao
        raise NotImplementedError("Strings nao sao suportadas nesta implementacao")

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
        # Gera o codigo para avaliar a expressao e colocar o resultado em EAX
        code += self.expression.Generate(symbol_table)
        # Armazena o valor de EAX na variavel usando EBX
        var_info = symbol_table.get(self.identifier.name)
        offset = var_info['offset']
        code += "    MOV EBX, EAX\n"
        code += "    MOV [EBP{0}], EBX ; {1} = ...\n".format(offset, self.identifier.name)
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
            # Gera 'PUSH DWORD 0' para reservar espaco na pilha
            offset = symbol_table.get(identifier.name)['offset']
            code += "    PUSH DWORD 0 ; Dim {0} as Integer [EBP{1}]\n".format(identifier.name, offset)
            if expression:
                # Gera o codigo para avaliar a expressao e armazenar na variavel
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
        # Gera o codigo para avaliar a expressao e colocar o resultado em EAX
        code += self.expression.Generate(symbol_table)
        # Empilha o argumento para a sub-rotina de impressao
        code += "    PUSH EAX ; empilha argumento para print\n"
        # Chama a sub-rotina de impressao
        code += "    CALL print\n"
        # Ajusta o ESP apos a chamada (limpa o argumento da pilha)
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
        # Gera o codigo para a condicao (resultado em EAX)
        code += self.condition.Generate(symbol_table)
        # Compara EAX com zero
        code += "    CMP EAX, 0\n"
        if self.else_block:
            else_label = "ELSE_{0}".format(self.id)
            end_label = "ENDIF_{0}".format(self.id)
            # Se EAX == 0, pula para o else
            code += "    JE {0}\n".format(else_label)
            # Gera o codigo para o bloco 'if'
            code += self.if_block.Generate(symbol_table)
            # Pula para o final
            code += "    JMP {0}\n".format(end_label)
            # Label 'else'
            code += "{0}:\n".format(else_label)
            # Gera o codigo para o bloco 'else'
            code += self.else_block.Generate(symbol_table)
            # Label final
            code += "{0}:\n".format(end_label)
        else:
            end_label = "ENDIF_{0}".format(self.id)
            # Se EAX == 0, pula para o fim
            code += "    JE {0}\n".format(end_label)
            # Gera o codigo para o bloco 'if'
            code += self.if_block.Generate(symbol_table)
            # Label final
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
        # Label de inicio do loop
        code += "{0}:\n".format(start_label)
        # Gera o codigo para a condicao (resultado em EAX)
        code += self.condition.Generate(symbol_table)
        # Compara EAX com zero
        code += "    CMP EAX, 0\n"
        # Se EAX == 0, sai do loop
        code += "    JE {0}\n".format(end_label)
        # Gera o codigo para o bloco do loop
        code += self.block.Generate(symbol_table)
        # Volta ao inicio do loop
        code += "    JMP {0}\n".format(start_label)
        # Label de fim do loop
        code += "{0}:\n".format(end_label)
        return code

class InputNode(Node):
    def __init__(self):
        self.id = Node.newId()

    def Generate(self, symbol_table):
        # Implementacao do scanf nao e trivial em assembly e nao sera suportada aqui
        raise NotImplementedError("scanf nao e suportado nesta implementacao")

class NoOp(Node):
    def __init__(self):
        self.id = Node.newId()

    def Generate(self, symbol_table):
        return ""
