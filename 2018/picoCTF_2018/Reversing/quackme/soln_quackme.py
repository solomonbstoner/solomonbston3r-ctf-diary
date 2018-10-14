#from pwn import *

#p = process('./main')

string_checker = "You have now entered the Duck Web, and you're in for a honkin' good time.Can you figure out my trick?"

sekrut_buffer = "2906164f2b35301e511b5b144b085d2b53105451434d5c545d"

input_str = ""

for i in range(0,0x19):
	input_str += chr(int(sekrut_buffer[i*2:(i+1)*2],16) ^ ord(string_checker[i]))

print input_str
