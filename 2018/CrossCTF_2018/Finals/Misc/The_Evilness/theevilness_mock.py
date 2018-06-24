#!/usr/bin/env python

import sys
flag = 'A'
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
    global flag
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(10) # 10 seconds

    # Write the flag to the temp file
    temp_file.file.write(flag)
    temp_file.file.flush()

    # Oh I'm sorry, did you want this?
    del flag

    write(open(__file__).read())

    command = "/usr/bin/shred " + temp_file.name # replaced
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
    print('[DEBUG] command_fault is %s' % command_fault)
    index = int(readline())
    byt = int(readline(), 16)
    print('[DEBUG] index is %s, byt is %s' % (index, byt))
    if (0x0 <= index < len(command_fault)):
        print('[DEBUG] index is valid')
        if (0x0 <= byt <= 0xff):
            print('[DEBUG] byt is valid: %s'% chr(byt))
            command_fault[index] = chr(byt)
            command = "".join(command_fault)
            print('[DEBUG] resultant command is %s' % command)
    #
    # TRANSMISSION ENDED
    #
    ######################################################################

    # Oooh, did you want this too? Too bad it's being... shredded.
    print('[DEBUG] executing command %s' % command)
    # os.system(command) # potentially dangerous


if __name__ == "__main__":
    main()
