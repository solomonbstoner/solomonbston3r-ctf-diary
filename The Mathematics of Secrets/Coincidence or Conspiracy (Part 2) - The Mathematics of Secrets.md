# For Coincidence or Conspiracy in The Mathematics of Secrets

On page 36 of Chapter 2, we are challenged to cryptanalyse the following cipher.
```
IW*CI W@G*L &H&L( ASN*A E)U&V $CNPC
SIW*E DDSA@ LTCIH !(A#C V%EIW *!#HA
*IW@N TAEHR $CI(C JTS!C SHDS# SIW@S
DVW@R G$HH* SIW*W )JH@( CUGDC IDUIW
*&AIP GWTUA TLS$L CIW*D IWTG! #HATW
TRG$H H*SQT U$G*I W@S)D GHWTR APBDG
*S%EI W@WDB @HIG@ IRWWX H&CV+ XHWVG
*LLXI WW#HE G)VG@ HHI#A AEGTH @CIAN
W*L!H Q%I!L )DAAN R)BTI B)K#C VXC#I
HDGQX ILXIW IW@VA *&B!C SIWTH E**S$
UA(VW I
```

> I'll even give you a hint. The cipher is an additive cipher plus homophones added for the vowels, very similar to the Mantuan cipher. Thus, you should probably look for ciphertext letters that correspond to high-frequency plaintext consonants.
>  
> -- *The Mathematics of Secrets pg 36

The formula of an additive cipher is ` C ≡  kP + m (mod 26)` where `k=1`, `m` is the key, `C` is the cipher, and `P` is the plaintext character. 

I ran a Python script to analyse the frequency and percentage frequency of each character in the cipher text. I will provide the source code later. For now, let's discuss about how its output helps us decipher the cipher.
```
$ python3 frequency.py 
Total number of characters : 306
Total number of unique characters : 31

Analysis of individual characters:
-------------------------------
( :	5	:	1.633987%
% :	3	:	0.980392%
P :	3	:	0.980392%
I :	29	:	9.477124%
R :	6	:	1.960784%
& :	6	:	1.960784%
Q :	3	:	0.980392%
E :	8	:	2.614379%
# :	8	:	2.614379%
B :	5	:	1.633987%
! :	7	:	2.287582%
T :	13	:	4.248366%
L :	10	:	3.267974%
A :	17	:	5.555556%
H :	22	:	7.189542%
) :	7	:	2.287582%
X :	6	:	1.960784%
C :	16	:	5.228758%
@ :	13	:	4.248366%
G :	15	:	4.901961%
S :	15	:	4.901961%
* :	18	:	5.882353%
$ :	7	:	2.287582%
V :	9	:	2.941176%
D :	12	:	3.921569%
W :	28	:	9.150327%
J :	2	:	0.653595%
K :	1	:	0.326797%
N :	5	:	1.633987%
U :	6	:	1.960784%
+ :	1	:	0.326797%
-------------------------------
[...]
```
Let's compare the English letters and cipher characters with the highest number of occurances.

| English Letter | Percentage frequency in English text | Cipher Letter | Percentage frequency in cipher text |
| --- | --- | --- | --- |
| E | 12.02 | I | 9.48 | 
| T | 9.10 | W | 9.15 |
| A | 8.12 | H | 7.19 |
| O | 7.68 | | |
| I | 7.31 | | |
| N | 6.95 | | |
| S | 6.28 | | |

Since the vowels are encrypted using homophones just like a Mantuan cipher, we can ignore the vowels in the "English letter" column of the table. That means there are 3 possibilities 

1. `T -> I`, `N -> W`

We start with 2 equations.

Eqn 1 -> `8 ≡ 19k + m (mod 26)`
Eqn 2 -> `22 ≡ 13k + m (mod 26)`
Eqn 2 - Eqn 1 -> `-14 ≡ 6k (mod 26)`

Since there is no multiplicative inverse of `6 (mod 26)`, we cannot find the value of `k`, where `k ∈ N`.

2. `T -> I`, `S -> W`

Eqn 1 -> `8 ≡ 19k + m (mod 26)`
Eqn 2 -> `22 ≡ 18k + m (mod 26)`
Eqn 2 - Eqn 1 -> `-14 ≡ k (mod 26)`

We get the answer `k=12`. The clue tells us that the cipher is *additive*, which means that this value of `k` is incorrect. It should be `k=1` instead. Besides, there is no multiplicative inverse of `12 mod 26`, so `k=12` is a *bad* key. Thus, we can dismiss this possiblity.

3. `T -> I`, `S -> H`

Eqn 1 -> `8 ≡ 19k + m (mod 26)`
Eqn 2 -> `7 ≡ 18k + m (mod 26)`
Eqn 2 - Eqn 1 -> `1 ≡ k (mod 26)`

