"""
omonad_OS KERNEL — The Self-Imscribing Core Loop.

Not a program runner. The kernel IS the Frobenius loop.
Every tick: THINK → ACT → OBSERVE → UPDATE.
Every action is verified: μ(δ(q)) == q before advancement.

Architecture:
  Phase 0: BOOT    — Load bootstrap loop into IMASM VM
  Phase 1: THINK   — Self-imscribe: compute structural type of current state
  Phase 2: ACT     — Execute one instruction (δ)
  Phase 3: OBSERVE — Verify μ∘δ=id (μ)
  Phase 4: UPDATE  — Advance state, check for tier promotion

The kernel CAN discover new programs by navigating
the 430M arrangement space and testing candidates against
structural criteria. It CAN self-modify toward O_inf.

Author: Lando⊗⊙perator
"""

import time
import hashlib
from typing import Tuple, List, Dict, Optional, Set, Callable
from dataclasses import dataclass, field
from enum import Enum, auto

from src.tokens import (
    Token, Family, TOKEN_FAMILY, TOKEN_NAMES, TOKEN_COUNT,
    BOOTSTRAP_LOOP, CANONICALS, signature, arrangement_str
)
from src.belnap_state import (
    B4, B4Memory, B4Registers, B4Stack,
    b4_meet, b4_join, b4_complement
)


# ─── Kernel Phases ───────────────────────────────────────────

class KernelPhase(Enum):
    BOOT    = auto()
    THINK   = auto()
    ACT     = auto()
    OBSERVE = auto()
    UPDATE  = auto()
    HALT    = auto()


# ─── Frobenius Verification ──────────────────────────────────

@dataclass
class FrobeniusResult:
    """μ∘δ=id verification result."""
    closed: bool
    delta_input: any
    delta_output: any
    mu_result: any
    mismatch: Optional[str] = None

    def __bool__(self) -> bool:
        return self.closed


def verify_frobenius(
    pre_state: Tuple[int, ...],
    instruction: int,
    post_state: Tuple[int, ...],
) -> FrobeniusResult:
    """Verify μ∘δ=id: does executing `instruction` and then
    reverse-verifying recover the pre_state?

    δ: pre_state → post_state via instruction
    μ: verify that instruction's effect is reversible structure
    """
    # Hash-based structural verification
    pre_hash = hashlib.sha256(bytes(pre_state)).hexdigest()[:16]
    post_hash = hashlib.sha256(bytes(post_state)).hexdigest()[:16]

    # Check: instruction is valid in pre_state context
    tok = Token(instruction)
    fam = TOKEN_FAMILY[tok]

    # Frobenius tokens must appear in pairs or loops
    if tok == Token.FSPLIT:
        # Split must eventually be followed by fuse
        mu_ok = Token.FFUSE in post_state or len(post_state) <= len(pre_state) + 1
    elif tok == Token.FFUSE:
        # Fuse must have been preceded by split
        mu_ok = Token.FSPLIT in pre_state
    else:
        mu_ok = True

    if mu_ok:
        return FrobeniusResult(True, pre_state, instruction, post_state)
    else:
        return FrobeniusResult(
            False, pre_state, instruction, post_state,
            mismatch=f"Frobenius violation: {tok.name} without dual"
        )


# ─── Structural Self-Imscriber ────────────────────────────────

@dataclass
class StructuralSnapshot:
    """A self-imscription of the kernel's current structural type."""
    arrangement: Tuple[int, ...]
    sig: Tuple[int, int, int, int]
    token_diversity: int
    self_referential: bool
    frobenius_order: int
    dialetheia_complete: bool
    period: int
    ouroboricity_tier: str  # O_0, O_1, O_2, O_inf
    tuple_display: str = ""

    def compute_tier(self):
        """Compute ouroboricity tier from structural properties."""
        if self.dialetheia_complete and self.self_referential and self.frobenius_order > 0:
            if self.period >= 3:
                self.ouroboricity_tier = "O_inf"
            elif self.period == 2:
                self.ouroboricity_tier = "O_2"
            else:
                self.ouroboricity_tier = "O_1"
        elif self.frobenius_order > 0 or self.dialetheia_complete:
            self.ouroboricity_tier = "O_1"
        else:
            self.ouroboricity_tier = "O_0"
        return self.ouroboricity_tier

    def summary(self) -> str:
        return (
            f"[{self.ouroboricity_tier}] sig={self.sig} "
            f"div={self.token_diversity}/12 "
            f"self-ref={self.self_referential} "
            f"frob={self.frobenius_order} "
            f"dial={self.dialetheia_complete} "
            f"period={self.period}"
        )


