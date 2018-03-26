# For soRandom in PicoCTF

This challenge was given.
>"We found sorandom.py running at shell2017.picoctf.com:33123. It seems to be outputting the flag but randomizing all the characters first. Is there anyway to get back the original flag?
>Update (text only) 16:16 EST 1 Apr Running python 2 (same version as on the server)."

### Playing with the server

This is the output from the server
```
solomonbstoner@UbuntuAcer:~$ nc shell2017.picoctf.com 33123
Unguessably Randomized Flag: BNZQ:2m8807395d9os2156v70qu84sy1w2i6e
solomonbstoner@UbuntuAcer:~$ nc shell2017.picoctf.com 33123
Unguessably Randomized Flag: BNZQ:2m8807395d9os2156v70qu84sy1w2i6e
solomonbstoner@UbuntuAcer:~$ nc shell2017.picoctf.com 33123
Unguessably Randomized Flag: BNZQ:2m8807395d9os2156v70qu84sy1w2i6e
solomonbstoner@UbuntuAcer:~$ nc shell2017.picoctf.com 33123
Unguessably Randomized Flag: BNZQ:2m8807395d9os2156v70qu84sy1w2i6e
```

According to Python docs, Python random function uses *Mersenne Twister algorithm*. So, we find how to predict the seed of the algorithm.
https://jazzy.id.au/2010/09/22/cracking_random_number_generators_part_3.html <\- this is the resource. 

### Uninformed attempt to solve
I tried downloading `untwister` and using it to "crack" the randomised `flag BNZQ:2m8807395d9os2156v70qu84sy1w2i6e`. (I had no idea what I was doing. I was just trying my luck).
```
solomonbstoner@UbuntuAcer:~/Apps from GIthub/untwister$ ./untwister -r mt19937 -i tmp 
[!] Not enough observed values to perform state inference, try again with more than 624 values.
[*] Looking for seed using mt19937
[*] Spawning 4 worker thread(s) ...
[*] Completed in 15 second(s)
[$] Found seed 1074981138 with a confidence of 100.00%
```
But the seed 1074981138 is not the flag. 

### Realisation of a dumb mistake

It turns out I forgot one important clue - the source file of soRandom itself:

```
#!/usr/bin/python -u
import random,string

1	flag = "FLAG:"+open("flag", "r").read()[:-1]
2	encflag = ""
3	random.seed("random")
4	for c in flag:
5	  if c.islower():
	    #rotate number around alphabet a random amount
6		encflag += chr((ord(c)-ord('a')+random.randrange(0,26))%26 + ord('a'))
7	  elif c.isupper():
8		encflag += chr((ord(c)-ord('A')+random.randrange(0,26))%26 + ord('A'))
9	  elif c.isdigit():
10		encflag += chr((ord(c)-ord('0')+random.randrange(0,10))%10 + ord('0'))
11	  else:
12		encflag += c
13	print "Unguessably Randomized Flag: "+encflag
```
### Analysis of the big clue

Pseudocode of the snippet of code above - 
```
Read the flag from the file and store it in the variable "flag" in the format "FLAG: xxxxx"
We create an empty string variable "encflag" that will contain the encoded flag.
1	Set the seed of the PRNG to the string "random".
2	For every character in the flag,
3		if the char is a lower alphebet,
4			c = (c - 'a' + rand int between 0 & 25 inc )%26 + 'a';
5			Then we add it to the encflag string.
6		if the char is a capital alphebet.
7			c = (c - 'A' + rand int between 0 & 25 inc )%26 + 'A';
8			Then we add it to the encflag string.
9		if the char is a digit,
10			c = (c - '0' + rand int between 0 & 10 inc )%10 + '0';
11			Then we add it to the encflag string.
12		else,
13			We just add it to the encflag string.
```

From this, it is obvious that a character in the original flag & its corresponding character in the encflag are of the same category (category meaning a lower alphebet, capital alphabet, or a digit).

Q: So, how are we going to predict all the random int generated? 
A: Using the same seed used in the sorandom.py program, we can reproduce the random int.
Below is the code I created to decode the encoded flag. The process is literally the reverse of the encoding as it looks like symmetrical encryption to me.
```
#!/usr/bin/python -u
import random,string

decflag = ""
encflag = "BNZQ:2m8807395d9os2156v70qu84sy1w2i6e"


random.seed("random")
for c in encflag:
  if c.islower():
    decflag += chr((ord(c)-ord('a')-random.randrange(0,26))%26 + ord('a'))
  elif c.isupper():
    decflag += chr((ord(c)-ord('A')-random.randrange(0,26))%26 + ord('A'))
  elif c.isdigit():
    decflag += chr((ord(c)-ord('0')-random.randrange(0,10))%10 + ord('0'))
  else:
    decflag += c

print "Encoded flag: " + encflag
print "Decoded flag: " + decflag
```

Note: the code above can only be run with python2. When I ran it with Python3, the program gave a totally different flag. (see below for output, and [here](https://stackoverflow.com/questions/11929701/why-is-seeding-the-random-generator-not-stable-between-versions-of-python) for the explanation)
```
solomonbstoner@UbuntuAcer:~/Desktop/CTF files/picoCTF/Lvl 2/soRandom$ python3 sorandom\ \(reversed\).py 
Encoded flag: BNZQ:2m8807395d9os2156v70qu84sy1w2i6e
Decoded flag: LZTY:0o8060300x6kb9899m25oj07af9l1y5r
solomonbstoner@UbuntuAcer:~/Desktop/CTF files/picoCTF/Lvl 2/soRandom$ python sorandom\ \(reversed\).py 
Encoded flag: BNZQ:2m8807395d9os2156v70qu84sy1w2i6e
Decoded flag: FLAG:9b6098160b2ca5139c83fe29fd7c9e5d
```

Turns out that `untwister` was not needed at all. I did not even need to realise that Python random generator uses the Mersenne Twister algorithm. I just had to know that **with the same seed, the output will the same** as the value of `rand()` depends on its previous value.


END