# LogCompGESO
Repositório da disciplina de Logica Computacional do Insper


![git status]( http://3.129.230.99/svg/gustavoeso/LogCompGESO/)

Diagrama sintático do compilador:

![v1](imgs/diagrama_v1.png)

Representação EBNF do compilador:
```ebnf
expression = <term> { ("+" | "-") <term> }

term = <factor> { ("*" | "/") <factor> }

factor = <number>

number = <digit> { <digit> }

digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```