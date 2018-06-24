# BabyRSA3

## Challenge

> So I heard that you can flip the private and public information for RSA...
> 
> Creator - prokarius (@prokarius)
>
> [outNerfed.txt](outNerfed.txt)

## Solution

*We didn't solve this challenge and this writeup is inspired by the write-ups at the end of this document.*

From [outNerfed.txt](outNerfed.txt), we are given the RSA ciphertext (`c`), private key/exponent (`d`) and the Euler totient function (`phi`). We are unable to decrypt the ciphertext because we are missing the RSA modulus (`N`):

![latex](http://latex.codecogs.com/gif.latex?N%20%3D%20p%20%5Ccdot%20q)

If we are able to factor the Euler totient function, we can recover the prime factors (`p` and `q`) and reconstruct the RSA modulus:

![latex](http://latex.codecogs.com/gif.latex?\phi%28N%29&space;=&space;%28p-1%29%28q-1%29)

We use [Primefac](https://pypi.org/project/primefac/) (or [Yafu](https://sourceforge.net/projects/yafu/)) to factorize `phi`, but further investigation is required to recover `p` and `q`:

```
>>> primefac.factorint(phi)
{mpz(2767687179787): 1, 2: 2, mpz(3680247726403): 1, mpz(1973804930501): 1, mpz(6060693342503): 1, mpz(9566431650679): 1, mpz(3639128890921): 1, mpz(333600482773): 1, mpz(8313722160551): 1, mpz(4754509728797): 1, mpz(6938103821809): 1, mpz(7230980905199): 1, mpz(9220079755217): 1, mpz(2293498615990071511610820895302086940796564989168281123737588839386922876088484808070018553110125686555051L): 1, mpz(7265658595571): 1, mpz(6672422609813): 1, mpz(4065711354007): 1, mpz(1984419944251): 1, mpz(6438418759151): 1, mpz(6545600536253): 1, mpz(6579600728639): 1}
>>>
```

We try to split the factors of `phi` in different ways to guess `p-1` and `q-1` -- we know our guesses are correct when `p` and `q` are *both* prime.

Using `p` and `q`, we recover `N` and decrypt the message using

![latex](https://latex.codecogs.com/gif.latex?m%20%3D%20c%20%5E%20d%20%5Cpmod%20N)

to get the flag `CrossCTF{Pub7ic_prIv4te_K3ys_4_R5A_t33ns}`.

```
[DEBUG] complete integer factorization in 28.652856 s
[DEBUG] flag is:
CrossCTF{Pub7ic_prIv4te_K3ys_4_R5A_t33ns}slightlylessshittypaddingslightlylessshittypaddingslightlylessshittypaddingslightlylessshittypadding
```

## Other writeups

* [NUS OSI Layer 8 writeup](https://osilayer8.cf/crossctf-finals2018/crypto/babyrsa3/README/)
