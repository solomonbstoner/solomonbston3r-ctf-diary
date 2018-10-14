# This exploit script is my first. I have to manually change the paddings before and after the input to get the desired chosen plaintext. I created it to understand how desired chosen plaintext attack works. See automatic_soln_for_spyfi.py for the automatic solution.

from pwn import *

padding_before = "A" * 11
padding_after = "A" * 11

cipher = ''
for char_to_test in range(33,127):
	p = remote('2018shell2.picoctf.com', 34490)
	p.clean()
	#context.log_level = 'DEBUG'
	p.recvuntil('report:')

	str_to_test = "c00l3$t_5168610" + chr(char_to_test)


	bruteforce_str = padding_before + str_to_test + padding_after


	p.sendline(bruteforce_str)


	cipher = p.recvline()[1:]

	p.close()

	print "Hex of encrypted input : %s"%(cipher[32*4:32*5])

	print "Hex of actual message : %s"%(cipher[32*9:32*10])

	print "%d - %s"%(char_to_test,str(cipher[32*4:32*5] == cipher[32*9:32*10]))

	#for i in range(0, len(cipher), 32):
	#	print "%s"%(cipher[i:i+32])

	if cipher[32*4:32*5] == cipher[32*9:32*10]:
		print chr(char_to_test)
		break

'''
# Example of output:

121 - False
[+] Opening connection to 2018shell2.picoctf.com on port 34490: Done
[*] Closed connection to 2018shell2.picoctf.com port 34490
Hex of encrypted input : 4a98d4a9994ef48bf16cc333f9b06335
Hex of actual message : a845efa04ec8c99b52e6233f9da3d597
122 - False
[+] Opening connection to 2018shell2.picoctf.com on port 34490: Done
[*] Closed connection to 2018shell2.picoctf.com port 34490
Hex of encrypted input : 742750ba80677cab5621c2604da75c2d
Hex of actual message : a845efa04ec8c99b52e6233f9da3d597
123 - False
[+] Opening connection to 2018shell2.picoctf.com on port 34490: Done
[*] Closed connection to 2018shell2.picoctf.com port 34490
Hex of encrypted input : dfedd6a1698d98859c94fe3acfa96635
Hex of actual message : a845efa04ec8c99b52e6233f9da3d597
124 - False
[+] Opening connection to 2018shell2.picoctf.com on port 34490: Done
[*] Closed connection to 2018shell2.picoctf.com port 34490
Hex of encrypted input : a845efa04ec8c99b52e6233f9da3d597
Hex of actual message : a845efa04ec8c99b52e6233f9da3d597
125 - True
}

'''
