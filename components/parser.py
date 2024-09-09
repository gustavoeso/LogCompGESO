from components.tokenizer import Tokenizer
from components.nodes import BinOp, UnOp, IntVal, NoOp, AssignmentNode, BlockNode, PrintNode, IdentifierNode

class Parser:
    @staticmethod
    def parseFactor(tokenizer: Tokenizer):
        if tokenizer.next.type == "OPERATOR" and tokenizer.next.value in ["+", "-"]:
            operator = tokenizer.next.value
            tokenizer.selectNext()
            factor = Parser.parseFactor(tokenizer)
            return UnOp(operator, factor)
        elif tokenizer.next.type == "NUMBER":
            value = tokenizer.next.value
            tokenizer.selectNext()
            return IntVal(value)
        elif tokenizer.next.type == "PARENTHESIS" and tokenizer.next.value == "(":
            tokenizer.selectNext()
            expression = Parser.parseExpression(tokenizer)
            if tokenizer.next.type != "PARENTHESIS" or tokenizer.next.value != ")":
                raise ValueError("Mismatched parenthesis: expected `)` but found something else")
            tokenizer.selectNext()
            return expression
        elif tokenizer.next.type == "IDENTIFIER":  # Verifica se é um identificador (variável)
            identifier = tokenizer.next.value
            tokenizer.selectNext()
            return IdentifierNode(identifier)
        else:
            raise ValueError("Expected a number, an operator, or a parenthesis")

    @staticmethod
    def parseTerm(tokenizer: Tokenizer):
        left = Parser.parseFactor(tokenizer)
        while tokenizer.next.type == "OPERATOR" and tokenizer.next.value in ['*', '/']:
            operator = tokenizer.next.value
            tokenizer.selectNext()
            right = Parser.parseFactor(tokenizer)
            left = BinOp(left, operator, right)
        return left

    @staticmethod
    def parseExpression(tokenizer: Tokenizer):
        left = Parser.parseTerm(tokenizer)
        while tokenizer.next.type == "OPERATOR" and tokenizer.next.value in ['+', '-']:
            operator = tokenizer.next.value
            tokenizer.selectNext()
            right = Parser.parseTerm(tokenizer)
            left = BinOp(left, operator, right)
        return left

    @staticmethod
    def parseAssignment(tokenizer: Tokenizer):
        identifier = tokenizer.next.value
        tokenizer.selectNext()  # Consumir o identificador
        if tokenizer.next.type != "OPERATOR" or tokenizer.next.value != "=":
            raise ValueError("Expected '=' after identifier")
        tokenizer.selectNext()  # Consumir o '='
        expression = Parser.parseExpression(tokenizer)
        if tokenizer.next.type != "SEMICOLON":
            raise ValueError("Expected ';' after assignment")
        tokenizer.selectNext()  # Consumir ';'
        return AssignmentNode(identifier, expression)

    @staticmethod
    def parseBlock(tokenizer: Tokenizer):
        instructions = []
        if tokenizer.next.type == "OPEN_BRACE":
            tokenizer.selectNext()  # Consumir '{'
            while tokenizer.next.type != "CLOSE_BRACE":
                instructions.append(Parser.parseStatement(tokenizer))
            tokenizer.selectNext()  # Consumir '}'
        else:
            raise ValueError("Expected '{' at the beginning of the block")
        return BlockNode(instructions)

    @staticmethod
    def parsePrint(tokenizer: Tokenizer):
        tokenizer.selectNext()  # Consumir 'printf'
        if tokenizer.next.type != "PARENTHESIS" or tokenizer.next.value != '(':
            raise ValueError("Expected '(' after 'printf'")
        tokenizer.selectNext()  # Consumir '('
        expression = Parser.parseExpression(tokenizer)
        if tokenizer.next.type != "PARENTHESIS" or tokenizer.next.value != ')':
            raise ValueError("Expected ')' after expression")
        tokenizer.selectNext()  # Consumir ')'
        if tokenizer.next.type != "SEMICOLON":
            raise ValueError("Expected ';' after 'printf'")
        tokenizer.selectNext()  # Consumir ';'
        return PrintNode(expression)

    @staticmethod
    def parseStatement(tokenizer: Tokenizer):
        if tokenizer.next.type == "IDENTIFIER":
            identifier = tokenizer.next.value
            tokenizer.selectNext()

            # Verifica se é uma atribuição ou apenas uma expressão
            if tokenizer.next.type == "OPERATOR" and tokenizer.next.value == "=":
                tokenizer.selectNext()  # Consumir o '='
                expression = Parser.parseExpression(tokenizer)
                if tokenizer.next.type != "SEMICOLON":
                    raise ValueError("Expected ';' after assignment")
                tokenizer.selectNext()  # Consumir ';'
                return AssignmentNode(identifier, expression)
            else:
                # Se não for uma atribuição, deve ser uma expressão envolvendo o identificador
                return IdentifierNode(identifier)

        elif tokenizer.next.type == "PRINTF":
            return Parser.parsePrint(tokenizer)
        elif tokenizer.next.type == "OPEN_BRACE":
            return Parser.parseBlock(tokenizer)
        elif tokenizer.next.type == "SEMICOLON":  # Ignora múltiplos pontos e vírgulas
            tokenizer.selectNext()
            return NoOp()
        else:
            raise ValueError("Unexpected statement")

    @staticmethod
    def run(code: str):
        tokenizer = Tokenizer(code)
        tokenizer.selectNext()
        tree = Parser.parseStatement(tokenizer)
        if tokenizer.next.type != "EOF":
            raise ValueError(f"Unexpected characters at the end of the expression: {tokenizer.next.value}")
        return tree
