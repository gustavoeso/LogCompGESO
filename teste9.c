{
    int count = 0;
    while (count < 5) {
        printf(count);
        count = count + 1;
    }
    if (count == 5) {
        printf("Loop completed");
    } else {
        printf("Unexpected count value");
    }
}
