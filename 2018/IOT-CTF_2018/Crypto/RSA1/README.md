# RSA1 - 559

## Challenge
 
> You will need access into Home Invasion network to complete this challenge. There is only one flag in this challenge.
> 
> Sometimes IOT devices dont generate the best numbers.
> 
> nc 192.168.51.15 11001

## Solution

Interacting with the server on 192.168.51.15 and port 11001, we are given the RSA modulus (`N`) and prompted for the prime factors (`p` and `q`):

```
N = ... [OUTPUT OMITTED]
p?
q?
```

Based on the challenge's hint, we suspect that `N` (and its factors) is poorly generated. Since `N` is large (~1024 bits) and we have no other clues, we cannot try to factorize `N` using "brute-force" but instead look at short-cuts that exploit the weakness in the number generation process discussed in [this paper](https://eprint.iacr.org/2015/398.pdf).

First, we search [factordb.com](https://factordb.com/) for records on `N`, which turns out to be a deadend.

Next, we try [Fermat's factorization method](https://facthacks.cr.yp.to/fermat.html) that factorizes `N` efficient if `p` and `q` share half of their leading bits. Using [this Python code snippet](https://wiremask.eu/writeups/hackingweek-2015-crypto-2/), we successfully factorize `N`. Alternatively, you can feed `N` to the [Prime Factorization Machine](http://mathsolutions.50webs.com/primefactor.html).

After successfully factoring several `N`s, we are given the flag. 

(Sorry we did not manage to capture any screenshots before the server was taken down.)
