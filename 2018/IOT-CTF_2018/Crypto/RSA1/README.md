# RSA1

## Challenge

> RSA1 (1000)
> 
> You will need access into Home Invasion network to complete this challenge. There is only one flag in this challenge.
> 
> Sometimes IOT devices dont generate the best numbers.
> 
> nc 192.168.51.15 11001

## Solution

Interacting with the server on 192.168.51.15 and port 11001, we are given the RSA modulus (`N`) and prompted for the prime factors (`p` and `q`). 

Acting on a hunch, we try [Fermat's factorization method](https://facthacks.cr.yp.to/fermat.html) using [this Python code snippet](https://wiremask.eu/writeups/hackingweek-2015-crypto-2/) and it works! After successfully factoring several RSA moduli, we are given the flag. 

(Sorry we did not manage to capture any screenshots before the server was taken down.)
