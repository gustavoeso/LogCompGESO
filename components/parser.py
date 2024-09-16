from components.tokenizer import Tokenizer
from components.nodes import BinOp, UnOp, IntVal, NoOp, AssignmentNode, BlockNode, PrintNode, IdentifierNode, BoolOp, RelOp, IfNode, WhileNode, InputNode

class Parser:
    @staticmethod
    def parseFactor(tokenizer: Tokenizer):
        if tokenizer.next.type == "SYMBOL" and tokenizer.next.value in ["+", "-"]:
            operator = tokenizer.next.value
            tokenizer.selectNext()
            factor = Parser.parseFactor(tokenizer)
            return UnOp(operator, factor)
        elif tokenizer.next.type == "NUMBER":
            value = tokenizer.next.value
            tokenizer.selectNext()
            return IntVal(value)
        elif tokenizer.next.type == "SYMBOL" and tokenizer.next.value == "(":
            tokenizer.selectNext()
            expression = Parser.parseBooleanExpression(tokenizer)
            if tokenizer.next.type != "SYMBOL" or tokenizer.next.value != ")":
                raise ValueError("Mismatched parenthesis")
            tokenizer.selectNext()
            return expression
        elif tokenizer.next.type == "LOGOP" and tokenizer.next.value == "!":
            tokenizer.selectNext()
            factor = Parser.parseFactor(tokenizer)
            return UnOp("!", factor)
        elif tokenizer.next.type == "IDENTIFIER":
            identifier = tokenizer.next.value
            tokenizer.selectNext()
            return IdentifierNode(identifier)
        elif tokenizer.next.type == "SCANF":
            return Parser.parseInput(tokenizer)
        else:
            raise ValueError("Expected a number, an operator, or a parenthesis")

    @staticmethod
    def parseTerm(tokenizer: Tokenizer):
        left = Parser.parseFactor(tokenizer)
        while tokenizer.next.type == "SYMBOL" and tokenizer.next.value in ['*', '/']:
            operator = tokenizer.next.value
            tokenizer.selectNext()
            right = Parser.parseFactor(tokenizer)
            left = BinOp(left, operator, right)
        return left

    @staticmethod
    def parseExpression(tokenizer: Tokenizer):
        left = Parser.parseTerm(tokenizer)
        while tokenizer.next.type == "SYMBOL" and tokenizer.next.value in ['+', '-']:
            operator = tokenizer.next.value
            tokenizer.selectNext()
            right = Parser.parseTerm(tokenizer)
            left = BinOp(left, operator, right)
        return left

    @staticmethod
    def parseAssignment(tokenizer: Tokenizer):
        identifier = tokenizer.next.value
        tokenizer.selectNext()  # Consumir o identificador
        if tokenizer.next.type != "SYMBOL" or tokenizer.next.value != "=":
            raise ValueError("Expected '=' after identifier")
        tokenizer.selectNext()  # Consumir o '='
        expression = Parser.parseExpression(tokenizer)
        if tokenizer.next.type != "SYMBOL" or tokenizer.next.value != ";":
            raise ValueError("Expected ';' after assignment")
        tokenizer.selectNext()  # Consumir ';'
        return AssignmentNode(identifier, expression)

    @staticmethod
    def parseBlock(tokenizer: Tokenizer):
        instructions = []
        if tokenizer.next.type == "SYMBOL" and tokenizer.next.value == "{":
            tokenizer.selectNext()  # Consumir '{'
            while tokenizer.next.type != "SYMBOL" or tokenizer.next.value != "}":
                instructions.append(Parser.parseStatement(tokenizer))
            tokenizer.selectNext()  # Consumir '}'
        else:
            raise ValueError("Expected '{' at the beginning of the block")
        return BlockNode(instructions)

    @staticmethod
    def parsePrint(tokenizer: Tokenizer):
        tokenizer.selectNext()  # Consumir 'printf'
        if tokenizer.next.type != "SYMBOL" or tokenizer.next.value != '(':
            raise ValueError("Expected '(' after 'printf'")
        tokenizer.selectNext()  # Consumir '('
        expression = Parser.parseExpression(tokenizer)
        if tokenizer.next.type != "SYMBOL" or tokenizer.next.value != ')':
            raise ValueError("Expected ')' after expression")
        tokenizer.selectNext()  # Consumir ')'
        if tokenizer.next.type != "SYMBOL" or tokenizer.next.value != ";":
            raise ValueError("Expected ';' after 'printf'")
        tokenizer.selectNext()  # Consumir ';'
        return PrintNode(expression)

    @staticmethod
    def parseStatement(tokenizer: Tokenizer):
        if tokenizer.next.type == "IDENTIFIER":
            return Parser.parseAssignment(tokenizer)
        elif tokenizer.next.type == "PRINTF":
            return Parser.parsePrint(tokenizer)
        elif tokenizer.next.type == "SCANF":
            return Parser.parseInput(tokenizer)
        elif tokenizer.next.type == "IF":
            return Parser.parseIf(tokenizer)
        elif tokenizer.next.type == "WHILE":
            return Parser.parseWhile(tokenizer)
        elif tokenizer.next.type == "SYMBOL" and tokenizer.next.value == "{":
            return Parser.parseBlock(tokenizer)
        elif tokenizer.next.type == "SYMBOL" and tokenizer.next.value == ";":  # Ignora múltiplos ';'
            tokenizer.selectNext()
            return NoOp()
        else:
            raise ValueError("Unexpected statement")

    @staticmethod
    def parseBooleanExpression(tokenizer: Tokenizer):
        left = Parser.parseRelationalExpression(tokenizer)
        while tokenizer.next.type == "LOGOP" and tokenizer.next.value in ["&&", "||"]:
            operator = tokenizer.next.value
            tokenizer.selectNext()
            right = Parser.parseRelationalExpression(tokenizer)
            left = BoolOp(left, operator, right)
        return left

    @staticmethod
    def parseRelationalExpression(tokenizer: Tokenizer):
        left = Parser.parseExpression(tokenizer)
        if tokenizer.next.type == "RELOP":
            operator = tokenizer.next.value
            tokenizer.selectNext()
            right = Parser.parseExpression(tokenizer)
            return RelOp(left, operator, right)
        return left

    @staticmethod
    def parseIf(tokenizer: Tokenizer):
        tokenizer.selectNext()  # Consumir 'if'
        if tokenizer.next.type != "SYMBOL" or tokenizer.next.value != "(":
            raise ValueError("Expected '(' after 'if'")
        tokenizer.selectNext()
        condition = Parser.parseBooleanExpression(tokenizer)
        if tokenizer.next.type != "SYMBOL" or tokenizer.next.value != ")":
            raise ValueError("Expected ')' after condition")
        tokenizer.selectNext()
        
        # Verificar se é um bloco ou uma única instrução
        if tokenizer.next.type == "SYMBOL" and tokenizer.next.value == "{":
            if_block = Parser.parseBlock(tokenizer)
        else:
            if_block = Parser.parseStatement(tokenizer)

        else_block = None
        if tokenizer.next.type == "ELSE":
            tokenizer.selectNext()
            if tokenizer.next.type == "SYMBOL" and tokenizer.next.value == "{":
                else_block = Parser.parseBlock(tokenizer)
            else:
                else_block = Parser.parseStatement(tokenizer)

        return IfNode(condition, if_block, else_block)

    @staticmethod
    def parseWhile(tokenizer: Tokenizer):
        tokenizer.selectNext()  # Consumir 'while'
        if tokenizer.next.type != "SYMBOL" or tokenizer.next.value != "(":
            raise ValueError("Expected '(' after 'while'")
        tokenizer.selectNext()
        condition = Parser.parseBooleanExpression(tokenizer)
        if tokenizer.next.type != "SYMBOL" or tokenizer.next.value != ")":
            raise ValueError("Expected ')' after condition")
        tokenizer.selectNext()
        block = Parser.parseBlock(tokenizer)
        return WhileNode(condition, block)

    @staticmethod
    def parseInput(tokenizer: Tokenizer):
        tokenizer.selectNext()  # Consumir 'scanf'
        if tokenizer.next.type != "SYMBOL" or tokenizer.next.value != "(":
            raise ValueError("Expected '(' after 'scanf'")
        tokenizer.selectNext()
        if tokenizer.next.type != "SYMBOL" or tokenizer.next.value != ")":
            raise ValueError("Expected ')' after 'scanf'")
        tokenizer.selectNext()
        if tokenizer.next.type != "SYMBOL" or tokenizer.next.value != ";":
            raise ValueError("Expected ';' after 'scanf'")
        tokenizer.selectNext()
        return InputNode("scanf")  # Identificamos que o scanf retorna um valor

    @staticmethod
    def run(code: str):
        tokenizer = Tokenizer(code)
        tokenizer.selectNext()
        tree = Parser.parseBlock(tokenizer)
        if tokenizer.next.type != "EOF":
            raise ValueError(f"Unexpected characters at the end of the expression: {tokenizer.next.value}")
        return tree
