# Easter Egg 1 - 676

## Challenge

> You need access into the Home Invasion network before you can solve this challenge. There is only one flag in this challenge
>  
> This is an easter egg in this one.
>  
> If you have tried for at least 30 mins and still dunno what this is about, consult facilitators.

## Solution

The easter egg is in the flashing LED strip of the smart lights device. It flashes in the format of the gif image below.

![](../../img/iot_ctf2018_easter_egg_1_flashing_lights.gif)

We used a phone to record down a video of the flashing lights for analysis. It took us a long while to figure out what the flashing lights meant. We guessed and ruled out 3 possible encodings before we finally got it.

1. We thought it could be morse code. However, the complete recording we had showed lengths of light ranging from 1 to 5, meaning there were 5 different characters. Morse code is essentially a binary, with either a "dit" or a "dat", so it does not fit.

2. We then thought it might be JSFuck. However, JSFuck uses 6 characters. It does not fit the 5 characters we saw in the video.

3. We ruled out Brainfuck too because Brainfuck uses 8 characters. 

We were told "Don't overthink it". Perhaps, each lit light represented a 1, and each unlit light represented a 0. 

We watched the video a few times and recorded the number of lit and dark lights in [easter_egg](easter_egg). This is a small excerpt from [easter_egg](easter_egg):

```
[...]
3D
2L
1D
1L
2D
1L
1D
2L
[...]
```

Let us explain what it means. `3D` means 3 '0's (off bits) and `2L` means 2 '1's (on bits). With that intepretation, the excerpt above represents `0001101001011`. 

We were lazy to analyze the file manually, so we wrote [solver.py](solver.py) to interpret it for us as described above.

Running [solver.py](solver.py) with [easter_egg](easter_egg),

```
python2 solver.py
>> msg is:
�S��X�_HI{Y0uActu4llyNotic32��
```

We obtained a jumble of characters (some unprintable) with clues of a flag in between: `HI{Y0uActu4llyNotic32`. Knowing that we are close the solution, we submitted different combinations of the flag until `HI{Y0uActu4llyNotic3d!}` was accepted.
