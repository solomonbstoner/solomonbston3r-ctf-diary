## Crypto Warmup 1

Ciphertext : llkjmlmpadkkc
Key : thisisalilkey
Cipher algorithm : Vignere Cipher ( I know it because of the [table given](crypto_warmup_1_table.txt))


Using the key as the column index, 

| C | P |
|-|-|
|l | S|
|l | E|
|k | C|
|j | R|
|m | E|
|l | T|
|m | M|
|p | E|
|a | S|
|d | S|
|k | A|
|k | G|
|c | E|

The flag is : `picoCTF{SECRETMESSAGE}`.

## Crypto Warmup 2

Ciphertext : cvpbPGS{guvf_vf_pelcgb!}
Key : m=13 (ie `c = (p + m) mod 26`)
Cipher algorithm : ROT13

```
>>> cipher = 'cvpbPGS{guvf_vf_pelcgb!}'
>>> plaintext = ''
>>> for c in cipher:
...     if c.isalpha():
...             plaintext += chr((ord(c.lower())-ord('a') + 13) % 26 + ord('a'))
...     else:
...             plaintext += c
... 
>>> plaintext
'picoctf{this_is_crypto!}'
>>> 
```

The flag is `picoCTF{this_is_crypto!}`.

## Caesar Cipher 1

Ciphertext : picoCTF{yjhipvddsdasrpthpgrxewtgdqnjytto}
Cipher algorithm : ~~Caesar Cipher~~ Shift cipher 

The challenge claims it is a caesar cipher. However, that means the key is `m=-3`. However, that is not the case here. The ciphertext is not encrypted using Caesar's Cipher.

```
>>> cipher = "yjhipvddsdasrpthpgrxewtgdqnjytto"
>>> plaintext
'vgefmsaapaxpomqemdoubtqdankgvqql'
>>> for c in cipher:
...     if c.isalpha():
...             plaintext += chr((ord(c.lower())-ord('a') + 3) % 26 + ord('a'))
...     else:
...             plaintext += c
... 
>>> plaintext
'bmklsyggvgdvuswksjuahzwjgtqmbwwr'
```

I tried all possible keys of a shift cipher to see which worked. Turns out the key for encryption was `m = 15`.

```
>>> cipher = "yjhipvddsdasrpthpgrxewtgdqnjytto"
>>> plaintext=''
>>> for i in range(1,26):
...     for c in cipher:
...             plaintext += chr((ord(c.lower())-ord('a') - i) % 26 + ord('a'))
...     print "%d : %s"%(i, plaintext)
...     plaintext = ''
... 
1 : xighouccrczrqosgofqwdvsfcpmixssn
2 : whfgntbbqbyqpnrfnepvcurebolhwrrm
3 : vgefmsaapaxpomqemdoubtqdankgvqql
4 : ufdelrzzozwonlpdlcntaspczmjfuppk
5 : tecdkqyynyvnmkockbmszrobylietooj
6 : sdbcjpxxmxumljnbjalryqnaxkhdsnni
7 : rcabiowwlwtlkimaizkqxpmzwjgcrmmh
8 : qbzahnvvkvskjhlzhyjpwolyvifbqllg
9 : payzgmuujurjigkygxiovnkxuheapkkf
10 : ozxyflttitqihfjxfwhnumjwtgdzojje
11 : nywxeksshsphgeiwevgmtlivsfcyniid
12 : mxvwdjrrgrogfdhvduflskhurebxmhhc
13 : lwuvciqqfqnfecguctekrjgtqdawlggb
14 : kvtubhppepmedbftbsdjqifspczvkffa us decrypt this message? We believe it is a form of a caesar cipher. You can find the ciphertext in /problems/caesar-cipher-2_0_372a62ea0204
15 : justagoodoldcaesarcipherobyujeez
16 : itrszfnncnkcbzdrzqbhogdqnaxtiddy
17 : hsqryemmbmjbaycqypagnfcpmzwshccx
18 : grpqxdllaliazxbpxozfmebolyvrgbbw
19 : fqopwckkzkhzywaownyeldankxuqfaav
20 : epnovbjjyjgyxvznvmxdkczmjwtpezzu
21 : domnuaiixifxwuymulwcjbylivsodyyt
22 : cnlmtzhhwhewvtxltkvbiaxkhurncxxs
23 : bmklsyggvgdvuswksjuahzwjgtqmbwwr
24 : aljkrxffufcutrvjritzgyvifsplavvq
25 : zkijqweetebtsquiqhsyfxuherokzuup
>>> 

```

