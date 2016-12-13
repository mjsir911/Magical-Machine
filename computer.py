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
    from random import random # ask kevin about this

    def __new__(cls, arch, bits=0b0000):
        return super(Word, cls).__new__(cls, bits)

    def __init__(self, arch, bits=0b0000):
        super().__init__()
        self.arch = arch
        self._memory = (ceil(log(arch / 2, 2)))
        #
        ## Format of input would be:
        # Instruction: [:self.arch - self._memory}
        # Register   : [self.arch - self._memory:self.arch * 2 - self._memory]
        # Address    : [self.arch:]
        ##
        #
        self._bits = bits  # Our full data as an integer

    def __repr__(self):
        # return repr(self.inst + " | " + self.data)
        return repr("{}W{}W{}".format(self.inst, self.regs, self.data))

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
        min = 0
        max = (1 << self.arch * 2) - 1

        assert isinstance(bits, int)

        if min >= bits:
            bits = -bits & (1 << self.arch) - 1 # Two's compliment
        elif max <= bits :
            bits = bits % max # Get overflow

        assert 0 <= bits < (1 << self.arch) ** 2, (
                '{} cannot fit inside this word'.format(bits)
                )
        assert isinstance(bits, int)
        self._bits = bits

    @property
    def inst(self):  # or instruction?
        """Return first half(instruction) of data as an integer"""
        return int(str(self)[:self.arch - self._memory], 2)

    @property
    def regs(self):
        """Returns register of data as integer"""
        return int(str(self)[
            self.arch - self._memory:self.arch
        ], 2)

    @property
    def data(self):
        """Return second half(data) of data as an integer"""
        return int(str(self)[self.arch:], 2)

    def magnet(self):
        self.bits = int(self.random()) * 1 << self.arch


class Memory(tuple):
    """A device containing many words of data(architecture squared)"""
    def __new__(cls, arch, amount=0):
        if not amount:
            amount = 1 << arch
        return super(Memory, cls).__new__(
            cls,
            (Word(arch) for i in range(amount))
        )

    def __init__(self, arch, amount=0):
        self._arch = arch

    def load(self, name):
        """Load contents from file"""
        file = open(name, 'r')
        for num, line in enumerate(file.read().splitlines()):
            self[num].bits = int(line.split()[0], 2)

    def dump(self, name):
        """Dump contents to file"""
        file = open(name, 'w')
        file.write('\n'.join(str(line) for line in self))
        file.close()

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
        return orig.replace(
            name,
            '{}.{}'.format(
                name, self.name.upper()
            )
        ).replace('object', self.subname)

    def __call__(self, reg, mem):
        return self.function(reg.bits, mem.bits)


class ALU(Chip):
    def __init__(self, name, operator):
        super().__init__(name, operator)
        self.subname = 'operator'

    def __call__(self, reg, mem):
        reg.bits = int(self.function(reg.bits, mem.bits))
        return 0


class SIO(Chip):
    def __init__(self, name, bus):
        super().__init__(name, bus)
        self.subname = 'serial IO'

    def __call__(self, reg, mem):
        #print(self)
        input, output = self.function(reg, mem)
        if output is None:
            print('no')
            return 1

        assert isinstance(output, Word), 'output is {}'.format(type(output))
        if isinstance(input, Word):
            input = input.bits

        output.bits = input  # Somehow function this works
        return 0

class KYC(SIO):
    def __init__(self, ram):
        super().__init__('keyboard', lambda r, m: (r, m))
        self.ram = ram
        self.subname = 'peripheral'

    # something like @classmethod
    def _bord(self, char, len):
        num = ord(char)
        fstring = '0{}b'.format(len)
        return format(num, fstring)


    def __call__(self, mem):
        arch = len(str(mem)) // 2
        ram = iter(self.ram[self.ram.index(mem):])
        while True:
            try:
                inp = input()
            except KeyboardInterrupt:
                break
            inp = inp.replace(" ", "") # Get rid of spaces
            if len(inp) == arch * 2:
                try:
                    super().__call__(int(inp, 2), next(ram))
                except ValueError:
                    pass
                else:
                    continue # Repeat the loop Gotta ask kevin for better way to do this

            # Continue on acting like characters were used

            inp += chr(0) # add a trailing null
            inp = iter(inp) # turn into iterable
            for first, last in zip(inp, inp):
                first = self._bord(first, arch)
                last = self._bord(last, arch)
                print(str(first), str(last))
                chrint = int(str(first) + str(last), 2)
                super().__call__(chrint, next(ram))

class CPU:
    def __init__(self, arch=8):

        self.arch = arch

        self.ram = Memory(self.arch, 1 << self.arch)

        self.registers = Memory(self.arch, 1 << (ceil(log(arch / 2, 2))))

        self.counter = self.registers[-1]  # Use last register as counter
        self.iReg    = self.registers[-2]
        # Second to last register as instructional register
        self.iSet = (#Everything in here needs to be callable with 2 args
            Chip('nop', lambda r, m: (0)),
            SIO('load', lambda r, m: (m, r)),
            SIO('stor', lambda r, m: (r, m)),
            # Mathematical
            ALU('add' , lambda r, m: (r + m)),
            ALU('sub' , lambda r, m: (r - m)),
            ALU('mul' , lambda r, m: (r * m)),
            ALU('div' , lambda r, m: (r / m)),
            Chip('nop', lambda r, m: (0)),
            # Cuz 4-bit calc skips this for SOME reason
            Chip('prn', lambda r, m: print(m)),
            SIO('inpt', lambda r, m: (int(input(), 0), m)),
            SIO('jump', lambda r, m: (m.data, self.registers[-1])),
            SIO('ijmp', lambda r, m: (m.data, self.registers[-1]) if r.bits == 0 else (None, None)), # Gotta improve this
        )

    def fetch(self):
        self.iReg.bits = self.ram[self.counter.bits].bits

    def exec(self):
        register = self.registers[self.iReg.regs]
        memory   = self.ram[self.iReg.data]
        self.counter.bits = self.counter.bits + 1
        self.iSet[self.iReg.inst](register, memory)
        # return self.iSet[self.iReg.inst](register, memory)

    def run(self, repeat=1): # Just for simplicities' sake
        for num in range(repeat):
            self.fetch()
            self.exec()

    def reset(self):
        for register in self.registers:
            register.bits = 0
