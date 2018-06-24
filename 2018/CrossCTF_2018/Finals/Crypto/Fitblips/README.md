# Fitblips

## Challenge

> How many steps does your Fitblip beep?
> 
> nc ctf.pwn.sg 4003
> 
> Creator - amon (@nn_amon)
>
> [fitblips.py](fitblips.py)

## Solution

This is an easy one -- all finalists in CrossCTF 2018 solved it.

From [fitblips.py](fitblips.py), we see that the server returns a score based on the "close-ness" of our guess with the flag. We submit multiple guesses and improve our guesses based on the observed scores. Eventually, we obtain a score of 0 and the flag `CrossCTF{t1m1ng_att4ck5_r_4_th3_d3vil}`.

We test our solution [solver.py](solver_mock.py) using a mock-up based on [solver_mock.py](solver_mock.py) and [fitblips_mock.py](fitblips_mock.py).

> [OUTPUT omitted]
>
> [DEBUG] trying ord 124 (43726F73734354467B74316D316E675F61747434636B355F725F345F7468335F643376696C7C)
>
> [x] Opening connection to ctf.pwn.sg on port 4003
>
> [x] Opening connection to ctf.pwn.sg on port 4003: Trying 209.97.170.43
>
> [+] Opening connection to ctf.pwn.sg on port 4003: Done
>
> [*] Closed connection to ctf.pwn.sg port 4003
>
> [DEBUG] result = 1
>
> [DEBUG] trying ord 125 (43726F73734354467B74316D316E675F61747434636B355F725F345F7468335F643376696C7D)
>
> [x] Opening connection to ctf.pwn.sg on port 4003
>
> [x] Opening connection to ctf.pwn.sg on port 4003: Trying 209.97.170.43
>
> [+] Opening connection to ctf.pwn.sg on port 4003: Done
>
> [*] Closed connection to ctf.pwn.sg port 4003
>
> [DEBUG] result = 0
>
> [DEBUG] found one char: }
>
> [DEBUG] SOLVED: password is 43726F73734354467B74316D316E675F61747434636B355F725F345F7468335F643376696C7D
>
> [DEBUG] In plaintext, CrossCTF{t1m1ng_att4ck5_r_4_th3_d3vil}
