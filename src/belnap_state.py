"""
omonad_OS BELNAP STATE — The fundamental memory model.

Not binary. Not ternary. Belnap FOUR (B4): N, T, F, B.

  N (0b00) — Neither:    no information, the void
  T (0b01) — True:       affirmed
  F (0b10) — False:      denied
  B (0b11) — Both:       paradox stabilized (dialetheia)

Every memory cell is a B4 value. Every register. Every flag.
The OS can hold contradiction without crashing — it's built for it.

B4 forms a De Morgan lattice:
  Meet (∧): bitwise AND — cautious, takes the less informed
  Join (∨): bitwise OR  — bold, takes the more informed
  Complement (¬): ~val & 0b11 — four-valued negation

Author: Lando⊗⊙perator
"""

from enum import IntEnum
from typing import List, Tuple, Optional, Callable
from dataclasses import dataclass, field
import struct


class B4(IntEnum):
    """Belnap FOUR truth values."""
    N = 0b00  # Neither — no information, the void
    T = 0b01  # True — affirmed
    F = 0b10  # False — denied
    B = 0b11  # Both — paradox stabilized

    @classmethod
    def from_bool(cls, b: bool) -> 'B4':
        return cls.T if b else cls.F

    @classmethod
    def from_bits(cls, val: int) -> 'B4':
        return cls(val & 0b11)

    @property
    def is_dialetheic(self) -> bool:
        return self == B4.B

    @property
    def has_information(self) -> bool:
        return self != B4.N

    @property
    def is_classical(self) -> bool:
        return self in (B4.T, B4.F)

    def __str__(self) -> str:
        return self.name


# ─── Lattice operations ───────────────────────────────────────

def b4_meet(a: B4, b: B4) -> B4:
    """Cautious join — AND of bits. a ∧ b."""
    return B4(int(a) & int(b))

def b4_join(a: B4, b: B4) -> B4:
    """Bold join — OR of bits. a ∨ b."""
    return B4(int(a) | int(b))

def b4_complement(a: B4) -> B4:
    """Four-valued negation. ~a masked to 2 bits."""
    return B4((~int(a)) & 0b11)

def b4_entails(a: B4, b: B4) -> bool:
    """Information order: a ≤ b if a has no more information than b."""
    return (int(a) & int(b)) == int(a)


# ─── B4 Memory ────────────────────────────────────────────────

@dataclass
class B4Memory:
    """A block of Belnap FOUR memory.

    Each cell is 2 bits. 4 cells per byte. The fundamental
    addressable unit is the nybble (4 bits = 2 B4 cells).
    """
    size: int
    data: bytearray = field(default_factory=bytearray)
    _cell_count: int = 0

    def __post_init__(self):
        bytes_needed = (self.size + 3) // 4
        self.data = bytearray(bytes_needed)
        self._cell_count = self.size

    def read(self, addr: int) -> B4:
        if addr < 0 or addr >= self._cell_count:
            raise IndexError(f"B4 address {addr} out of range")
        byte_idx = addr // 4
        shift = (addr % 4) * 2
        val = (self.data[byte_idx] >> shift) & 0b11
        return B4(val)

    def write(self, addr: int, val: B4):
        if addr < 0 or addr >= self._cell_count:
            raise IndexError(f"B4 address {addr} out of range")
        byte_idx = addr // 4
        shift = (addr % 4) * 2
        mask = 0b11 << shift
        self.data[byte_idx] = (self.data[byte_idx] & ~mask) | (int(val) << shift)

    def dump(self, start: int = 0, count: Optional[int] = None) -> List[B4]:
        if count is None:
            count = self._cell_count - start
        return [self.read(start + i) for i in range(count)]


# ─── B4 Register File ─────────────────────────────────────────

@dataclass
class B4Registers:
    """8 Belnap FOUR registers: R0–R7.

    R7 is the DIALETHEIA register — can hold B (Both).
    Writing B to any other register triggers PARADOX INTERRUPT
    unless ENGAGR flag is set.
    """
    regs: bytearray = field(default_factory=lambda: bytearray(8))
    engagr_flag: bool = False
    paradox_interrupt: bool = False
    paradox_addr: int = 0

    def read(self, n: int) -> B4:
        if 0 <= n <= 7:
            return B4(self.regs[n] & 0b11)
        raise IndexError(f"Register R{n} does not exist")

    def write(self, n: int, val: B4):
        if n < 0 or n > 7:
            raise IndexError(f"Register R{n} does not exist")
        if val == B4.B and n != 7 and not self.engagr_flag:
            self.paradox_interrupt = True
            self.paradox_addr = n
        self.regs[n] = int(val) & 0b11

    def set_engagr(self, val: bool):
        self.engagr_flag = val

    def clear_interrupt(self):
        self.paradox_interrupt = False


# ─── B4 Stack ─────────────────────────────────────────────────

@dataclass
class B4Stack:
    """Belnap FOUR stack. Supports paradox on the stack."""
    max_depth: int = 256
    data: List[B4] = field(default_factory=list)

    def push(self, val: B4):
        if len(self.data) >= self.max_depth:
            raise OverflowError("B4 stack overflow")
        self.data.append(val)

    def pop(self) -> B4:
        if not self.data:
            return B4.N
        return self.data.pop()

    def peek(self) -> B4:
        if not self.data:
            return B4.N
        return self.data[-1]

    @property
    def depth(self) -> int:
        return len(self.data)
