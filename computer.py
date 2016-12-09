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

class Word(int):# I just really wanted this to inherit int
    """You can get me by just viewing, but if you wanna set me do Word.bits = 4"""

    def __new__(cls, arch, bits=0b0000):
        return super(Word, cls).__new__(cls, bits)

    def __init__(self, arch, bits=0b0000):
        super().__init__()
        self.arch = arch
        self._bits = bits # Our full data as an integer

    def __repr__(self):
        #return repr(self.inst + " | " + self.data)
        return repr("{}W{}".format(self.inst, self.data))

    def __str__(self):
        return str("{}W{}".format(self.inst, self.data))

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

class Memory(tuple):
    """A device containing many words of data(architecture squared)"""
    def __new__(cls, arch, amount = 0):
        if not amount:
            amount = arch ** 2
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
    def __init__(self, arch):

        self.ram = Memory(arch)

        self.arch = arch
        self.registers = Memory(self.arch, amount=self.arch//2)
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
        self.iReg.bits = self.ram[self.counter].bits

    def exec(self):
        self.iSet[self.iReg.inst](self.iReg.data)
        self.counter

    def address(self, data):
        amount_ram = len(self.ram) - len(self.registers)
        if data < amount_ram:
            return self.ram[data]
        elif amount_ram + len(self.registers) - 2 > data >= amount_ram:
            return self.registers[data - len(self.ram)]
        else:
            assert False

    # And now, the instruction sets
    def nop(self, data):
        return 0

    def load(self, data):
        address1 = int(format(self.bits, '0{}b'.format(self.arch * 2))[:self.arch], 2)
        address2 = int(format(self.bits, '0{}b'.format(self.arch * 2))[self.arch:], 2)

        self.address(address2).bits = self.address(address1).bits


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
