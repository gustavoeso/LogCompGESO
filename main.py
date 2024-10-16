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

        tree = Parser.run(source)  # Executa o parser e retorna a arvore de sintaxe abstrata

        # Cria a tabela de simbolos
        symbol_table = SymbolTable()
        # Gera o codigo assembly
        code = ""
        # Incluir secoes iniciais do assembly (exemplo: constantes, secao .data, etc.)
        code += "; Codigo gerado pelo compilador\n"
        code += "; c o n s t a n t e s\n"
        code += "SYS_EXIT equ 1\n"
        code += "SYS_READ equ 3\n"
        code += "SYS_WRITE equ 4\n"
        code += "STDIN equ 0\n"
        code += "STDOUT equ 1\n"
        code += "True equ 1\n"
        code += "False equ 0\n\n"
        code += "section .data\n"
        code += "  newline db 0xA\n"  # Adiciona a nova linha
        code += "  ; Aqui poderiam ser definidas constantes e mensagens\n"
        code += "section .bss\n"
        code += "  res RESB 1\n"
        code += "section .text\n"
        code += "global _start\n"
        # Adicione subrotinas como 'print'

        code += """
print:
    PUSH EBP
    MOV EBP, ESP
    ; Salva os registradores que serao usados
    PUSH EAX
    PUSH EBX
    PUSH ECX
    PUSH EDX
    PUSH ESI
    ; Obtem o valor a ser impresso
    MOV EAX, [EBP+8]
    XOR ESI, ESI
    CMP EAX, 0
    JGE print_start
    ; Se o numero for negativo, imprime o sinal de menos
    PUSH EAX
    MOV EAX, '-'
    PUSH EAX
    MOV EAX, SYS_WRITE
    MOV EBX, STDOUT
    MOV ECX, ESP
    MOV EDX, 1
    INT 0x80
    ADD ESP, 4
    POP EAX
    ; Converte para positivo
    NEG EAX
print_start:
    MOV EBX, 10
print_loop:
    XOR EDX, EDX
    DIV EBX
    ADD EDX, '0'
    PUSH EDX
    INC ESI
    CMP EAX, 0
    JNZ print_loop
print_print:
    CMP ESI, 0
    JE print_end
    DEC ESI
    MOV EAX, SYS_WRITE
    MOV EBX, STDOUT
    POP ECX
    MOV [res], ECX
    MOV ECX, res
    MOV EDX, 1
    INT 0x80
    JMP print_print
print_end:
    ; Imprime a quebra de linha
    MOV EAX, SYS_WRITE
    MOV EBX, STDOUT
    MOV ECX, newline
    MOV EDX, 1
    INT 0x80
    ; Restaura os registradores
    POP ESI
    POP EDX
    POP ECX
    POP EBX
    POP EAX
    POP EBP
    RET
"""

        # Adicione o ponto de entrada '_start'
        code += "_start:\n"
        code += "    PUSH EBP\n"
        code += "    MOV EBP, ESP\n"
        # Ajuste o ESP para alocar espaco para as variaveis locais
        total_stack_space = -symbol_table.offset
        if total_stack_space > 0:
            code += f"    SUB ESP, {total_stack_space}\n"
        # Gera o codigo do programa
        code += tree.Generate(symbol_table)
        # Finaliza o programa
        code += "    ; Interrupcao de saida\n"
        code += "    MOV EAX, SYS_EXIT\n"
        code += "    MOV EBX, 0\n"
        code += "    INT 0x80\n"

        # Escreve o codigo assembly em um arquivo
        with open('program.asm', 'w') as asm_file:
            asm_file.write(code)
        
        print("Codigo assembly gerado com sucesso em 'program.asm'.")

    except ValueError as e:
        sys.stderr.write(f"Erro: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