The flag is `picoCTF{justagoodoldcaesarcipherobyujeez}`.


## Blaise's Cipher

The cipher text is [in this file](Cryptography/blaise_cipher_ciphertext). It is long enough to conduct cryptanalysis using Index of Coincidence (IC). According to online IC calculator, the cipher's IC is 0.04335. That means it is NOT a simple substitution cipher. It is either a polygraphic or polyalphabetic cipher. I decided to test if its a polyaphabetic cipher first. [The Kasiski Test](https://asecu us decrypt this message? We believe it is a form of a caesar cipher. You can find the ciphertext in /problems/caesar-cipher-2_0_372a62ea0204ritysite.com/encryption/kasiski) stated that the key's most likely size were 2 or 4. I used [the Vigenere Solver](https://www.guballa.de/vigenere-solver) to solve it. The key is `flag`. Part of the decrypted message is shown below.

```
[...]

Blaise de Vigenere published his description of a similar but stronger autokey cipher before the court of Henry III of France, in 1586. Later, in the 19th century, the invention of Bellaso's cipher was misattributed to Vigenere. David Kahn in his book The Codebreakers lamented the misattribution by saying that history had "ignored this important contribution and instead named a regressive and elementary cipher for him [Vigenere] though he had nothing to do with it". picoCTF{v1gn3r3_c1ph3rs_ar3n7_bad_5352bf72}

The Vigenere cipher gained a reputation for being exceptionally strong. Noted author and mathematician Charles Lutwidge Dodgson (Lewis Carroll) called the Vigenere cipher unbreakable in his 1868 piece "The Alphabet Cipher" in a children's magazine. In 1917, Scientific American described the Vigenere cipher as "impossible of translation". This reputation was not deserved. Charles Babbage is known to have broken a variant of the cipher as early as 1854; however, he didn't publish his work. Kasiski entirely broke the cipher and published the technique in the 19th century. Even before this, though, some skilled cryptanalysts could occasionally break the cipher in the 16th century.

[...]
```

The flag is `picoCTF{v1gn3r3_c1ph3rs_ar3n7_bad_5352bf72}`.

## Caesar Cipher 2

Cihpertext : ^WQ]1B4iQ/SaO@M1W>V3\`AMXcABMO@3\BMa3QC\`3k
Cipher algorithm : Shift cipher

The difference between this challenge and Caesar Cipher 1 is that that this challenge uses the [entire ASCII table (including the extended ASCII)](). Thus, while Caesar Cipher 1's encryption algorithm is `C = (P + m) mod 26`, this challenge's encryption algorithm is `C = (P + m) mod 256`.

```
>>> for i in range(1,256):
...     for c in cipher:
...             plaintext += chr((ord(c) + i) % 256)
...     print "%d : %s"%(i, plaintext)
...     plaintext = ""
...

[...]

