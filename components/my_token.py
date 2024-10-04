import sys
import re

class Token:
    def __init__(self, type: str, value):
        self.type = type
        self.value = value