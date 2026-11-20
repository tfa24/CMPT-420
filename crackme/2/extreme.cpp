#include <stdio.h>
#include <string.h>
#include <immintrin.h>

#include "../Cloakwork/cloakwork.h"

#define ANSWER ""

int main(int argc, char **argv)
{
    return CW_PROTECT(int, {
        CW_BRANCH(argc != CW_CONST(2))
        {
            printf(CW_STR("Need exactly one argument.\n"));
            return CW_CONST(-1);
        }

        const char *correct = CW_STR(ANSWER);

        int i = 0;
        while (correct[i] != CW_CONST(0) && argv[1][i] != CW_CONST(0))
        {
            CW_BRANCH(correct[i] - CW_CONST(1) != argv[1][i])
            {
                printf(CW_STR("No, %s is not correct.\n"), argv[1]);
                return CW_CONST(1);
            }
            i++;
        }

        printf(CW_STR("Yes, %s is correct!\n"), argv[1]);
        return CW_CONST(0);
    });
}
