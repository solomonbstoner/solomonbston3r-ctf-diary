"""
Each time I asked for the flag, it gets encoded through RSA. I'm lucky I kept all those values.


See https://www.quaxio.com/exploring_three_weaknesses_in_rsa/
https://rdist.root.org/2009/10/06/why-rsa-encryption-padding-is-critical/
"""

import auxilliary2

### process file

FILENAME = 'out.txt'

count = 0
triplet = {}
triplets = []
with open(FILENAME, 'r') as f:
    for line in f:
        if line != ' \n':
            tmp = line.split(' ')
            triplet[tmp[0]] = int(tmp[2])
        else:
            triplets.append(triplet)
            triplet = {}

### verify

for triplet in triplets:
    if len(triplet) != 3 or 'c' not in triplet or 'e' not in triplet or 'n' not in triplet:
        print('>> error!')

### analysis

# extract patterns

ns = []
cs = []

for triplet in triplets:
    ns.append(triplet['n'])
    cs.append(triplet['c'])

e = triplet['e']

# perform CRT

print(">> calculating CRT")

crt = auxilliary2.chinese_remainder(ns[:e], cs[:e])

print(">> calculating i-th root")

r = auxilliary2.nthroot(e, crt)

print(">> converting to string")

sol = auxilliary2.I2OSP(r)

print(">> flag is %s" % sol)
