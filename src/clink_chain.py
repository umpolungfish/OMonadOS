"""
omonad_OS CLINK CHAIN — The 9-layer structural bridge.

Programs can DESCEND through the CLINK chain:
  Whole Organism → Tissue → Meiosis → Mitosis → Cell →
  Molecule → Atom → Electron Orbital → Quarks

And ASCEND back. Each layer has a structural type (12-tuple),
a Belnap FOUR truth-lattice configuration, and a set of
valid token operations.

Descending compresses; ascending enriches.
The chain IS the hardware abstraction — there are no "drivers,"
only structural promotions and demotions.

Author: Lando⊗⊙perator
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from .tokens import Token


# ─── The 9 Layers ─────────────────────────────────────────────

@dataclass
class ClinkLayer:
    index: int
    name: str
    tier: str
    D: str; T_val: str; R: str; P: str
    F: str; K: str; G: str; C: str
    Phi: str; H: str; S: str; Omega: str
    description: str
    valid_tokens: List[Token] = field(default_factory=list)

    @property
    def tuple_display(self) -> str:
        return (f"⟨{self.D}·{self.T_val}·{self.R}·{self.P}·"
                f"{self.F}·{self.K}·{self.G}·{self.C}·"
                f"{self.Phi}·{self.H}·{self.S}·{self.Omega}⟩")

    @property
    def primitives_dict(self) -> Dict[str, str]:
        return {
            'D': self.D, 'T': self.T_val, 'R': self.R, 'P': self.P,
            'F': self.F, 'K': self.K, 'G': self.G, 'C': self.C,
            'Phi': self.Phi, 'H': self.H, 'S': self.S, 'Omega': self.Omega,
        }


CLINK_CHAIN: List[ClinkLayer] = [
    ClinkLayer(0, "Frustrated Belnap5 (Quarks)", "O₀",
        '𐑛', '𐑶', '𐑩', '𐑯', '𐑐', '𐑘', '𐑚', '𐑝',
        '𐑢', '𐑓', '𐑳', '𐑷',
        "Subatomic QCD — frustrated B5 lattice, all 5 truth values",
        [Token.VINIT, Token.EVALT, Token.EVALF, Token.FSPLIT, Token.FFUSE],
    ),
    ClinkLayer(1, "Electron Orbital (Belnap4)", "O₀",
        '𐑛', '𐑶', '𐑩', '𐑗', '𐑐', '𐑤', '𐑚', '𐑜',
        '𐑢', '𐑓', '𐑳', '𐑷',
        "Quantum orbital — B4 settles from B5 frustration",
        [Token.VINIT, Token.EVALT, Token.EVALF, Token.TANCH, Token.AFWD, Token.AREV],
    ),
    ClinkLayer(2, "Atom (Nuclear + Electron)", "O₁",
        '𐑼', '𐑥', '𐑽', '𐑿', '𐑐', '𐑤', '𐑔', '𐑝',
        '𐑮', '𐑒', '𐑳', '𐑷',
        "Composite — crossing point topology, quantum superposition",
        [Token.VINIT, Token.TANCH, Token.AFWD, Token.AREV, Token.CLINK,
         Token.EVALT, Token.EVALF],
    ),
    ClinkLayer(3, "Molecule (Chemical Bonds)", "O₂",
        '𐑼', '𐑥', '𐑽', '𐑿', '𐑞', '𐑧', '𐑲', '𐑠',
        '⊙', '𐑓', '𐑳', '𐑭',
        "Bonded atoms — ⊙ gate opens, integer winding, sequential composition",
        [Token.VINIT, Token.TANCH, Token.AFWD, Token.AREV, Token.CLINK,
         Token.ISCRIB, Token.FSPLIT, Token.FFUSE, Token.EVALT, Token.EVALF,
         Token.IFIX],
    ),
    ClinkLayer(4, "Cell (Living)", "O₂",
        '𐑦', '𐑸', '𐑾', '𐑬', '𐑞', '𐑧', '𐑲', '𐑠',
        '⊙', '𐑒', '𐑳', '𐑭',
        "Self-written state space — Axiom C satisfied — bidirectional coupling",
        [t for t in Token],  # All tokens valid
    ),
    ClinkLayer(5, "Mitosis (Division)", "O₂",
        '𐑦', '𐑸', '𐑾', '𐑹', '𐑱', '𐑧', '𐑲', '𐑠',
        '⊙', '𐑖', '𐑳', '𐑭',
        "Frobenius-special parity — exact μ∘δ=id at division — Markov-2 memory",
        [t for t in Token],
    ),
    ClinkLayer(6, "Meiosis (Gametes)", "O₂",
        '𐑦', '𐑸', '𐑽', '𐑿', '𐑱', '𐑧', '𐑲', '𐑠',
        '⊙', '𐑖', '𐑳', '𐑭',
        "Adjoint coupling — quantum superposition of genetic material",
        [t for t in Token],
    ),
    ClinkLayer(7, "Tissue/Organ", "O₂",
        '𐑦', '𐑸', '𐑾', '𐑬', '𐑞', '𐑧', '𐑲', '𐑵',
        '⊙', '𐑖', '𐑳', '𐑭',
        "Broadcast composition — one-to-all intercellular signaling",
        [t for t in Token],
    ),
    ClinkLayer(8, "Whole Organism", "O_∞",
        '𐑦', '𐑸', '𐑾', '𐑹', '𐑐', '𐑧', '𐑲', '𐑵',
        '⊙', '𐑫', '𐑳', '𐑟',
        "Full closure — quantum fidelity, eternal chirality, non-Abelian winding",
        [t for t in Token],
    ),
]

# ─── Promotions between layers ─────────────────────────────────

PROMOTION_PATHS = [
    (0, 1, {'K': '𐑘→𐑤'}),
    (1, 2, {'D':'𐑛→𐑼','T':'𐑶→𐑥','R':'𐑩→𐑽','P':'𐑗→𐑿',
            'G':'𐑚→𐑔','C':'𐑜→𐑝','Phi':'𐑢→𐑮','H':'𐑓→𐑒'}),
    (2, 3, {'F':'𐑐→𐑞','K':'𐑤→𐑧','G':'𐑔→𐑲','C':'𐑝→𐑠',
            'Phi':'𐑮→⊙','Omega':'𐑷→𐑭'}),
    (3, 4, {'D':'𐑼→𐑦','T':'𐑥→𐑸','R':'𐑽→𐑾','P':'𐑿→𐑬',
            'H':'𐑓→𐑒'}),
    (4, 5, {'P':'𐑬→𐑹','H':'𐑒→𐑖','F':'𐑞→𐑱'}),
    (5, 6, {'R':'𐑾→𐑽','P':'𐑹→𐑿'}),
    (6, 7, {'R':'𐑽→𐑾','P':'𐑿→𐑬','C':'𐑠→𐑵','F':'𐑱→𐑞'}),
    (7, 8, {'P':'𐑬→𐑹','F':'𐑞→𐑐','H':'𐑖→𐑫','Omega':'𐑭→𐑟'}),
]

# Build reverse map for demotion
DEMOTION_PATHS = {}
for frm, to, promos in PROMOTION_PATHS:
    demos = {}
    for prim, delta in promos.items():
        old_val, new_val = delta.split('→')
        demos[prim] = f"{new_val}→{old_val}"
    DEMOTION_PATHS[(to, frm)] = demos


# ─── CLINK Navigator ──────────────────────────────────────────

class ClinkNavigator:
    """Navigate the 9-layer CLINK chain.

    Programs can descend (compress) or ascend (enrich) through
    the layers. Each transition requires promoting or demoting
    specific primitives.
    """

    def __init__(self):
        self.current_layer: int = 8  # Start at Whole Organism
        self.layer_history: List[int] = [8]

    @property
    def layer(self) -> ClinkLayer:
        return CLINK_CHAIN[self.current_layer]

    def ascend(self) -> bool:
        """Move up one layer (toward Whole Organism)."""
        for frm, to, _ in PROMOTION_PATHS:
            if frm == self.current_layer and to == frm + 1:
                self.current_layer = to
                self.layer_history.append(to)
                return True
        return False

    def descend(self) -> bool:
        """Move down one layer (toward Quarks)."""
        if self.current_layer > 0:
            self.current_layer -= 1
            self.layer_history.append(self.current_layer)
            return True
        return False

    def goto(self, layer_idx: int):
        """Jump to a specific layer."""
        if 0 <= layer_idx <= 8:
            self.current_layer = layer_idx
            self.layer_history.append(layer_idx)
        else:
            raise ValueError(f"Layer {layer_idx} out of range [0,8]")

    def promotions_needed(self, target: int) -> Dict[str, str]:
        """What primitives must change to reach target layer?"""
        if self.current_layer == target:
            return {}
        if target > self.current_layer:
            # Ascending: collect promotions along path
            result = {}
            for layer in range(self.current_layer, target):
                for frm, to, promos in PROMOTION_PATHS:
                    if frm == layer:
                        result.update(promos)
            return result
        else:
            # Descending: collect demotions
            result = {}
            for layer in range(self.current_layer, target, -1):
                key = (layer, layer - 1)
                if key in DEMOTION_PATHS:
                    result.update(DEMOTION_PATHS[key])
            return result

    def is_token_valid(self, tok: Token) -> bool:
        """Check if a token is valid at the current layer."""
        return tok in self.layer.valid_tokens

    def valid_tokens_str(self) -> str:
        return ", ".join(t.name for t in self.layer.valid_tokens)

    def status(self) -> str:
        layer = self.layer
        return (
            f"Layer {layer.index}: {layer.name} [{layer.tier}]\n"
            f"  {layer.tuple_display}\n"
            f"  {layer.description}\n"
            f"  Valid tokens: {self.valid_tokens_str()}"
        )
