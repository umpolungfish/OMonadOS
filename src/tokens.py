"""
omonad_OS TOKENS — The 12 IMASM opcodes as living runtime atoms.

These are not just instructions. They are the 12 categories of being
that the OS can distinguish, compose, and verify. Each token is a
structural primitive in executable form.

The 12 tokens decompose into 4 families:
  LOGICAL (6):    category skeleton — init, term, fwd, rev, compose, identity
  FROBENIUS (2):  μ∘δ=id algebra — split, fuse
  DIALETHEIA (3): Belnap FOUR lattice — T, F, B (N is absence)
  LINEAR (1):     irreversible fixation — the ! exponential

Author: Lando⊗⊙perator
"""

from enum import IntEnum
from typing import Tuple, List, Dict, Optional

class Token(IntEnum):
    """The 12 IMASM opcodes — categorical duals of the 12 IG primitives."""
    VINIT   = 0x0  # Initial object ∅ — void
    TANCH   = 0x1  # Terminal anchor ⊤ — boundary
    AFWD    = 0x2  # Forward morphism → — directed
    AREV    = 0x3  # Contravariant inversion ← — reversal
    CLINK   = 0x4  # Composition ∘ — linkage
    IMSCRIB = 0x5  # Identity id — self-imscription
    FSPLIT  = 0x6  # Co-multiplication δ — bifurcation
    FFUSE   = 0x7  # Multiplication μ — recombination
    EVALT   = 0x8  # True — affirmation
    EVALF   = 0x9  # False — negation
    ENGAGR  = 0xA  # Both — paradox stabilized
    IFIX    = 0xB  # Permanent brand — irreversible !

class Family(IntEnum):
    LOGICAL    = 0  # 6 tokens
    FROBENIUS  = 1  # 2 tokens
    DIALETHEIA = 2  # 3 tokens
    LINEAR     = 3  # 1 token

# Family membership
TOKEN_FAMILY: Dict[Token, Family] = {
    Token.VINIT: Family.LOGICAL,    Token.TANCH: Family.LOGICAL,
    Token.AFWD: Family.LOGICAL,     Token.AREV: Family.LOGICAL,
    Token.CLINK: Family.LOGICAL,    Token.IMSCRIB: Family.LOGICAL,
    Token.FSPLIT: Family.FROBENIUS, Token.FFUSE: Family.FROBENIUS,
    Token.EVALT: Family.DIALETHEIA, Token.EVALF: Family.DIALETHEIA,
    Token.ENGAGR: Family.DIALETHEIA,
    Token.IFIX: Family.LINEAR,
}

FAMILY_TOKENS: Dict[Family, List[Token]] = {
    Family.LOGICAL:    [Token.VINIT, Token.TANCH, Token.AFWD, Token.AREV,
                         Token.CLINK, Token.IMSCRIB],
    Family.FROBENIUS:  [Token.FSPLIT, Token.FFUSE],
    Family.DIALETHEIA: [Token.EVALT, Token.EVALF, Token.ENGAGR],
    Family.LINEAR:     [Token.IFIX],
}

TOKEN_NAMES: List[str] = [t.name for t in Token]
TOKEN_COUNT: int = 12

# ─── The Bootstrap Loop ───────────────────────────────────────
# μ∘δ=id compiled to 8 instructions.
# Found in ALL domains: ISCRIB → AREV → FSPLIT → AFWD → FFUSE → CLINK → IFIX → ISCRIB
BOOTSTRAP_LOOP: Tuple[Token, ...] = (
    Token.IMSCRIB, Token.AREV, Token.FSPLIT,
    Token.AFWD, Token.FFUSE, Token.CLINK,
    Token.IFIX, Token.IMSCRIB,
)

# ─── Canonical Arrangements ───────────────────────────────────
CANONICALS: Dict[str, Tuple[Token, ...]] = {
    "I_Dialetheic_Bootstrap":   (Token.IMSCRIB, Token.EVALT, Token.FSPLIT,
                                  Token.EVALF, Token.FFUSE, Token.ENGAGR,
                                  Token.IFIX, Token.IMSCRIB),
    "II_Void_Genesis":          (Token.VINIT, Token.FSPLIT, Token.EVALT,
                                  Token.FFUSE, Token.EVALF, Token.CLINK,
                                  Token.IFIX, Token.IMSCRIB),
    "III_Anchor_Protocol":      (Token.TANCH, Token.AFWD, Token.EVALT,
                                  Token.AREV, Token.EVALF, Token.CLINK,
                                  Token.IFIX, Token.TANCH),
    "IV_Dual_Bootstrap":        (Token.IMSCRIB, Token.AFWD, Token.FFUSE,
                                  Token.FSPLIT, Token.AREV, Token.CLINK,
                                  Token.IFIX, Token.IMSCRIB),
    "V_Linear_Chain":           (Token.IFIX,) * 8,
    "VI_Empty_Bootstrap":       (Token.VINIT, Token.IMSCRIB) * 4,
    "VII_Parakernel":           (Token.ENGAGR, Token.AFWD, Token.FSPLIT,
                                  Token.EVALT, Token.FFUSE, Token.EVALF,
                                  Token.IFIX, Token.ENGAGR),
    "VIII_Frobenius_Kernel":    (Token.FSPLIT, Token.FFUSE) * 2,
    "IX_Chiral_Pairs":          (Token.AFWD, Token.AREV) * 4,
    "X_Truth_Machine":          (Token.IMSCRIB, Token.FSPLIT, Token.EVALT,
                                  Token.IFIX, Token.IMSCRIB, Token.FSPLIT,
                                  Token.EVALF, Token.IFIX),
    "XI_Eternal_Return":        (Token.TANCH, Token.AFWD, Token.AREV,
                                  Token.TANCH, Token.AFWD, Token.AREV,
                                  Token.TANCH, Token.AFWD),
    "XII_ROM_Burn":             (Token.EVALT, Token.IFIX, Token.EVALF,
                                  Token.IFIX, Token.ENGAGR, Token.IFIX,
                                  Token.IMSCRIB, Token.IFIX),
}

def signature(arr: Tuple[int, ...]) -> Tuple[int, int, int, int]:
    """Family signature (L, F, D, X)."""
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
