# For Coincidence or Conspiracy in The Mathematics of Secrets

In page 31 of The Mathematics of Secrets, Eve intercepted the following ciphertext sent by Alice to decipher. Alice has removed the spaces from her plaintext and divided it up into 5-letter groups in order to make things harder for Eve by obscuring any short, common words.
```
QBVDL WXTEQ GXOKT NGZJQ GKXST RQLYR
XJYGJ NALRX OTQLS LRKJQ FJYGJ NGXLK
QLYUZ GJSXQ GXSLQ XNQXL VXKOJ DVJNN
BTKJZ BKPXU LYUNZ XLQXU JYQGX NTYQG
XKXQJ KXULK QJNQN LQBYL OLKKX SJYQG
XNGLU XRSBN XOFUL YDSXU GJNSX DNVTY
RGXUG JNLEE SXLYU ESLYY XUQGX NSLTD
GQXKB AVBKX JYYBR XYQNQ GXKXZ LNYBS
LRPBA VLQXK JLSOB FNGLE EXYXU LSBYD
XWXKF SJQQS XZGJS XQGXF RLVXQ BMXXK
OTQKX VLJYX UQBZG JQXZL NG
```

### Monographic or polygraphic cipher?

Before this challenge is issued, the book introduces 3 different types of ciphers - monographic affine ciphers, polygraphic Hill ciphers, and homophonic ciphers. Each has a different method to solving it. How does Eve tell which type of cipher this is? Eve starts by getting information on the letter frequencies in the ciphertext. The Python script below does that.

```
ciphertext = """
QBVDL WXTEQ GXOKT NGZJQ GKXST RQLYR
XJYGJ NALRX OTQLS LRKJQ FJYGJ NGXLK
QLYUZ GJSXQ GXSLQ XNQXL VXKOJ DVJNN
BTKJZ BKPXU LYUNZ XLQXU JYQGX NTYQG
XKXQJ KXULK QJNQN LQBYL OLKKX SJYQG
XNGLU XRSBN XOFUL YDSXU GJNSX DNVTY
RGXUG JNLEE SXLYU ESLYY XUQGX NSLTD
GQXKB AVBKX JYYBR XYQNQ GXKXZ LNYBS
LRPBA VLQXK JLSOB FNGLE EXYXU LSBYD
XWXKF SJQQS XZGJS XQGXF RLVXQ BMXXK
OTQKX VLJYX UQBZG JQXZL NG
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

print ("\nAnalysis of individual letters:")
print ("-------------------------------")


for c in cipher_frequency:
	percentage_frequency = cipher_frequency[c] / total_num_of_chars * 100.00
	print("%s :	%d	:	%f%%" % (c, cipher_frequency[c], percentage_frequency ))

print ("-------------------------------")
```

Running the script gives Eve the following results. It is similar to the one in page 33 of the book.
```
$ python frequency_analysis.py 
Total number of characters : 322

Analysis of individual letters:
-------------------------------
Q :	30	:	9.316770%
B :	14	:	4.347826%
V :	8	:	2.484472%
D :	6	:	1.863354%
L :	30	:	9.316770%
W :	2	:	0.621118%
X :	47	:	14.596273%
T :	9	:	2.795031%
E :	6	:	1.863354%
G :	23	:	7.142857%
O :	7	:	2.173913%
K :	19	:	5.900621%
N :	20	:	6.211180%
Z :	8	:	2.484472%
J :	22	:	6.832298%
S :	17	:	5.279503%
R :	9	:	2.795031%
Y :	21	:	6.521739%
A :	3	:	0.931677%
F :	5	:	1.552795%
U :	13	:	4.037267%
P :	2	:	0.621118%
M :	1	:	0.310559%
-------------------------------
```

Eve notices that there are 2 high-frequency letters, X and Q. This rules out the ciphertext as a homophonic cipher.

> If homophones were being used, we would expect to see more low-frequency letters and fewer(if any) high frequency ones.
>  
> -- *The Mathematics of Secrets pg 32*

Another way to determine the type of the cipher is to use Friedman's Index of Coincidence.

> In other words, the index of coincidence of actual English text is about .066, or 6.6%. The first thing Friedman realized is that this number won't change if you apply a simple substitution cipher to the text - the order in which the numbers are added will change, but the total won't. So if our ciphertext was encrypted with a simple substitution cipher, we would expect the index of coincidence to be about .066, and if the cipher had homophones, we would expect it to be substantially different.
> 
> -- *The Mathematics of Secrets pg 35*

