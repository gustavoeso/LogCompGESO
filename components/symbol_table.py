class SymbolTable:
    def __init__(self):
        self.table = {}
        self.offset = 0  # Deslocamento atual em relacao ao EBP

    def declare(self, identifier, var_type):
        if identifier in self.table:
            raise ValueError(f"Variavel '{identifier}' ja declarada.")
        # Cada variavel ocupa 4 bytes (DWORD)
        self.offset -= 4
        self.table[identifier] = {'type': var_type, 'offset': self.offset}

    def get(self, identifier):
        if identifier in self.table:
            return self.table[identifier]
        else:
            raise ValueError(f"Variavel '{identifier}' nao declarada.")

    def set(self, identifier, value):
        if identifier not in self.table:
            raise ValueError(f"Variavel '{identifier}' nao declarada.")
        self.table[identifier]['value'] = value
