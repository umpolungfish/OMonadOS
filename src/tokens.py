"""
omonad_OS TOKENS — The 12 IMASM opcodes as living runtime atoms.

These are not just instructions. They are the 12 categories of being
that the OS can distinguish, compose, and verify. Each token is a
structural primitive in executable form.

Imports the authoritative 12-token set from imasmic_core (the shared
umbrella for ALL Imscribing Grammar ecosystem projects) and adds
omonad_OS-specific extensions: the full 12 canonical arrangements,
helper functions, and arrangement-space utilities.

The 12 tokens decompose into 4 families:
  LOGICAL (6):    category skeleton — init, term, fwd, rev, compose, identity
  FROBENIUS (2):  μ∘δ=id algebra — split, fuse
  DIALETHEIA (3): Belnap FOUR lattice — T, F, B (N is absence)
  LINEAR (1):     irreversible fixation — the ! exponential

Author: Lando⊗⊙perator
"""

from typing import Tuple, List, Dict, Optional

# ─── Core definitions from imasmic_core (shared umbrella) ─────
from imasmic_core import (
    Token,
    Family,
    FAMILY_MAP,
    FAMILY_TOKENS,
    BOOTSTRAP_LOOP,
    CANONICALS as IMASMIC_CANONICALS,
)

# ─── Backward-compatible aliases ──────────────────────────────
TOKEN_FAMILY: Dict[Token, Family] = FAMILY_MAP
TOKEN_NAMES: List[str] = [t.name for t in Token]
TOKEN_COUNT: int = 12

# ─── Backward compatibility: IMSCRIB (legacy spelling) ────────
# omonad_OS originally used IMSCRIB; imasmic_core uses ISCRIB.
# Both refer to the same opcode (0x5). This alias preserves
# existing omonad_OS code.
IMSCRIB = Token.ISCRIB

# ─── The Bootstrap Loop (from imasmic_core) ───────────────────
# μ∘δ=id compiled to 8 instructions.
# Found in ALL domains: ISCRIB → AREV → FSPLIT → AFWD → FFUSE → CLINK → IFIX → ISCRIB


# ─── Omonad_OS Canonical Arrangements (full set of 12) ────────
# The 7 shared canonicals from imasmic_core are re-mapped to the
# omonad_OS naming convention. 5 additional omonad_OS-specific
# canonicals complete the set of 12.

CANONICALS: Dict[str, Tuple[Token, ...]] = {
    "I_Dialetheic_Bootstrap":   (Token.ISCRIB, Token.EVALT, Token.FSPLIT,
                                  Token.EVALF, Token.FFUSE, Token.ENGAGR,
                                  Token.IFIX, Token.ISCRIB),
    "II_Void_Genesis":          (Token.VINIT, Token.FSPLIT, Token.EVALT,
                                  Token.FFUSE, Token.EVALF, Token.CLINK,
                                  Token.IFIX, Token.ISCRIB),
    "III_Anchor_Protocol":      (Token.TANCH, Token.AFWD, Token.EVALT,
                                  Token.AREV, Token.EVALF, Token.CLINK,
                                  Token.IFIX, Token.TANCH),
    "IV_Dual_Bootstrap":        (Token.ISCRIB, Token.AFWD, Token.FFUSE,
                                  Token.FSPLIT, Token.AREV, Token.CLINK,
                                  Token.IFIX, Token.ISCRIB),
    "V_Linear_Chain":           (Token.IFIX,) * 8,
    "VI_Empty_Bootstrap":       (Token.VINIT, Token.ISCRIB) * 4,
    "VII_Parakernel":           (Token.ENGAGR, Token.AFWD, Token.FSPLIT,
                                  Token.EVALT, Token.FFUSE, Token.EVALF,
                                  Token.IFIX, Token.ENGAGR),
    "VIII_Frobenius_Kernel":    (Token.FSPLIT, Token.FFUSE) * 2,
    "IX_Chiral_Pairs":          (Token.AFWD, Token.AREV) * 4,
    "X_Truth_Machine":          (Token.ISCRIB, Token.FSPLIT, Token.EVALT,
                                  Token.IFIX, Token.ISCRIB, Token.FSPLIT,
                                  Token.EVALF, Token.IFIX),
    "XI_Eternal_Return":        (Token.TANCH, Token.AFWD, Token.AREV,
                                  Token.TANCH, Token.AFWD, Token.AREV,
                                  Token.TANCH, Token.AFWD),
    "XII_ROM_Burn":             (Token.EVALT, Token.IFIX, Token.EVALF,
                                  Token.IFIX, Token.ENGAGR, Token.IFIX,
                                  Token.ISCRIB, Token.IFIX),
}


def signature(arr: Tuple[int, ...]) -> Tuple[int, int, int, int]:
    """Family signature (L, F, D, X) — Logical, Frobenius, Dialetheia, Linear."""
    counts = [0, 0, 0, 0]
    for t in arr:
        counts[TOKEN_FAMILY[Token(t)]] += 1
    return (counts[0], counts[1], counts[2], counts[3])


def arrangement_str(arr: Tuple[int, ...]) -> str:
    """Pretty-print as token chain."""
    return " → ".join(TOKEN_NAMES[t] for t in arr)


def token_name(idx: int) -> str:
    return Token(idx).name


def token_family(idx: int) -> Family:
    return TOKEN_FAMILY[Token(idx)]
