from components.tokenizer import Tokenizer
from components.nodes import (
    BinOp, UnOp, IntVal, NoOp, AssignmentNode, BlockNode, PrintNode,
    IdentifierNode, VarDec, StringVal, IfNode, WhileNode, InputNode
)

class Parser:
    tokens = None

    @staticmethod
    def run(code: str):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()
        tree = Parser.parseProgram()
        if Parser.tokens.next.type != "EOF":
            raise ValueError(f"Token inesperado '{Parser.tokens.next.value}' após o fim do programa")
        return tree

    @staticmethod
    def parseProgram():
        return Parser.parseBlock()

    @staticmethod
    def parseBlock():
        if Parser.tokens.next.type != "LBRACE":
            raise ValueError("Esperado '{' no início do bloco")
        Parser.tokens.selectNext()
        statements = []
        while Parser.tokens.next.type != "RBRACE":
            statements.append(Parser.parseStatement())
        Parser.tokens.selectNext()
        return BlockNode(statements)

    @staticmethod
    def parseStatement():
        if Parser.tokens.next.type == "TYPE":
            node = Parser.parseVarDec()
        elif Parser.tokens.next.type == "IDENTIFIER":
            node = Parser.parseAssignment()
        elif Parser.tokens.next.type == "IF":
            node = Parser.parseIf()
        elif Parser.tokens.next.type == "WHILE":
            node = Parser.parseWhile()
        elif Parser.tokens.next.type == "PRINTF":
            node = Parser.parsePrint()
        elif Parser.tokens.next.type == "LBRACE":
            node = Parser.parseBlock()
        elif Parser.tokens.next.type == "SEMICOLON":
            Parser.tokens.selectNext()
            node = NoOp()
        else:
            raise ValueError(f"Comando inesperado '{Parser.tokens.next.value}'")
        return node

    @staticmethod
    def parseVarDec():
        var_type = Parser.tokens.next.value
        Parser.tokens.selectNext()
        declarations = []

        while True:
            if Parser.tokens.next.type != "IDENTIFIER":
                raise ValueError("Esperado um identificador na declaração")
            identifier = IdentifierNode(Parser.tokens.next.value)
            Parser.tokens.selectNext()

            expression = None
            if Parser.tokens.next.type == "ASSIGN":
                Parser.tokens.selectNext()
                expression = Parser.parseExpression()

            declarations.append((identifier, expression))

            if Parser.tokens.next.type == "COMMA":
                Parser.tokens.selectNext()
                continue
            elif Parser.tokens.next.type == "SEMICOLON":
                Parser.tokens.selectNext()
                break
            else:
                raise ValueError("Esperado ',' ou ';' na declaração")

        return VarDec(var_type, declarations)

    @staticmethod
    def parseAssignment():
        identifier = IdentifierNode(Parser.tokens.next.value)
        Parser.tokens.selectNext()
        if Parser.tokens.next.type != "ASSIGN":
            raise ValueError("Esperado '=' na atribuição")
        Parser.tokens.selectNext()
        expression = Parser.parseExpression()
        if Parser.tokens.next.type != "SEMICOLON":
            raise ValueError("Esperado ';' após a atribuição")
        Parser.tokens.selectNext()
        return AssignmentNode(identifier, expression)

    @staticmethod
    def parseIf():
        Parser.tokens.selectNext()
        if Parser.tokens.next.type != "LPAREN":
            raise ValueError("Esperado '(' após 'if'")
        Parser.tokens.selectNext()
        condition = Parser.parseBooleanExpression()
        if Parser.tokens.next.type != "RPAREN":
            raise ValueError("Esperado ')' após a condição 'if'")
        Parser.tokens.selectNext()
        if_block = Parser.parseStatement()
        else_block = None
        if Parser.tokens.next.type == "ELSE":
            Parser.tokens.selectNext()
            else_block = Parser.parseStatement()
        return IfNode(condition, if_block, else_block)

    @staticmethod
    def parseWhile():
        Parser.tokens.selectNext()
        if Parser.tokens.next.type != "LPAREN":
            raise ValueError("Esperado '(' após 'while'")
        Parser.tokens.selectNext()
        condition = Parser.parseBooleanExpression()
        if Parser.tokens.next.type != "RPAREN":
            raise ValueError("Esperado ')' após a condição 'while'")
        Parser.tokens.selectNext()
        block = Parser.parseStatement()
        return WhileNode(condition, block)

    @staticmethod
    def parsePrint():
        Parser.tokens.selectNext()
        if Parser.tokens.next.type != "LPAREN":
            raise ValueError("Esperado '(' após 'printf'")
        Parser.tokens.selectNext()
        expression = Parser.parseBooleanExpression()
        if Parser.tokens.next.type != "RPAREN":
            raise ValueError("Esperado ')' após a expressão em 'printf'")
        Parser.tokens.selectNext()
        if Parser.tokens.next.type != "SEMICOLON":
            raise ValueError("Esperado ';' após 'printf'")
        Parser.tokens.selectNext()
        return PrintNode(expression)

    @staticmethod
    def parseBooleanExpression():
        return Parser.parseLogicalOrExpression()

    @staticmethod
    def parseLogicalOrExpression():
        left = Parser.parseLogicalAndExpression()
        while Parser.tokens.next.type == "OR":
            operator = Parser.tokens.next.type
            Parser.tokens.selectNext()
            right = Parser.parseLogicalAndExpression()
            left = BinOp(left, operator, right)
        return left

    @staticmethod
    def parseLogicalAndExpression():
        left = Parser.parseEqualityExpression()
        while Parser.tokens.next.type == "AND":
            operator = Parser.tokens.next.type
            Parser.tokens.selectNext()
            right = Parser.parseEqualityExpression()
            left = BinOp(left, operator, right)
        return left

    @staticmethod
    def parseEqualityExpression():
        left = Parser.parseRelationalExpression()
        while Parser.tokens.next.type == "EQOP":
            operator = Parser.tokens.next.value
            Parser.tokens.selectNext()
            right = Parser.parseRelationalExpression()
            left = BinOp(left, operator, right)
        return left

    @staticmethod
    def parseRelationalExpression():
        left = Parser.parseExpression()
        while Parser.tokens.next.type == "RELOP":
            operator = Parser.tokens.next.value
            Parser.tokens.selectNext()
            right = Parser.parseExpression()
            left = BinOp(left, operator, right)
        return left

    @staticmethod
    def parseExpression():
        left = Parser.parseTerm()
        while Parser.tokens.next.type in ("PLUS", "MINUS"):
            operator = Parser.tokens.next.type
            Parser.tokens.selectNext()
            right = Parser.parseTerm()
            left = BinOp(left, operator, right)
        return left

    @staticmethod
    def parseTerm():
        left = Parser.parseFactor()
        while Parser.tokens.next.type in ("MULT", "DIV"):
            operator = Parser.tokens.next.type
            Parser.tokens.selectNext()
            right = Parser.parseFactor()
            left = BinOp(left, operator, right)
        return left

    @staticmethod
    def parseFactor():
        if Parser.tokens.next.type == "PLUS":
            Parser.tokens.selectNext()
            factor = Parser.parseFactor()
            return UnOp("PLUS", factor)
        elif Parser.tokens.next.type == "MINUS":
            Parser.tokens.selectNext()
            factor = Parser.parseFactor()
            return UnOp("MINUS", factor)
        elif Parser.tokens.next.type == "NOT":
            Parser.tokens.selectNext()
            factor = Parser.parseFactor()
            return UnOp("NOT", factor)
        elif Parser.tokens.next.type == "NUMBER":
            value = Parser.tokens.next.value
            Parser.tokens.selectNext()
            return IntVal(value)
        elif Parser.tokens.next.type == "IDENTIFIER":
            identifier = IdentifierNode(Parser.tokens.next.value)
            Parser.tokens.selectNext()
            return identifier
        elif Parser.tokens.next.type == "STRING":
            value = Parser.tokens.next.value
            Parser.tokens.selectNext()
            return StringVal(value)
        elif Parser.tokens.next.type == "TRUE":
            Parser.tokens.selectNext()
            return IntVal(1)
        elif Parser.tokens.next.type == "FALSE":
            Parser.tokens.selectNext()
            return IntVal(0)
        elif Parser.tokens.next.type == "LPAREN":
            Parser.tokens.selectNext()
            expression = Parser.parseBooleanExpression()
            if Parser.tokens.next.type != "RPAREN":
                raise ValueError("Esperado ')' após a expressão")
            Parser.tokens.selectNext()
            return expression
        elif Parser.tokens.next.type == "SCANF":
            return Parser.parseInput()
        else:
            raise ValueError(f"Fator inesperado '{Parser.tokens.next.value}'")

    @staticmethod
    def parseInput():
        Parser.tokens.selectNext()  # Consumir 'scanf'
        if Parser.tokens.next.type != "LPAREN":
            raise ValueError("Esperado '(' após 'scanf'")
        Parser.tokens.selectNext()  # Consumir '('
        if Parser.tokens.next.type != "RPAREN":
            raise ValueError("Esperado ')' em 'scanf'")
        Parser.tokens.selectNext()  # Consumir ')'
        return InputNode()
