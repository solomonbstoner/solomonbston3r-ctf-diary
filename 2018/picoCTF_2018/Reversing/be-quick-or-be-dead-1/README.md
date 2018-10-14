# be-quick-or-be-dead-1

## Challenge

You find [this](https://www.youtube.com/watch?v=CTt1vk9nM9c) when searching for some music, which leads you to [be-quick-or-be-dead-1](be-quick-or-be-dead-1). Can you run it fast enough? You can also find the executable in [`/problems/be-quick-or-be-dead-1_2_83a2a5193f0340b364675a2f0cc4d71e`](be-quick-or-be-dead-1).

## Solution

Running the [executable](be-quick-or-be-dead-1),

```
mqf20@pico-2018-shell-1:/problems/be-quick-or-be-dead-1_2_83a2a5193f0340b364675a2f0cc4d71e$ ./be-quick-or-be-dead-1
Be Quick Or Be Dead 1
=====================

Calculating key...
You need a faster machine. Bye bye.
```

It appears that some sort of countdown mechanism is preventing the program from calculating a key (and flag?). We use gdb to debug the program:

```
mqf20@pico-2018-shell-1:/problems/be-quick-or-be-dead-1_2_83a2a5193f0340b364675a2f0cc4d71e$ gdb -q ./be-quick-or-be-dead-1
Reading symbols from ./be-quick-or-be-dead-1...(no debugging symbols found)...done.
(gdb) disass main
Dump of assembler code for function main:
   0x0000000000400827 <+0>:	push   rbp
   0x0000000000400828 <+1>:	mov    rbp,rsp
   0x000000000040082b <+4>:	sub    rsp,0x10
   0x000000000040082f <+8>:	mov    DWORD PTR [rbp-0x4],edi
   0x0000000000400832 <+11>:	mov    QWORD PTR [rbp-0x10],rsi
   0x0000000000400836 <+15>:	mov    eax,0x0
   0x000000000040083b <+20>:	call   0x4007e9 <header>
   0x0000000000400840 <+25>:	mov    eax,0x0
   0x0000000000400845 <+30>:	call   0x400742 <set_timer>
   0x000000000040084a <+35>:	mov    eax,0x0
   0x000000000040084f <+40>:	call   0x400796 <get_key>
   0x0000000000400854 <+45>:	mov    eax,0x0
   0x0000000000400859 <+50>:	call   0x4007c1 <print_flag>
   0x000000000040085e <+55>:	mov    eax,0x0
   0x0000000000400863 <+60>:	leave
   0x0000000000400864 <+61>:	ret
End of assembler dump.
```

It appears that the `set_timer()` procedure is creating a countdown mechanism that terminates the program before it can reveal the flag. We set a breakpoint just before `set_timer()` is called, at address `0x0000000000400845`.

```
(gdb) break *0x0000000000400845
Breakpoint 1 at 0x400845
(gdb) run
Starting program: /home/mqf20/be-quick-or-be-dead-1
Be Quick Or Be Dead 1
=====================


Breakpoint 1, 0x0000000000400845 in main ()
(gdb) disass main
Dump of assembler code for function main:
   0x0000000000400827 <+0>:	push   rbp
   0x0000000000400828 <+1>:	mov    rbp,rsp
   0x000000000040082b <+4>:	sub    rsp,0x10
   0x000000000040082f <+8>:	mov    DWORD PTR [rbp-0x4],edi
   0x0000000000400832 <+11>:	mov    QWORD PTR [rbp-0x10],rsi
   0x0000000000400836 <+15>:	mov    eax,0x0
   0x000000000040083b <+20>:	call   0x4007e9 <header>
   0x0000000000400840 <+25>:	mov    eax,0x0
=> 0x0000000000400845 <+30>:	call   0x400742 <set_timer>
   0x000000000040084a <+35>:	mov    eax,0x0
   0x000000000040084f <+40>:	call   0x400796 <get_key>
   0x0000000000400854 <+45>:	mov    eax,0x0
   0x0000000000400859 <+50>:	call   0x4007c1 <print_flag>
   0x000000000040085e <+55>:	mov    eax,0x0
   0x0000000000400863 <+60>:	leave
   0x0000000000400864 <+61>:	ret
End of assembler dump.
```

Now, we overwrite the instruction pointer `rip` to jump ahead to the next instruction in `main()`, `0x000000000040084a`:

```
(gdb) set $rip=0x000000000040084a
```

We then allow the program to continue, which reveals the flag.

```
(gdb) c
Continuing.
Calculating key...
Done calculating key
Printing flag:
picoCTF{why_bother_doing_unnecessary_computation_d0c6aace}
[Inferior 1 (process 957893) exited normally]
```


## Alternate Soln

We know that the problem is caused by the function `sym.set_timer`. The `SIGALARM` always kills the program before it can print the flag. So, an alternative to running the program in debug mode and bypassing the `sym.set_timer` manually is to remove the function call altogether.


Below, we see the original `main` function. There, we see `call sym.set_timer`. We want to remove that.
```
[0x00400827]> pdf
|           ;-- main:
/ (fcn) sym.main 62
|   sym.main (int arg1, int arg2);
|           ; var int local_10h @ rbp-0x10
|           ; var int local_4h @ rbp-0x4
|           ; DATA XREF from entry0 (0x4005bd)
|           0x00400827      55             push rbp
|           0x00400828      4889e5         mov rbp, rsp
|           0x0040082b      4883ec10       sub rsp, 0x10
|           0x0040082f      897dfc         mov dword [local_4h], edi   ; arg1
|           0x00400832      488975f0       mov qword [local_10h], rsi  ; arg2
|           0x00400836      b800000000     mov eax, 0
|           0x0040083b      e8a9ffffff     call sym.header
|           0x00400840      b800000000     mov eax, 0
|           0x00400845      e8f8feffff     call sym.set_timer
|           0x0040084a      b800000000     mov eax, 0
|           0x0040084f      e842ffffff     call sym.get_key
|           0x00400854      b800000000     mov eax, 0
|           0x00400859      e863ffffff     call sym.print_flag
|           0x0040085e      b800000000     mov eax, 0
|           0x00400863      c9             leave
\           0x00400864      c3             ret
[0x00400827]>
```

We cannot possibly "delete the instruction", but we can replace it with `nop`s, which essentially does nothing. We will replace all 5 bytes of opcode `e8f8feffff` with `9090909090`. Radare2's `wa` command comes in handy. I believe it is shortform for 'write assembly'.

```
[0x00400845]> wa?
|Usage: wa[of*] [arg]
| wa nop           write nopcode using asm.arch and asm.bits
| wa* mov eax, 33  show 'wx' op with hexpair bytes of assembled opcode
| "wa nop;nop"     assemble more than one instruction (note the quotes)
| waffoo.asm       assemble file and write bytes
| wao?             show help for assembler operation on current opcode (hack)
```

There we go. Remember to reopen the current file in read-write mode with `oo+`, and seek the current address, the instruction of which we want to replace. Then, we run the command below. 
```
[0x00400845]> "wa nop;nop;nop;nop;nop"
Written 5 byte(s) (nop;nop;nop;nop;nop) = wx 9090909090
```

Don't forget to save the file! 
```
[0x00400845]> wci
[0x00400845]>
```

Let's verify that the file has been patched. We quit radare2, then reopen the file again. `call sym.set_timer` is now gone.
```
[0x00000000]> q
Do you want to quit? (Y/n) y
Do you want to kill the process? (Y/n) y
➜  be-quick-or-be-dead-1 git:(master) ✗ r2 be-quick-or-be-dead-1 
 -- r2-goverity: found corruption - please eliminate!
[0x004005a0]> aa
[x] Analyze all flags starting with sym. and entry0 (aa)
[0x004005a0]> aac
[0x004005a0]> s main
[0x00400827]> pdf
|           ;-- main:
/ (fcn) sym.main 62
|   sym.main (int arg1, int arg2);
|           ; var int local_10h @ rbp-0x10
|           ; var int local_4h @ rbp-0x4
|           ; DATA XREF from entry0 (0x4005bd)
|           0x00400827      55             push rbp
|           0x00400828      4889e5         mov rbp, rsp
|           0x0040082b      4883ec10       sub rsp, 0x10
|           0x0040082f      897dfc         mov dword [local_4h], edi   ; arg1
|           0x00400832      488975f0       mov qword [local_10h], rsi  ; arg2
|           0x00400836      b800000000     mov eax, 0
|           0x0040083b      e8a9ffffff     call sym.header
|           0x00400840      b800000000     mov eax, 0
|           0x00400845      90             nop
|           0x00400846      90             nop
|           0x00400847      90             nop
|           0x00400848      90             nop
|           0x00400849      90             nop
|           0x0040084a      b800000000     mov eax, 0
|           0x0040084f      e842ffffff     call sym.get_key
|           0x00400854      b800000000     mov eax, 0
|           0x00400859      e863ffffff     call sym.print_flag
|           0x0040085e      b800000000     mov eax, 0
|           0x00400863      c9             leave
\           0x00400864      c3             ret
[0x00400827]> 
```

Now, we are free to run the program and it prints the flag.
```
[0x00400827]> ood
Process with PID 28987 started...
File dbg:///home/solomonbstoner/Documents/Scr3enSl4y3rs/picoCTF_2018/Reversing/be-quick-or-be-dead-1/be-quick-or-be-dead-1  reopened in read-write mode
= attach 28987 28987
28987
[0x7f5b38e32090]> dc
Be Quick Or Be Dead 1
=====================

Calculating key...
Done calculating key
Printing flag:
picoCTF{why_bother_doing_unnecessary_computation_d0c6aace}
[0x7f5b38b24e06]> 
```
