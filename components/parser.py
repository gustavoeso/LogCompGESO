import sys
import re
from components.tokenizer import Tokenizer

class Parser:
    @staticmethod
    def parseTerm(tokenizer: Tokenizer):
        result = Parser.parseFactor(tokenizer)
        while tokenizer.next.type == "OPERATOR" and tokenizer.next.value in ['*', '/']:
            operator = tokenizer.next.value
            tokenizer.selectNext()
            if tokenizer.next.type != "NUMBER":
                raise ValueError("Expected a number after the operator")
            if operator == "*":
                result *= tokenizer.next.value
            elif operator == "/":
                result /= tokenizer.next.value
            tokenizer.selectNext()
        return result

    @staticmethod
    def parseExpression(tokenizer: Tokenizer):
        result = Parser.parseTerm(tokenizer)
        
        while tokenizer.next.type == "OPERATOR" and tokenizer.next.value in ['+', '-']:
            operator = tokenizer.next.value
            tokenizer.selectNext()
            if tokenizer.next.type != "NUMBER":
                raise ValueError("Expected a number after the operator")
            if operator == "+":
                result += Parser.parseTerm(tokenizer)
            elif operator == "-":
                result -= Parser.parseTerm(tokenizer)
        return result

    @staticmethod
    def parseFactor(tokenizer: Tokenizer):
        if tokenizer.next.type != "NUMBER":
            raise ValueError('Expression must start with a number')
        result = tokenizer.next.value
        tokenizer.selectNext()
        return result

    @staticmethod
    def run(code: str):
        tokenizer = Tokenizer(code)
        tokenizer.selectNext()
        result = Parser.parseExpression(tokenizer)
        if tokenizer.next.type != "EOF":
            raise ValueError("Unexpected characters at the end of the expression")
        return result
