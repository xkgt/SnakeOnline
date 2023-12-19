import struct
import sys
import io
from uuid import UUID


class DataStream(io.BytesIO):
    def __init__(self, *args):  # 删掉后某地方会有类型警告
        super().__init__(*args)

    # def write(self, __buffer):
    #     print(__buffer)
    #     return super().write(__buffer)
    #
    # def read(self, __size = ...):
    #     print(__size)
    #     a = super().read(__size)
    #     print(a)
    #     return a

    def __lshift__(self, other):
        if hasattr(other, "write"):
            other.write(self)
        else:
            getattr(self, "write_"+type(other).__name__.lower())(other)
        return self

    def __rshift__(self, other):
        if hasattr(other, "read"):
            return other.read(self)
        if isinstance(other, str):
            return getattr(self, "read_" + other.lower())()
        return getattr(self, "read_" + other.__name__.lower())()

    write_bytes = io.BytesIO.write
    read_bytes = io.BytesIO.read

    def read_int(self) -> int:
        return struct.unpack("i", self.read(4))[0]

    def write_int(self, value: int):
        self.write(struct.pack("i", value))

    def write_short(self, value: int):
        self.write(struct.pack("h", value))

    def read_short(self) -> int:
        return struct.unpack("h", self.read(2))[0]

    def write_str(self, value: str):
        data = value.encode("utf8")
        self.write_short(len(data))
        self.write(data)

    def read_str(self) -> str:
        size = self.read_short()
        data = self.read(size)
        return data.decode("utf8")

    def read_float(self) -> float:
        return struct.unpack("f", self.read(4))[0]

    def write_float(self, value: float):
        self.write(struct.pack("f", value))

    def read_bool(self) -> bool:
        return bool.from_bytes(self.read(1), sys.byteorder)

    def write_bool(self, value: bool):
        self.write(value.to_bytes(1, sys.byteorder))

    def read_byte(self) -> int:
        return int.from_bytes(self.read(1), sys.byteorder)

    def write_byte(self, value: int):
        self.write(value.to_bytes(1, sys.byteorder))

    def read_uuid(self) -> UUID:
        return UUID(bytes=self.read(16))

    def write_uuid(self, value: UUID):
        self.write(value.bytes)

    def read_bools(self) -> tuple[bool, bool, bool, bool, bool, bool, bool, bool]:
        v = self.read_byte()
        b1 = v & 128 == 128
        b2 = v & 64 == 64
        b3 = v & 32 == 32
        b4 = v & 16 == 16
        b5 = v & 8 == 8
        b6 = v & 4 == 4
        b7 = v & 2 == 2
        b8 = v & 1 == 1
        return b1, b2, b3, b4, b5, b6, b7, b8

    def write_bools(self, b1, b2=False, b3=False, b4=False, b5=False, b6=False, b7=False, b8=False):
        a = (b1 << 1) + b2
        a = (a << 1) + b3
        a = (a << 1) + b4
        a = (a << 1) + b5
        a = (a << 1) + b6
        a = (a << 1) + b7
        a = (a << 1) + b8
        self.write_byte(a)
