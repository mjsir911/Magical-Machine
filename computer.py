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


class Word(int):  # I just really wanted this to inherit int

    def __new__(cls, arch, bits=0b0000):
        return super(Word, cls).__new__(cls, bits)

    def __init__(self, arch, bits=0b0000):
        super().__init__()
        self.arch = arch
        self._memory = (ceil(log(arch / 2, 2)))
        self._bits = bits  # Our full data as an integer

    def __repr__(self):
        # return repr(self.inst + " | " + self.data)
        return repr("{}W{}W{}".format(self.inst, self.data, self.regs))

    def __str__(self):  # Not the best practice, but needed for below functions
        # return str("{}W{}W{}".format(self.inst, self.data, self.regs))
        return format(self.bits, '0{}b'.format(self.arch * 2))

    def __bool__(self):
        return bool(self.bits)

    @property
    def bits(self):
        return self._bits

    @bits.setter
    def bits(self, bits):
        # print(type(bits))
        # print(bits)
        assert 0 <= bits < (2 ** self.arch) ** 2
        assert isinstance(bits, int)
        self._bits = bits

    @property
    def inst(self):  # or instruction?
        """Return first half(instruction) of data as an integer"""
        return int(str(self)[:self.arch - self._memory], 2)

    @property
    def data(self):
        """Return second half(data) of data as an integer"""
        return int(str(self)[
            self.arch     - self._memory:
            self.arch * 2 - self._memory
        ], 2)

    @property
    def regs(self):
        """Returns register of data as integer"""
        return int(str(self)[self.arch * 2 - self._memory:], 2)


class Memory(tuple):
    """A device containing many words of data(architecture squared)"""
    def __new__(cls, arch, amount=0):
        if not amount:
            amount = 2 ** arch
        return super(Memory, cls).__new__(
            cls,
            (Word(arch) for i in range(amount))
        )

    def __init__(self, arch, amount=0):
        self._arch = arch

    def reboot(self):
        """Wipe all values in ram and reinitialize"""
        # self = self.__new__(type(self), self._arch)
        for word in self:
            word.magnet()


class Chip:
    def __init__(self, name, lam):
        # self.self = parent
        self.name = name
        self.function = lam
        self.subname = 'chip'

    def __repr__(self):
        orig = super().__repr__()
        name = type(self).__name__
        # return '<bound operator ALU.{} of {}>'\
        #         .format(self.name.upper(), repr(self.self))
        return orig.replace(name, '{}.{}'.format(name, self.name.upper()).replace('object', self.subname))

    def __call__(self, reg, mem):
        # reg.bits = self.function(reg.bits, mem.bits)
        self.function(reg.bits, mem.bits)


class ALU(Chip):
    def __init__(self, name, operator):
        super().__init__(name, operator)
        self.subname = 'operator'

    def __call__(self, reg, mem):
        reg.bits = int(self.function(reg.bits, mem.bits))


class SIO(Chip):
    def __init__(self, name, bus):
        super().__init__(name, bus)
        self.subname = 'serial'

    def __call__(self, reg, mem):
        # print(mem)
        input = self.function(reg, mem)
        # if input is not mem or input is not mem.bits:
        if input is mem.bits:
            # print('output = reg')
            output = reg
        else:
            output = mem

        # print(output)
        output.bits = input  # Somehow function this works


class CPU:
    def __init__(self, arch=8):

        self.arch = arch

        self.ram = Memory(self.arch, 2 ** self.arch)

        self.registers = Memory(self.arch, 2 ** (ceil(log(arch / 2, 2))))

        self.counter = self.registers[-1]  # Use last register as counter
        self.iReg    = self.registers[-2]  # Second to last register as instructional register
        self.iSet = (
            Chip('nop', lambda r, m: 0),
            SIO('load', lambda r, m: m.bits),
            SIO('stor', lambda r, m: r.bits),
            # Mathematical
            ALU('add', lambda r, m: r + m),
            ALU('sub', lambda r, m: r - m),
            ALU('mul', lambda r, m: r * m),
            ALU('div', lambda r, m: r / m),
            Chip'nop', lambda r, m: 0,),
            # Cuz 4-bit calc skips this for SOME reason
            Chip('prn', lambda r, m: print(m)),
            SIO('inpt', lambda r, m: int(input(), 0)),
        )

    def fetch(self):
        self.iReg.bits = self.ram[self.counter.bits].bits

    def exec(self):
        register = self.registers[self.iReg.regs]
        memory   = self.ram[self.iReg.data]
        self.iSet[self.iReg.inst](register, memory)
        self.counter.bits = self.counter.bits + 1
