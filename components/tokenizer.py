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

        # Verificação para identificar variáveis, palavras reservadas ('int') ou 'printf'
        if current_char.isalpha():  # Identificadores (variáveis) ou palavras-chave como 'int' e 'printf'
            identifier = ""
            while self.position < len(self.source) and self.source[self.position].isalnum():
                identifier += self.source[self.position]
                self.position += 1
            
            # Se o identificador for 'int', ignorar (é uma palavra reservada)
            if identifier == "int":
                self.selectNext()  # Ignora 'int' e vai para o próximo token
            elif identifier == "printf":
                self.next = Token("PRINTF", identifier)
            else:
                self.next = Token("IDENTIFIER", identifier)

        # Verificação para números
        elif current_char.isdigit():
            num = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num += self.source[self.position]
                self.position += 1
            self.next = Token("NUMBER", int(num))

        # Verificação para operadores, parênteses, chaves (blocos de instruções), e agora o operador '='
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
