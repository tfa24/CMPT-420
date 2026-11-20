#include <stdio.h>
#include <immintrin.h>
#include "../Cloakwork/cloakwork.h"

#define CORRECT_LEN 0
#define CORRECT_SUM 0

int main(int argc, char **argv)
{
    char correct = 0;

    CW_BRANCH(argc != 2)
    {
        printf("Need exactly one argument.\n");
        return -1;
    }

    int i = 0;
    int sum = 0;
    while (argv[1][i] != 0)
    {
        sum += argv[1][i];
        i++;
    }

    correct = (i == CORRECT_LEN) && (sum == CORRECT_SUM);

    CW_IF(correct)
    {
        printf("Yes, %s is correct!\n", argv[1]);
        return 0;
    }
    CW_ELSE
    {
        printf("No, %s is not correct.\n", argv[1]);
        return 1;
    }
}
