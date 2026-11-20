#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <immintrin.h>

#include "../Cloakwork/cloakwork.h"

#define CORRECT_LEN 16
#define FIXED_INDEX_A 0
#define FIXED_CHAR_A 0
#define FIXED_INDEX_B 0
#define FIXED_CHAR_B 0
#define MOD_0 0
#define MOD_1 0
#define MOD_2 0
#define MOD_3 0

void succeed(const char *string)
{
    printf(CW_STR("Yes, %s is correct!\n"), string);
    exit(CW_CONST(0));
}

void fail(const char *string)
{
    printf(CW_STR("No, %s is not correct.\n"), string);
    exit(CW_CONST(1));
}

int check_with_mod(const char *substring, int n, int mod)
{
    int sum = 0;
    for (int i = 0; i < n; i++)
    {
        sum = sum + substring[i];
    }

    return (sum % mod) == CW_CONST(0);
}

int main(int argc, char **argv)
{
    CW_BRANCH(argc != CW_CONST(2))
    {
        printf(CW_STR("Need exactly one argument.\n"));
        return CW_CONST(-1);
    }

    const char *input = argv[1];
    int len = strnlen(input, CW_CONST(1000));
    CW_BRANCH(len != CW_CONST(CORRECT_LEN))
        fail(input);

    CW_BRANCH(input[CW_CONST(FIXED_INDEX_A)] != CW_CONST(FIXED_CHAR_A))
        fail(input);

    CW_BRANCH(input[CW_CONST(FIXED_INDEX_B)] != CW_CONST(FIXED_CHAR_B))
        fail(input);

    CW_BRANCH(!check_with_mod(input, CW_CONST(4), CW_CONST(MOD_0)))
        fail(input);

    CW_BRANCH(!check_with_mod(input + CW_CONST(4), CW_CONST(4), CW_CONST(MOD_1)))
        fail(input);

    CW_BRANCH(!check_with_mod(input + CW_CONST(8), CW_CONST(4), CW_CONST(MOD_2)))
        fail(input);

    CW_BRANCH(!check_with_mod(input + CW_CONST(12), CW_CONST(4), CW_CONST(MOD_3)))
        fail(input);

    succeed(input);
}
