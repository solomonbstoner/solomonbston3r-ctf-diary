"""
Hint: Each time I asked for the flag, it gets encoded through RSA.... again... I'm lucky I kept all those values... AGAIN!

This time n is repeated, but c and e are unique.
"""

import auxilliary2
import fractions
import pdb

### process file

FILENAME = 'out.txt'

count = 0
triplet = {}
triplets = []
with open(FILENAME, 'r') as f:
    for line in f:
        if line.strip():
            tmp = line.split(' ')
            triplet[tmp[0]] = int(tmp[2])
        else:
            triplets.append(triplet)
            triplet = {}
    triplets.append(triplet)

### verify

for triplet in triplets:
    if len(triplet) != 3 or 'c' not in triplet or 'e' not in triplet or 'n' not in triplet:
        raise Exception('Processing error!')

# extract patterns

cs = []
es = []

for triplet in triplets:
    cs.append(triplet['c'])
    es.append(triplet['e'])

n = triplet['n'] # same throughout

### we need GCD of 1

for i in range(1,len(triplets)):
    gcd = auxilliary2.xgcd(es[:i+1])
    if gcd == 1:
        print(">> found! GCD of %s is %s" % (es[:i+1], gcd))
        break

### compute coefs

coefs = auxilliary2.calculateBezoutCoefficients(es)

### verify solution

check = 0
for i in range(len(coefs)):
    check += es[i] * coefs[i]

if check != 1:
    raise Exception('Wrong coefficients')

res = 1
for i in range(len(coefs)):
    if coefs[i] > 0:
        res *= pow(cs[i], coefs[i], n)
    else:
        # see https://stackoverflow.com/questions/34119110/negative-power-in-modular-pow for hint on dealing with negative exponents
        res *= pow(auxilliary2.mul_inv(cs[i], n), -coefs[i], n)
res = res % n

flag = auxilliary2.I2OSP(res)

print(">> flag is %s" % flag)
