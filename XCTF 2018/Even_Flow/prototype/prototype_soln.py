from pwn import *


allowed = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz{}"
allowed_len = len(allowed)

MIN = 0
MAX = len(allowed)

correct_flag = ""

x=0
while (True):
	r = process('even_flow.py')
	r.recvuntil('Flag: ')
	str_to_test = correct_flag + allowed[x]
	print "Testing: " + str_to_test
	r.sendline(str_to_test)
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
