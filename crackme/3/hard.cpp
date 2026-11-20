#include <stdio.h>
#include <string.h>
#include <immintrin.h>

#include "../Cloakwork/cloakwork.h"

#define CORRECT_LEN 0
#define ANSWER ""

int check_pw(const char *password, const char *correct, const char *mask)
{
    int i = 0;
    char success = 1;
    do
    {
        char masked_char = correct[i] + mask[i];
        CW_BRANCH(masked_char != password[i])
        return CW_CONST(0);

        i++;
    } while (correct[i] != CW_CONST(0) && password[i] != CW_CONST(0));

    return CW_CONST(1);
}

int main(int argc, char **argv)
{
    CW_BRANCH(argc != CW_CONST(2))
    {
        printf(CW_STR("Need exactly one argument.\n"));
        return CW_CONST(-1);
    }

    const char *correct = CW_STR(ANSWER);
    char mask[CORRECT_LEN + 1] = {0};

    CW_BRANCH(strlen(argv[1]) == CW_CONST(CORRECT_LEN) && check_pw(argv[1], correct, mask))
    {
        printf(CW_STR("Yes, %s is correct!\n"), argv[1]);
        return CW_CONST(0);
    }

    printf(CW_STR("No, %s is not correct.\n"), argv[1]);
    return CW_CONST(1);
}
