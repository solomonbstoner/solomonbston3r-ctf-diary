# 

## Challenge

This is one of the older ciphers in the books, can you decrypt the message? You can find the [ciphertext](ciphertext) in [`/problems/caesar-cipher-1_2_73ab1c3e92ea50396ad143ca48039b86/ciphertext`](ciphertext) on the shell server.

## Solution

By observing [how Caesar ciphers work](https://learncryptography.com/classical-encryption/caesar-cipher), all we have to do is rotate all the characters in `payzgmuujurjigkygxiovnkxlcgihubb` until we arrive at something sensible:

Using a [Python script](solver.py) to rotate the characters one at a time,

```
$ python solver.py
Shift 0: payzgmuujurjigkygxiovnkxlcgihubb
Shift 1: qbzahnvvkvskjhlzhyjpwolymdhjivcc
Shift 2: rcabiowwlwtlkimaizkqxpmzneikjwdd
Shift 3: sdbcjpxxmxumljnbjalryqnaofjlkxee
Shift 4: tecdkqyynyvnmkockbmszrobpgkmlyff
Shift 5: ufdelrzzozwonlpdlcntaspcqhlnmzgg
Shift 6: vgefmsaapaxpomqemdoubtqdrimonahh
Shift 7: whfgntbbqbyqpnrfnepvcuresjnpobii
Shift 8: xighouccrczrqosgofqwdvsftkoqpcjj
Shift 9: yjhipvddsdasrpthpgrxewtgulprqdkk
Shift 10: zkijqweetebtsquiqhsyfxuhvmqsrell
Shift 11: aljkrxffufcutrvjritzgyviwnrtsfmm
Shift 12: bmklsyggvgdvuswksjuahzwjxosutgnn
Shift 13: cnlmtzhhwhewvtxltkvbiaxkyptvuhoo
Shift 14: domnuaiixifxwuymulwcjbylzquwvipp
Shift 15: epnovbjjyjgyxvznvmxdkczmarvxwjqq
Shift 16: fqopwckkzkhzywaownyeldanbswyxkrr
Shift 17: grpqxdllaliazxbpxozfmeboctxzylss
Shift 18: hsqryemmbmjbaycqypagnfcpduyazmtt
Shift 19: itrszfnncnkcbzdrzqbhogdqevzbanuu
Shift 20: justagoodoldcaesarcipherfwacbovv
Shift 21: kvtubhppepmedbftbsdjqifsgxbdcpww
Shift 22: lwuvciqqfqnfecguctekrjgthycedqxx
Shift 23: mxvwdjrrgrogfdhvduflskhuizdferyy
Shift 24: nywxeksshsphgeiwevgmtlivjaegfszz
Shift 25: ozxyflttitqihfjxfwhnumjwkbfhgtaa
```

We notice that a shift of 20 characters result in somethig sensible: `justagoodoldcaesarcipherfwacbovv`. Our flag is `picoCTF{justagoodoldcaesarcipherfwacbovv}`.


