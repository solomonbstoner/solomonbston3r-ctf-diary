#!/usr/bin/python

import os
import sys
import re

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

"""
evenflow.c

size_t get_file_size(char * filename) {
    struct stat st;
    stat(filename, &st);
    return st.st_size;
}

int main(int argc, char ** argv) {
    FILE * fd = fopen("flag", "r");
    size_t file_size = get_file_size("flag");
    char * buffer = malloc(file_size);
    fread(buffer, 1, file_size, fd);
    return strcmp(buffer, argv[1]);
}
"""

sys.stdout.write("Flag: ")
sys.stdout.flush()
flag = sys.stdin.readline().strip()

assert(re.match("^[a-zA-Z0-9_{}]+$", flag) is not None)

os.system("./evenflow " + flag + "; echo \"$?\"");