Now we know we're on the right track. Let's substitute value `k=1` into eqn 1. 
```
8 ≡ 19 + m (mod 26)
-11 ≡ m (mod 26)
15 ≡ m (mod 26)
```

Let's try deciphering all the cipher *alphebets* using `solve.py` from the previous writeup, [Coincidence or Conspiracy - The Mathematics of Secrets](https://github.com/solomonbstoner/solomonbston3r-ctf-diary/blob/master/The%20Mathematics%20of%20Secrets/Coincidence%20or%20Conspiracy%20-%20The%20Mathematics%20of%20Secrets.md), with some changes below. I will provide the full script at the end of this writeup. The other ASCII characters that are not alphabets are homophones for the vowels. We do not know which character is the cipher substitute for which vowel. Thus, we solve for the consonants first.
```
[...]
for c in ciphertext:
	print("-----------------")
	print("Cipher: " + c)
	c = c.upper()
	if 0x41 <= ord(c) <= 0x5A :
		c = ord(c) - ord('A')		# Converts 'A'=0, 'B'=1... 'Z'=25
		p = k_inverse * ( c - m )
		p = p % 26
		print("%d ≡ %d * (%d - %d) (mod 26)" % (p, k_inverse, c, m))
		p = chr(p + ord('A'))		# Converts 0='A', 1='B'... 25='Z'
		print("Plaintext: " + p)
		print("-----------------")
		plaintext += p
	else:
		plaintext += '[' + c + ']'
		

print('Plaintext: \n' + plaintext)
exit(0)
```
```
$ python solve.py 1 15

Ciphertext: 
IW*CIW@G*L&H&L(ASN*AE)U&V$CNPCSIW*EDDSA@LTCIH!(A#CV%EIW*!#HA*IW@NTAEHR$CI(CJTS!CSHDS#SIW@SDVW@RG$HH*SIW*W)JH@(CUGDCIDUIW*&AIPGWTUATLS$LCIW*DIWTG!#HATWTRG$HH*SQTU$G*IW@S)DGHWTRAPBDG*S%EIW@WDB@HIG@IRWWXH&CV+XHWVG*LLXIWW#HEG)VG@HHI#AAEGTH@CIANW*L!HQ%I!L)DAANR)BTIB)K#CVXC#IHDGQXILXIWIW@VA*&B!CSIWTHE**S$UA(VWI

[...]
-----------------
Plaintext: 
TH[*]NTH[@]R[*]W[&]S[&]W[(]LDY[*]LP[)]F[&]G[$]NYANDTH[*]POODL[@]WENTS[!][(]L[#]NG[%]PTH[*][!][#]SL[*]TH[@]YELPSC[$]NT[(]NUED[!]NDSOD[#]DTH[@]DOGH[@]CR[$]SS[*]DTH[*]H[)]US[@][(]NFRONTOFTH[*][&]LTARHEFLEWD[$]WNTH[*]OTHER[!][#]SLEHECR[$]SS[*]DBEF[$]R[*]TH[@]D[)]ORSHECLAMOR[*]D[%]PTH[@]HOM[@]STR[@]TCHHIS[&]NG[+]ISHGR[*]WWITHH[#]SPR[)]GR[@]SST[#]LLPRES[@]NTLYH[*]W[!]SB[%]T[!]W[)]OLLYC[)]METM[)]V[#]NGIN[#]TSORBITWITHTH[@]GL[*][&]M[!]NDTHESP[*][*]D[$]FL[(]GHT
```


`'TH[*]NTH[@]R[*]W[&]S...'` looks a lot like `'Then there was'`. Thus, `e -> *`, `e -> @`, and `a -> &`.

`'THESP[*][*]D[$]FL[(]GHT'` looks a lot like `'the speed of flight'`. Thus, `o -> $`, and `i -> (`.

Let's update `solve.py` to decrypt the non-alphabet cipher characters we know corresponds to their respective vowels.
```
		if c == '&':
			# cipher is a
			plaintext += 'a'
		elif c == '@' or c == '*':
			#ciper is e
			plaintext += 'e'
		elif c == '$':
			#ciper is o
			plaintext += 'o'
		elif c == '(':
			#ciper is i
			plaintext += 'i'
		else:
			plaintext += '[' + c + ']'
		
```
```
$ python solve.py 1 15
[...]
Plaintext: 
THeNTHeReWaSaWiLDYeLP[)]FaGoNYANDTHePOODLeWENTS[!]iL[#]NG[%]PTHe[!][#]SLeTHeYELPSCoNTiNUED[!]NDSOD[#]DTHeDOGHeCRoSSeDTHeH[)]USeiNFRONTOFTHeaLTARHEFLEWDoWNTHeOTHER[!][#]SLEHECRoSSeDBEFoReTHeD[)]ORSHECLAMOReD[%]PTHeHOMeSTReTCHHISaNG[+]ISHGReWWITHH[#]SPR[)]GReSST[#]LLPRESeNTLYHeW[!]SB[%]T[!]W[)]OLLYC[)]METM[)]V[#]NGIN[#]TSORBITWITHTHeGLeaM[!]NDTHESPeeDoFLiGHT
```

