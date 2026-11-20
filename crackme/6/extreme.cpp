#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <immintrin.h>

#include "../Cloakwork/cloakwork.h"

#define CORRECT_LEN 0
#define ANSWER ""

void succeed()
{
    CW_PROTECT_VOID({
        printf(CW_STR("Access granted!\n"));
        exit(CW_CONST(0));
    });
}

void fail()
{
    CW_PROTECT_VOID({
        printf(CW_STR("Access denied.\n"));
        exit(CW_CONST(1));
    });
}

int main(int argc, char **argv)
{
    return CW_PROTECT(int, {
        CW_BRANCH(argc != CW_CONST(2))
        {
            printf(CW_STR("Need exactly one argument.\n"));
            return CW_CONST(-1);
        }

        const char *filename = argv[1];
        FILE *f = fopen(filename, CW_STR("r"));
        CW_BRANCH(errno != CW_CONST(0))
        {
            perror(CW_STR("PANIC! Aborting due to"));
            return CW_CONST(-1);
        }

        char buffer[CORRECT_LEN];
        int read = fread(buffer, CW_CONST(CORRECT_LEN), CW_CONST(1), f);
        CW_BRANCH(errno != CW_CONST(0))
        {
            perror(CW_STR("PANIC! Aborting due to"));
            return CW_CONST(-1);
        }

        CW_BRANCH(strncmp(CW_STR(ANSWER), buffer, CW_CONST(CORRECT_LEN)) != CW_CONST(0))
            fail();

        succeed();
    });
}
