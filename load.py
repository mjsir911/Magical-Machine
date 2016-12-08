#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

__appname__     = ""
__author__      = "Marco Sirabella"
__copyright__   = ""
__credits__     = ["Marco Sirabella"]  # Authors and bug reporters
__license__     = "GPL"
__version__     = "1.0"
__maintainers__ = "Marco Sirabella"
__email__       = "msirabel@gmail.com"
__status__      = "Prototype"  # "Prototype", "Development" or "Production"
__module__      = ""

halt = 0b000000

arch = 4

ram = [(halt, 0b00)] * arch ** 2

def load(filename):
    file = open(filename, 'r')
    contents = file.read()
    begin = True
    for line in contents.splitlines():
        words = line.split()
        #print(words[0] + ' : ' + words[1])
        addr = int(words[0], 2)
        data = words[1]
        assert len(data) == arch*2
        instruction = int(data[:arch], 2)
        pointer     = int(data[arch:], 2)
        data = (instruction, pointer)

        ram[addr] = data


def main():
    load(sys.argv[1])

    print(ram)


if __name__ == '__main__':
    main()
