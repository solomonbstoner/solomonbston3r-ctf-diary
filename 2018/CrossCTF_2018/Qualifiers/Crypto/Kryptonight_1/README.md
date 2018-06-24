# Kryptonight 1

## Problem

> I took a walk around the world to ease my troubled mind. 
>
> nc ctf.pwn.sg 1502 
>
> Creator - amon (@nn_amon)

## Solution

The title of this challenge is a reference to [CryptoNight](https://en.bitcoin.it/wiki/CryptoNight), a proof-of-work algorithm used by altcoins such as [Monero](https://getmonero.org/), Electroneium and Bytecoin.

When you connect to the socket, you are presented with a clue followed by a (randomly generated) challenge. The clue is of the format `[some hexadecimal string] -> [32 byte hexadecimal string]`. From the title of this challenge, we can guess that the 32 byte hexadecimal string on the RHS is the hash of the LHS, with the hash being variant 1 of the CryptoNight hash (discovered after several tries). Our implementation uses [ph4r05's py-cryptonight library](https://github.com/ph4r05/py-cryptonight).

Using the same hash algorithm on the challenge and returning it to the socket, we obtain the flag `CrossCTF{h0dl_t1l_u_d1e}`.

Also refer to [Amos Ng's write up](https://writeups.amosng.com/2018/crossctf_2018/qualifiers/crypto/kryptonight-1_775/).

### Useful links

* [Monero StackExchange](https://monero.stackexchange.com/questions/1110/where-can-i-find-a-description-of-the-cryptonight-hash-algorithm)

* [Python reimplementation of cryptonights hash function](http://www.nothisispatrik.com/2018/03/30/python-reimplementation-of-cryptonights-hash-function/)

* [Original implementation of CryptoNight's slow hash function](https://github.com/monero-project/monero/blob/master/src/crypto/slow-hash.c#L543)

* [Cryptonight (XCN)](http://cryptonite.info/)
