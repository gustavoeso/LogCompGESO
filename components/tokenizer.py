import sys
import re
from components.my_token import Token

class Tokenizer:
    def __init__(self, source: str, position: int = 0, next: Token = None):
        self.source = source
        self.position = position
        self.next = next

    def selectNext(self):
        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return
        
        current_char = self.source[self.position]

        if current_char.isdigit():
            num = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num += self.source[self.position]
                self.position += 1
            self.next = Token("NUMBER", int(num))
        
        elif current_char in ['+', '-']:
            self.next = Token("OPERATOR", current_char)
            self.position += 1
        
        else:
            raise ValueError(f"Unexpected character: {current_char}")
        
        # Skipping whitespace
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1