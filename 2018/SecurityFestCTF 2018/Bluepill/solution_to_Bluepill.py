

proc_ver_string = "Linux version 4.17.0-rc4+ (likvidera@ubuntu) (gcc version 7.2.0 (Ubuntu 7.2.0-8ubuntu3.2)) #9 Sat May 12 12:57:01 PDT 2018"


hash_of_user_str = ["40369e8c78b46122a4e813228ae8ee6e", "e4a75afe114e4483a46aaa20fe4e6ead", "8c3749214f4a9131ebc67e6c7a86d162"]

xor_decrypted_hash_of_chars_0_to_3 = ""
xor_decrypted_hash_of_chars_4_to_7 = ""
xor_decrypted_hash_of_chars_8_to_11 = ""

# Decrypt the md5 hash for user_string[0:4]. The decrypted hash is stored in xor_decrypted_hash_of_chars_0_to_3

proc_ver_index = 0
hash_str_index = 0
hash_str = hash_of_user_str[0]
for i in range(16):
	proc_ver_byte = ord(proc_ver_string[proc_ver_index])
	hash_byte = int(hash_str[hash_str_index:hash_str_index+2], 16)
	result_hash = proc_ver_byte ^ hash_byte
	result_hash = hex(result_hash)[2:]
	if(len(result_hash) == 1):
		result_hash = "0" + result_hash
	proc_ver_index = proc_ver_index + 1
	hash_str_index = hash_str_index + 2
	xor_decrypted_hash_of_chars_0_to_3 += result_hash
	print hex(hash_byte) + " ^ " + hex(proc_ver_byte) + " = " + result_hash



# Decrypt the md5 hash for user_string[4:8]. The decrypted hash is stored in xor_decrypted_hash_of_chars_4_to_7

hash_str_index = 0
proc_ver_index = 0
hash_str = hash_of_user_str[1]
for i in range(16):
	proc_ver_byte = ord(proc_ver_string[proc_ver_index])
	hash_byte = int(hash_str[hash_str_index:hash_str_index+2], 16)
	result_hash = proc_ver_byte ^ hash_byte
	result_hash = hex(result_hash)[2:]
	if(len(result_hash) == 1):
		result_hash = "0" + result_hash
	proc_ver_index = proc_ver_index + 1
	hash_str_index = hash_str_index + 2
	xor_decrypted_hash_of_chars_4_to_7 += result_hash
	print hex(hash_byte) + " ^ " + hex(proc_ver_byte) + " = " + result_hash



# Decrypt the md5 hash for user_string[8:12]. The decrypted hash is stored in xor_decrypted_hash_of_chars_8_to_11

hash_str_index = 0
proc_ver_index = 0
hash_str = hash_of_user_str[2]
for i in range(16):
	proc_ver_byte = ord(proc_ver_string[proc_ver_index])
	hash_byte = int(hash_str[hash_str_index:hash_str_index+2], 16)
	result_hash = proc_ver_byte ^ hash_byte
	result_hash = hex(result_hash)[2:]
	if(len(result_hash) == 1):
		result_hash = "0" + result_hash
	proc_ver_index = proc_ver_index + 1
	hash_str_index = hash_str_index + 2
	xor_decrypted_hash_of_chars_8_to_11 += result_hash
	print hex(hash_byte) + " ^ " + hex(proc_ver_byte) + " = " + result_hash

assert len(xor_decrypted_hash_of_chars_0_to_3) == 32
assert len(xor_decrypted_hash_of_chars_4_to_7) == 32
assert len(xor_decrypted_hash_of_chars_8_to_11) == 32

print "XOR decrypted hash for user_string[0:4] : " + xor_decrypted_hash_of_chars_0_to_3
print "XOR decrypted hash for user_string[4:8] : " + xor_decrypted_hash_of_chars_4_to_7
print "XOR decrypted hash for user_string[8:12] : " + xor_decrypted_hash_of_chars_8_to_11

