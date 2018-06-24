"""
Use Python 2.X only
"""

import gmpy2
import primefac # https://pypi.org/project/primefac/
import pdb
import itertools
import time
import python23_encoding

c = gmpy2.mpz(5499541793182458916572235549176816842668241174266452504513113060755436878677967801073969318886578771261808846567771826513941339489235903308596884669082743082338194484742630141310604711117885643229642732544775605225440292634865971099525895746978617397424574658645139588374017720075991171820873126258830306451326541384750806605195470098194462985494)

d = gmpy2.mpz(15664449102383123741256492823637853135125214807384742239549570131336662433268993001893338579081447660916548171028888182200587902832321164315176336792229529488626556438838274357507327295590873540152237706572328731885382033467068457038670389341764040515475556103158917133155868200492242619473451848383350924192696773958592530565397202086200003936447)

phi = gmpy2.mpz(25744472610420721576721354142700666534585707423276540379553111662924462766649397845238736588395849560582824664399879219093936415146333463826035714360316647265405615591383999147878527778914526369981160444050742606139799706884875928674153255909145624833489266194817757115584913491575124670523917871310421296173148930930573096639196103714702234087492)

start_time = time.time()
factors_ = primefac.factorint(phi)

print('[DEBUG] complete integer factorization in %f s' % (time.time() - start_time))

## parse factors into list

factors = []

for k, v in factors_.items():
    for i in range(v):
        factors.append(k)

## generate all 2-subsets of factors

indices = range(len(factors))
success = False

for i in range(len(factors)//2):
    # print('[DEBUG] inspecting subsets of size %d' % i)
    if not success:
        for p_indices in itertools.combinations(indices, i):
            p_1 = 1
            for p_ in p_indices:
                p_1 *= factors[p_]
            q_indices = set(indices) - set(p_indices)
            q_1 = 1
            for q_ in q_indices:
                q_1 *= factors[q_] # or q_1 = gmpy2.c_div(phi, p_1)
            assert p_1 * q_1 == phi
            if gmpy2.is_prime(p_1 + 1):
                if gmpy2.is_prime(q_1 + 1):
                    p = p_1 + 1
                    q = q_1 + 1
                    # print('[DEBUG] p is %s, q is %s' % (p, q))
                    N = p * q
                    # print('[DEBUG] N is %s' % N)
                    success = True
                    break

if success:

    m = pow(c, d, N)
    print('[DEBUG] flag is:\n%s' % python23_encoding.I2OSP(m))

else:

    print('[DEBUG] failed to find flag')
