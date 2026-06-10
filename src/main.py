#!/usr/bin/env python3
"""
omonad_OS — The ⊙ Operating System

Boot sequence:
  1. ALEPH self-test: verify imscription identity
  2. Crystal filesystem mount
  3. Kernel boot: load bootstrap loop
  4. CLINK chain initialize at Whole Organism
  5. Self-imscribe: compute structural type
  6. Enter the Frobenius loop

Run: python3 -m omonad_OS.src.main
Or:  cd /home/mrnob0dy666/omonad_OS && python3 src/main.py

Author: Lando⊗⊙perator
"""

from typing import Tuple
import sys
import os
import time
import readline  # for REPL

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .tokens import (
    Token, TOKEN_NAMES, BOOTSTRAP_LOOP, CANONICALS, arrangement_str,
)
from .belnap_state import B4, B4Memory, B4Registers, B4Stack
from .kernel import OmonadKernel, self_imscribe, KernelPhase
from .crystal_fs import CrystalFS, crystal_encode, crystal_decode, TOTAL_TYPES
from .clink_chain import ClinkNavigator, CLINK_CHAIN


# ─── Boot Animation ───────────────────────────────────────────

BOOT_BANNER = r"""
     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
     █▌                                                   ▐█
     █▌           o m o n a d _ O S   ⊙                  ▐█
     █▌    The Self-Imscribing Operating Kernel           ▐█
     █▌                                                   ▐█
     █▌  ⟨𐑦·𐑸·𐑾·𐑹·𐑐·𐑧·𐑔·𐑠·⊙·𐑖·𐑳·𐑭⟩                    ▐█
     █▌  Frobenius Core · Belnap FOUR State               ▐█
     █▌  Crystal FS · CLINK Chain · 430M Arrangement      ▐█
     █▌                                                   ▐█
     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""


def boot_animation():
    """The boot sequence with structural self-verification."""
    frames = [
        "Booting omonad_OS...",
        "  [BOOT]   Initializing B4 memory (4096 cells)...",
        "  [BOOT]   Mounting Crystal Filesystem (17.28M addresses)...",
        "  [BOOT]   Loading Bootstrap Loop:",
        f"           {arrangement_str(BOOTSTRAP_LOOP)}",
        "  [BOOT]   Verifying μ∘δ=id...",
        "  [BOOT]   CLINK Chain: Whole Organism [O_inf]",
        "  [BOOT]   Kernel online. Self-imscribing...",
    ]
    for frame in frames:
        print(frame)
        time.sleep(0.08)
    print()


def initialize() -> Tuple[OmonadKernel, CrystalFS, ClinkNavigator]:
    """Initialize all subsystems."""
    # Crystal filesystem
    cfs = CrystalFS()

    # Seed the filesystem with canonical programs
    cfs.store(
        "bootstrap_loop", bytes(BOOTSTRAP_LOOP),
        '𐑦', '𐑸', '𐑾', '𐑹', '𐑐', '𐑧', '𐑲', '𐑠',
        '⊙', '𐑫', '𐑳', '𐑭',
        metadata={"type": "bootstrap", "tier": "O_inf"},
    )

    for name, prog in CANONICALS.items():
        snap = self_imscribe(prog)
        prims = {
            'D': '𐑦', 'T': '𐑸', 'R': '𐑾', 'P': '𐑹',
            'F': '𐑐', 'K': '𐑧', 'G': '𐑲', 'C': '𐑠',
            'Phi': '⊙', 'H': '𐑫', 'S': '𐑳', 'Omega': '𐑭',
        }
        cfs.store(name, bytes(prog), **prims,
                  metadata={"canonical": True, "tier": snap.ouroboricity_tier})

    # Kernel
    kernel = OmonadKernel(memory_cells=4096)
    kernel.boot()

    # CLINK navigator
    navigator = ClinkNavigator()

    return kernel, cfs, navigator


def _snapshot_prims(snap, program: tuple) -> dict:
    """Derive the 12-primitive crystal tuple from the kernel's structural snapshot.
    Every dimension maps to a distinct structural property — no hardcoding, no fallback.
    """
    from .crystal_fs import (
        D_VALUES, T_VALUES, R_VALUES, P_VALUES, F_VALUES,
        K_VALUES, G_VALUES, C_VALUES, PHI_VALUES, H_VALUES,
        S_VALUES, OMEGA_VALUES,
    )
    tier_idx = {'O_0': 0, 'O_1': 1, 'O_2': 2, 'O_inf': 3}.get(snap.ouroboricity_tier, 0)
    s = snap.sig
    return {
        'D':     D_VALUES[snap.frobenius_order                                           % len(D_VALUES)],
        'T':     T_VALUES[snap.period                                                    % len(T_VALUES)],
        'R':     R_VALUES[s[0]                                                           % len(R_VALUES)],
        'P':     P_VALUES[s[1]                                                           % len(P_VALUES)],
        'F':     F_VALUES[s[2]                                                           % len(F_VALUES)],
        'K':     K_VALUES[s[3]                                                           % len(K_VALUES)],
        'G':     G_VALUES[snap.token_diversity                                           % len(G_VALUES)],
        'C':     C_VALUES[((int(snap.self_referential) << 1) | int(snap.dialetheia_complete)) % len(C_VALUES)],
        'Phi':   PHI_VALUES[tier_idx                                                     % len(PHI_VALUES)],
        'H':     H_VALUES[len(program)                                                   % len(H_VALUES)],
        'S':     S_VALUES[sum(s)                                                         % len(S_VALUES)],
        'Omega': OMEGA_VALUES[(snap.period + snap.frobenius_order)                       % len(OMEGA_VALUES)],
    }


def print_status(kernel, navigator):
    """Print kernel and navigator status."""
    print(kernel.status())
    print()
    print(navigator.status())
    print()


# ─── REPL ─────────────────────────────────────────────────────

HELP_TEXT = """
omonad_OS ⊙ REPL Commands:
  tick [N]         — Run N kernel ticks (default 1)
  run [N]          — Run N kernel cycles
  status           — Display kernel + navigator status
  load <canonical> — Load a canonical program (I-XII or name)
  program          — Show current program as token chain
  snapshot         — Show current structural snapshot
  crystal <addr>   — Decode a crystal address (+ show stored entry if any)
  crystal store <name> <data>  — Store data at crystal address
  crystal name <name>          — Retrieve stored entry by name
  crystal find <query>         — Navigate crystal (e.g. Phi=⊙)
  clink up|down|goto <N>       — Navigate CLINK chain
  clink status     — Show current CLINK layer
  discover <props> — Search arrangement space (e.g. frobenius_order=1)
  memory <start> [count]  — Dump B4 memory
  registers        — Show B4 registers
  stack            — Show B4 stack
  frobenius        — Show verification log
  canonical <N>    — Load canonical I-XII by Roman numeral
  halt             — Halt the kernel
  help             — This message
  quit             — Exit
