from components.tokenizer import Tokenizer
from components.nodes import BinOp, UnOp, IntVal, NoOp

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
                raise ValueError("Mismatched parenthesis")
            tokenizer.selectNext()  # Consume the closing parenthesis
            return expression
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
            right = Parser.parseTerm(tokenizer)  # Chamando parseTerm para garantir precedência
            left = BinOp(left, operator, right)
        return left

    @staticmethod
    def run(code: str):
        tokenizer = Tokenizer(code)
        tokenizer.selectNext()
        tree = Parser.parseExpression(tokenizer)
        if tokenizer.next.type != "EOF":
            raise ValueError("Unexpected characters at the end of the expression")
        return tree
