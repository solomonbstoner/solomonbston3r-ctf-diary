# RSA2 - 676

## Challenge

>You will need access into Home Invasion network to complete this challenge. There is only one flag in this challenge.
>
>Sometimes IOT devices dont send their best numbers.
>
>nc 192.168.51.15 11003

## Solution

Interacting with the server on 192.168.51.15 and port 11003, we are given a pair of RSA moduli (`N1` and `N2`) and prompted for their prime factors (`p1` and `q1`, `p2` and `q2`).

The presentation of a pair of RSA moduli is a hint that they are vulnerable to the [Common Factor Attack](http://www.loyalty.org/~schoen/rsa/). We simpy calculate the GCD of `N1` and `N2`, and if the result is greater than 1 then the result is also a common prime factor of `N1` and `N2`. 

Using this method, we successfully factored several pairs of RSA moduli and we are given the flag `HI{W3ak_K3y_G3n3r4t10n_2149uf14f94dgs0}`.

(Sorry we did not manage to capture any screenshots before the server was taken down.)
