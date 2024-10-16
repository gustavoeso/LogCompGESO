; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0
segment .data
segment .bss
  res RESB 1
section .text
global _start

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

binop_je:
    JE binop_true
    JMP binop_false
binop_jg:
    JG binop_true
    JMP binop_false
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
_start:
    PUSH EBP
    MOV EBP, ESP
    PUSH DWORD 0 ; Dim i as Integer [EBP-4]
    PUSH DWORD 0 ; Dim n as Integer [EBP-8]
    PUSH DWORD 0 ; Dim f as Integer [EBP-12]
    MOV EAX, 5
    MOV EBX, EAX
    MOV [EBP-8], EBX ; n = ...
    MOV EAX, 2
    MOV EBX, EAX
    MOV [EBP-4], EBX ; i = ...
    MOV EAX, 1
    MOV EBX, EAX
    MOV [EBP-12], EBX ; f = ...
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
    CALL binop_jl
    CMP EAX, 0
    JE EXIT_32
    MOV EAX, [EBP-12]
    PUSH EAX
    MOV EAX, [EBP-4]
    MOV EBX, EAX
    POP EAX
    IMUL EBX
    MOV EBX, EAX
    MOV [EBP-12], EBX ; f = ...
    MOV EAX, [EBP-4]
    PUSH EAX
    MOV EAX, 1
    MOV EBX, EAX
    POP EAX
    ADD EAX, EBX
    MOV EBX, EAX
    MOV [EBP-4], EBX ; i = ...
    JMP LOOP_32
EXIT_32:
    MOV EAX, [EBP-12]
    PUSH EAX ; empilha argumento para print
    CALL print
    POP EBX ; limpa args
    ; interrupcao de saida
    POP EBP
    MOV EAX, SYS_EXIT
    INT 0x80
