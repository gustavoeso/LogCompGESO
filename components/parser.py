from components.tokenizer import Tokenizer

class Parser:
    @staticmethod
    def parseFactor(tokenizer: Tokenizer):
        if tokenizer.next.type == "OPERATOR" and tokenizer.next.value in ["+", "-"]:
            unary_operator = tokenizer.next.value
            tokenizer.selectNext()
            result = Parser.parseFactor(tokenizer)
            if unary_operator == "-":
                return -result
            else:
                return result
        elif tokenizer.next.type == "NUMBER":
            result = tokenizer.next.value
            tokenizer.selectNext()
            return result
        elif tokenizer.next.type == "PARENTHESIS" and tokenizer.next.value == "(":
            tokenizer.selectNext()
            result = Parser.parseExpression(tokenizer)
            if tokenizer.next.type != "PARENTHESIS" or tokenizer.next.value != ")":
                raise ValueError("Mismatched parenthesis")
            tokenizer.selectNext()  # Consume the closing parenthesis
            return result
        else:
            raise ValueError("Expected a number, an operator, or a parenthesis")

    @staticmethod
    def parseTerm(tokenizer: Tokenizer):
        result = Parser.parseFactor(tokenizer)
        while tokenizer.next.type == "OPERATOR" and tokenizer.next.value in ['*', '/']:
            operator = tokenizer.next.value
            tokenizer.selectNext()
            if tokenizer.next.type != "NUMBER" and tokenizer.next.type != "PARENTHESIS" and tokenizer.next.type != "OPERATOR":
                raise ValueError("Expected a number, a parenthesis, or an operator after the operator")
            if operator == "*":
                result *= Parser.parseFactor(tokenizer)
            elif operator == "/":
                denominator = Parser.parseFactor(tokenizer)
                if denominator == 0:
                    raise ValueError("Division by zero is not allowed")
                result /= denominator
        return result

    @staticmethod
    def parseExpression(tokenizer: Tokenizer):
        result = Parser.parseTerm(tokenizer)
        while tokenizer.next.type == "OPERATOR" and tokenizer.next.value in ['+', '-']:
            operator = tokenizer.next.value
            tokenizer.selectNext()
            if tokenizer.next.type != "NUMBER" and tokenizer.next.type != "PARENTHESIS" and tokenizer.next.type != "OPERATOR":
                raise ValueError("Expected a number, a parenthesis, or an operator after the operator")
            if operator == "+":
                result += Parser.parseTerm(tokenizer)
            elif operator == "-":
                result -= Parser.parseTerm(tokenizer)
        return result

    @staticmethod
    def run(code: str):
        tokenizer = Tokenizer(code)
        tokenizer.selectNext()
        result = Parser.parseExpression(tokenizer)
        if tokenizer.next.type != "EOF":
            raise ValueError("Unexpected characters at the end of the expression")
        return result
