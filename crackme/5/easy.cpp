#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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
    printf("Yes, %s is correct!\n", string);
    exit(0);
}

void fail(const char *string)
{
    printf("No, %s is not correct.\n", string);
    exit(1);
}

int check_with_mod(const char *substring, int n, int mod)
{
    int sum = 0;
    for (int i = 0; i < n; i++)
    {
        sum = sum + substring[i];
    }

    return (sum % mod) == 0;
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        printf("Need exactly one argument.\n");
        return -1;
    }

    const char *input = argv[1];
    int len = strnlen(input, 1000);
    if (len != CORRECT_LEN)
        fail(input);

    if (input[FIXED_INDEX_A] != FIXED_CHAR_A)
        fail(input);

    if (input[FIXED_INDEX_B] != FIXED_CHAR_B)
        fail(input);

    if (!check_with_mod(input, 4, MOD_0))
        fail(input);

    if (!check_with_mod(input + 4, 4, MOD_1))
        fail(input);

    if (!check_with_mod(input + 8, 4, MOD_2))
        fail(input);

    if (!check_with_mod(input + 12, 4, MOD_3))
        fail(input);

    succeed(input);
}