12 : jc]i=N@u];_m[LY=cJb?lMYdoMNY[L?hNYm?]Ol?w
13 : kd^j>OAv^<`n\MZ>dKc@mNZepNOZ\M@iOZn@^Pm@x
14 : le_k?PBw_=ao]N[?eLdAnO[fqOP[]NAjP[oA_QnAy
15 : mf`l@QCx`>bp^O\@fMeBoP\grPQ\^OBkQ\pB`RoBz
16 : ngamARDya?cq_P]AgNfCpQ]hsQR]_PClR]qCaSpC{
17 : ohbnBSEzb@dr`Q^BhOgDqR^itRS^`QDmS^rDbTqD|
18 : picoCTF{cAesaR_CiPhErS_juST_aREnT_sEcUrE}
19 : qjdpDUG|dBftbS`DjQiFsT`kvTU`bSFoU`tFdVsF~
20 : rkeqEVH}eCgucTaEkRjGtUalwUVacTGpVauGeWtG
21 : slfrFWI~fDhvdUbFlSkHuVbmxVWbdUHqWbvHfXuH� 
```

The key for encryption is `m = -18`.
The flag is `picoCTF{cAesaR_CiPhErS_juST_aREnT_sEcUrE}`.

## rsa-madlibs

This is a challenge introducing one to RSA. The output from the interaction with the server is [in this file](Cryptography/rsa_madlibs_output). The challenge consists of many smaller ones, the last one being decrypting a cipher given the values, `p`, `e` and `n`. 
```
#### NEW MADLIB ####
p : 153143042272527868798412612417204434156935146874282990942386694020462861918068684561281763577034706600608387699148071015194725533394126069826857182428660427818277378724977554365910231524827258160904493774748749088477328204812171935987088715261127321911849092207070653272176072509933245978935455542420691737433
ciphertext : 2887512232927570212720289007617218056059430602904994311768865248937186092346045634461113653200410008027930318598899961967398819457005578177750855122616645816143754424929892030705859313377266089203195245015545475756780591749438383925678961618918887123573182347018588636929367129348683955602230289203565347486263264786442219851846011532640387672302559499309153498019746553031047474066734422816867560702848158992070366148525244203275301204388654920924623403169692782505561391649873520950447510664771965559666379810356768249845746489087039846408953680555639864400302957371546072298362982071553184164689418758473539792781
e : 65537
n : 23952937352643527451379227516428377705004894508566304313177880191662177061878993798938496818120987817049538365206671401938265663712351239785237507341311858383628932183083145614696585411921662992078376103990806989257289472590902167457302888198293135333083734504191910953238278860923153746261500759411620299864395158783509535039259714359526738924736952759753503357614939203434092075676169179112452620687731670534906069845965633455748606649062394293289967059348143206600765820021392608270528856238306849191113241355842396325210132358046616312901337987464473799040762271876389031455051640937681745409057246190498795697239
##### WE'RE GONNA NEED THE FOLLOWING ####
plaintext
IS THIS POSSIBLE and FEASIBLE? (Y/N):Y
#### TIME TO FILL IN THE MADLIB! ###
plaintext: 240109877286251840533272915662757983981706320845661471802585807564915966910385128423526644303028605 
YAHHH! That one was a great madlib!!!
```

The flag is `picoCTF{d0_u_kn0w_th3_w@y_2_RS@_b38be18a}`.

## SpyFi

The source code is in [this file](Cryptography/spy_terminal_no_flag.py). The flag is encrypted using AES ECB with null bytes as padding. Since we know the plaintext, and ECB encrypts each block independent of the other, we can use the [chosen plaintext attack](https://crypto.stackexchange.com/questions/42891/chosen-plaintext-attack-on-aes-in-ecb-mode?answertab=votes#tab-top) to bruteforce the flag byte by byte.

See [this file](SpyFi/automatic_soln_for_spyfi.py) for the automatic solution.

The flag is `picoCTF{@g3nt6_1$_th3_c00l3$t_5168610}`

## Safe RSA

We are [given the ciphertext, value N and e](Cryptography/safe_rsa_ciphertext). The key to solving this challenge is to realise that `(P ^ e) < N`. This means that `(p ^ e) = C` (because the modulo N is useless). The formula to get the plaintext is `C ^ (1/e) = p`. Watch [this YouTube video](https://www.youtube.com/watch?v=aS57JCzJw_o) between 1:45 and 2:38.

To solve this challenge, we need to ensure that the function that does the cuberoot keeps its precision because of the large number involved. I tried using the [regular method as suggested by Stackoverflow](https://stackoverflow.com/questions/19255120/is-there-a-short-hand-for-nth-root-of-x-in-python). It did not work. The values at the end of the plaintext were lost.

```
>>> 2205316413931134031046440767620541984801091216351222789180582564557328762455422721368029531360076729972211412236072921577317264715424950823091382203435489460522094689149595951010342662368347987862878338851038892082799389023900415351164773 ** (1/float(3))
1.3016382529448975e+79
>>> long (1.3016382529448975e+79)
13016382529448975049937056264654191108020998208395813341903515045258909345382400L
>>> plaintext = ""
>>> plaintext_hex = hex(13016382529448975049937056264654191108020998208395813341903515045258909345382400)[2:-1]
>>> for i in range(0, len(plaintext_hex), 2):
...     plaintext += chr(int(plaintext_hex[i:i+2], 16))
... 
>>> plaintext
'picoCS\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
>>>
```

I then tried the [gmpy2 library](https://gmpy2.readthedocs.io/en/latest/mpz.html). it seems appropriate for this.

> The gmpy2 mpz type supports arbitrary precision integers. It should be a drop-in replacement for Python’s long type. Depending on the platform and the specific operation, an mpz will be faster than Python’s long once the precision exceeds 20 to 50 digits. All the special integer functions in GMP are supported.

First, I got the plaintext (in decimals).
```
>>> cipher =  2205316413931134031046440767620541984801091216351222789180582564557328762455422721368029531360076729972211412236072921577317264715424950823091382203435489460522094689149595951010342662368347987862878338851038892082799389023900415351164773
>>> gmpy2.iroot(cipher, 3)
(mpz(13016382529449106065839070830454998857466392684017754632233906857023684751222397L), True)
```

Then, I converted it to hex, then ASCII. And I got the flag.
```
>>> hex(13016382529449106065839070830454998857466392684017754632233906857023684751222397)
'0x7069636f4354467b655f7734795f7430305f736d3431315f38316236353539667dL'
>>> plaintext_hex = "7069636f4354467b655f7734795f7430305f736d3431315f38316236353539667d"
>>> plaintext = ""
>>> for i in range(0, len(plaintext_hex), 2):
...     plaintext += chr(int(plaintext_hex[i:i+2], 16))
... 
>>> plaintext
'picoCTF{e_w4y_t00_sm411_81b6559f}'
>>> 

