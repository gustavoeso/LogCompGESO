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
    SUB ESP, 8
    MOV EBP, ESP
    MOV EAX, [EBP+8]
    XOR ESI, ESI
print_dec:
    MOV EDX, 0
    MOV EBX, 10
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
_start:
    PUSH EBP
    SUB ESP, 8
    MOV EBP, ESP
    MOV EAX, 5
    MOV [EBP-4], EAX
    MOV EAX, 1
    MOV [EBP-8], EAX
LOOP_25:
    MOV EAX, [EBP-4]
    PUSH EAX
    MOV EAX, 1
    MOV EBX, EAX
    POP EAX
    CMP EAX, EBX
    JG binop_true_13
    MOV EAX, 0
    JMP binop_exit_13
binop_true_13:
    MOV EAX, 1
binop_exit_13:
    CMP EAX, 0
    JE ENDLOOP_25
    MOV EAX, [EBP-8]
    PUSH EAX
    MOV EAX, [EBP-4]
    MOV EBX, EAX
    POP EAX
    IMUL EAX, EBX
    MOV [EBP-8], EAX
    MOV EAX, [EBP-4]
    PUSH EAX
    MOV EAX, 1
    MOV EBX, EAX
    POP EAX
    SUB EAX, EBX
    MOV [EBP-4], EAX
    JMP LOOP_25
ENDLOOP_25:
    MOV EAX, [EBP-8]
    PUSH EAX
    CALL print
    POP EAX
    ; Interrupcao de saida
    MOV EAX, SYS_EXIT
    MOV EBX, 0
    INT 0x80
