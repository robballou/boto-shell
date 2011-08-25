#!/usr/bin/env python
from botoshell import BotoShell

if __name__ == '__main__':
    b = BotoShell()
    try:
        b.cmdloop()
    except KeyboardInterrupt, e:
        print ""