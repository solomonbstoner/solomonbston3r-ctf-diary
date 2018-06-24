"""
Solution from https://writeups.amosng.com/2018/crossctf_2018/qualifiers/crypto/babyrsa-2_951/ but no idea how it works.
"""

import auxilliary2
import gmpy2

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

# extract patterns

cs = []
es = []

for triplet in triplets:
    cs.append(triplet['c'])
    es.append(triplet['e'])

n = triplet['n'] # same throughout

###

sum_e = sum(es)
x = gmpy2.invert(es[0], sum_e) # GCD of 1
mul_c = cs[0] * cs[1] * cs[2] * cs[3] * cs[4]
inversed = gmpy2.invert(mul_c, n)
res = int(pow(inversed, int((x * es[0]) / sum_e), n) * pow(cs[0], x, n)) % n

flag = auxilliary2.I2OSP(res)

print(">> flag is:\n%s" % flag)

