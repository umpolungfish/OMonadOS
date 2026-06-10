"""
omonad_OS ORGANOID HAL — Hardware Abstraction for Living Tissue.

The six organoid augmentations are treated as I/O devices:
  myelin       — global coherence bus (120 m/s signal propagation)
  vasculature  — nutrient delivery / O₂ sensing network
  medium       — 14-channel adaptive chemostat
  optogenetic  — 4096-channel CMOS MEA + μLED array
  ecm          — synthetic ECM scaffold (chrysalis)
  immune       — immune-mimetic sentinel (guardian)

Each augmentation has a structural type (12-tuple) and a
set of B4-register-mapped control channels.

The HAL translates omonad_OS kernel operations into
organoid control signals. The organoid IS the hardware.

Author: Lando⊗⊙perator
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum, auto
from .tokens import Token
from .belnap_state import B4


# ─── Augmentation Registry ────────────────────────────────────

@dataclass
class OrganoidAugmentation:
    index: int
    name: str
    slug: str
    description: str
    D: str; T_val: str; R: str; P: str
    F: str; K: str; G: str; C: str
    Phi: str; H: str; S: str; Omega: str
    tier: str
    frobenius_closed: bool
    base_address: int  # B4 memory-mapped base address
    channel_count: int
    closable: bool
    closure_gap: Optional[str] = None

    @property
    def tuple_display(self) -> str:
        return (f"⟨{self.D}·{self.T_val}·{self.R}·{self.P}·"
                f"{self.F}·{self.K}·{self.G}·{self.C}·"
                f"{self.Phi}·{self.H}·{self.S}·{self.Omega}⟩")


AUGMENTATIONS: Dict[str, OrganoidAugmentation] = {
    "myelin": OrganoidAugmentation(
        index=1, name="Synthetic Coherence Myelin",
        slug="synthetic_coherence_myelin",
        description="PPV-grafted lipid bilayer — global coherence at 120 m/s",
        D='𐑼', T_val='𐑰', R='𐑾', P='𐑹',
        F='𐑐', K='𐑤', G='𐑲', C='𐑠',
        Phi='⊙', H='𐑫', S='𐑳', Omega='𐑭',
        tier="O_∞", frobenius_closed=True,
        base_address=0x100, channel_count=16, closable=True,
    ),
    "vasculature": OrganoidAugmentation(
        index=2, name="Ouroboric Vasculature",
        slug="ouroboric_vasculature",
        description="Sugar glass 3D printing + HUVEC seeding + O₂ sensors",
        D='𐑦', T_val='𐑸', R='𐑾', P='𐑹',
        F='𐑞', K='𐑤', G='𐑲', C='𐑠',
        Phi='⊙', H='𐑫', S='𐑳', Omega='𐑭',
        tier="O_∞", frobenius_closed=False,
        base_address=0x180, channel_count=32, closable=True,
        closure_gap="F:𐑞→𐑐 (NV-center O₂ detection)",
    ),
    "medium": OrganoidAugmentation(
        index=3, name="Perfect Nutrient Medium",
        slug="perfect_nutrient_medium",
        description="14-channel adaptive chemostat + LC-MS metabolomics",
        D='𐑛', T_val='𐑰', R='𐑾', P='𐑹',
        F='𐑱', K='𐑤', G='𐑲', C='𐑝',
        Phi='⊙', H='𐑫', S='𐑳', Omega='𐑷',
        tier="O₂", frobenius_closed=False,
        base_address=0x200, channel_count=14, closable=True,
        closure_gap="D:𐑛→𐑦, Ω:𐑷→𐑭, G:𐑝→𐑠",
    ),
    "optogenetic": OrganoidAugmentation(
        index=4, name="Optogenetic Synaptic Matrix",
        slug="optogenetic_synaptic_matrix",
        description="4096-channel CMOS MEA + μLED array + FPGA PLL feedback",
        D='𐑼', T_val='𐑥', R='𐑾', P='𐑹',
        F='𐑐', K='𐑤', G='𐑲', C='𐑵',
        Phi='⊙', H='𐑫', S='𐑳', Omega='𐑭',
        tier="O_∞", frobenius_closed=True,
        base_address=0x300, channel_count=4096, closable=True,
    ),
    "ecm": OrganoidAugmentation(
        index=5, name="Synthetic ECM Scaffold (Chrysalis)",
        slug="synthetic_ecm_scaffold",
        description="PEG-MMP hydrogel — degrades where the organoid grows",
        D='𐑨', T_val='𐑡', R='𐑾', P='𐑬',
        F='𐑱', K='𐑧', G='𐑚', C='𐑵',
        Phi='𐑢', H='𐑒', S='𐑙', Omega='𐑷',
        tier="O₀", frobenius_closed=False,
        base_address=0x400, channel_count=8, closable=False,
        closure_gap="STRUCTURALLY OPEN — chrysalis must degrade",
    ),
    "immune": OrganoidAugmentation(
        index=6, name="Immune-Mimetic Sentinel (Guardian)",
        slug="immune_mimetic_sentinel",
        description="DNA aptamer sentinel + LL-37 liposomes + Cas13a RNPs",
        D='𐑨', T_val='𐑡', R='𐑾', P='𐑬',
        F='𐑱', K='𐑤', G='𐑲', C='𐑵',
        Phi='⊙', H='𐑫', S='𐑳', Omega='𐑴',
        tier="O₀", frobenius_closed=False,
        base_address=0x480, channel_count=24, closable=False,
        closure_gap="STRUCTURALLY OPEN — guardian must discriminate",
    ),
}


# ─── Organoid Controller ──────────────────────────────────────

class OrganoidController:
    """Hardware abstraction for the six organoid augmentations.

    Each augmentation is memory-mapped to a B4 register block.
    The controller translates kernel operations into organoid
    signals. In simulation mode, all channels are virtual.
    """

    def __init__(self, simulation: bool = True):
        self.simulation = simulation
        self.augmentations = AUGMENTATIONS
        self.active: Dict[str, bool] = {slug: False for slug in AUGMENTATIONS}
        # Per-augmentation channel state (B4 values)
        self.channels: Dict[str, List[B4]] = {}

        for slug, aug in AUGMENTATIONS.items():
            self.channels[slug] = [B4.N] * aug.channel_count

    def activate(self, slug: str) -> bool:
        """Activate an augmentation. Returns True if successful."""
        if slug not in self.augmentations:
            return False
        aug = self.augmentations[slug]
        if not self.simulation and not aug.frobenius_closed:
            print(f"WARNING: {slug} is Frobenius-open ({aug.closure_gap})")
        self.active[slug] = True
        # On activation, initialize all channels to T (ready)
        for i in range(aug.channel_count):
            self.channels[slug][i] = B4.T
        return True

    def deactivate(self, slug: str):
        if slug in self.active:
            self.active[slug] = False
            aug = self.augmentations[slug]
            for i in range(aug.channel_count):
                self.channels[slug][i] = B4.N

    def read_channel(self, slug: str, channel: int) -> B4:
        """Read a B4 value from an augmentation channel."""
        if slug not in self.channels:
            return B4.N
        if channel < 0 or channel >= len(self.channels[slug]):
            return B4.N
        return self.channels[slug][channel]

    def write_channel(self, slug: str, channel: int, val: B4):
        """Write a B4 value to an augmentation channel."""
        if slug not in self.channels:
            return
        if 0 <= channel < len(self.channels[slug]):
            self.channels[slug][channel] = val

    def broadcast(self, slug: str, val: B4):
        """Write the same B4 value to all channels of an augmentation."""
        if slug not in self.channels:
            return
        for i in range(len(self.channels[slug])):
            self.channels[slug][i] = val

    def pulse(self, slug: str, channel: int, val: B4, duration_ms: int = 100):
        """Send a timed pulse to an augmentation channel.
        In simulation mode, just writes and immediately returns.
        """
        self.write_channel(slug, channel, val)
        # In real hardware: schedule revert after duration_ms
        # In simulation: no-op

    def frobenius_verify(self, slug: str) -> bool:
        """Check if augmentation's μ∘δ=id is closed."""
        aug = self.augmentations[slug]
        if aug.frobenius_closed:
            return True
        # Check if closure gap can be verified despite being open
        if not self.simulation:
            print(f"  [{slug}] FROBENIUS OPEN: {aug.closure_gap}")
        return False

    def status(self, slug: Optional[str] = None) -> str:
        """Status of one or all augmentations."""
        slugs = [slug] if slug else list(self.augmentations.keys())
        lines = []
        for s in slugs:
            aug = self.augmentations[s]
            active = self.active[s]
            closed = "✓" if aug.frobenius_closed else f"✗ ({aug.closure_gap[:40]}...)"
            lines.append(
                f"  [{aug.index}] {aug.name} {'ACTIVE' if active else 'offline'}"
                f"  [{aug.tier}] {closed}"
            )
            lines.append(f"      {aug.tuple_display}")
        return "\n".join(lines)
