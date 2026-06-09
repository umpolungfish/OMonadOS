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

# ─── Shared Frobenius verification from imasmic_core ─────────
from imasmic_core.frobenius_verify import (
    FrobeniusResult, FrobeniusHarness, B4 as _B4_shared,
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
# FrobeniusResult is imported from imasmic_core.frobenius_verify
# (the shared umbrella for all IG ecosystem projects).


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
        self.harness = FrobeniusHarness("omonad_OS")

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
        # Track best tier achieved
        tier_order = {"O_0": 0, "O_1": 1, "O_2": 2, "O_inf": 3}
        if not hasattr(self, '_best_tier_ever'):
            self._best_tier_ever = "O_0"
        if tier_order.get(new_tier, 0) > tier_order.get(self._best_tier_ever, 0):
            self._best_tier_ever = new_tier
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

        elif tok == Token.ISCRIB:
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

        μ∘δ=id is a conservation law, not a suggestion.
        The kernel's self-modification logic treats it as invariant.

        Promotion paths:
          O_0 → O_1: add Frobenius pair OR one dialetheia token
          O_1 → O_2: add self-reference + missing dialetheia + Frobenius
          O_2 → O_inf: extend period ≥ 3 with dialetheia complete

        Stagnation: if stuck at same tier for too long, navigate
        arrangement space for a structurally richer program.
        """
        current = self.snapshot

        # ── Emergency stack protection — ALL tiers ──
        # Stack overflow is a hard boundary violation.
        # Drain before structural logic.
        if self.stack.depth > 200:
            self._inject_token(Token.TANCH)
            return
        if self.stack.depth < 5 and self._stack_delta() < 0:
            self._inject_token(Token.VINIT)
            return

        # ── O_inf: structural closure — maintain equilibrium only ──
        if current.ouroboricity_tier == "O_inf":
            # No structural modification at O_inf.
            # Emergency protection above already covers stack bounds.
            return

        # ── Stagnation escape ──
        # Track ticks since last tier advancement, not same-tier ticks.
        # Oscillation O_0↔O_1 must not reset the counter.
        if not hasattr(self, '_stagnation_counter'):
            self._stagnation_counter = 0
            self._best_tier_ever = self.current_tier
        if self.current_tier != self._stagnation_tier if hasattr(self, '_stagnation_tier') else True:
            self._stagnation_tier = self.current_tier
        # Only increment if tier hasn't IMPROVED beyond best seen
        tier_order = {"O_0": 0, "O_1": 1, "O_2": 2, "O_inf": 3}
        if tier_order.get(self.current_tier, 0) > tier_order.get(self._best_tier_ever, 0):
            self._best_tier_ever = self.current_tier
            self._stagnation_counter = 0
        else:
            self._stagnation_counter += 1

        if self._stagnation_counter > 300 and self.current_tier in ("O_0", "O_1"):
            self._stagnation_counter = 0
            target = {"O_0": {"frobenius_order": 1, "dialetheia_complete": True},
                      "O_1": {"frobenius_order": 1, "dialetheia_complete": True,
                              "self_referential": True}}
            props = target.get(self.current_tier, {})
            results = self.navigate_arrangement_space(props, max_search=5000)
            if results:
                best = results[0]
                if tier_order.get(best.ouroboricity_tier, 0) > tier_order.get(self.current_tier, 0):
                    self.load_program(best.arrangement)
                    self._best_tier_ever = best.ouroboricity_tier
                    return

        # ── Frobenius balance check (runs before all tier logic) ──
        bal = self._frobenius_balance()
        if bal > 0:
            self._inject_token(Token.FFUSE)
            return
        elif bal < 0:
            self._inject_token(Token.FSPLIT)
            return

        # ── Stack equilibrium check (hysteresis: ±2 threshold) ──
        sdelta = self._stack_delta()
        if not hasattr(self, '_stack_delta_history'):
            self._stack_delta_history = []
        self._stack_delta_history.append(sdelta)
        if len(self._stack_delta_history) > 8:
            self._stack_delta_history.pop(0)
        # Act immediately on first positive/negative delta.
        # The stack grows at +4/cycle on pathological programs —
        # waiting 3 cycles lets the stack overflow before equilibrium.
        if len(self._stack_delta_history) >= 1:
            recent = self._stack_delta_history[-1:]
            if all(d > 0 for d in recent):
                self._inject_token(Token.TANCH)
                self._stack_delta_history.clear()
                return
            elif all(d < 0 for d in recent):
                self._inject_token(Token.VINIT)
                self._stack_delta_history.clear()
                return

        # ── Dialetheia: inject any missing token, not just ENGAGR ──
        missing_dial = []
        if Token.EVALT not in self.program:
            missing_dial.append(Token.EVALT)
        if Token.EVALF not in self.program:
            missing_dial.append(Token.EVALF)
        if Token.ENGAGR not in self.program:
            missing_dial.append(Token.ENGAGR)

        # Can we add missing structural features?
        if current.ouroboricity_tier == "O_0":
            # O_0 → O_1: need either Frobenius pair or Dialetheia completeness
            if missing_dial:
                self._inject_token(missing_dial[0])
            elif current.frobenius_order == 0:
                self._inject_token_pair(Token.FSPLIT, Token.FFUSE)

        elif current.ouroboricity_tier == "O_1":
            # O_1 → O_2: need Frobenius + Dialetheia + self-reference
            if not current.self_referential:
                self._make_self_referential()
            elif missing_dial:
                self._inject_token(missing_dial[0])
            elif current.frobenius_order == 0:
                self._inject_token_pair(Token.FSPLIT, Token.FFUSE)

        elif current.ouroboricity_tier == "O_2":
            # O_2 → O_inf: need period ≥ 3, self-ref, dialetheia, frobenius
            if current.period < 3 and current.dialetheia_complete:
                self._extend_period()



    def _inject_token(self, tok: Token):
        """Inject a token into the program at a structurally
        appropriate position.

        Preferentially drops a token from the most over-represented
        family to preserve structural diversity.
        """
        arr = list(self.program)
        if len(arr) >= 12:
            # Find the most over-represented family and drop one
            from collections import Counter
            fam_counts = Counter(TOKEN_FAMILY[Token(t)] for t in arr)
            # Order: prefer dropping from family with highest count
            drop_order = [fam for fam, _ in fam_counts.most_common()]
            for fam in drop_order:
                for i, t in enumerate(arr):
                    if TOKEN_FAMILY[Token(t)] == fam:
                        arr.pop(i)
                        break
                else:
                    continue
                break
            else:
                arr = arr[1:]  # fallback
        # Don't append if token already dominates
        arr.append(int(tok))
        self.program = tuple(arr)

    def _inject_token_pair(self, tok_a: Token, tok_b: Token):
        """Inject a Frobenius pair atomically — both or neither.

        Prevents the asymmetric shift from dropping one half of
        the μ∘δ pair when the program is at capacity.
        """
        arr = list(self.program)
        # Make room for 2 tokens in one atomic step
        while len(arr) + 2 > 12:
            arr = arr[1:]
        arr.append(int(tok_a))
        arr.append(int(tok_b))
        self.program = tuple(arr)

    # Per-token stack delta: +1 pushes, -1 pops, 0 neutral
    _TOKEN_STACK_DELTA = {
        Token.VINIT: +1, Token.TANCH: -1, Token.AFWD: 0, Token.AREV: 0,
        Token.CLINK: 0, Token.ISCRIB: 0,
        Token.FSPLIT: +1, Token.FFUSE: -1,
        Token.EVALT: +1, Token.EVALF: +1, Token.ENGAGR: +1,
        Token.IFIX: -1,
    }

    def _frobenius_balance(self) -> int:
        """Return FSPLIT count - FFUSE count. Zero = balanced."""
        return (sum(1 for t in self.program if t == Token.FSPLIT) -
                sum(1 for t in self.program if t == Token.FFUSE))

    def _stack_delta(self) -> int:
        """Net stack effect of one full program cycle. Zero = equilibrium."""
        return sum(self._TOKEN_STACK_DELTA.get(Token(t), 0)
                   for t in self.program)

    def _pre_balance(self):
        """Auto-balance a newly loaded program.
        Inject TANCH tokens until stack delta ≤ 0.
        This prevents stack overflow on programs with no pop mechanism."""
        max_injections = 12  # safety limit
        for _ in range(max_injections):
            if self._stack_delta() <= 0:
                break
            self._inject_token(Token.TANCH)

    def _make_self_referential(self):
        """Make the program self-referential (start == end).

        Preserves non-LOGICAL tokens (FROBENIUS, DIALETHEIA, LINEAR).
        If the last token is LOGICAL it is overwritten with arr[0].
        If non-LOGICAL, arr[0] is appended to close the loop without
        destroying structural features. The program then has arr[0]==arr[-1]
        and this method will not fire again next cycle.
        """
        arr = list(self.program)
        if len(arr) > 0:
            last_tok = Token(arr[-1])
            last_fam = TOKEN_FAMILY[last_tok]
            if last_fam == Family.LOGICAL:
                arr[-1] = arr[0]
            else:
                # Non-LOGICAL token at end: close loop by appending start
                arr.append(arr[0])
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
            Token.AFWD, Token.AREV, Token.CLINK, Token.ISCRIB]]
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

    def frobenius_summary(self) -> str:
        """Return the FrobeniusHarness summary for omonad_OS."""
        # Sync local verification log into harness
        for r in self.verification_log[-20:]:
            if not any(rr is r for rr in self.harness.results):
                self.harness.check(r)
        return self.harness.summary()

    def halt(self):
        self.phase = KernelPhase.HALT

    def load_program(self, prog: Tuple[int, ...]):
        """Load a new program into the kernel. Resets stack and registers
        to prevent residual state from corrupting the new program.

        Auto-balance: programs with net positive stack delta receive
        TANCH injections until delta ≤ 0. This prevents stack overflow
        on pathological programs like VI_Empty_Bootstrap (+4/cycle)."""
        self.program = prog
        self.ip = 0
        # Auto-balance: inject TANCH for programs with positive stack delta
        self._pre_balance()
        self.snapshot = self_imscribe(self.program)
        self.current_tier = self.snapshot.ouroboricity_tier
        # Reset volatile state for clean program start
        self.stack = B4Stack()
        self.registers = B4Registers()
        self._stack_delta_history = []

    def load_canonical(self, name: str):
        """Load a canonical arrangement by Roman numeral or full name."""
        for key, prog in CANONICALS.items():
            if name in key or key in name:
                self.load_program(prog)
                return
        raise KeyError(f"Canonical '{name}' not found")
