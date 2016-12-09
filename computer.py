#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import log, ceil

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

class Word(int):# I just really wanted this to inherit int

    def __new__(cls, arch, bits=0b0000):
        return super(Word, cls).__new__(cls, bits)

    def __init__(self, arch, bits=0b0000):
        super().__init__()
        self.arch = arch
        self._memory = (ceil(log(arch/2, 2)))
        self._bits = bits # Our full data as an integer

    def __repr__(self):
        #return repr(self.inst + " | " + self.data)
        return repr("{}W{}W{}".format(self.inst, self.data, self.regs))

    def __str__(self):
        #return str("{}W{}W{}".format(self.inst, self.data, self.regs))
        return format(self.bits, '0{}b'.format(self.arch * 2))

    def __bool__(self):
        return bool(bits)

    #def __add__(self, other):
        #return Word(self.arch, self.bits + other)

    @property
    def bits(self):
        return self._bits

    @bits.setter
    def bits(self, bits):
        assert 0 <= bits < (2 ** self.arch) ** 2
        assert type(bits) == type(int())
        self._bits = bits

    #@property
    #def _str_bits(self):
        #return format(self.bits, '0{}b'.format(self.arch * 2))

    @property
    def inst(self):#or instruction?
        """Return first half(instruction) of data as an integer"""
        #return int(format(self.bits, '0{}b'.format(self.arch * 2))[:self.arch], 2)
        return int(str(self)[:self.arch - self._memory], 2)

    @property
    def data(self):
        """Return second half(data) of data as an integer"""
        #return int(format(self.bits, '0{}b'.format(self.arch * 2))[self.arch:], 2)
        return int(str(self)[self.arch - self._memory : self.arch * 2 - self._memory], 2)

    @property
    def regs(self):
        """Returns register of data as integer"""
        return int(str(self)[self.arch * 2 - self._memory:], 2)

class Memory(tuple):
    """A device containing many words of data(architecture squared)"""
    def __new__(cls, arch, amount = 0):
        if not amount:
            amount = 2 ** arch
        return super(Memory, cls).__new__(cls,
                (Word(arch) for i in range(amount)))

    def __init__(self, arch, amount = 0):
        self._arch = arch

    def reboot(self):
        """Wipe all values in ram and reinitialize"""
        #self = self.__new__(type(self), self._arch)
        for word in self:
            word.magnet()

class CPU:
    def __init__(self, arch=8):

        self.arch = arch

        self.ram = Memory(self.arch, 2 ** self.arch)

        self.registers = Memory(self.arch, 2 ** (ceil(log(arch/2, 2))))

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
        self.iReg.bits = self.ram[self.counter.bits].bits

    def exec(self):
        memory   = self.ram[self.iReg.data]
        register = self.registers[self.iReg.regs]
        self.iSet[self.iReg.inst](memory.bits, register.bits)
        self.counter.bits = self.counter.bits + 1

    # And now, the instruction sets
    def nop(self, mem, reg):
        return 0

    def load(self, mem, reg):
        reg = mem

    def store(self, mem, reg):
        mem = reg

    def add(self, mem, reg):
        reg += mem

    def sub(self, mem, reg):
        reg -= mem

    def mul(self, mem, reg):
        reg *= mem

    def div(self, mem, reg):
        reg = reg // mem

    def print(self, mem, reg):
        print(mem)

    def input(self, mem, reg):
        mem = int(input())
