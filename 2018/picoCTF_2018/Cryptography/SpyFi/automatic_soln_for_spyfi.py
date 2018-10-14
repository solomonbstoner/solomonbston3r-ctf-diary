# This solution is an improvement of the manual solution, manual_soln_for_spyfi.py, I first created. The manual soln was created to let me experiment with the concept of chosen plaintext attack. Once I got the concept, creating an automatic solution was easier.

#!/usr/bin/env python2
from pwn import remote
import string
import re

# to get a collection of letters for flag
charset = string.ascii_letters + string.punctuation + string.digits
flag ="picoCTF{"
padding_before = 'A' * 11
padding_after = 'A' * 8		# padding_after changes as we bruteforce the next byte

chosen_plaintext = 'de is: picoCTF{'	#initialise the chosen plaintext with the first block of plaintext. Note: it is 15 chars long so that I can apend the char I want to bruteforce to the end.

index_of_cipher_block_of_input = 4
index_of_cipher_block_of_known_plaintext = 7

index_of_char = 0

while True:

	char_to_bruteforce = charset[index_of_char]
	print char_to_bruteforce
	index_of_char = (index_of_char + 1) % len(charset)

	str_to_test = padding_before + chosen_plaintext + char_to_bruteforce + padding_after

	r = remote("2018shell1.picoctf.com",31123)
	r.recvuntil('Please enter your situation report:')
	r.sendline(str_to_test) 

	cipher = r.recvline()[1:]

	cipher_block_of_input = cipher[(index_of_cipher_block_of_input * 32) : ((index_of_cipher_block_of_input + 1) * 32)]

	cipher_block_of_known_plaintext = cipher[(index_of_cipher_block_of_known_plaintext * 32) : ((index_of_cipher_block_of_known_plaintext + 1) * 32)]


	print cipher_block_of_input + " : " + cipher_block_of_known_plaintext
	r.close()
	if cipher_block_of_input == cipher_block_of_known_plaintext:	#if test passes, it means we found the correct byte -> move on to the next byte
		flag += char_to_bruteforce
		chosen_plaintext = chosen_plaintext[1:] + char_to_bruteforce
		index_of_char = 0
		print "Found : " + flag
		if len(padding_after) == 0:
			padding_after = "A" * 15		# reset padding
			index_of_cipher_block_of_known_plaintext += 1
		else:
			padding_after = padding_after[:-1]	#reduce padding by 1 character

		
		if char_to_bruteforce == '}':
			break

		continue

print "The flag is : " + flag
