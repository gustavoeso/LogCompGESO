; Codigo gerado pelo compilador
; c o n s t a n t e s
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

section .data
  ; Aqui poderiam ser definidas constantes e mensagens
section .bss
  res RESB 1
section .text
global _start

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
    ; Restaura os registradores
    POP ESI
    POP EDX
    POP ECX
    POP EBX
    POP EAX
    POP EBP
    RET
_start:
    PUSH EBP
    MOV EBP, ESP
    MOV EAX, 5
    MOV [EBP-8], EAX
    MOV EAX, 2
    MOV [EBP-4], EAX
    MOV EAX, 1
    MOV [EBP-12], EAX
LOOP_32:
    MOV EAX, [EBP-4]
    PUSH EAX
    MOV EAX, [EBP-8]
    PUSH EAX
    MOV EAX, 1
    MOV EBX, EAX
    POP EAX
    ADD EAX, EBX
    MOV EBX, EAX
    POP EAX
    CMP EAX, EBX
    JL binop_true_20
    MOV EAX, 0
    JMP binop_exit_20
binop_true_20:
    MOV EAX, 1
binop_exit_20:
    CMP EAX, 0
    JE ENDLOOP_32
    MOV EAX, [EBP-12]
    PUSH EAX
    MOV EAX, [EBP-4]
    MOV EBX, EAX
    POP EAX
    IMUL EAX, EBX
    MOV [EBP-12], EAX
    MOV EAX, [EBP-4]
    PUSH EAX
    MOV EAX, 1
    MOV EBX, EAX
    POP EAX
    ADD EAX, EBX
    MOV [EBP-4], EAX
    JMP LOOP_32
ENDLOOP_32:
    MOV EAX, [EBP-12]
    PUSH EAX
    CALL print
    ADD ESP, 4
    ; Interrupcao de saida
    MOV EAX, SYS_EXIT
    MOV EBX, 0
    INT 0x80
