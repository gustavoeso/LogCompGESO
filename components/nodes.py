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
        elif self.operator == '==':
            code += "    CMP EAX, EBX\n"
            code += f"    JE binop_true_{self.id}\n"
            code += "    MOV EAX, 0\n"
            code += f"    JMP binop_exit_{self.id}\n"
            code += f"binop_true_{self.id}:\n"
            code += "    MOV EAX, 1\n"
            code += f"binop_exit_{self.id}:\n"
        elif self.operator == '<':
            code += "    CMP EAX, EBX\n"
            code += f"    JL binop_true_{self.id}\n"
            code += "    MOV EAX, 0\n"
            code += f"    JMP binop_exit_{self.id}\n"
            code += f"binop_true_{self.id}:\n"
            code += "    MOV EAX, 1\n"
            code += f"binop_exit_{self.id}:\n"
        elif self.operator == '>':
            code += "    CMP EAX, EBX\n"
            code += f"    JG binop_true_{self.id}\n"
            code += "    MOV EAX, 0\n"
            code += f"    JMP binop_exit_{self.id}\n"
            code += f"binop_true_{self.id}:\n"
            code += "    MOV EAX, 1\n"
            code += f"binop_exit_{self.id}:\n"
        else:
            raise ValueError(f"Operador desconhecido '{self.operator}'")

        # O resultado final fica em EAX
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
            code += f"    JE unop_true_{self.id}\n"
            code += "    MOV EAX, 0\n"
            code += f"    JMP unop_exit_{self.id}\n"
            code += f"unop_true_{self.id}:\n"
            code += "    MOV EAX, 1\n"
            code += f"unop_exit_{self.id}:\n"
        else:
            raise ValueError(f"Operador unário desconhecido '{self.operator}'")
        return code

class IntVal(Node):
    def __init__(self, value):
        self.value = value
        self.id = Node.newId()

    def Generate(self, symbol_table):
        code = f"    MOV EAX, {self.value}\n"
        return code

class StringVal(Node):
    def __init__(self, value):
        self.value = value
        self.id = Node.newId()
        # Note que lidar com strings em assembly requer manipulação adicional

    def Generate(self, symbol_table):
        # Para simplificar, não implementaremos strings neste exemplo
        raise NotImplementedError("Strings não são suportadas nesta implementação")

class NoOp(Node):
    def __init__(self):
        self.id = Node.newId()

    def Generate(self, symbol_table):
        return ""

class IdentifierNode(Node):
    def __init__(self, name):
        self.name = name
        self.id = Node.newId()

    def Generate(self, symbol_table):
        var_info = symbol_table.get(self.name)
        offset = var_info['offset']
        code = f"    MOV EAX, [EBP{offset}]\n"
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
        # Armazena o valor de EAX na variável
        var_info = symbol_table.get(self.identifier.name)
        offset = var_info['offset']
        code += f"    MOV [EBP{offset}], EAX\n"
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
            if expression:
                # Gera o código para avaliar a expressão e armazenar na variável
                code += expression.Generate(symbol_table)
                var_info = symbol_table.get(identifier.name)
                offset = var_info['offset']
                code += f"    MOV [EBP{offset}], EAX\n"
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
        # Gera o código para avaliar a expressão e colocar o resultado em EAX
        code += self.expression.Generate(symbol_table)
        # Empilha o argumento para a subrotina de impressão
        code += "    PUSH EAX\n"
        # Chama a subrotina de impressão
        code += "    CALL print\n"
        # Limpa a pilha
        code += "    POP EAX\n"
        return code

class IfNode(Node):
    def __init__(self, condition, if_block, else_block=None):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block
        self.id = Node.newId()

    def Generate(self, symbol_table):
        code = ""
        # Gera o código para a condição (resultado em EAX)
        code += self.condition.Generate(symbol_table)
        # Compara EAX com zero
        code += "    CMP EAX, 0\n"
        if self.else_block:
            else_label = f"ELSE_{self.id}"
            end_label = f"ENDIF_{self.id}"
            # Se EAX == 0, pula para o else
            code += f"    JE {else_label}\n"
            # Gera o código para o bloco 'if'
            code += self.if_block.Generate(symbol_table)
            # Pula para o final
            code += f"    JMP {end_label}\n"
            # Label 'else'
            code += f"{else_label}:\n"
            # Gera o código para o bloco 'else'
            code += self.else_block.Generate(symbol_table)
            # Label final
            code += f"{end_label}:\n"
        else:
            end_label = f"ENDIF_{self.id}"
            # Se EAX == 0, pula para o fim
            code += f"    JE {end_label}\n"
            # Gera o código para o bloco 'if'
            code += self.if_block.Generate(symbol_table)
            # Label final
            code += f"{end_label}:\n"
        return code

class WhileNode(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block
        self.id = Node.newId()

    def Generate(self, symbol_table):
        code = ""
        start_label = f"LOOP_{self.id}"
        end_label = f"ENDLOOP_{self.id}"
        # Label de início do loop
        code += f"{start_label}:\n"
        # Gera o código para a condição (resultado em EAX)
        code += self.condition.Generate(symbol_table)
        # Compara EAX com zero
        code += "    CMP EAX, 0\n"
        # Se EAX == 0, sai do loop
        code += f"    JE {end_label}\n"
        # Gera o código para o bloco do loop
        code += self.block.Generate(symbol_table)
        # Volta ao início do loop
        code += f"    JMP {start_label}\n"
        # Label de fim do loop
        code += f"{end_label}:\n"
        return code

class InputNode(Node):
    def __init__(self):
        self.id = Node.newId()

    def Generate(self, symbol_table):
        # Implementação do scanf não é trivial em assembly e não será suportada aqui
        raise NotImplementedError("scanf não é suportado nesta implementação")
