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

        CW_IF(strncmp(argv[1], correct, strlen(correct)))
        {
            printf(CW_STR("No, %s is not correct.\n"), argv[1]);
            return CW_CONST(1);
        }
        CW_ELSE
        {
            printf(CW_STR("Yes, %s is correct!\n"), argv[1]);
            return CW_CONST(0);
        }
    });
}
