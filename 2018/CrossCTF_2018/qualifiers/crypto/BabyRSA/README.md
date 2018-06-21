# BabyRSA

## Problem

> Each time I asked for the flag, it gets encoded through RSA. I'm lucky I kept all those values.
>
> [output.txt](out.txt)

## Solution

Inspecing [output.txt](out.txt), we are given 2736 *sets* of RSA exponents (`e`), modulus (`n`) and ciphertexts (`c`). We also notice that the RSA exponent (`e`) is common but the modulus (`n`) and ciphertexts (`c`) are different. That is, we are given

![latex](https://latex.codecogs.com/gif.latex?e_i,%20\%20c_i,%20\%20n_i,%20\%20i%20=%201,%20\ldots,%202736)

and 

![latex](https://latex.codecogs.com/gif.latex?e_1%20=%20e_2%20=%20\ldots%20=%20e_{2736}%20=%20e)

Since the hint has implied that the plaintext (`m`) is common, we can recover the plaintext using [Hastad's Broadcast Attack](https://www.coursera.org/learn/number-theory-cryptography/lecture/fyPIB/hastads-broadcast-attack).

### Step 1: Applicaiton of the Chinese Remainder Theorem

Since the RSA modulus (`n`) are pairwise co-prime (we can verify this -- otherwise, there is an easier attack that allows us to factorize any RSA modulus to obtain the private key), we can use the [Chinese Remainder Theorem](https://brilliant.org/wiki/chinese-remainder-theorem/) to compute 

![latex](https://latex.codecogs.com/gif.latex?m%20^%20e%20\bmod%20n_1%20\cdot%20n_2%20\cdot%20\%20\ldots%20\%20\cdot%20n_e)

### Step 2: Solve for e-th root

Since the plaintext (`m`) must be less than each RSA modulus (`n`) (see [Stackexchange.com](https://crypto.stackexchange.com/questions/11904/why-does-plain-rsa-not-work-with-big-messages-mn) for why this is always true), that is,

![latex](https://latex.codecogs.com/gif.latex?m%20%3C%20n_i)

we also know that

![latex](https://latex.codecogs.com/gif.latex?m%20^%20e%20%3C%20n_1%20\cdot%20n_2%20\cdot%20\%20\ldots%20\%20\cdot%20n_e)

Hence,

![latex](https://latex.codecogs.com/gif.latex?m%20^%20e%20=%20m%20^%20e%20\bmod%20n_1%20\cdot%20n_2%20\cdot%20\%20\ldots%20\%20\cdot%20n_e)

Now, we can now compute the *e*-th root (without modulo) of our value from Step 1 to recover the plaintext (`m`). We also use the [gmpy](https://github.com/aleaxit/gmpy) library to speed up this process.

Note that we couldn't have simply computed the *n*-th root of 

![latex](https://latex.codecogs.com/gif.latex?m%20^%20e%20\bmod%20n_i)

since this is the RSA problem -- computing the *e*-th root modolu a composite number (`n`) is difficult.

## References

* https://www.quaxio.com/exploring_three_weaknesses_in_rsa/
* https://rdist.root.org/2009/10/06/why-rsa-encryption-padding-is-critical/
