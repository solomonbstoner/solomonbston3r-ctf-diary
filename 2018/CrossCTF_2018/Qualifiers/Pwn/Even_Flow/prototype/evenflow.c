#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>


int main(int argc, char ** argv) {
    char flag[] = "CrossCTF{Hi_there}";
    return strcmp(flag, argv[1]);
}