```

The flag is `picoCTF{e_w4y_t00_sm411_81b6559f}`.

## Super safe RSA

```
$ nc 2018shell2.picoctf.com 1317
c: 7921847833537353810811804554269941449648469036359900743380533792152506101148420
n: 18358313795796886893911411590218101662889849255949813292991951580284040334529041
e: 65537
```

The shortcut is to just factorise `n` to find `p` and `q`. However I could not find a way to do it. The [Python scripts in StackOverflow](https://stackoverflow.com/questions/15347174/python-finding-prime-factors) could not solve it. They resulted in `MemoryError`.
```
>>> prime_factors(18358313795796886893911411590218101662889849255949813292991951580284040334529041)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 14, in prime_factors
MemoryError
>>> 
```

So, I took the long way around. I used [RSACTFTool](https://github.com/Ganapati/RsaCtfTool) to first create the public key from `n` and `e`. Since the public key was small enough, I used the tool to create [the private key](Cryptography/super_safe_rsa_private.pem) from [the public key](Cryptography/super_safe_rsa_pub.pub). Then, I dumped the value of `d`.
```
$ python2 RsaCtfTool.py --publickey /home/solomonbstoner/Documents/Scr3enSl4y3rs/picoCTF_2018/Cryptography/super_safe_rsa_pub.pub --private --verbose
[*] Performing hastads attack.
[*] Performing factordb attack.
[*] Performing pastctfprimes attack.
[*] Loaded 71 primes
[*] Performing mersenne_primes attack.
[*] Performing noveltyprimes attack.
[*] Performing smallq attack.
[*] Performing wiener attack.
[*] Performing comfact_cn attack.
[*] Performing primefac attack.
[*] Performing fermat attack.
[*] Performing siqs attack.
[*] Yafu SIQS is working.
-----BEGIN RSA PRIVATE KEY-----
MIGsAgEAAiIAnoulYpwyD0E5nn24UAg0Q1WXKZYcAYPt55I/Pvvq09IRAgMBAAEC
IST2a51cyvLxguxnZQQLlZtYKimw5zylk/RUQE/ZcqaSAQIQdP/JQUKKt4pPhtP8
4F5G8QISAVrnyov68J8pKbO0nOWQmX0hAhAadmwntYw4fTEFltcATHKRAhEu0wal
6lM8SIQWe5SJ8ACnwQIQWXX1stXRrJEQTUqVTwPa+Q==
-----END RSA PRIVATE KEY-----
```
```
$ python2 RsaCtfTool.py --dumpkey --key /home/solomonbstoner/Documents/Scr3enSl4y3rs/picoCTF_2018/Cryptography/super_safe_rsa_private.pem
[*] n: 18358313795796886893911411590218101662889849255949813292991951580284040334529041
[*] e: 65537
[*] d: 4279974312006662417444687088010473096197384817737853822017170434986214334829057
[*] p: 155518565144731228870817193872198616817
[*] q: 118045802304772892312246363084177635114273
```

I tested that `p` and `q` were correct by verifying that `p*q = n`.
```
>>> 155518565144731228870817193872198616817 * 118045802304772892312246363084177635114273 == 18358313795796886893911411590218101662889849255949813292991951580284040334529041
True
```

Then, I used [this website](http://extranet.cryptomathic.com/rsacalc/index) to decrypt the message. It requires me to convert the values to hex.
```
>>> plainhex = "7069636f4354467b7573335f6c40726733725f7072316d33245f313639357d"
>>> plaintext = ""
>>> for i in range(0, len(plainhex), 2):
...     plaintext += chr(int(plainhex[i:i+2], 16))
... 
>>> plaintext
'picoCTF{us3_l@rg3r_pr1m3$_1695}'
```

The flag is `picoCTF{us3_l@rg3r_pr1m3$_1695}`.


## Super safe RSA 2

We are given a large `n`, so factoring it for the primes is unlikely to work. However, as the problem statement hints, `e` is too large for its own good. 


```
➜  ~ nc 2018shell2.picoctf.com 59549
c: 44577539188418770554409937079677390141184854371495016235658616384958609746983033530944747770339369168677510655521287905900609974875927095180021465038987926666089350832704859235881413527120741050203171207918770005332948445521199035591239427528644443725667219533749083023262340991552458032793325170987643049729
n: 109028710402957279352744165345032572035708981051068118315724547448464743289508010459496315954459326431088684247390427921356320304523709204666794915494137496899258577848019784981294751451210323175398904015386325768783155321683332166559311442759602833953418643834480139070174731580553338375199873599674687849379
e: 88519594302927413172408933790741689815646721283340456649852563363983101540983440324386826916410978532306907550229599756892266156269009003633298604735150539947229345856816581346021325301730899840705957749114544321011297063368054288821504788454854503124749550073461557305221305646903832149777514120134174889161

