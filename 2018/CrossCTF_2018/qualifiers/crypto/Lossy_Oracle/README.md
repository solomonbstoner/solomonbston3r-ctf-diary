# LossyORacle

## Problem

> No one believes I can recover the message from this crappy ORacle.
> 
> nc ctf.pwn.sg 1401
> 
> Creator - prokarius (@prokarius)

The oracle runs the script [lossyoracle.py](lossyoracle.py).

## Solution

Inspecting script [lossyoracle.py](lossyoracle.py), we see that the oracle returns the result of an OR operation with a flag and a randomly generated string of bytes.

As we probe the oracle, we inspect each bit of the result and use the following property of bitwise operation to aid our analysis:
* If the bit returned is 0, we know that flag the bit is definitely 0.
* If the bit returned is 1, there's a chance that the flag bit is actually 0 but OR-ed with 1 (random bit).

After repeating this probing process many times, we grow increasingly confident that our guess is correct and stop once we have completed 20 experiments.

Checking the filetype of the resultant flag (which has a size of 14 kB, too large to be a text file), we find that it is a MPEG file. We play the file to reveal an audio recording of the flag.
