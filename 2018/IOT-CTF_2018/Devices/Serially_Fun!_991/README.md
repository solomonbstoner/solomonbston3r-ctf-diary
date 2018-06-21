# Serially FUN! - 991

> This challenge requires you to make use of the evaluation board (STM32 Discovery board). There is only one flag in this challenge. You can bring the board home if you solve this challenge ;)
>  
> We have forgotten the username and password to the device, can you find it for us?
>  
> If the flag is ABC123, submit your flag in the format of HI{ABC123}

This challenge was created by DSO National Laboratories. 

![](../../img/iot_ctf2018_serially_fun_dso_announcement.png)

When we came for the CTF, we were determined to solve this challenge at all cost. Afterall, Solomon is a huge fan (but still a n00b) of embedded systems, but never got the chance to play hardware challenges. This was his first time, and oh boy was he excited! 


> DSO XCTF Challenge
>  
> Connect User USB and push blue btn to begin

We followed the board's instructions, and connected to it serially using the command `screen /dev/ttyACM0`.

We received a prompt asking for the username. This told us this was the correct way to communicate with the board. 

```
$ screen /dev/ttyACM0

User: 
```

As we entered the username, our input was reflected back to us on the computer, and after submission, printed out on the board's screen too. Then the board would prompt for the password, where we were given unlimited tries.

Usually, when a challenge pipes user input back to standard output, it means format string vulnerability is involved. We tried format string specifiers like `"%x %x
` but the board's screen did not print out the stack's content. We ruled out format string exploit.


Next, we tried to fuzz the program by keying in input of different lengths. We tried input of about 25 characters, and were presented with the warning `"Canary dead"`. That meant that we could not smash the stack. Bummer.
```
User: aaaaabbbbbcccccdddddeeeeefffff
Password: 
SYS_INTEGRITY_VIOLATION: SYSTEM HALTED
```

![](../../img/iot_ctf2018_serially_fun_fuzzing.jpg)

We recalled from a previous challenge called [Dubblesort in Pwnable.tw](https://github.com/solomonbstoner/solomonbston3r-ctf-diary/blob/master/Others/Pwnable.tw/dubblesort%20pwnable.tw%20.md) where the libc's base address was simply sitting in the buffer for user input. To read that value, we needed a string of a specific length so that the `<puts>` instruction would append the target value (that we want to print) to the end of the user-supplied string. We thought the same might apply here.

Thus, we decreased the length of our input gradually from 25 to 24.... to 15. The canary kept dying.  But once we reached length 15, something magical happened. Some additional characters were printed out, exactly like Dubblesort in Pwnable.tw. However, each time we restarted the board, the values were different. We have attached pictures from 2 separate runs to let you see what the values looks like in each run. Our input in both cases were `"aaaaabbbbbccccc"`. This magic happens only when input length is 15 characters long. 

This was the first run:

![](../../img/iot_ctf2018_serially_fun_1st_leak.jpg) 

This was the second run:

![](../../img/iot_ctf2018_serially_fun_2nd_leak.jpg)

If an input of 15 characters prints out some values, but input of 16 characters kills the canary, this means that the additional characters printed are the value of the stack canary. We did not know what to do with this value. We could not use it to smash the stack for 2 reasons:

1. The stack canary's value changes with every run, so we cannot run it once to get the canary's value, then run it again to insert it in with a return address to change program execution.
2. We were not given any binary to analyse. So even if it were possible to somehow bypass the stack canary, we did not know what return address to return to.

But, there was no harm trying to see if it was the password. We keyed in the extra characters as our password, and voila, we got a flag! It is `HI{M0R3_H45T3_LE55_5P33D}`.

![](../../img/iot_ctf2018_serially_fun_flag.jpg)

Note: Not all the extra characters are part of the password. For instance, if the extra characters are `"[Wx89x@po"`, the password could actually be `"Wx89x@po"` (ie without the `"["`) or even `"x89x@po"` (ie without the `"[W"`). Sometimes they are all the extra characters, sometimes they are not. We are not sure why either. You just have to try a few times until the input is accepted. Also, sometimes the characters printed are hard to read, like in the screenshot from the first run above. In that case, we simply resetted the board and tried again until all the extra characters were legible.

### Second challenge (Not part of IoT-CTF)

After we solved the challenge above, DSO informed us that there is a *second* flag included. They hinted that it could be found by extracting the firmware from the device using ST-Link. We are currently attempting this challenge, and will post updates here.
