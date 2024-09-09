import sys
import re
from components.my_token import Token

class Tokenizer:
    def __init__(self, source: str, position: int = 0, next: Token = None):
        self.source = source
        self.position = position
        self.next = next

    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return
        
        current_char = self.source[self.position]

        # Verificação para identificar variáveis, palavras-chave como 'printf' e agora identificadores com '_'
        if current_char.isalpha() or current_char == "_":  # Identificadores podem começar com letra ou underscore
            identifier = ""
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                identifier += self.source[self.position]
                self.position += 1
            
            # Se o identificador for 'printf', retornar um token especial
            if identifier == "printf":
                self.next = Token("PRINTF", identifier)
            # Se o identificador for 'int', apenas ignorar, pois é uma palavra-chave
            elif identifier == "int":
                self.selectNext()  # Consumir 'int' e passar para o próximo token
            else:
                self.next = Token("IDENTIFIER", identifier)

        # Verificação para números
        elif current_char.isdigit():
            num = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num += self.source[self.position]
                self.position += 1
            self.next = Token("NUMBER", int(num))

        # Verificação para operadores, parênteses, chaves (blocos de instruções), e o operador '='
        elif current_char in ['+', '-', '*', '/', '(', ')', '{', '}', '=']:
            if current_char in ['+', '-', '*', '/']:
                self.next = Token("OPERATOR", current_char)
            elif current_char == '=':
                self.next = Token("OPERATOR", '=')
            elif current_char == '(':
                self.next = Token("PARENTHESIS", '(')
            elif current_char == ')':
                self.next = Token("PARENTHESIS", ')')
            elif current_char == '{':
                self.next = Token("OPEN_BRACE", '{')
            elif current_char == '}':
                self.next = Token("CLOSE_BRACE", '}')
            self.position += 1

        # Verificação para ponto e vírgula
        elif current_char == ';':
            self.next = Token("SEMICOLON", current_char)
            self.position += 1

        # Caso de erro para caracteres inesperados
        else:
            raise ValueError(f"Unexpected character: {current_char}")
