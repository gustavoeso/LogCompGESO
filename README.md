# LogCompGESO
Repositório da disciplina de Logica Computacional do Insper


![git status]( http://3.129.230.99/svg/gustavoeso/LogCompGESO/)

Diagrama sintático do compilador:

![v1](imgs/diagrama_v4.png)

Representação EBNF do compilador:
```ebnf
PROGRAM = { DECLARATION }, MAIN_CALL ;

DECLARATION = FUNC_DECLARATION
            | VAR_DECLARATION ";" ;

FUNC_DECLARATION = FUNC_TYPE, IDENTIFIER, "(", [ PARAM_LIST ], ")", BLOCK ;

FUNC_TYPE = TYPE | "void" ;

PARAM_LIST = PARAM, { ",", PARAM } ;

PARAM = TYPE, IDENTIFIER ;

MAIN_CALL = FUNC_CALL ";" ;  (* Chamada implícita da função 'main' *)

BLOCK = "{", { STATEMENT }, "}" ;

STATEMENT = VAR_DECLARATION ";"
          | ASSIGNMENT ";"
          | PRINT ";"
          | IF
          | WHILE
          | RETURN_STATEMENT
          | FUNC_CALL ";"
          | BLOCK
          | ";" ;

VAR_DECLARATION = TYPE, VAR_DECLARATOR_LIST ;

TYPE = "int" | "str" | "bool" ;

VAR_DECLARATOR_LIST = VAR_DECLARATOR, { ",", VAR_DECLARATOR } ;

VAR_DECLARATOR = IDENTIFIER, [ "=", EXPRESSION ] ;

ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;

RETURN_STATEMENT = "return", [ "(", EXPRESSION, ")" ], ";" ;

PRINT = "printf", "(", EXPRESSION, ")" ;

IF = "if", "(", EXPRESSION, ")", STATEMENT, [ "else", STATEMENT ] ;

WHILE = "while", "(", EXPRESSION, ")", STATEMENT ;

EXPRESSION = BOOLEAN_EXPRESSION ;

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
       | IDENTIFIER, [ "(", [ ARGUMENT_LIST ], ")" ]
       | "scanf", "(", ")" ;

ARGUMENT_LIST = EXPRESSION, { ",", EXPRESSION } ;

FUNC_CALL = IDENTIFIER, "(", [ ARGUMENT_LIST ], ")" ;

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;

NUMBER = DIGIT, { DIGIT } ;

STRING_LITERAL = '"', { STRING_CHARACTER }, '"' ;

STRING_CHARACTER = ANY_CHARACTER_EXCEPT_QUOTE ;

ANY_CHARACTER_EXCEPT_QUOTE = ( Todos os caracteres exceto aspas duplas " ) ;

LETTER = ( a | ... | z | A | ... | Z ) ;

DIGIT = ( 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ) ;
```