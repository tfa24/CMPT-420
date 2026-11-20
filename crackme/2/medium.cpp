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

    int i = 0;
    while (correct[i] != 0 && argv[1][i] != 0)
    {
        CW_BRANCH(correct[i] - 1 != argv[1][i])
        {
            printf("No, %s is not correct.\n", argv[1]);
            return 1;
        }
        i++;
    }

    printf("Yes, %s is correct!\n", argv[1]);
    return 0;
}