`'THeNTHeReWaSaWiLDYeLP[)]FaGoNY'` looks a lot like `'There was a wild yelp of agony'`. Thus, `o -> )`.


`'THeYELPSCoNTiNUED[!]NDSO'` looks a lot like `'the yelps continued and so'`. Thus, `a -> !`.

Let's update `solve.py` with this new information.
```
		if c == '&' or c == '!':
			# cipher is a
			plaintext += 'a'
		elif c == '@' or c == '*':
			#ciper is e
			plaintext += 'e'
		elif c == '$' or c == ')':
			#ciper is o
			plaintext += 'o'
		elif c == '(':
			#ciper is i
			plaintext += 'i'
		else:
			plaintext += '[' + c + ']'
```

`'THePOODLeWENTS[!]iL[#]NG[%]PTHe[!][#]SLe'` looks a lot like `'the poodle went sailing up the aisle'`. Thus, `u -> %`, and `i -> #`.

Let's update `solve.py` with this new information.
```
		if c == '&' or c == '!':
			# cipher is a
			plaintext += 'a'
		elif c == '@' or c == '*':
			#ciper is e
			plaintext += 'e'
		elif c == '$' or c == ')':
			#ciper is o
			plaintext += 'o'
		elif c == '(' or c == '#':
			#ciper is i
			plaintext += 'i'
		elif c == '%':
			#cipher is u
			plaintext += 'u'
		else:
			plaintext += '[' + c + ']'
```
```
Plaintext: 
THeNTHeReWaSaWiLDYeLPoFaGoNYANDTHePOODLeWENTSaiLiNGuPTHeaiSLeTHeYELPSCoNTiNUEDaNDSODiDTHeDOGHeCRoSSeDTHeHoUSeiNFRONTOFTHeaLTARHEFLEWDoWNTHeOTHERaiSLEHECRoSSeDBEFoReTHeDoORSHECLAMOReDuPTHeHOMeSTReTCHHISaNG[+]ISHGReWWITHHiSPRoGReSSTiLLPRESeNTLYHeWaSBuTaWoOLLYCoMETMoViNGINiTSORBITWITHTHeGLeaMaNDTHESPeeDoFLiGHT

```

`'HISaNG[+]ISHGReWWITHHiSPRoGReSS'` looks a lot like `'his anguish grew with his progress'`. Thus, we know `u -> +`.

Let's update `solve.py`.
```
		if c == '&' or c == '!':
			# cipher is a
			plaintext += 'a'
		elif c == '@' or c == '*':
			#ciper is e
			plaintext += 'e'
		elif c == '$' or c == ')':
			#ciper is o
			plaintext += 'o'
		elif c == '(' or c == '#':
			#ciper is i
			plaintext += 'i'
		elif c == '%' or c == '+':
			#cipher is u
			plaintext += 'u'
		else:
			plaintext += '[' + c + ']'
```
```
Plaintext: 
THeNTHeReWaSaWiLDYeLPoFaGoNYANDTHePOODLeWENTSaiLiNGuPTHeaiSLeTHeYELPSCoNTiNUEDaNDSODiDTHeDOGHeCRoSSeDTHeHoUSeiNFRONTOFTHeaLTARHEFLEWDoWNTHeOTHERaiSLEHECRoSSeDBEFoReTHeDoORSHECLAMOReDuPTHeHOMeSTReTCHHISaNGuISHGReWWITHHiSPRoGReSSTiLLPRESeNTLYHeWaSBuTaWoOLLYCoMETMoViNGINiTSORBITWITHTHeGLeaMaNDTHESPeeDoFLiGHT
```

We successfully deciphered the cipher text. We know we did it correctly because it is legible English text. To make it more presentable and readable, let's add some spaces and punctuation marks. 

> Then there was a wild yelp of agony and the poodle went sailing up the aisle. The yelps continued, and so did the dog. He crossed the house in front of the altar. He flew down the other aisle. He crossed before the doors. He clamored up the home-stretch. His anguish grew with his progress, till presently he was but a woolly comet moving in its orbit with the gleam and the speed of light. 

### Script source

As promised, here are the 2 full scripts used to solve this challenge.

1. The one below is used to anaylyse the cipher text.

