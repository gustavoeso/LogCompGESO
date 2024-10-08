# symbol_table.py

class SymbolTable:
    def __init__(self):
        self.table = {}
    
    def declare(self, identifier, var_type):
        if identifier in self.table:
            raise ValueError(f"Variável '{identifier}' já declarada.")
        self.table[identifier] = {'value': None, 'type': var_type}

    def get(self, identifier):
        if identifier in self.table:
            return self.table[identifier]
        else:
            raise ValueError(f"Variável '{identifier}' não declarada.")

    def set(self, identifier, value):
        if identifier not in self.table:
            raise ValueError(f"Variável '{identifier}' não declarada.")
        self.table[identifier]['value'] = value
