class SymbolTable:
    def __init__(self, parent=None):
        self.table = {}
        self.parent = parent  # Referência para a tabela de símbolos do escopo pai
        self.has_returned = False
        self.return_value = None

    def declare(self, identifier, var_type):
        if identifier in self.table:
            raise ValueError(f"Variável ou função '{identifier}' já declarada.")
        self.table[identifier] = {'value': None, 'type': var_type}

    def get(self, identifier):
        if identifier in self.table:
            return self.table[identifier]
        elif self.parent:
            return self.parent.get(identifier)
        else:
            raise ValueError(f"Variável ou função '{identifier}' não declarada.")

    def set(self, identifier, value):
        if identifier in self.table:
            self.table[identifier]['value'] = value
        elif self.parent:
            self.parent.set(identifier, value)
        else:
            raise ValueError(f"Variável '{identifier}' não declarada.")

    def set_return(self, value, var_type):
        self.has_returned = True
        self.return_value = (value, var_type)