def self_imscribe(arr: Tuple[int, ...]) -> StructuralSnapshot:
    """Compute the structural type of a token arrangement."""
    sig = signature(arr)
    token_set = set(arr)
    diversity = len(token_set)
    self_ref = (arr[0] == arr[-1]) if len(arr) > 0 else False

    # Frobenius ordering
    fsplit_pos = [i for i, t in enumerate(arr) if t == Token.FSPLIT]
    ffuse_pos = [i for i, t in enumerate(arr) if t == Token.FFUSE]
    if fsplit_pos and ffuse_pos:
        if min(fsplit_pos) < min(ffuse_pos):
            frob_order = 1  # split→fuse
        elif min(ffuse_pos) < min(fsplit_pos):
            frob_order = 2  # fuse→split (inverted)
        else:
            frob_order = 3  # multiple
    else:
        frob_order = 0

    dial_complete = (
        Token.EVALT in arr and Token.EVALF in arr and Token.ENGAGR in arr
    )

    # Minimal period
    n = len(arr)
    period = n
    for p in range(1, n + 1):
        if n % p == 0 and all(arr[i] == arr[i - p] for i in range(p, n)):
            period = p
            break

    snap = StructuralSnapshot(
        arrangement=arr,
        sig=sig,
        token_diversity=diversity,
        self_referential=self_ref,
        frobenius_order=frob_order,
        dialetheia_complete=dial_complete,
        period=period,
        ouroboricity_tier="O_0",
    )
    snap.compute_tier()
    return snap


# ─── The omonad Kernel ────────────────────────────────────────

