import sys
import re
from components.tokenizer import Tokenizer

class Parser:
    @staticmethod
    def parseExpression(tokenizer: Tokenizer):
        tokenizer.selectNext()
        result = 0
        
        if tokenizer.next.type == "NUMBER":
            result = tokenizer.next.value
            tokenizer.selectNext()
        
        while tokenizer.next.type == "OPERATOR":
            operator = tokenizer.next.value
            tokenizer.selectNext()
            
            if tokenizer.next.type != "NUMBER":
                raise ValueError("Expected a number after the operator")
            
            if operator == "+":
                result += tokenizer.next.value
            elif operator == "-":
                result -= tokenizer.next.value
            
            tokenizer.selectNext()
        
        if tokenizer.next.type != "EOF":
            raise ValueError("Unexpected characters at the end of the expression")
        
        return result

    @staticmethod
    def run(code: str):
        tokenizer = Tokenizer(source = code)
        return Parser.parseExpression(tokenizer)