Eve adds the following code to the script above to analyse the text's Index of Coincidence.
```
def index_of_coincidence():
	probability_of_coincidence = 0.0
	for c in cipher_frequency:
		probability_of_coincidence += (cipher_frequency[c] / total_num_of_chars) * (cipher_frequency[c] - 1) / (total_num_of_chars - 1)
		print("Index of coincidence for %s : %d/%d * %d/%d" % (c, cipher_frequency[c], total_num_of_chars, cipher_frequency[c] - 1, total_num_of_chars - 1))
	return probability_of_coincidence

[...]

print ("Index of coincidence : %f" % index_of_coincidence())
print ("-------------------------------")
```

```
Analysing Index of coincidence of the cipher :
-------------------------------
Index of coincidence for Q : 30/322 * 29/321
Index of coincidence for B : 14/322 * 13/321
Index of coincidence for V : 8/322 * 7/321
Index of coincidence for D : 6/322 * 5/321
Index of coincidence for L : 30/322 * 29/321
Index of coincidence for W : 2/322 * 1/321
Index of coincidence for X : 47/322 * 46/321
Index of coincidence for T : 9/322 * 8/321
Index of coincidence for E : 6/322 * 5/321
Index of coincidence for G : 23/322 * 22/321
Index of coincidence for O : 7/322 * 6/321
Index of coincidence for K : 19/322 * 18/321
Index of coincidence for N : 20/322 * 19/321
Index of coincidence for Z : 8/322 * 7/321
Index of coincidence for J : 22/322 * 21/321
Index of coincidence for S : 17/322 * 16/321
Index of coincidence for R : 9/322 * 8/321
Index of coincidence for Y : 21/322 * 20/321
Index of coincidence for A : 3/322 * 2/321
Index of coincidence for F : 5/322 * 4/321
Index of coincidence for U : 13/322 * 12/321
Index of coincidence for P : 2/322 * 1/321
Index of coincidence for M : 1/322 * 0/321
Index of coincidence : 0.067820
-------------------------------
```

The index of coincidence of the cipher text is 0.067820. It is very close to the index of coincidence of actual English text, which is 0.066. Hence, Eve concludes that the cipher is an affine cipher.

### Solving for the keys k & m.

According to the Phi test (see page 35 of The Mathematics of Secrets), Eve determined that it is highly probable that the ciphertext Eve intercepted is an affine cipher. Since it is monographic, Eve knows the plaintext was encrypted using the following formula: `C ≡ kP + m (mod 26)`.

> The general form of this method for solving a system of several equations in the same number of unknowns is usually known as Cramer's rule
>  
> -- *The Mathematics of Secrets pg 23*

By Cramer's Rule, Eve needs just 2 equations to solve these 2 unknowns `k` and `m`. That means Eve only needs to find out which 2 cipher alphabets correspond to which 2 plaintext alphabets. Since Eve does not have the plaintext, Eve can't carry out the known-plaintext attack. Thus, Eve uses frequency analysis.

> A very effective way of breaking simple substitution ciphers is called letter frequency analysis. [...] The idea is simply that some letters in English, Arabic, or any other human language are used more often than others.
>  
> -- *The Mathematics of Secrets pg 18*

