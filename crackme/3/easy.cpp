#include <stdio.h>
#include <string.h>

#define CORRECT_LEN 0
#define ANSWER ""

int check_pw(const char *password, const char *correct, const char *mask)
{
    int i = 0;
    char success = 1;
    do
    {
        char masked_char = correct[i] + mask[i];
        if (masked_char != password[i])
            return 0;

        i++;
    } while (correct[i] != 0 && password[i] != 0);

    return 1;
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        printf("Need exactly one argument.\n");
        return -1;
    }

    const char *correct = ANSWER;
    char mask[CORRECT_LEN + 1] = {0};

    if (strlen(argv[1]) == CORRECT_LEN && check_pw(argv[1], correct, mask))
    {
        printf("Yes, %s is correct!\n", argv[1]);
        return 0;
    }

    printf("No, %s is not correct.\n", argv[1]);

    return 1;
}
