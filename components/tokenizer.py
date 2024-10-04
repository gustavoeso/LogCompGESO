from components.my_token import Token

class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        # Ignorar espaços em branco
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return

        current_char = self.source[self.position]

        # Identificadores e palavras-chave
        if current_char.isalpha() or current_char == "_":
            identifier = ""
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                identifier += self.source[self.position]
                self.position += 1

            # Verificar palavras-chave
            keywords = {
                "if": "IF",
                "else": "ELSE",
                "while": "WHILE",
                "scanf": "SCANF",
                "printf": "PRINTF"
            }

            token_type = keywords.get(identifier, "IDENTIFIER")
            self.next = Token(token_type, identifier)

        # Números
        elif current_char.isdigit():
            num = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num += self.source[self.position]
                self.position += 1
            self.next = Token("NUMBER", int(num))

        # Operadores e símbolos
        else:
            two_char_operators = {"==": "RELOP", "!=": "RELOP", "&&": "LOGOP", "||": "LOGOP"}
            one_char_operators = {'=': "ASSIGN", '>': "RELOP", '<': "RELOP", '+': "PLUS", '-': "MINUS", '*': "MULT", '/': "DIV", '(': "LPAREN", ')': "RPAREN", '{': "LBRACE", '}': "RBRACE", ';': "SEMICOLON", '!': "NOT"}

            if self.position + 1 < len(self.source):
                two_char = self.source[self.position:self.position+2]
                if two_char in two_char_operators:
                    self.next = Token(two_char_operators[two_char], two_char)
                    self.position += 2
                    return

            if current_char in one_char_operators:
                token_type = one_char_operators[current_char]
                self.next = Token(token_type, current_char)
                self.position += 1
            else:
                raise ValueError(f"Caractere inesperado: '{current_char}' na posição {self.position}")