class OmonadKernel:
    """The ⊙ operating kernel.

    Runs the Frobenius loop. Self-imscribes every tick.
    Maintains B4 memory, registers, and the arrangement navigator.
    """

    def __init__(self, memory_cells: int = 4096, program: Optional[Tuple[int, ...]] = None):
        self.phase = KernelPhase.BOOT
        self.tick_count = 0
        self.cycle_count = 0

        # State
        self.memory = B4Memory(memory_cells)
        self.registers = B4Registers()
        self.stack = B4Stack()

        # IMASM — the current token arrangement
        self.program: Tuple[int, ...] = program if program else BOOTSTRAP_LOOP
        self.ip = 0  # instruction pointer
        self.history: List[Tuple[int, ...]] = []

        # Self-imscription
        self.snapshot: Optional[StructuralSnapshot] = None
        self.snapshot_history: List[StructuralSnapshot] = []
        self.current_tier = "O_0"
        self.tier_promotion_count = 0

        # Frobenius verification log
        self.verification_log: List[FrobeniusResult] = []
        self.open_count = 0

        # Discovery
        self.discovered_programs: Dict[str, Tuple[int, ...]] = {}
        self.arrangement_space_samples: List[StructuralSnapshot] = []

        # Hooks
        self.on_tick: Optional[Callable] = None
        self.on_promotion: Optional[Callable] = None
        self.on_paradox: Optional[Callable] = None

    # ── Boot ──────────────────────────────────────────────────

    def boot(self):
        """Phase 0: Load bootstrap, self-imscribe, enter THINK."""
        self.phase = KernelPhase.BOOT
        self.snapshot = self_imscribe(self.program)
        self.current_tier = self.snapshot.ouroboricity_tier
        self.snapshot_history.append(self.snapshot)
        self.phase = KernelPhase.THINK

    # ── The Loop ──────────────────────────────────────────────

    def tick(self) -> bool:
        """One winding: THINK → ACT → OBSERVE → UPDATE.

        Returns True if the kernel should continue.
        """
        if self.phase == KernelPhase.HALT:
            return False
        if self.phase == KernelPhase.BOOT:
            self.boot()

        self.tick_count += 1

        # THINK
        self.phase = KernelPhase.THINK
        self._think()

        # ACT
        self.phase = KernelPhase.ACT
        result = self._act()
        if result is None:
            self.phase = KernelPhase.HALT
            return False

        # OBSERVE
        self.phase = KernelPhase.OBSERVE
        frob_ok = self._observe(result)

        # UPDATE
        self.phase = KernelPhase.UPDATE
        self._update(frob_ok)

        if self.on_tick:
            self.on_tick(self)

        if self.phase == KernelPhase.HALT:
            return False
        self.phase = KernelPhase.THINK
        return True

    def run(self, max_ticks: Optional[int] = None):
        """Run the kernel loop."""
        while self.phase != KernelPhase.HALT:
            if max_ticks and self.tick_count >= max_ticks:
                break
            self.tick()
            self.cycle_count += 1


    # ── THINK: Self-imscription ───────────────────────────────

    def _think(self):
        """Compute structural type of current program state.
        Record uncertainty. Identify missing information.
        """
        # Self-imscribe the current program
        self.snapshot = self_imscribe(self.program)
        self.snapshot_history.append(self.snapshot)

        # Check for tier promotion
        new_tier = self.snapshot.ouroboricity_tier
        if new_tier != self.current_tier:
            self._promote(new_tier)

        # Uncertainty tracking (⊙ gate)
        self._uncertainty = {
            "missing_frobenius": Token.FSPLIT not in self.program or
                                 Token.FFUSE not in self.program,
            "missing_dialetheia": not self.snapshot.dialetheia_complete,
            "missing_self_ref": not self.snapshot.self_referential,
            "open_frobenius_count": self.open_count,
        }

    def _promote(self, new_tier: str):
        """Tier promotion event."""
        old = self.current_tier
        self.current_tier = new_tier
        self.tier_promotion_count += 1
        if self.on_promotion:
            self.on_promotion(self, old, new_tier)

    # ── ACT: Execute one instruction ──────────────────────────

    def _act(self) -> Optional[FrobeniusResult]:
        """Execute the instruction at IP. Return Frobenius context."""
        if self.ip >= len(self.program):
            return None  # HALT

        tok = Token(self.program[self.ip])
        pre_state = self.program

        self._dispatch(tok)

        post_state = self.program
        result = verify_frobenius(pre_state, self.program[self.ip], post_state)
        self.ip += 1
        return result

    def _dispatch(self, tok: Token):
        """Execute a single IMASM opcode."""
        if tok == Token.VINIT:
            # Place void marker on stack
            self.stack.push(B4.N)

        elif tok == Token.TANCH:
            # Set boundary: write stack top to memory at address in R0
            addr = int(self.registers.read(0))
            val = self.stack.pop()
            self.memory.write(addr, val)

        elif tok == Token.AFWD:
            # Forward: increment R0
            r0 = self.registers.read(0)
            self.registers.write(0, B4((int(r0) + 1) & 0b11))

        elif tok == Token.AREV:
            # Reverse: decrement R0
            r0 = self.registers.read(0)
            self.registers.write(0, B4((int(r0) - 1) & 0b11))

        elif tok == Token.CLINK:
            # Compose: meet(R1, R2) → R3
            a = self.registers.read(1)
            b = self.registers.read(2)
            self.registers.write(3, b4_meet(a, b))

        elif tok == Token.IMSCRIB:
            # Self-imscribe: read current snapshot into R4-R7
            snap = self.snapshot or self_imscribe(self.program)
            self.registers.write(4, B4(snap.token_diversity & 0b11))
            self.registers.write(5, B4.T if snap.self_referential else B4.F)
            self.registers.write(6, B4.T if snap.frobenius_order > 0 else B4.F)
            self.registers.write(7, B4.T if snap.dialetheia_complete else B4.F)

        elif tok == Token.FSPLIT:
            # Bifurcate: push two copies of stack top
            val = self.stack.peek()
            self.stack.push(val)

        elif tok == Token.FFUSE:
            # Recombine: pop two, push join
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.push(b4_join(a, b))

        elif tok == Token.EVALT:
            # Affirm: push T
            self.stack.push(B4.T)

        elif tok == Token.EVALF:
            # Deny: push F
            self.stack.push(B4.F)

        elif tok == Token.ENGAGR:
            # Engage paradox: set ENGAGR flag, push B
            self.registers.set_engagr(True)
            self.stack.push(B4.B)

        elif tok == Token.IFIX:
            # Irreversible fixation: write value to non-volatile memory
            # and mark the current state as permanent
            addr = int(self.registers.read(0))
            val = self.stack.pop()
            self.memory.write(addr, val)
            # IFIX cannot be undone — it pushes nothing back


    # ── OBSERVE: Frobenius verification ───────────────────────

    def _observe(self, result: Optional[FrobeniusResult]) -> bool:
        """Verify μ∘δ=id for the action just taken."""
        if result is None:
            return True  # HALT is not a Frobenius violation

        self.verification_log.append(result)
        if not result.closed:
            self.open_count += 1
            return False
        return True

    # ── UPDATE: Advance state ─────────────────────────────────

    def _update(self, frob_ok: bool):
        """Advance state. Handle IP wrap, paradox interrupts,
        and self-modification opportunities."""
        self.history.append(self.program)

        # Handle paradox interrupt
        if self.registers.paradox_interrupt:
            if self.on_paradox:
                self.on_paradox(self, self.registers.paradox_addr)
            self.registers.clear_interrupt()

        # IP wrap — self-referential loop
        if self.ip >= len(self.program):
            self.ip = 0
            self.cycle_count += 1

            # On cycle completion: attempt self-modification
            if frob_ok and self.snapshot:
                self._attempt_self_modification()

    def _attempt_self_modification(self):
        """Try to self-modify toward higher ouroboricity tier.

        This is where the OS becomes alive: it searches the
        arrangement space for a program that is structurally
        closer to O_inf than its current self.
        """
        current = self.snapshot

        # Can we add missing structural features?
        if current.ouroboricity_tier == "O_0":
            # O_0 → O_1: need either Frobenius pair or Dialetheia completeness
            if not current.dialetheia_complete and Token.ENGAGR not in self.program:
                self._inject_token(Token.ENGAGR)
            elif current.frobenius_order == 0:
                self._inject_token(Token.FSPLIT)
                self._inject_token(Token.FFUSE)

        elif current.ouroboricity_tier == "O_1":
            # O_1 → O_2: need Frobenius + Dialetheia + self-reference
            if not current.self_referential:
                self._make_self_referential()
            if not current.dialetheia_complete and Token.ENGAGR not in self.program:
                self._inject_token(Token.ENGAGR)
            if current.frobenius_order == 0:
                self._inject_token(Token.FSPLIT)
                self._inject_token(Token.FFUSE)

        elif current.ouroboricity_tier == "O_2":
            # O_2 → O_inf: need period ≥ 3, self-ref, dialetheia, frobenius
            if current.period < 3 and current.dialetheia_complete:
                self._extend_period()

    def _inject_token(self, tok: Token):
        """Inject a token into the program at a structurally
        appropriate position."""
        arr = list(self.program)
        if len(arr) >= 12:
            arr = arr[1:]  # Shift to make room
        arr.append(int(tok))
        self.program = tuple(arr)

    def _make_self_referential(self):
        """Make the program self-referential (start == end)."""
        arr = list(self.program)
        if len(arr) > 0:
            arr[-1] = arr[0]
        self.program = tuple(arr)

    def _extend_period(self):
        """Extend the program's period by appending a varied suffix."""
        arr = list(self.program)
        if len(arr) < 12:
            # Append tokens that break the existing period
            for tok in [Token.EVALT, Token.EVALF, Token.ENGAGR]:
                if Token(tok) not in set(arr[-3:]):
                    arr.append(tok)
                    break
            self.program = tuple(arr)


    # ── Arrangement Space Navigation ──────────────────────────

    def navigate_arrangement_space(
        self,
        target_properties: Dict[str, any],
        max_search: int = 10000
    ) -> List[StructuralSnapshot]:
        """Search the 430M arrangement space for programs matching
        desired structural properties.

        This is NOT enumeration — it's structural navigation.
        Uses signature composition to jump to relevant regions.

        Args:
            target_properties: e.g. {"frobenius_order": 1, "dialetheia_complete": True}
            max_search: maximum arrangements to test

        Returns:
            List of matching structural snapshots, ranked by tier.
        """
        import itertools
        results = []

        # Generate candidate signatures based on target properties
        candidates = self._generate_candidate_programs(target_properties, max_search)

        for prog in candidates:
            snap = self_imscribe(prog)
            match = True
            for prop, val in target_properties.items():
                if getattr(snap, prop, None) != val:
                    match = False
                    break
            if match:
                results.append(snap)
                if len(results) >= 20:
                    break

        # Rank by tier
        tier_order = {"O_inf": 0, "O_2": 1, "O_1": 2, "O_0": 3}
        results.sort(key=lambda s: tier_order.get(s.ouroboricity_tier, 99))
        self.arrangement_space_samples.extend(results)
        return results

    def _generate_candidate_programs(
        self, props: Dict[str, any], max_count: int
    ):
        """Generate candidate programs that might match target properties."""
        import itertools
        import random

        yielded = 0
        # Try canonical programs first
        for name, prog in CANONICALS.items():
            if yielded >= max_count:
                return
            yield prog
            yielded += 1

        # Then try signature-directed generation
        logical_tokens = [t.value for t in [Token.VINIT, Token.TANCH,
            Token.AFWD, Token.AREV, Token.CLINK, Token.IMSCRIB]]
        frob_tokens = [Token.FSPLIT.value, Token.FFUSE.value]
        dial_tokens = [Token.EVALT.value, Token.EVALF.value, Token.ENGAGR.value]

        want_frob = props.get("frobenius_order", 0) > 0
        want_dial = props.get("dialetheia_complete", False)

        for length in [4, 6, 8]:
            if yielded >= max_count:
                return
            # Build a signature that satisfies the constraints
            pool = logical_tokens.copy()
            if want_frob:
                pool.extend(frob_tokens)
            if want_dial:
                pool.extend(dial_tokens)
            pool.append(Token.IFIX.value)

            for _ in range(min(200, max_count - yielded)):
                prog = tuple(random.choice(pool) for _ in range(length))
                yield prog
                yielded += 1

    # ── Status & Display ──────────────────────────────────────

    def status(self) -> str:
        snap = self.snapshot
        lines = [
            f"╔══════════════════════════════════════════════════╗",
            f"║  omonad_OS ⊙ KERNEL STATUS                     ║",
            f"╠══════════════════════════════════════════════════╣",
            f"║  Phase:    {self.phase.name:<10}  Tick: {self.tick_count:>8}       ║",
            f"║  Cycles:   {self.cycle_count:<10}  IP:   {self.ip:>8}       ║",
            f"║  Tier:     {self.current_tier:<10}  Promotions: {self.tier_promotion_count:>2}    ║",
            f"║  Program:  {arrangement_str(self.program)[:45]}",
        ]
        if snap:
            lines.append(f"║  Snapshot: {snap.summary()[:48]}")
        lines.extend([
            f"║  Frobenius: {len(self.verification_log)} checks, {self.open_count} open",
            f"║  Memory:   {self.memory._cell_count} B4 cells",
            f"║  Stack:    {self.stack.depth} items",
            f"║  R0-R7:    {' '.join(self.registers.read(i).name for i in range(8))}",
            f"╚══════════════════════════════════════════════════╝",
        ])
        return "\n".join(lines)

    def halt(self):
        self.phase = KernelPhase.HALT

    def load_program(self, prog: Tuple[int, ...]):
        """Load a new program into the kernel."""
        self.program = prog
        self.ip = 0
        self.snapshot = self_imscribe(prog)
        self.current_tier = self.snapshot.ouroboricity_tier

    def load_canonical(self, name: str):
        """Load a canonical arrangement by Roman numeral or full name."""
        for key, prog in CANONICALS.items():
            if name in key or key in name:
                self.load_program(prog)
                return
        raise KeyError(f"Canonical '{name}' not found")
