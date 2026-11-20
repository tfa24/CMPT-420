#include <stdio.h>
#include <string.h>
#include <immintrin.h>
#include "../Cloakwork/cloakwork.h"

#define ANSWER ""

int main(int argc, char **argv)
{
    CW_BRANCH(argc != 2)
    {
        printf("Need exactly one argument.\n");
        return -1;
    }

    const char *correct = ANSWER;

    CW_IF(strncmp(argv[1], correct, strlen(correct)))
    {
        printf("No, %s is not correct.\n", argv[1]);
        return 1;
    }
    CW_ELSE
    {
        printf("Yes, %s is correct!\n", argv[1]);
        return 0;
    }
}
