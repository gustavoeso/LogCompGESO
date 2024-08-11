import sys
import re

def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("Usage: python main.py '<expression>'")
        
        expression = sys.argv[1].replace(" ", "")
        
        # Check for invalid characters
        if not re.match(r'^[\d+\-]+$', expression):
            raise ValueError("Invalid expression: contains invalid characters or sequences")
        
        # Tokenize the expression
        tokens = re.findall(r'\d+|[+-]', expression)
        
        # Validate the expression
        if not tokens or tokens[0] in '+-' or not tokens[-1].isdigit():
            raise ValueError("Invalid expression: starts or ends with an operator")
        
        # Check for consecutive operators
        for i in range(1, len(tokens) - 1):
            if tokens[i] in '+-' and tokens[i+1] in '+-':
                raise ValueError("Invalid expression: consecutive operators")
        
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
        
        print(total)
    
    except ValueError as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
