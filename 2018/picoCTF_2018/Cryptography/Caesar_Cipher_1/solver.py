clue = 'payzgmuujurjigkygxiovnkxlcgihubb'

for i in range(26):
    cand = ''
    for c in clue:
        cand += chr(0x61 + (ord(c.lower()) + i - 0x61) % 26)

    print('Shift %d: %s' % (i, cand))