➜  ~
```


The quote from Stack Overflow below suggests a large `e` results in a small `d`.

> However, one can find a few reasons why a big public exponent shall be avoided:
> [...]
> There are security issues about having a small private exponent; a key-recovery attack has been described when the private exponent length is no more than 29% of the public exponent length. When you want to force the private exponent to be short (e.g. to speed up private key operations), you more or less have to use a big public exponent (as big as the modulus); requiring the public exponent to be short may then be viewed as a kind of indirect countermeasure.
>  
> *--[Stackoverflow](https://security.stackexchange.com/questions/2335/should-rsa-public-exponent-be-only-in-3-5-17-257-or-65537-due-to-security-c)*




This means we can do a Wiener's attack to obtain the private key. First, we create the public key from components `n` and `e`.
```
➜  RsaCtfTool git:(master) python2 RsaCtfTool.py --createpub -e 88519594302927413172408933790741689815646721283340456649852563363983101540983440324386826916410978532306907550229599756892266156269009003633298604735150539947229345856816581346021325301730899840705957749114544321011297063368054288821504788454854503124749550073461557305221305646903832149777514120134174889161 -n 109028710402957279352744165345032572035708981051068118315724547448464743289508010459496315954459326431088684247390427921356320304523709204666794915494137496899258577848019784981294751451210323175398904015386325768783155321683332166559311442759602833953418643834480139070174731580553338375199873599674687849379
```

Then, we use `RsaCtfTool` to find the private key. The verbose output shows that it's the Wiener's Attack that gets us the private key.
```
➜  RsaCtfTool git:(master) python2 RsaCtfTool.py --publickey ~/test.pub --private --verbose
[*] Performing hastads attack.
[*] Performing factordb attack.
[*] Performing pastctfprimes attack.
[*] Loaded 71 primes
[*] Performing mersenne_primes attack.
[*] Performing noveltyprimes attack.
[*] Performing smallq attack.
[*] Performing wiener attack.
-----BEGIN RSA PRIVATE KEY-----
MIIB4QIBAAKBgQCbQxThD1d4BlqWkQ4WyOEiML6E0f4U/BHonyJOCBQf/YLEC0z1
ysWajBkAWivbn4xdGJMpbFd0tn78NdYdWMK2ogYWL+1C+97Rfgnf3Xfa4bVwJBPn
6IP2m7xUlrfSwyeA/XWpXxzblX+eY8l/qocxAORyaQo4xq/7BVo9gsaDowKBgH4O
W7BSfWi0d+4Q/UhgdfEFdFlwCQNOmNeuA/MoufYzJG0445YXuJG+tznC/CLHCfY3
0ptqHCNlW/o3V4ziGMtWENcqVOciHYLRZcRK5WaWT78OsHyw3OhpoOz93f1d0eQ0
Iw+LJBlpO7Ica05BhmxRDnAt88j0nnw383R7AtTJAgMBAAECQQChdIB/6uQ/GiAs
UsZ1EGjtI7aM0iZwzrLcBHwjhOC+auhQycvO0KV+ohwC+w/KbVQwhLoXuAdvUtYQ
roHR6WtfAkEA9i4wTgTWAxwqav7P2cvaV0PR6gzqyN7SliXJ1t5FjARpzbG7XVRT
PScEqRfJGuLRdQn5LjuoTmc6vSQvSGzSPQIDAQABAgMBAAECQDQQTFDNsIkb9QJq
iSmKWl937WoPzs462iFsG70qinpqGut7+JCTMx8xO3PvTnSfSLIqxrMaG7KofzvF
VXrs/WA=
-----END RSA PRIVATE KEY-----
➜  RsaCtfTool git:(master)
```

As expected, the value of `d` is very small.
```
➜  RsaCtfTool git:(master) python2 RsaCtfTool.py --dumpkey --key ~/Documents/Scr3enSl4y3rs/picoCTF_2018/Cryptography/super_safe_rsa_2_private_key.pem
[*] n: 109028710402957279352744165345032572035708981051068118315724547448464743289508010459496315954459326431088684247390427921356320304523709204666794915494137496899258577848019784981294751451210323175398904015386325768783155321683332166559311442759602833953418643834480139070174731580553338375199873599674687849379
[*] e: 88519594302927413172408933790741689815646721283340456649852563363983101540983440324386826916410978532306907550229599756892266156269009003633298604735150539947229345856816581346021325301730899840705957749114544321011297063368054288821504788454854503124749550073461557305221305646903832149777514120134174889161
[*] d: 65537
[*] p: 8456088980630616731394213530317694524198096229629220186073502175431983787983054803561278225872137198863128836133549298896073442064952243956537359023565663
[*] q: 12893515034278460613554864874344447446201262035528008311298466204651639212774786152728763494656730863708177228698315096950202348236199930320962196635177533
➜  RsaCtfTool git:(master) 
```

I used `d` and `n` to decrypt `c`.
```
>>> pow(44577539188418770554409937079677390141184854371495016235658616384958609746983033530944747770339369168677510655521287905900609974875927095180021465038987926666089350832704859235881413527120741050203171207918770005332948445521199035591239427528644443725667219533749083023262340991552458032793325170987643049729, 65537, 109028710402957279352744165345032572035708981051068118315724547448464743289508010459496315954459326431088684247390427921356320304523709204666794915494137496899258577848019784981294751451210323175398904015386325768783155321683332166559311442759602833953418643834480139070174731580553338375199873599674687849379)
264003602020102370693041857442610586342633199683725005643958437442448465210344626586049655751813147243861914237L
>>> plainhex = hex(264003602020102370693041857442610586342633199683725005643958437442448465210344626586049655751813147243861914237)[2:-1]
>>> plainhex
'7069636f4354467b77407463685f793075725f5870306e336e74245f6340723366753131795f333632303736327d'
>>> plaintext = ""
>>> for i in range(0, len(plainhex), 2):
...     plaintext += chr(int(plainhex[i:i+2], 16))
... 
>>> plaintext
'picoCTF{w@tch_y0ur_Xp0n3nt$_c@r3fu11y_3620762}'
>>> 
```

The flag is `picoCTF{w@tch_y0ur_Xp0n3nt$_c@r3fu11y_3620762}`.


