#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define ANSWER ""
#define PASSLEN 0
#define HOUR_START 0
#define HOUR_END 0

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

int cur_hour()
{
    time_t rawtime;
    time(&rawtime);
    if (errno != 0)
    {
        printf("ERROR: Could not get time: %s", strerror(errno));
        return (-1);
    }

    struct tm *current_time = localtime(&rawtime);
    if (errno != 0)
    {
        printf("ERROR: Could not get time: %s", strerror(errno));
        return (-1);
    }

    return current_time->tm_hour;
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        printf("Need exactly one argument.\n");
        return -1;
    }

    int hour = cur_hour();
    const char *input = argv[1];

    if (strncmp(input, ANSWER, PASSLEN) != 0)
        fail();

    if (hour < HOUR_START || hour > HOUR_END)
        fail();

    succeed();
}
