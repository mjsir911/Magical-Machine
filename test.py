class Word(int):
    def __init__(self, arch, bits=0b0000):
        self.arch = arch
        self.bits = bits # Our full data as an integer

    def __repr__(self):
        return repr(self.bits)

    @property
    def bits(self):
        return self._bits

    @bits.setter
    def bits(self, bits):
        assert bits < self.arch ** 4
        self._bits = bits
        return self.__new__(type(self), self.arch)

x = Word(4)
