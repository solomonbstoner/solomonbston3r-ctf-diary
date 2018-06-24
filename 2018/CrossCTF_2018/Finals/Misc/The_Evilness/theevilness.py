#!/usr/bin/env python

import sys
import flag
import signal
import os
import tempfile

temp_file = tempfile.NamedTemporaryFile(prefix="cartoon-",
                                        suffix=".dat",
                                        delete=True)


def handler(signum, frame):
    write("Times up!")
    temp_file.close()
    sys.exit(0)


def write(data, endl='\n'):
    sys.stdout.write(data + endl)
    sys.stdout.flush()


def readline():
    return sys.stdin.readline().strip()


def main():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(10)

    # Write the flag to the temp file
    temp_file.file.write(flag.flag)
    temp_file.file.flush()

    # Oh I'm sorry, did you want this?
    del flag.flag

    write(open(__file__).read())

    command = "/usr/bin/shred " + temp_file.name
    write("Here comes the shredder! (%s)" % command)

    ######################################################################
    #
    # INCOMING TRANSMISSION...
    #
    # CAREFUL AGENT. WE DO NOT HAVE MUCH TIME. I'VE OPENED A WORMHOLE IN
    # THE FABRIC OF TIME AND SPACE TO INTRODUCE A FAULT IN ONE BYTE!
    #
    # MAKE USE OF IT WISELY!
    #
    command_fault = list(command)
    index = int(readline())
    byt = int(readline(), 16)
    if (0x0 <= index < len(command_fault)):
        if (0x0 <= byt <= 0xff):
            command_fault[index] = chr(byt)
            command = "".join(command_fault)
    #
    # TRANSMISSION ENDED
    #
    ######################################################################

    # Oooh, did you want this too? Too bad it's being... shredded.
    os.system(command)


if __name__ == "__main__":
    main()