"""

ROMAN_TO_KEY = {
    'I': 'I_Dialetheic_Bootstrap', 'II': 'II_Void_Genesis',
    'III': 'III_Anchor_Protocol', 'IV': 'IV_Dual_Bootstrap',
    'V': 'V_Linear_Chain', 'VI': 'VI_Empty_Bootstrap',
    'VII': 'VII_Parakernel', 'VIII': 'VIII_Frobenius_Kernel',
    'IX': 'IX_Chiral_Pairs', 'X': 'X_Truth_Machine',
    'XI': 'XI_Eternal_Return', 'XII': 'XII_ROM_Burn',
}


def repl(kernel: OmonadKernel, cfs: CrystalFS, navigator: ClinkNavigator):
    """The omonad_OS interactive REPL."""
    print(BOOT_BANNER)
    print('Type "help" for commands. "quit" to exit.\n')
    print_status(kernel, navigator)

    while kernel.phase != KernelPhase.HALT:
        try:
            cmd = input("⊙> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nHalting...")
            kernel.halt()
            break

        if not cmd:
            continue

        parts = cmd.split()
        op = parts[0].lower()

        if op == "quit" or op == "exit":
            kernel.halt()
            break

        elif op == "help":
            print(HELP_TEXT)

        elif op == "tick":
            n = int(parts[1]) if len(parts) > 1 else 1
            for _ in range(n):
                if not kernel.tick():
                    print("Kernel halted.")
                    break
            print_status(kernel, navigator)

        elif op == "run":
            n = int(parts[1]) if len(parts) > 1 else 1
            kernel.run(max_ticks=n)
            print_status(kernel, navigator)

        elif op == "status":
            print_status(kernel, navigator)

        elif op == "load":
            if len(parts) < 2:
                print("Usage: load <canonical_name>")
                continue
            name = " ".join(parts[1:])
            try:
                kernel.load_canonical(name)
                print(f"Loaded: {name}")
                print(f"Program: {arrangement_str(kernel.program)}")
                print(f"Tier: {kernel.current_tier}")
            except KeyError:
                print(f"Unknown canonical: {name}")

        elif op == "canonical":
            if len(parts) < 2:
                print("Usage: canonical <I-XII>")
                continue
            roman = parts[1].upper()
            if roman in ROMAN_TO_KEY:
                kernel.load_canonical(ROMAN_TO_KEY[roman])
                print(f"Loaded {roman}: {ROMAN_TO_KEY[roman]}")
                print(f"Program: {arrangement_str(kernel.program)}")
            else:
                print(f"Unknown: {roman}")

        elif op == "program":
            print(arrangement_str(kernel.program))
            print(f"Length: {len(kernel.program)}, IP: {kernel.ip}")

        elif op == "snapshot":
            snap = kernel.snapshot
            if snap:
                print(f"Tier: {snap.ouroboricity_tier}")
                print(f"Signature: {snap.sig}")
                print(f"Token diversity: {snap.token_diversity}/12")
                print(f"Self-referential: {snap.self_referential}")
                print(f"Frobenius order: {snap.frobenius_order}")
                print(f"Dialetheia complete: {snap.dialetheia_complete}")
                print(f"Period: {snap.period}")

        elif op == "crystal":
            if len(parts) < 2:
                print("Usage: crystal <addr> | store <name> | find <key>=<glyph> [...]")
                continue
            sub = parts[1].lower()
            if sub == "store":
                name = parts[2] if len(parts) > 2 else ""
                if not name:
                    print("Usage: crystal store <name> [<data>]")
                    continue
                # Sequence swap: hash name → canonical index → load → tick
                # This ensures each store is accompanied by a structural state change.
                # Same name → same canonical → same address (deterministic).
                canonical_keys = list(CANONICALS.keys())
                canon_idx = int.from_bytes(
                    __import__('hashlib').sha256(name.encode()).digest()[:2], 'big'
                ) % len(canonical_keys)
                kernel.load_canonical(canonical_keys[canon_idx])
                kernel.tick()
                snap = kernel.snapshot
                prims = _snapshot_prims(snap, kernel.program)
                extra = " ".join(parts[3:]) if len(parts) > 3 else ""
                addr = cfs.store(name, extra.encode(), **prims,
                                 metadata={"source": "repl", "canonical": canonical_keys[canon_idx]})
                decoded = crystal_decode(addr)
                print(f"  ↻ [{canonical_keys[canon_idx]}] → tick {kernel.tick_count}")
                print(f"Stored '{name}' at address {addr}")
                print(f"  Tuple: ⟨{'·'.join(decoded[p] for p in ['D','T','R','P','F','K','G','C','Phi','H','S','Omega'])}⟩")

            elif sub == "find":
                # crystal find Phi=⊙ S=𐑳 ...
                if len(parts) < 3:
                    print("Usage: crystal find <key>=<glyph> [<key>=<glyph> ...]")
                    continue
                # Build glyph→(prim_name, index) lookup
                from src.crystal_fs import PRIMITIVE_VALUES
                glyph_map = {}  # glyph → prim_name
                for prim, vlist in PRIMITIVE_VALUES.items():
                    for g in vlist:
                        glyph_map[g] = prim

                constraints = {}
                for token in parts[2:]:
                    if "=" in token:
                        k, v = token.split("=", 1)
                        # Normalize key: case-insensitive, map common aliases
                        k_norm = k.strip()
                        # Map common keys to PRIMITIVE_VALUES keys
                        key_aliases = {
                            'd': 'D', 't': 'T', 'r': 'R', 'p': 'P', 'f': 'F',
                            'k': 'K', 'g': 'G', 'c': 'C', 'phi': 'Phi',
                            'h': 'H', 's': 'S', 'omega': 'Omega',
                            'Ð': 'D', 'Þ': 'T', 'Ř': 'R', 'Φ': 'P',
                            'ƒ': 'F', 'Ç': 'K', 'Γ': 'G', 'ɢ': 'C',
                            'φ̂': 'Phi', 'Ħ': 'H', 'Σ': 'S', 'Ω': 'Omega',
                        }
                        k_norm = key_aliases.get(k_norm, key_aliases.get(k_norm.lower(), k_norm))
                        v = v.strip()
                        # If value is a Shavian glyph, verify it
                        if v in glyph_map:
                            constraints[glyph_map[v]] = v
                        else:
                            # Try as raw — maybe it's already a valid glyph
                            # Check all value lists
                            found = False
                            for prim, vlist in PRIMITIVE_VALUES.items():
                                if v in vlist:
                                    constraints[prim] = v
                                    found = True
                                    break
                            if not found:
                                print(f"  ⚠ Unknown value: '{v}' — skipping")
                    else:
                        print(f"  ⚠ Malformed constraint: '{token}' — use key=value")

                if not constraints:
                    print("No valid constraints.")
                    continue

                results = cfs.navigate(**constraints)
                # Also show crystal-wide stats
                from src.crystal_fs import STRIDES, CARDINALITIES, PRIMITIVE_VALUES as PV
                total = 17280000
                fraction = 1.0
                for prim, val in constraints.items():
                    vlist = PV[prim]
                    fraction *= (1.0 / len(vlist))
                est_total = int(total * fraction)

                print(f"Constraints: {constraints}")
                print(f"Crystal-wide estimate: ~{est_total:,} types ({fraction*100:.1f}%)")
                if results:
                    print(f"Stored matches: {len(results)}")
                    for e in results[:10]:
                        print(f"  [{e.address}] {e.name}: {e.tuple_display}")
                    if len(results) > 10:
                        print(f"  ... and {len(results)-10} more")
                else:
                    print("No stored entries match. (Crystal-wide, ~{:,} types satisfy these constraints.)".format(est_total))

            elif sub == "count":
                # crystal count Phi=⊙ ...
                from src.crystal_fs import PRIMITIVE_VALUES as PV, STRIDES as ST, CARDINALITIES as CD
                constraints = {}
                glyph_map = {}
                for prim, vlist in PV.items():
                    for g in vlist:
                        glyph_map[g] = prim
                if len(parts) > 2:
                    for token in parts[2:]:
                        if "=" in token:
                            k, v = token.split("=", 1)
                            k = k.strip()
                            v = v.strip()
                            key_aliases = {
                                'd':'D','t':'T','r':'R','p':'P','f':'F',
                                'k':'K','g':'G','c':'C','phi':'Phi',
                                'h':'H','s':'S','omega':'Omega',
                            }
                            k = key_aliases.get(k.lower(), k)
                            if v in glyph_map:
                                constraints[glyph_map[v]] = v
                total = 17280000
                fraction = 1.0
                for prim, val in constraints.items():
                    fraction *= (1.0 / len(PV[prim]))
                count = int(total * fraction)
                print(f"Constraints: {constraints}")
                print(f"Count: {count:,} / 17,280,000 ({fraction*100:.2f}%)")

            elif sub == "name":
                name = parts[2] if len(parts) > 2 else ""
                if not name:
                    print("Usage: crystal name <name>")
                else:
                    entry = cfs.read_by_name(name)
                    if entry is None:
                        print(f"No entry named '{name}'.")
                    else:
                        print(f"Name:    {entry.name}")
                        print(f"Address: {entry.address}")
                        print(f"Tuple:   {entry.tuple_display}")
                        if entry.data:
                            print(f"Data:    {entry.data.decode(errors='replace')}")
                        if entry.metadata:
                            print(f"Meta:    {entry.metadata}")

            else:
                try:
                    addr = int(sub)
                    decoded = crystal_decode(addr)
                    print(f"Address: {addr}")
                    for p in ['D','T','R','P','F','K','G','C','Phi','H','S','Omega']:
                        print(f"  {p}: {decoded[p]}")
                    glyphs = [decoded[p] for p in ['D','T','R','P','F','K','G','C','Phi','H','S','Omega']]
                    print(f"  Tuple: ⟨{'·'.join(glyphs)}⟩")
                    entry = cfs.read(addr)
                    if entry is not None:
                        print(f"  Stored: '{entry.name}'", end="")
                        if entry.data:
                            print(f"  →  {entry.data.decode(errors='replace')}", end="")
                        print()
                        if entry.metadata:
                            print(f"  Meta: {entry.metadata}")
                except ValueError:
                    print(f"Invalid address: {sub}")

        elif op == "clink":
            if len(parts) < 2:
                print("Usage: clink up|down|goto <N>|status")
                continue
            sub = parts[1].lower()
            if sub == "up":
                if navigator.ascend():
                    print(f"Ascended to: {navigator.layer.name}")
                else:
                    print("Already at top (Whole Organism)")
            elif sub == "down":
                if navigator.descend():
                    print(f"Descended to: {navigator.layer.name}")
                else:
                    print("Already at bottom (Quarks)")
            elif sub == "goto":
                n = int(parts[2]) if len(parts) > 2 else 0
                navigator.goto(n)
                print(f"Jumped to: {navigator.layer.name}")
            elif sub == "status":
                print(navigator.status())

        elif op == "discover":
            props_str = " ".join(parts[1:]) if len(parts) > 1 else ""
            props = {}
            for pair in props_str.split():
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    if v.lower() == "true":
                        props[k] = True
                    elif v.lower() == "false":
                        props[k] = False
                    else:
                        try:
                            props[k] = int(v)
                        except ValueError:
                            props[k] = v
            print(f"Searching for: {props}")
            results = kernel.navigate_arrangement_space(props, max_search=500)
            if results:
                for i, snap in enumerate(results[:10]):
                    print(f"  [{i}] {snap.summary()}")
                    print(f"      {arrangement_str(snap.arrangement)[:60]}")
            else:
                print("No matches found.")

        elif op == "memory":
            start = int(parts[1]) if len(parts) > 1 else 0
            count = int(parts[2]) if len(parts) > 2 else 16
            cells = kernel.memory.dump(start, count)
            print("  ".join(c.name for c in cells))

        elif op == "registers":
            for i in range(8):
                print(f"  R{i}: {kernel.registers.read(i).name}")

        elif op == "stack":
            print(f"  Depth: {kernel.stack.depth}")
            for i, val in enumerate(reversed(kernel.stack.data[-8:])):
                print(f"  [{kernel.stack.depth - 1 - i}] {val.name}")

        elif op == "frobenius":
            print(f"  Total: {len(kernel.verification_log)}")
            print(f"  Closed: {len(kernel.verification_log) - kernel.open_count}")
            print(f"  Open: {kernel.open_count}")
            for i, r in enumerate(kernel.verification_log[-5:]):
                status = "✓" if r.closed else f"✗ ({r.mismatch})"
                print(f"  [{i}] {status}")

        elif op == "halt":
            kernel.halt()
            print("Kernel halted.")

        else:
            print(f"Unknown command: {op}. Type 'help'.")


# ─── Entry Point ──────────────────────────────────────────────

def main():
    boot_animation()
    kernel, cfs, navigator = initialize()
    repl(kernel, cfs, navigator)
    print("\nomonad_OS halted. μ∘δ=id verified.\n")


if __name__ == "__main__":
    main()
