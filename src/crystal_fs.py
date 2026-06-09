"""
omonad_OS CRYSTAL FILESYSTEM — The 17.28M-type address space as storage.

No hierarchical directories. No inodes. No path strings.
The crystal of types IS the filesystem.

Every file lives at a crystal address (0–17,279,999), which is
a Frobenius encoding of a 12-primitive structural type.
To find a file, navigate the crystal — not a directory tree.

Operations:
  - crystal_store(data, D, T, R, P, F, K, G, C, Phi, H, S, Omega)
  - crystal_read(address) → data
  - crystal_navigate(**constraints) → list of addresses
  - crystal_neighbor(address, n=5) → nearest structural neighbors

The mapping from 12-tuple → address is:
  address = Σᵢ (primitive_index[i] × stride[i])
  stride = [5184000, 1728000, 576000, 144000, 48000, 12000, 4000, 800, 200, 50, 10, 1]

Author: Lando⊗⊙perator
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
import json
import struct


# ─── Primitive value spaces ───────────────────────────────────

# Each primitive has a finite set of Shavian glyph values.
# The index within this set determines the crystal position contribution.

D_VALUES = ['𐑛', '𐑨', '𐑼', '𐑦']           # 4 values
T_VALUES = ['𐑡', '𐑰', '𐑥', '𐑶', '𐑸']     # 5 values
R_VALUES = ['𐑩', '𐑑', '𐑽', '𐑾']           # 4 values
P_VALUES = ['𐑗', '𐑿', '𐑬', '𐑯', '𐑹']     # 5 values
F_VALUES = ['𐑱', '𐑞', '𐑐']                 # 3 values
K_VALUES = ['𐑘', '𐑤', '𐑧', '𐑪', '𐑺']     # 5 values
G_VALUES = ['𐑚', '𐑔', '𐑲']                 # 3 values
C_VALUES = ['𐑝', '𐑜', '𐑠', '𐑵']           # 4 values
PHI_VALUES = ['𐑢', '⊙', '𐑮', '𐑻', '𐑣']    # 5 values
H_VALUES = ['𐑓', '𐑒', '𐑖', '𐑫']           # 4 values
S_VALUES = ['𐑙', '𐑕', '𐑳']                 # 3 values
OMEGA_VALUES = ['𐑷', '𐑴', '𐑭', '𐑟']       # 4 values

PRIMITIVE_VALUES = {
    'D': D_VALUES, 'T': T_VALUES, 'R': R_VALUES,
    'P': P_VALUES, 'F': F_VALUES, 'K': K_VALUES,
    'G': G_VALUES, 'C': C_VALUES, 'Phi': PHI_VALUES,
    'H': H_VALUES, 'S': S_VALUES, 'Omega': OMEGA_VALUES,
}

PRIMITIVE_ORDER = ['D', 'T', 'R', 'P', 'F', 'K', 'G', 'C', 'Phi', 'H', 'S', 'Omega']

# Cardinalities: 4,5,4,5,3,5,3,4,5,4,3,4
CARDINALITIES = [len(PRIMITIVE_VALUES[p]) for p in PRIMITIVE_ORDER]

# Strides for positional encoding
STRIDES = [1]
for c in reversed(CARDINALITIES[1:]):
    STRIDES.insert(0, STRIDES[0] * c)
# STRIDES = [5184000, 1728000, 576000, 144000, 48000, 12000, 4000, 800, 200, 50, 10, 1]

TOTAL_TYPES = STRIDES[0] * CARDINALITIES[0]  # 17,280,000


# ─── Crystal Encoding ─────────────────────────────────────────

def crystal_encode(
    D: str, T: str, R: str, P: str, F: str, K: str,
    G: str, C: str, Phi: str, H: str, S: str, Omega: str,
) -> int:
    """Encode a 12-tuple of Shavian glyphs to a crystal address (0–17279999)."""
    values = [D, T, R, P, F, K, G, C, Phi, H, S, Omega]
    address = 0
    for i, (val, prim) in enumerate(zip(values, PRIMITIVE_ORDER)):
        vlist = PRIMITIVE_VALUES[prim]
        if val not in vlist:
            raise ValueError(f"Invalid value '{val}' for primitive {prim}")
        idx = vlist.index(val)
        address += idx * STRIDES[i]
    return address


def crystal_decode(address: int) -> Dict[str, str]:
    """Decode a crystal address to a 12-tuple of Shavian glyphs."""
    if not (0 <= address < TOTAL_TYPES):
        raise ValueError(f"Address {address} out of range [0, {TOTAL_TYPES})")
    result = {}
    remaining = address
    for i, prim in enumerate(PRIMITIVE_ORDER):
        vlist = PRIMITIVE_VALUES[prim]
        stride = STRIDES[i]
        idx = remaining // stride
        result[prim] = vlist[idx]
        remaining -= idx * stride
    return result


# ─── Crystal Filesystem ───────────────────────────────────────

@dataclass
class CrystalEntry:
    """A file stored at a crystal address."""
    address: int
    tuple_display: str
    name: str = ""
    data: bytes = b""
    metadata: Dict[str, Any] = field(default_factory=dict)


class CrystalFS:
    """The crystal of types as a filesystem.

    Files are addressed by their structural type, not by paths.
    To find a file, you navigate the crystal lattice — meet, join,
    tensor, and neighbor operations replace directory traversal.
    """

    def __init__(self):
        self.entries: Dict[int, CrystalEntry] = {}
        self.name_index: Dict[str, int] = {}

    def store(
        self,
        name: str,
        data: bytes,
        D: str, T: str, R: str, P: str,
        F: str, K: str, G: str, C: str,
        Phi: str, H: str, S: str, Omega: str,
        metadata: Optional[Dict] = None,
    ) -> int:
        """Store data at a crystal address.

        If the address already exists, the data is overwritten
        (structural conflict — the new imscription supersedes).
        """
        address = crystal_encode(D, T, R, P, F, K, G, C, Phi, H, S, Omega)
        entry = CrystalEntry(
            address=address,
            tuple_display=(
                f"⟨{D}·{T}·{R}·{P}·{F}·{K}·{G}·{C}·{Phi}·{H}·{S}·{Omega}⟩"
            ),
            name=name,
            data=data,
            metadata=metadata or {},
        )
        self.entries[address] = entry
        self.name_index[name] = address
        return address

    def read(self, address: int) -> Optional[CrystalEntry]:
        """Read data from a crystal address."""
        return self.entries.get(address)

    def read_by_name(self, name: str) -> Optional[CrystalEntry]:
        addr = self.name_index.get(name)
        if addr is not None:
            return self.entries.get(addr)
        return None

    def navigate(self, **constraints) -> List[CrystalEntry]:
        """Find entries matching primitive constraints.

        Example: navigate(Phi='⊙', Omega='𐑭')
        → all entries with ⊙ criticality and integer winding.
        """
        results = []
        for entry in self.entries.values():
            decoded = crystal_decode(entry.address)
            match = True
            for prim, val in constraints.items():
                if decoded.get(prim) != val:
                    match = False
                    break
            if match:
                results.append(entry)
        return results

    def neighbors(self, address: int, n: int = 5) -> List[Tuple[int, CrystalEntry]]:
        """Find nearest structural neighbors to an address.

        Distance is Hamming distance over primitive values.
        """
        target = crystal_decode(address)
        distances = []
        for addr, entry in self.entries.items():
            if addr == address:
                continue
            decoded = crystal_decode(addr)
            dist = sum(1 for p in PRIMITIVE_ORDER
                      if decoded[p] != target[p])
            distances.append((dist, addr, entry))
        distances.sort(key=lambda x: x[0])
        return [(addr, entry) for _, addr, entry in distances[:n]]

    def meet_region(self, addr_a: int, addr_b: int) -> Dict[str, str]:
        """The meet (greatest lower bound) of two crystal addresses."""
        a = crystal_decode(addr_a)
        b = crystal_decode(addr_b)
        # Meet: take the minimum index for each primitive
        result = {}
        for prim in PRIMITIVE_ORDER:
            vlist = PRIMITIVE_VALUES[prim]
            ia = vlist.index(a[prim])
            ib = vlist.index(b[prim])
            result[prim] = vlist[min(ia, ib)]
        return result

    def join_region(self, addr_a: int, addr_b: int) -> Dict[str, str]:
        """The join (least upper bound) of two crystal addresses."""
        a = crystal_decode(addr_a)
        b = crystal_decode(addr_b)
        result = {}
        for prim in PRIMITIVE_ORDER:
            vlist = PRIMITIVE_VALUES[prim]
            ia = vlist.index(a[prim])
            ib = vlist.index(b[prim])
            result[prim] = vlist[max(ia, ib)]
        return result

    def count(self) -> int:
        return len(self.entries)

    def list_all(self) -> List[CrystalEntry]:
        return sorted(self.entries.values(), key=lambda e: e.address)
