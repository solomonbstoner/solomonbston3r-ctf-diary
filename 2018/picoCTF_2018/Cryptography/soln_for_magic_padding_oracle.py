from pwn import remote

r = remote('2018shell2.picoctf.com', 45008)

r.recvuntil('Here is a sample cookie: ')

encrypted_cookie = r.recvline()[:-1]

for index in range(0, len(encrypted_cookie), 32):
	print "%d : %s"%(index, encrypted_cookie[index:index+32]) 


