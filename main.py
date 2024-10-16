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
            raise ValueError(f"Arquivo '{input_file}' nao encontrado.")

        with open(input_file, 'r', encoding='utf-8') as file:
            source = file.read()
        
        source = PrePro.filter(source)

        tree = Parser.run(source)  # Executa o parser e retorna a arvore de sintaxe abstrata

        # Cria a tabela de simbolos
        symbol_table = SymbolTable()
        # Gera o codigo assembly
        code = ""
        # Incluir secoes iniciais do assembly
        code += "; constantes\n"
        code += "SYS_EXIT equ 1\n"
        code += "SYS_READ equ 3\n"
        code += "SYS_WRITE equ 4\n"
        code += "STDIN equ 0\n"
        code += "STDOUT equ 1\n"
        code += "True equ 1\n"
        code += "False equ 0\n"
        code += "section .data\n"
        code += "section .bss\n"
        code += "  res RESB 1\n"
        code += "section .text\n"
        code += "global main\n"

        # Adicione o ponto de entrada 'main'
        code += "main:\n"
        code += "    PUSH EBP\n"
        code += "    MOV EBP, ESP\n"
        # Gera o codigo do programa
        code += tree.Generate(symbol_table)
        # Finaliza a função main
        code += "    ; retorno da função main\n"
        code += "    MOV EAX, 0\n"  # Retorno 0 da função main
        code += "    MOV ESP, EBP\n"
        code += "    POP EBP\n"
        code += "    RET\n"

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

        # Sub-rotinas binarias
        code += """
binop_je:
    JE binop_true
    JMP binop_false
binop_jg:
    JG binop_true
    JMP binop_false
binop_jl:
    JL binop_true
    JMP binop_false
binop_false:
    MOV EBX, False
    JMP binop_exit
binop_true:
    MOV EBX, True
binop_exit:
    RET
"""

        # Gera o nome do arquivo assembly com a extensao '.asm'
        output_file = os.path.splitext(input_file)[0] + '.asm'

        # Escreve o codigo assembly em um arquivo
        with open(output_file, 'w', encoding='utf-8') as asm_file:
            asm_file.write(code)
        
        print(f"Codigo assembly gerado com sucesso em '{output_file}'.")

    except ValueError as e:
        sys.stderr.write(f"Erro: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
