{
    int x = 10;
    int y = 5;
    printf(x > y);       /* Deve imprimir 1 */
    printf(x < y);       /* Deve imprimir 0 */
    printf(x == y);      /* Deve imprimir 0 */
    printf(x != y);      /* Deve imprimir 1 */
    printf("abc" == "abc");  /* Deve imprimir 1 */
    printf("abc" != "def");  /* Deve imprimir 1 */
    printf("abc" < "def");   /* Deve imprimir 1 (ordem lexicográfica) */
    printf("abc" > "def");   /* Deve imprimir 0 */
}
