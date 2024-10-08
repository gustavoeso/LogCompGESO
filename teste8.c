{
    int a, b = 2, c;
    a = 1;
    c = a + b;
    printf(c);          /* Deve imprimir 3 */
    str s1 = "foo", s2, s3 = "bar";
    s2 = "baz";
    printf(s1 + s2 + s3); /* Deve imprimir "foobazbar" */
}
