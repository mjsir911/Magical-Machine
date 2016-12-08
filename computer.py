#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

class Word:
    def __init__(self, arch, bits=0b0000):
        self.arch = arch
        self._bits = bits # Our full data as an integer

    @property
    def bits(self):
        return self._bits

    @bits.setter
    def bits(self, bits):
        assert bits < self.arch ** 4
        self._bits = bits

    @property
    def inst(self):#or instruction?
        """Return first half(instruction) of data as an integer"""
        return int(format(self.bits, '0{}b'.format(self.arch * 2))[:self.arch], 2)

    @property
    def data(self):
        """Return second half(data) of data as an integer"""
        return int(format(self.bits, '0{}b'.format(self.arch * 2))[self.arch:], 2)

class RAM:
    """A device containing many words of data(architecture squared)"""
    def __init__(self, arch):
        self.arch = arch
        self.data = [Word(self.arch) for i in range(self.arch ** 2 // 2)] # Should i half it so i can reference registers

    def reboot(self):
        """Wipe all values in ram and reinitialize"""
        self.__init__(self.arch)

class CPU:
    def __init__(self, arch):

        self.ram = RAM(arch)

        self.arch = arch
        self.registers = [Word(self.arch) for i in range(self.arch // 2)] # Have half architecture as number of registers
        self.counter = self.registers[-1] # Use last register as counter
        self.iReg    = self.registers[-2] # Second to last register as instructional register
        self.iSet = (
                self.nop,
                self.load,
                self.store,
                self.add,
                self.sub,
                self.mul,
                self.div,
                self.nop, # Cuz 4-bit calc skips this for SOME reason
                self.print,
                self.input,
                )

    def fetch(self):
        self.iReg.bits = self.ram.data[self.counter.bits].bits

    def exec(self):
        self.iSet[self.iReg.inst](self.iReg.data)
        self.counter

    # And now, the instruction sets
    def nop(self, data):
        return 0

    def load(self, data):
        pass

    def store(self, data):
        pass

    def add(self, data):
        pass

    def sub(self, data):
        pass

    def mul(self, data):
        pass

    def div(self, data):
        pass

    def print(self, data):
        print('yo')

    def input(self, data):
        pass
