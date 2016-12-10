#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import computer
from random import randint

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

x = computer.CPU(8)

def run(num):
    for n in range(num):
        x.fetch()
        #print(x.iReg)
        x.exec()

for word in x.ram:
    word.bits = randint(0, 2 ** 8)

x.ram[0].bits = randint(0,255)
run(1)
#try: run(1)
#except e: 'NOP is not working correctly : {}'.format(e)

x.ram[1].bits = 0b0000010000000000
run(1)
assert x.ram[0].bits == x.registers[0].bits, (
    '{}, {}'.format(x.ram[0].bits, x.registers[0].bits))

x.ram[2].bits = 0b0000100000000001
run(1)
assert x.registers[0].bits == x.ram[1].bits, (
    '{}, {}'.format(x.ram[0].bits, x.registers[0].bits))

x.ram[3].bits = 0b0000110011111111
run(1)
assert x.ram[0].bits + x.ram[255].bits == x.registers[0].bits, (
    '{}, {}'.format(x.ram[0].bits, x.registers[0].bits))

x.ram[4].bits = 0b0001000011111111
run(1)
assert x.ram[0].bits == x.registers[0].bits, (
    '{}, {}'.format(x.ram[0].bits, x.registers[0].bits))

x.ram[5].bits = 0b0001010011111111
run(1)
assert x.ram[0].bits * x.ram[255].bits == x.registers[0].bits, (
    '{}, {}'.format(x.ram[0].bits, x.registers[0].bits))

x.ram[6].bits = 0b0001100011111111
run(1)
assert x.ram[0].bits == x.registers[0].bits, (
    '{}, {}'.format(x.ram[0].bits, x.registers[0].bits))
