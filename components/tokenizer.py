from components.my_token import Token

class Tokenizer:
    def __init__(self, source: str, position: int = 0, next: Token = None):
        self.source = source
        self.position = position
        self.next = next

    def selectNext(self):
        # Ignorar espaços em branco
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return

        current_char = self.source[self.position]

        # Identificação de identificadores e palavras-chave
        if current_char.isalpha() or current_char == "_":
            identifier = ""
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                identifier += self.source[self.position]
                self.position += 1

            # Verificar palavras-chave
            if identifier == "if":
                self.next = Token("IF", identifier)
            elif identifier == "else":
                self.next = Token("ELSE", identifier)
            elif identifier == "while":
                self.next = Token("WHILE", identifier)
            elif identifier == "scanf":
                self.next = Token("SCANF", identifier)
            elif identifier == "printf":
                self.next = Token("PRINTF", identifier)
            else:
                self.next = Token("IDENTIFIER", identifier)

        # Operadores relacionais e atribuição
        elif current_char == '=':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                self.next = Token("RELOP", "==")  # Operador relacional de igualdade
                self.position += 2
            else:
                self.next = Token("SYMBOL", "=")  # Operador de atribuição
                self.position += 1

        # Operadores booleanos e relacionais
        elif current_char in ['>', '<']:
            self.next = Token("RELOP", current_char)
            self.position += 1

        # Operadores lógicos: &&, ||, e !
        elif current_char == '&':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '&':
                self.next = Token("LOGOP", "&&")  # Operador lógico AND
                self.position += 2
            else:
                raise ValueError(f"Unexpected character: {current_char}")
        
        elif current_char == '|':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '|':
                self.next = Token("LOGOP", "||")  # Operador lógico OR
                self.position += 2
            else:
                raise ValueError(f"Unexpected character: {current_char}")

        elif current_char == '!':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                self.next = Token("RELOP", "!=")  # Diferente
                self.position += 2
            else:
                self.next = Token("LOGOP", "!")  # Operador lógico NOT
                self.position += 1

        # Números
        elif current_char.isdigit():
            num = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num += self.source[self.position]
                self.position += 1
            self.next = Token("NUMBER", int(num))

        # Operadores matemáticos, parênteses, e chaves
        elif current_char in ['+', '-', '*', '/', '(', ')', '{', '}', ';']:
            self.next = Token("SYMBOL", current_char)
            self.position += 1

        else:
            raise ValueError(f"Unexpected character: {current_char}")
