#include <stdio.h>
#include <immintrin.h>

#include "../Cloakwork/cloakwork.h"

#define CORRECT_LEN 0
#define CORRECT_SUM 0

int main(int argc, char **argv)
{
    return CW_PROTECT(int, {
        char correct = CW_CONST(0);

        CW_BRANCH(argc != CW_CONST(2))
        {
            printf(CW_STR("Need exactly one argument.\n"));
            return CW_CONST(-1);
        }

        int i = 0;
        int sum = 0;
        while (argv[1][i] != CW_CONST(0))
        {
            sum += argv[1][i];
            i++;
        }

        correct = (i == CW_CONST(CORRECT_LEN)) && (sum == CW_CONST(CORRECT_SUM));

        CW_IF(correct)
        {
            printf(CW_STR("Yes, %s is correct!\n"), argv[1]);
            return CW_CONST(0);
        }
        CW_ELSE
        {
            printf(CW_STR("No, %s is not correct.\n"), argv[1]);
            return CW_CONST(1);
        }
    });
}

