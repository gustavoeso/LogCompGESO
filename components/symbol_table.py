class SymbolTable:
    def __init__(self):
        self.table = {}

    def get(self, identifier):
        if identifier in self.table:
            return self.table[identifier]
        else:
            raise ValueError(f"Identificador '{identifier}' não encontrado.")

    def set(self, identifier, value):
        self.table[identifier] = value