```
# This Python script analyses the letter frequency of the cipher text in Coincidence or Conspiracy of page 36.

def index_of_coincidence():
	probability_of_coincidence = 0.0
	for c in cipher_frequency:
		probability_of_coincidence += ((cipher_frequency[c] / total_num_of_chars) * (cipher_frequency[c] - 1) / (total_num_of_chars - 1))
		print("Index of coincidence for %s : %d/%d * %d/%d" % (c, cipher_frequency[c], total_num_of_chars, cipher_frequency[c] - 1, total_num_of_chars - 1))
	return probability_of_coincidence

ciphertext = """
IW*CI W@G*L &H&L( ASN*A E)U&V $CNPC
SIW*E DDSA@ LTCIH !(A#C V%EIW *!#HA
*IW@N TAEHR $CI(C JTS!C SHDS# SIW@S
DVW@R G$HH* SIW*W )JH@( CUGDC IDUIW
*&AIP GWTUA TLS$L CIW*D IWTG! #HATW
TRG$H H*SQT U$G*I W@S)D GHWTR APBDG
*S%EI W@WDB @HIG@ IRWWX H&CV+ XHWVG
*LLXI WW#HE G)VG@ HHI#A AEGTH @CIAN
W*L!H Q%I!L )DAAN R)BTI B)K#C VXC#I
HDGQX ILXIW IW@VA *&B!C SIWTH E**S$
UA(VW I
"""

ciphertext = ciphertext.replace(" ","").replace("\n","")

cipher_frequency = {}

total_num_of_chars = 0

for c in ciphertext:
	total_num_of_chars += 1
	if c in cipher_frequency:
		cipher_frequency[c] += 1
	else:
		cipher_frequency[c] = 1

print ("Total number of characters : %d" % total_num_of_chars)
print ("Total number of unique characters : %d" % len(cipher_frequency))

print ("\nAnalysis of individual characters:")
print ("-------------------------------")


for c in cipher_frequency:
	percentage_frequency = 100.00 * cipher_frequency[c] / total_num_of_chars
	print("%s :	%d	:	%f%%" % (c, cipher_frequency[c], percentage_frequency ))

print ("-------------------------------")

print ("\nAnalysing Index of coincidence of the cipher :")
print ("-------------------------------")

print ("Index of coincidence : %f" % index_of_coincidence())
print ("-------------------------------")

```

2. The one below is used to decrypt the cipher.

```
# This Python script decrypts the cipher text in Coincidence or Conspiracy of page 36 using the keys k and m provided as an argument.

import sys

if(len(sys.argv) != 3):
	print("k = sys.argv[1], m = sys.argv[2]")
	exit(1)

# return (g, x, y) a*x + b*y = gcd(x, y)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

ciphertext = """
IW*CI W@G*L &H&L( ASN*A E)U&V $CNPC
SIW*E DDSA@ LTCIH !(A#C V%EIW *!#HA
*IW@N TAEHR $CI(C JTS!C SHDS# SIW@S
DVW@R G$HH* SIW*W )JH@( CUGDC IDUIW
*&AIP GWTUA TLS$L CIW*D IWTG! #HATW
TRG$H H*SQT U$G*I W@S)D GHWTR APBDG
*S%EI W@WDB @HIG@ IRWWX H&CV+ XHWVG
*LLXI WW#HE G)VG@ HHI#A AEGTH @CIAN
W*L!H Q%I!L )DAAN R)BTI B)K#C VXC#I
HDGQX ILXIW IW@VA *&B!C SIWTH E**S$
UA(VW I
"""
plaintext = ""

k = int(sys.argv[1])
m = int(sys.argv[2])

ciphertext = ciphertext.replace(" ","").replace("\n","")

print('Ciphertext: \n' + ciphertext)
print('\n')

k_inverse = mulinv(k, 26)

for c in ciphertext:
	print("-----------------")
	print("Cipher: " + c)
	c = c.upper()
	if 0x41 <= ord(c) <= 0x5A :
		c = ord(c) - ord('A')		# Converts 'A'=0, 'B'=1... 'Z'=25
		p = k_inverse * ( c - m )
		p = p % 26
		print("%d ≡ %d * (%d - %d) (mod 26)" % (p, k_inverse, c, m))
		p = chr(p + ord('A'))		# Converts 0='A', 1='B'... 25='Z'
		print("Plaintext: " + p)
		print("-----------------")
		plaintext += p
	else:
		if c == '&' or c == '!':
			# cipher is a
			plaintext += 'a'
		elif c == '@' or c == '*':
			#ciper is e
			plaintext += 'e'
		elif c == '$' or c == ')':
			#ciper is o
			plaintext += 'o'
		elif c == '(' or c == '#':
			#ciper is i
			plaintext += 'i'
		elif c == '%' or c == '+':
			#cipher is u
			plaintext += 'u'
		else:
			plaintext += '[' + c + ']'
		

print('Plaintext: \n' + plaintext)
exit(0)
```

END
