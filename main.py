from components.prepro import PrePro
from components.parser import Parser
from components.symbol_table import SymbolTable
import sys
import os

def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("Uso: python main.py <arquivo>.c")
        
        input_file = sys.argv[1]
        if not os.path.isfile(input_file):
            raise ValueError(f"Arquivo '{input_file}' não encontrado.")

        with open(input_file, 'r') as file:
            source = file.read()
        
        source = PrePro.filter(source)

        tree = Parser.run(source)  # Executa o parser e retorna a árvore de sintaxe abstrata

        # Cria a tabela de símbolos
        symbol_table = SymbolTable()
        # Gera o código assembly
        code = ""
        # Incluir seções iniciais do assembly (exemplo: constantes, seção .data, etc.)
        code += "; c o n s t a n t e s\n"
        code += "SYS_EXIT equ 1\n"
        code += "SYS_READ equ 3\n"
        code += "SYS_WRITE equ 4\n"
        code += "STDIN equ 0\n"
        code += "STDOUT equ 1\n"
        code += "True equ 1\n"
        code += "False equ 0\n"
        code += "segment .data\n"
        code += "segment .bss\n"
        code += "  res RESB 1\n"
        code += "section .text\n"
        code += "global _start\n"

        # Sub-rotina print
        code += """
print:
    PUSH EBP
    MOV EBP, ESP
    MOV EAX, [EBP+8]
    XOR ESI, ESI
print_dec:
    MOV EDX, 0
    MOV EBX, 0x000A
    DIV EBX
    ADD EDX, '0'
    PUSH EDX
    INC ESI
    CMP EAX, 0
    JZ print_next
    JMP print_dec
print_next:
    CMP ESI, 0
    JZ print_exit
    DEC ESI
    MOV EAX, SYS_WRITE
    MOV EBX, STDOUT
    POP ECX
    MOV [res], ECX
    MOV ECX, res
    MOV EDX, 1
    INT 0x80
    JMP print_next
print_exit:
    POP EBP
    RET
"""

        # Sub-rotinas binárias
        code += """
binop_jl:
    JL binop_true
    JMP binop_false
binop_true:
    MOV EAX, True
    JMP binop_exit
binop_false:
    MOV EAX, False
binop_exit:
    RET
"""

        # Adicione o ponto de entrada '_start'
        code += "_start:\n"
        code += "    PUSH EBP\n"
        code += "    MOV EBP, ESP\n"
        # Gera o código do programa
        code += tree.Generate(symbol_table)
        # Finaliza o programa
        code += "    ; interrupção de saída\n"
        code += "    POP EBP\n"
        code += "    MOV EAX, SYS_EXIT\n"
        code += "    INT 0x80\n"

        # Gera o nome do arquivo assembly com a extensão '.asm'
        output_file = os.path.splitext(input_file)[0] + '.asm'

        # Escreve o código assembly em um arquivo
        with open(output_file, 'w') as asm_file:
            asm_file.write(code)
        
        print(f"Código assembly gerado com sucesso em '{output_file}'.")

    except ValueError as e:
        sys.stderr.write(f"Erro: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
