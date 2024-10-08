# LogCompGESO
Repositório da disciplina de Logica Computacional do Insper


![git status]( http://3.129.230.99/svg/gustavoeso/LogCompGESO/)

Diagrama sintático do compilador:

![v1](imgs/diagrama_v4.png)

Representação EBNF do compilador:
```ebnf
BLOCK = "{", { STATEMENT }, "}" ;

STATEMENT = VAR_DECLARATION ";"
          | ASSIGNMENT ";"
          | PRINT ";"
          | IF
          | WHILE
          | BLOCK
          | ";" ;

VAR_DECLARATION = TYPE, VAR_DECLARATOR_LIST ;

TYPE = "int" | "str" | "bool" ;

VAR_DECLARATOR_LIST = VAR_DECLARATOR, { ",", VAR_DECLARATOR } ;

VAR_DECLARATOR = IDENTIFIER, [ "=", EXPRESSION ] ;

ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;

PRINT = "printf", "(", EXPRESSION, ")" ;

IF = "if", "(", EXPRESSION, ")", STATEMENT, [ "else", STATEMENT ] ;

WHILE = "while", "(", EXPRESSION, ")", STATEMENT ;

BOOLEAN_EXPRESSION = LOGICAL_OR_EXPRESSION ;

LOGICAL_OR_EXPRESSION = LOGICAL_AND_EXPRESSION, { "||", LOGICAL_AND_EXPRESSION } ;

LOGICAL_AND_EXPRESSION = EQUALITY_EXPRESSION, { "&&", EQUALITY_EXPRESSION } ;

EQUALITY_EXPRESSION = RELATIONAL_EXPRESSION, { ("==" | "!="), RELATIONAL_EXPRESSION } ;

RELATIONAL_EXPRESSION = ADDITIVE_EXPRESSION, { (">" | "<"), ADDITIVE_EXPRESSION } ;

ADDITIVE_EXPRESSION = TERM, { ("+" | "-"), TERM } ;

TERM = FACTOR, { ("*" | "/"), FACTOR } ;

FACTOR = ( ("+" | "-" | "!"), FACTOR )
       | NUMBER
       | STRING_LITERAL
       | "true"
       | "false"
       | "(", EXPRESSION, ")"
       | IDENTIFIER
       | "scanf", "(", ")" ;

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;

NUMBER = DIGIT, { DIGIT } ;

STRING_LITERAL = '"', { STRING_CHARACTER }, '"' ;

STRING_CHARACTER = ANY_CHARACTER_EXCEPT_QUOTE ;

ANY_CHARACTER_EXCEPT_QUOTE = ( Todos os caracteres exceto aspas duplas " ) ;

LETTER = ( a | ... | z | A | ... | Z ) ;

DIGIT = ( 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ) ;
```
