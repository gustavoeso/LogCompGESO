{
    int a = 5;
    int b = 0;
    printf(a + b);        /* Deve imprimir 5 */
    printf(a - b);        /* Deve imprimir 5 */
    printf(a * b);        /* Deve imprimir 0 */
    printf(a / (b + 1));  /* Deve imprimir 5 */
    printf(a && b);       /* Deve imprimir 0 */
    printf(!b);           /* Deve imprimir 1 */
}
