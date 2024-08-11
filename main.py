import sys
import re

def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("Usage: python main.py '<expression>'")
        
        expression = sys.argv[1].replace(" ", "")
        
        # Tokenize the expression
        tokens = re.findall(r'\d+|[+-]', expression)
        
        # Validate the expression
        if not tokens or tokens[0] in '+-' or not tokens[-1].isdigit():
            raise ValueError("Invalid expression")
        
        # Evaluate the expression
        total = 0
        current_operator = '+'
        
        for token in tokens:
            if token in '+-':
                current_operator = token
            else:
                number = int(token)
                if current_operator == '+':
                    total += number
                elif current_operator == '-':
                    total -= number
        
        print(f"The result of the expression '{expression}' is: {total}")
    
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
