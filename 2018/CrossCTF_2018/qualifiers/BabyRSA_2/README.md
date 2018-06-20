# BabyRSA 2

## Problem

> Each time I asked for the flag, it gets encoded through RSA.... again... I'm lucky I kept all the values... AGAIN!
> 
> [out.txt](out.txt)

## Solution

Although I didn't solve this, the write-ups that I'm not satisfied with the writeups that I've read hence I'm writing one myself.

Inspecing [output.txt](out.txt), we are given 5 *sets* of RSA exponents (`e`), modulus (`n`) and ciphertexts (`c`). We also notice that the RSA modulus (`n`) is common but the exponents (`e`) and ciphertexts (`c`) are different. That is, we are given

![latex](https://latex.codecogs.com/gif.latex?e_i,%20\%20c_i,%20\%20n_i,%20\%20i%20=%201,%20\ldots,%5)

and 

![latex](https://latex.codecogs.com/gif.latex?n_1%20=%20n_2%20=%20\ldots%20=%20n_{5}%20=%20n)

Since the hint has implied that the plaintext (`m`) is common, we can recover the plaintext using [Common Modulus Attack](https://crypto.stackexchange.com/questions/16283/how-to-use-common-modulus-attack). We calculate the GCD of different combinations of `e` (e.g., using [this method](https://www.geeksforgeeks.org/gcd-two-array-numbers/)) until we find that

![latex](https://latex.codecogs.com/gif.latex?gcd%28e_1,&space;e_2,&space;e_3,&space;e_4,&space;e_5%29%3D1)

Applying the [Extended Euclidean Algorithm repeatedly](https://math.stackexchange.com/questions/735093/method-of-solving-extended-euclidean-algorithm-for-three-numbers), we can find the Bezout coefficients (that are not unique) such that

![latex](https://latex.codecogs.com/gif.latex?%5Calpha_1%5Ccdot%5C;e_1%2B%5Calpha_2%5Ccdot%5C;e_2%2B%5Calpha_3%5Ccdot%5C;e_3%2B%5Calpha_4%5Ccdot%5C;e_4%2B%5Calpha_5%5Ccdot%5C;e_5%3Dgcd%28e_1,&space;e_2,&space;e_3,&space;e_4,&space;e_5%29%3D1)

According to the rules of modular arithmetic,

![latex](https://latex.codecogs.com/gif.latex?%5Cleft%28%5Cleft%28c_1%20%5Cright%20%29%5E%7B%5Calpha_1%7D%20%5Cpmod%20n%20%5Cright%29%20%5Ccdot%20%5Cleft%28%5Cleft%28c_2%20%5Cright%20%29%5E%7B%5Calpha_2%7D%20%5Cpmod%20n%20%5Cright%29%20%5Ccdots%20%5Cleft%28%5Cleft%28c_5%20%5Cright%20%29%5E%7B%5Calpha_5%7D%20%5Cpmod%20n%20%5Cright%29%20%5C%5C%20%3D%20%5Cleft%28%5Cleft%28m%5E%7Be_1%7D%20%5Cright%20%29%5E%7B%5Calpha_1%7D%20%5Cpmod%20n%20%5Cright%29%20%5Ccdot%20%5Cleft%28%5Cleft%28m%5E%7Be_2%7D%20%5Cright%20%29%5E%7B%5Calpha_2%7D%20%5Cpmod%20n%20%5Cright%29%20%5Ccdots%20%5Cleft%28%5Cleft%28m%5E%7Be_5%7D%20%5Cright%20%29%5E%7B%5Calpha_5%7D%20%5Cpmod%20n%20%5Cright%29%20%5C%5C%20%3D%20m%5E%7Be_1%20%5Calpha_1%20&plus;%20e_2%20%5Calpha_2%20&plus;%20%5Ccdots%20&plus;%20e_5%20%5Calpha_5%7D%20%5Cpmod%20n%20%5C%5C%20%3D%20m%5E1%20%5Cpmod%20n)

However, we have to be careful if the Bezout coefficient is negative, since we cannot compute

![latex](https://latex.codecogs.com/gif.latex?%5Cleft%28c_i%20%5Cright%20%29%5E%7B%5Calpha_1%7D%20%5Cpmod%20n%20%5Cqquad%20%5Ctext%7Bif%7D%20%5Cqquad%20%5Calpha_i%20%3C%200)

Instead we compute

![latex](https://latex.codecogs.com/gif.latex?%5Cleft%28c_i%20%5Cright%20%29%5E%7B%5Calpha_1%7D%20%5Cpmod%20n%20%5C%5C%20%3D%20m%5E%7Be_i%20%5Calpha_i%7D%20%5Cpmod%20n%20%5C%5C%20%3D%20%5Cleft%28%20m%5E%7B-e_i%7D%5Cright%20%29%5E%7B-%5Calpha_i%7D%20%5Cpmod%20n%20%5C%5C%20%3D%20%5Cleft%28%20m%5E%7B-e_i%7D%20%5Cpmod%20n%20%5Cright%29%20%5E%7B-%5Calpha_i%7D%20%5Cpmod%20n%20%5Cqquad%20%5Ctext%7Bif%7D%20%5Cqquad%20%5Calpha_i%20%3C%200)

where 

![latex](https://latex.codecogs.com/gif.latex?m%5E%7B-e_i%7D%20%5Cpmod%20n)

is the modular inverse of

![latex](https://latex.codecogs.com/gif.latex?m%5E%7Be_i%7D%20%5Cpmod%20n)

and can be computed using the Extended Euclidean Algorithm.
