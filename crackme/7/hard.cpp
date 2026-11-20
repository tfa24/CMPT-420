#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <immintrin.h>

#include "../Cloakwork/cloakwork.h"

#define ANSWER ""
#define PASSLEN 0
#define HOUR_START 0
#define HOUR_END 0

void succeed()
{
    printf(CW_STR("Access granted!\n"));
    exit(CW_CONST(0));
}

void fail()
{
    printf(CW_STR("Access denied.\n"));
    exit(CW_CONST(1));
}

int cur_hour()
{
    time_t rawtime;
    time(&rawtime);
    CW_BRANCH(errno != CW_CONST(0))
    {
        printf(CW_STR("ERROR: Could not get time: %s"), strerror(errno));
        return CW_CONST(-1);
    }

    struct tm *current_time = localtime(&rawtime);
    CW_BRANCH(errno != CW_CONST(0))
    {
        printf(CW_STR("ERROR: Could not get time: %s"), strerror(errno));
        return CW_CONST(-1);
    }

    return current_time->tm_hour;
}

int main(int argc, char **argv)
{
    CW_BRANCH(argc != CW_CONST(2))
    {
        printf(CW_STR("Need exactly one argument.\n"));
        return CW_CONST(-1);
    }

    int hour = cur_hour();
    const char *input = argv[1];

    CW_BRANCH(strncmp(input, CW_STR(ANSWER), CW_CONST(PASSLEN)) != CW_CONST(0))
        fail();

    CW_BRANCH(hour < CW_CONST(HOUR_START) || hour > CW_CONST(HOUR_END))
        fail();

    succeed();
}