Eve compares the percentage frequency of the cipher text to that of English text. The source of the English text percentage text is [this](https://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html).

| English Letter | Percentage frequency in English text | Cipher Letter | Percentage frequency in cipher text |
| --- | --- | --- | --- |
| E | 12.02 | X | 14.6 | 
| T | 9.10 | Q | 9.31 |
| A | 8.12 | L | 9.31 |

Eve knows it is highly likely that X is the cipher substitution of E, and either Q or L is the cipher substitution of T. The only way to know which is to calculate the value of `k` and `m`. One of the 2 guesses are wrong. I shall give show the case where Eve makes the right guess first. I will show the case where Eve makes the wrong guess later.

### X = E, Q = T (Correct guess)

Eve substitutes the letters with their respective integers, and arrives at equations 1 & 2.
```
E = 4
Q = 16
T = 19
X = 23
```

Eqn 1 --> `16 ≡ 19k + m (mod 26)`
Eqn 2 --> `23 ≡ 4k + m (mod 26)`

```
Eqn 3 = Eqn 2 - Eqn 1
 
7 ≡ -15k (mod 26)
7 ≡ 11k (mod 26) --> Eqn 3
```
To solve for `k`, Eve needs to find the multiplicative inverse of 11. Let it be `x∈ ℕ +` such that `1 ≡ 11x (mod 26)`. Eve uses the [extended Euclidean algorithm](https://brilliant.org/wiki/extended-euclidean-algorithm/) to solve for `x`.

> You might be wondering why we are bothering with Euclid’s algorithm instead of just factoring the numbers and looking for prime factors in common. There are two answers to that question: First, we will eventually see that this algorithm is faster than factoring for large numbers. Second, once we have done the Euclidean algorithm, we can do a neat little trick to get (the multiplicative inverse of) 3.
>  
> -- *The Mathematics of Secrets pg 13*

For 11 to have a multiplicative inverse, the values 26 and 11 must be coprime. Using the Euclidean Algorithm, Eve confirms that indeed they are. 
```
Dividend = Quotient(Divisor) + Remainder
26 = 2(11) + 4
11 = 4(2) + 3
4 = 3(1) + 1
```

On a side note, the values depend on your guess from the letter frequencies. If the values are not coprime, it means that your equation may have no solutions or more than 1 solution. It's about luck, and trial and error.

> If there are no solutions, it means in this case that Eve probably made a bad guess from the letter frequencies and she should try again.
>  
> -- *The Mathematics of Secrets pg 19*

Since 26 and 11 are coprime, Eve knows she is on the right track. Eve expresses the remainder as the subject of the 3 equations below.
```
Remainder = Dividend - Quotient(Divisor)
1 = 4 - 3(1)
3 = 11 - 4(2)
4 = 26 - 2(11)
```
```
1 = 4 - 3(1)
1 = 4 - 11 + 4(2)
  = 4(3) - 11
  = 4(11) - 4(4)(2) - 11
  = 3(11) - 8(4)
  = 3(11) - 8(26) + 2(8)(11)
  = 19(11) - 8(26)
1 ≡ 11(19) (mod 26)
```
Therefore, `x=19`.

```
Substituting x=19 into Eqn 3

k ≡ 7(19) (mod 26)
  ≡ 3 (mod 26)

Since k = 3, 
4(3) + m ≡ 23 (mod 26) 
m ≡ 11 (mod 26)
```

Therefore, `k=3, m=11`. To convert the ciphertext to plaintext, Eve finds the multiplicative inverse of `k mod 26`.

```
C ≡ kP + m (mod 26)
C - m ≡ kP (mod 26)
(C - m)k_inverse ≡ P (mod 26), where 1 ≡ k_inverse(k) (mod 26)
```

Eve created a Python script to decrypt the ciphertext. Take note that at this point, Eve arrived at a *possible* pair of keys. It's not a guarantee that it'll work. The only way to tell is to test it out.
```
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
QBVDL WXTEQ GXOKT NGZJQ GKXST RQLYR
XJYGJ NALRX OTQLS LRKJQ FJYGJ NGXLK
QLYUZ GJSXQ GXSLQ XNQXL VXKOJ DVJNN
BTKJZ BKPXU LYUNZ XLQXU JYQGX NTYQG
XKXQJ KXULK QJNQN LQBYL OLKKX SJYQG
XNGLU XRSBN XOFUL YDSXU GJNSX DNVTY
RGXUG JNLEE SXLYU ESLYY XUQGX NSLTD
GQXKB AVBKX JYYBR XYQNQ GXKXZ LNYBS
LRPBA VLQXK JLSOB FNGLE EXYXU LSBYD
XWXKF SJQQS XZGJS XQGXF RLVXQ BMXXK
OTQKX VLJYX UQBZG JQXZL NG
"""
plaintext = ""

k = int(sys.argv[1])
m = int(sys.argv[2])

ciphertext = ciphertext.replace(" ","").replace("\n","")   # Remove whitespaces

print('Ciphertext: \n' + ciphertext)
print('\n')

k_inverse = mulinv(k, 26)


for c in ciphertext:
	print("-----------------")
	print("Cipher: " + c)
	c = c.upper()
	c = ord(c) - ord('A')		# Converts 'A'=0, 'B'=1... 'Z'=25
	p = k_inverse * ( c - m )
	p = p % 26
	print("%d ≡ %d * (%d - %d) (mod 26)" % (p, k_inverse, c, m))
	p = chr(p + ord('A'))		# Converts 0='A', 1='B'... 25='Z'
	print("Plaintext: " + p)
	print("-----------------")
	plaintext += p

print('Plaintext: \n' + plaintext)
exit(0)
```



### Successful decryption

Eve runs the Python script above, and successfully decrypts the cipher.
```
$ python solve.py 3 11
Ciphertext: 
QBVDLWXTEQGXOKTNGZJQGKXSTRQLYRXJYGJNALRXOTQLSLRKJQFJYGJNGXLKQLYUZGJSXQGXSLQXNQXLVXKOJDVJNNBTKJZBKPXULYUNZXLQXUJYQGXNTYQGXKXQJKXULKQJNQNLQBYLOLKKXSJYQGXNGLUXRSBNXOFULYDSXUGJNSXDNVTYRGXUGJNLEESXLYUESLYYXUQGXNSLTDGQXKBAVBKXJYYBRXYQNQGXKXZLNYBSLRPBAVLQXKJLSOBFNGLEEXYXULSBYDXWXKFSJQQSXZGJSXQGXFRLVXQBMXXKOTQKXVLJYXUQBZGJQXZLNG


-----------------
Cipher: Q
19 ≡ 9 * (16 - 11) (mod 26)
Plaintext: T
-----------------
-----------------
Cipher: B
14 ≡ 9 * (1 - 11) (mod 26)
Plaintext: O
-----------------
-----------------
Cipher: V
12 ≡ 9 * (21 - 11) (mod 26)
Plaintext: M
-----------------

[...]

Plaintext: 
TOMGAVEUPTHEBRUSHWITHRELUCTANCEINHISFACEBUTALACRITYINHISHEARTANDWHILETHELATESTEAMERBIGMISSOURIWORKEDANDSWEATEDINTHESUNTHERETIREDARTISTSATONABARRELINTHESHADECLOSEBYDANGLEDHISLEGSMUNCHEDHISAPPLEANDPLANNEDTHESLAUGHTEROFMOREINNOCENTSTHEREWASNOLACKOFMATERIALBOYSHAPPENEDALONGEVERYLITTLEWHILETHEYCAMETOJEERBUTREMAINEDTOWHITEWASH
```
Since the plaintext is in legible English, Eve knows her keys `k` and `m` are correct. But it is not easy to read. So, let's manually add the spaces back into the plaintext. It turns out to be an extract from "The Adventures of Tom Sawyer".

> TOM GAVE UP THE BRUSH WITH RELUCTANCE IN HIS FACE BUT ALACRITY IN HIS HEART AND WHILE THE LATE STEAMER BIG MISSOURI WORKED AND SWEATED IN THE SUN THERE TIRED ARTIST SAT ON A BARREL IN THE SHADE CLOSE BY DANGLED HIS LEGS MUNCHED HIS APPLE AND PLANNED THE SLAUGHTER OF MORE INNOCENTS THERE WAS NO LACK OF MATERIAL BOYS HAPPENED ALONG EVERY LITTLE WHILE THEY CAME TO JEER BUT REMAINED TO WHITEWASH.


### X = E, L = T (Wrong guess)

As promised earlier, I would show an example where Eve made a wrong guess. Eve substitutes the letters with their respective integers, and arrives at equations 1 & 2.
```
E = 4
L = 11
T = 19
X = 23
```

Eqn 1 --> `11 ≡ 19k + m (mod 26)`
Eqn 2 --> `23 ≡ 4k + m (mod 26)`

```
Eqn 3 = Eqn 2 - Eqn 1
 
12 ≡ -15k (mod 26)
12 ≡ 11k (mod 26) --> Eqn 3

Since 1 ≡ 19(11) (mod 26),
therefore 12(19) ≡ k (mod 26)
k ≡ 20 (mod 26) --> Eqn 4

Substituting Eqn 4 into Eqn 2,
11 ≡ 19(20) + m (mod 26)
m ≡ 11 - 19(20) (mod 26)
m ≡  21 (mod 26)
```

Eve tries to decrypt the cipher with the keys `k=20, m=21`. She tries to use the Python script from earlier, but she gets an error!
```
$ python solve.py 20 21
Ciphertext: 
QBVDLWXTEQGXOKTNGZJQGKXSTRQLYRXJYGJNALRXOTQLSLRKJQFJYGJNGXLKQLYUZGJSXQGXSLQXNQXLVXKOJDVJNNBTKJZBKPXULYUNZXLQXUJYQGXNTYQGXKXQJKXULKQJNQNLQBYLOLKKXSJYQGXNGLUXRSBNXOFULYDSXUGJNSXDNVTYRGXUGJNLEESXLYUESLYYXUQGXNSLTDGQXKBAVBKXJYYBRXYQNQGXKXZLNYBSLRPBAVLQXKJLSOBFNGLEEXYXULSBYDXWXKFSJQQSXZGJSXQGXFRLVXQBMXXKOTQKXVLJYXUQBZGJQXZLNG


-----------------
Cipher: Q
Traceback (most recent call last):
  File "solve.py", line 51, in <module>
    p = k_inverse * ( c - m )
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
```

"Why?" she wonders. She realises that it is because the value of `k` and 26 are *not* coprime. That means there is no `k_inverse` to decrypt the cipher. The value 20 is a *bad* key.

> Remember that to decipher a message, you need to do the opposite from enciphering it. [...] If k is the key to a multiplicative cipher, can we be sure k_inverse exists? [...] We discovered that these bad keys are 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, and...
>  
> -- *The Mathematics of Secrets pg 10 to 12*

Eve knows that L is not the cipher substitution for T. That leaves Q as the only cipher substitution for T.

END

