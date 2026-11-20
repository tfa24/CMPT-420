#include <stdio.h>
#include <string.h>

#define ANSWER ""

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        printf("Need exactly one argument.\n");
        return -1;
    }

    const char *correct = ANSWER;

    if (strncmp(argv[1], correct, strlen(correct)))
    {
        printf("No, %s is not correct.\n", argv[1]);
        return 1;
    }
    else
    {
        printf("Yes, %s is correct!\n", argv[1]);
        return 0;
    }
}
