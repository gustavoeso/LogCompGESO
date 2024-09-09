from components.prepro import PrePro
from components.parser import Parser
from components.tokenizer import Tokenizer
from components.symbol_table import SymbolTable
import sys

def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("Usage: python main.py <filename>.c")
        
        with open(sys.argv[1], 'r') as file:
            source = file.read()
        
        source = PrePro.filter(source)

        tokenizer = Tokenizer(source)
        tokenizer.selectNext()
        
        tree = Parser.run(source)  # Executa o parser e retorna a árvore de sintaxe abstrata
        
        # Cria a tabela de símbolos e passa no Evaluate
        symbol_table = SymbolTable()
        result = tree.Evaluate(symbol_table)
        
        # Verifica se o resultado não é None antes de imprimir
        if result is not None:
            print(int(result))
    
    except ValueError as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
 