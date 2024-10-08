{
    str greeting = "Hello, ";
    str name = "World";
    int exclamation = 1;
    printf(greeting + name);              /* Deve imprimir "Hello, World" */
    printf(greeting + name + "!");        /* Deve imprimir "Hello, World!" */
    printf(greeting + name + exclamation);/* Deve imprimir "Hello, World1" */
    printf(exclamation + "!");            /* Deve imprimir "1!" */
    printf("Number: " + 42);              /* Deve imprimir "Number: 42" */
}
