# For Power Qword in swampctf


>The darkness increases as you descend down the stone steps towards The Source. The last vestiges of soft light begin to fade and a red haze starts to permeate the air. Suddenly, as you step on to a landing a MAGE blocks the way. He says...
>  
>Connect 
>nc chal1.swampctf.com 1999
>  
>-=Created By: digitalcold=-


I was unable to solve this challenge. I tried to but failed. [This writeup](https://fadec0d3.blogspot.sg/2018/04/swampctf-2018-power-qword.html) helped me understand where I went wrong. I just wish to share the dumb mistakes I made and what I learnt. This is a n00b's CTF diary, not an expert's guide on winning.

### The failed attempt

I downloaded the program and ran it locally.
```
solomonbstoner@swjsUbuntu:~/Downloads$ ./power 
Mage: The old books speak of a single Power QWord that grants
      its speaker a direct link to The Source.
Mage: Do you believe in such things? (yes/no): yes
Mage: Show me your conviction to The Source.
      Take this basis [the mage hands you 0x7f11c4bc5390]
      and speak the Power QWord: awfawf

Segmentation fault (core dumped)
```
The output was segmentation fault error. This means some memory that should not be accessed is being accessed. Okay. That is a clue, but not enough to solve the challenge.

##### Looks like ASLR
I noticed the value that the Mage hands me changes with each time I restart the program. When I see changing hex values, I think of ASLR.

```
Take this basis [the mage hands you 0x7f3544cda390]
Take this basis [the mage hands you 0x7f3310c54390]
Take this basis [the mage hands you 0x7f7c03713390]
Take this basis [the mage hands you 0x7f2e382cf390]
```



I *really* think it is ASLR. In GDB, The address returned is constant at `0x7ffff784e390` (and recall that gdb doesnt relect ASLR). So this is another clue.

##### Realising "yes" is the correct answer
Just out of curiousity, what happens if I were to be funny with Mage and say "no"?
```
Mage: Do you believe in such things? (yes/no): no
Mage: You underestimate the lessons of the old books...
[World: the mage fires a blinding white missile at you]
[World: you disintegrate]
solomonbstoner@swjsUbuntu:~/Downloads$ 
```
It looks like nothing useful happens. The disassembly also shows that the program executes `call exit` after disintigrating me, so our answer to Mage can only be "yes".
```
.text:00000000000009EE                 lea     rdi, aWorldTheMageFi ; "[World: the mage fires a blinding white"...
.text:00000000000009F5                 call    puts
.text:00000000000009FA                 lea     rdi, aWorldYouDisint ; "[World: you disintegrate]"
.text:0000000000000A01                 call    puts
.text:0000000000000A06                 xor     edi, edi        ; status
.text:0000000000000A08                 call    exit
```

After giving the input "yes", the following instructions are executed.
```
.text:0000000000000A37                 lea     rdi, file       ; "libc.so.6"
.text:0000000000000A3E                 mov     esi, 1          ; mode
.text:0000000000000A43                 call    dlopen
.text:0000000000000A48                 lea     rsi, name       ; "system"
.text:0000000000000A4F                 mov     rdi, rax        ; handle
.text:0000000000000A52                 call    dlsym
```
This opens up the file `libc.so.6` using `dlopen`. The function `dlsym()` takes a "handle" of a `libc.so.6` and the null-terminated symbol name "system", returning the address where that symbol is loaded into memory. My guess is that the address of the library function `system` is handed to us by Mage. That means it is possible for us to call `system('/bin//sh')` using Return Oriented Programming.

We can chain 2 ROP gadgets. The first one does `pop rdi; ret` to pop the string '/bin//sh' into `rdi`.  The second one, the address of which Mage gives to us, calls `system`. The format of the exploit code in my mind is somewhat like `< addr of 'pop rdi; ret' > < addr of the string '/bin//sh' > < addr of the library function system > < the string '/bin//sh' >`.

To see if this input is possible, I took a look at the disassembly that reads user input after "speak the Power QWord:" is printed.
```
.text:0000000000000A6D                 mov     rcx, cs:stdin@@GLIBC_2_2_5 ; stream
.text:0000000000000A74                 lea     rdi, [rbp+8]    ; ptr
.text:0000000000000A78                 mov     edx, 8          ; n
.text:0000000000000A7D                 mov     esi, 1          ; size
.text:0000000000000A82                 call    fread
```

`rbp+0x8` is `0x7fffffffdd18`. This means `fread` reads 8 chars from `stdin` to `0x7fffffffdd18`. Before the main function returns, `$rsp=0x7fffffffdd18`, so that means upon return, the program should return to whereever my value points. 8 characters is simply too short for my exploit code, so I am back to the drawing board. But at least I know now what the cause of the segmentation fault error is. 


As usual, when it looks like a function in any program returns to an address specified by user input, In this case, I tried with input "aaaabbb". Before the input, the return address from `main` is `0x7ffff7829830`.
```
0x7fffffffdd18:	0xf7829830	0x00007fff	0x00000001	0x00000000
0x7fffffffdd28:	0xffffdd28	0x00007fff	0xf7ffcca0	0x00000001
```

After `fread`, the return address is overwritten to value `0x0a62626261616161`. This is an illegal memory address, so a seg fault is expected.
```
0x7fffffffdd18:	0x61616161	0x0a626262	0x00000001	0x00000000
0x7fffffffdd28:	0xffffddf8	0x00007fff	0xf7ffcca0	0x00000001

=> 0x0000555555554a99 <main+297>:	c3	ret    
(gdb) ni

Program received signal SIGSEGV, Segmentation fault.
```

So, I found out the following:
1. ASLR is enabled
2. The address given by Mage is the address of library function `system` from the shared library`libc.so.6`
3. `fread` only accepts 8 characters, which is equivalent to just 1 return address. That means my exploit code can't work.

I am lost. I don't know what I can do. This challenge is too difficult for me...

##### Giving up

As I always do whenever I have exhausted every means of solving a problem but still cannot solve it, I just try random things that make no sense and hope it works. It fails everytime of course.

This time, I wrote this Python script to feed the address of the library function `system` into the program as input. It serves no purpose other than to illustrate my hopelessness.
```
from pwn import *

p = remote('chal1.swampctf.com', 1999)

p.recvuntil("):")

p.sendline("yes") #reply yes

addr = int(p.recvuntil("]")[-13:-1], 16)

p.recvuntil(":")

log.info("Address of system(): "+hex(addr))

payload = pack(addr, 'all', 'little', True)

log.info("Sending: " + payload)

p.send(payload)

p.interactive()
```


### Correcting my mistakes

Still reading the writeup...

END