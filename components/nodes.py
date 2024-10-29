from abc import ABC, abstractmethod
from components.symbol_table import SymbolTable

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
        left_value, left_type = self.left.Evaluate(symbol_table)
        right_value, right_type = self.right.Evaluate(symbol_table)

        # Operações aritméticas
        if self.operator == 'PLUS':
            if left_type == 'int' and right_type == 'int':
                return left_value + right_value, 'int'
            elif left_type == 'str' and right_type == 'str':
                return left_value + right_value, 'str'
            elif (left_type == 'str' and right_type == 'int') or (left_type == 'int' and right_type == 'str'):
                return str(left_value) + str(right_value), 'str'
            else:
                raise ValueError(f"Operação '+' inválida entre '{left_type}' e '{right_type}'")
        elif self.operator == 'MINUS':
            if left_type == 'int' and right_type == 'int':
                return left_value - right_value, 'int'
            else:
                raise ValueError(f"Operação '-' inválida entre '{left_type}' e '{right_type}'")
        elif self.operator == 'MULT':
            if left_type == 'int' and right_type == 'int':
                return left_value * right_value, 'int'
            else:
                raise ValueError(f"Operação '*' inválida entre '{left_type}' e '{right_type}'")
        elif self.operator == 'DIV':
            if left_type == 'int' and right_type == 'int':
                if right_value == 0:
                    raise ValueError("Divisão por zero")
                return left_value // right_value, 'int'
            else:
                raise ValueError(f"Operação '/' inválida entre '{left_type}' e '{right_type}'")
        # Operadores lógicos
        elif self.operator in ('AND', 'OR'):
            if left_type == 'int' and right_type == 'int':
                left_value = int(bool(left_value))
                right_value = int(bool(right_value))
                if self.operator == 'AND':
                    return int(left_value and right_value), 'int'
                elif self.operator == 'OR':
                    return int(left_value or right_value), 'int'
            else:
                raise ValueError(f"Operação lógica '{self.operator}' inválida entre '{left_type}' e '{right_type}'")
        # Operadores relacionais
        elif self.operator in ('==', '!=', '>', '<'):
            if left_type != right_type:
                raise ValueError(f"Comparação entre tipos diferentes: '{left_type}' e '{right_type}'")
            if self.operator == '==':
                return int(left_value == right_value), 'int'
            elif self.operator == '!=':
                return int(left_value != right_value), 'int'
            elif self.operator == '>':
                return int(left_value > right_value), 'int'
            elif self.operator == '<':
                return int(left_value < right_value), 'int'
            else:
                raise ValueError(f"Operador relacional desconhecido '{self.operator}'")
        else:
            raise ValueError(f"Operador desconhecido '{self.operator}'")

class UnOp(Node):
    def __init__(self, operator, child):
        self.operator = operator
        self.child = child

    def Evaluate(self, symbol_table):
        value, var_type = self.child.Evaluate(symbol_table)

        if self.operator == 'PLUS':
            if var_type == 'int':
                return +value, 'int'
            else:
                raise ValueError("Operação unária '+' inválida para o tipo")
        elif self.operator == 'MINUS':
            if var_type == 'int':
                return -value, 'int'
            else:
                raise ValueError("Operação unária '-' inválida para o tipo")
        elif self.operator == 'NOT':
            if var_type == 'int':
                return int(not bool(value)), 'int'
            else:
                raise ValueError("Operação '!' inválida para o tipo")
        else:
            raise ValueError(f"Operador unário desconhecido '{self.operator}'")

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self, symbol_table):
        return self.value, 'int'

class StringVal(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self, symbol_table):
        return self.value, 'str'

class NoOp(Node):
    def Evaluate(self, symbol_table):
        pass

class IdentifierNode(Node):
    def __init__(self, name):
        self.name = name

    def Evaluate(self, symbol_table):
        var_info = symbol_table.get(self.name)
        return var_info['value'], var_info['type']

class AssignmentNode(Node):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def Evaluate(self, symbol_table):
        var_info = symbol_table.get(self.identifier.name)
        value, expr_type = self.expression.Evaluate(symbol_table)
        var_type = var_info['type']

        if expr_type != var_type:
            # Não permitir atribuição de 'int' para 'str' ou vice-versa
            raise ValueError(f"Tipo incompatível na atribuição para '{self.identifier.name}': esperado '{var_type}', mas obteve '{expr_type}'")
        symbol_table.set(self.identifier.name, value)

