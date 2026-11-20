#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CORRECT_LEN 0
#define ANSWER ""

void succeed()
{
    printf("Access granted!\n");
    exit(0);
}

void fail()
{
    printf("Access denied.\n");
    exit(1);
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        printf("Need exactly one argument.\n");
        return -1;
    }

    const char *filename = argv[1];
    FILE *f = fopen(filename, "r");
    if (errno != 0)
    {
        perror("PANIC! Aborting due to");
        return -1;
    }

    char buffer[CORRECT_LEN];
    int read = fread(buffer, CORRECT_LEN, 1, f);
    if (errno != 0)
    {
        perror("PANIC! Aborting due to");
        return -1;
    }

    if (strncmp(ANSWER, buffer, CORRECT_LEN) != 0)
        fail();

    succeed();
}
