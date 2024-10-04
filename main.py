from components.prepro import PrePro
from components.parser import Parser
from components.symbol_table import SymbolTable
import sys

def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("Uso: python main.py <arquivo>.c")
        
        with open(sys.argv[1], 'r') as file:
            source = file.read()
        
        source = PrePro.filter(source)

        tree = Parser.run(source)  # Executa o parser e retorna a árvore de sintaxe abstrata
        
        # Cria a tabela de símbolos e avalia a árvore
        symbol_table = SymbolTable()
        tree.Evaluate(symbol_table)
    
    except ValueError as e:
        sys.stderr.write(f"Erro: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