class VarDec(Node):
    def __init__(self, var_type, declarations):
        self.var_type = var_type
        self.declarations = declarations  # Lista de (IdentifierNode, ExpressionNode ou None)

    def Evaluate(self, symbol_table):
        for identifier, expression in self.declarations:
            symbol_table.declare(identifier.name, self.var_type)
            if expression:
                value, expr_type = expression.Evaluate(symbol_table)
                var_type = self.var_type
                if expr_type != var_type:
                    raise ValueError(f"Tipo incompatível na inicialização de '{identifier.name}': esperado '{var_type}', mas obteve '{expr_type}'")
                symbol_table.set(identifier.name, value)

class BlockNode(Node):
    def __init__(self, statements):
        self.statements = statements

    def Evaluate(self, symbol_table):
        for statement in self.statements:
            statement.Evaluate(symbol_table)
            if symbol_table.has_returned:
                break

class PrintNode(Node):
    def __init__(self, expression):
        self.expression = expression

    def Evaluate(self, symbol_table):
        value, _ = self.expression.Evaluate(symbol_table)
        print(value)

class IfNode(Node):
    def __init__(self, condition, if_block, else_block=None):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block

    def Evaluate(self, symbol_table):
        condition_value, _ = self.condition.Evaluate(symbol_table)
        if condition_value:
            self.if_block.Evaluate(symbol_table)
        elif self.else_block:
            self.else_block.Evaluate(symbol_table)

class WhileNode(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def Evaluate(self, symbol_table):
        while True:
            condition_value, _ = self.condition.Evaluate(symbol_table)
            if condition_value:
                self.block.Evaluate(symbol_table)
            else:
                break

class InputNode(Node):
    def Evaluate(self, symbol_table):
        user_input = input()
        try:
            value = int(user_input)
            return value, 'int'
        except ValueError:
            raise ValueError(f"Entrada inválida: '{user_input}' não é um número inteiro")

class FuncDec(Node):
    def __init__(self, func_type, name, params, body):
        self.func_type = func_type  # Tipo de retorno da função
        self.name = name            # Nome da função
        self.params = params        # Lista de (tipo, nome) dos parâmetros
        self.body = body            # Bloco de statements

    def Evaluate(self, symbol_table):
        # Registrar a função na tabela de símbolos atual
        symbol_table.declare(self.name, 'FUNCTION')
        symbol_table.set(self.name, self)

class FuncCall(Node):
    def __init__(self, name, args):
        self.name = name    # Nome da função a ser chamada
        self.args = args    # Lista de expressões como argumentos

    def Evaluate(self, symbol_table):
        # Procurar a função na tabela de símbolos
        func_info = symbol_table.get(self.name)
        if func_info['type'] != 'FUNCTION':
            raise ValueError(f"'{self.name}' não é uma função.")

        func_node = func_info['value']

        # Verificar número de argumentos
        if len(self.args) != len(func_node.params):
            raise ValueError(f"Número incorreto de argumentos na chamada de '{self.name}'.")

        # Criar nova tabela de símbolos para a função
        local_symbol_table = SymbolTable(symbol_table)  # Passamos a tabela de símbolos atual como pai

        # Avaliar os argumentos e declarar as variáveis locais
        for (param_type, param_name), arg_expr in zip(func_node.params, self.args):
            arg_value, arg_type = arg_expr.Evaluate(symbol_table)
            if arg_type != param_type:
                raise ValueError(f"Tipo do argumento '{param_name}' incompatível na chamada de '{self.name}'.")
            local_symbol_table.declare(param_name, param_type)
            local_symbol_table.set(param_name, arg_value)

        # Executar o corpo da função
        func_node.body.Evaluate(local_symbol_table)

        # Verificar se a função retornou um valor
        if local_symbol_table.has_returned:
            return_value = local_symbol_table.return_value
            if func_node.func_type == 'void':
                if return_value is not None:
                    raise ValueError(f"Função '{self.name}' é 'void' e não deve retornar valor.")
                return None, 'void'
            else:
                if return_value is None:
                    raise ValueError(f"Função '{self.name}' deveria retornar '{func_node.func_type}', mas não retornou nenhum valor.")
                if return_value[1] != func_node.func_type:
                    raise ValueError(f"Tipo de retorno incompatível na função '{self.name}'. Esperado '{func_node.func_type}', mas obteve '{return_value[1]}'.")
                return return_value
        else:
            if func_node.func_type != 'void':
                raise ValueError(f"Função '{self.name}' deveria retornar '{func_node.func_type}', mas não retornou nenhum valor.")
            return None, 'void'

class ReturnNode(Node):
    def __init__(self, expression):
        self.expression = expression  # Pode ser None para 'return;'

    def Evaluate(self, symbol_table):
        if self.expression:
            value, var_type = self.expression.Evaluate(symbol_table)
            symbol_table.set_return(value, var_type)
        else:
            symbol_table.set_return(None, None)
