import sys
import re
from components.parser import Parser

def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("Usage: python main.py '<expression>'")
        
        expression = sys.argv[1]
        result = Parser.run(expression)
        print(int(result))
    
    except ValueError as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()