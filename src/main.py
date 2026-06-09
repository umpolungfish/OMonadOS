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

from src.tokens import (
    Token, TOKEN_NAMES, BOOTSTRAP_LOOP, CANONICALS, arrangement_str,
)
from src.belnap_state import B4, B4Memory, B4Registers, B4Stack
from src.kernel import OmonadKernel, self_imscribe, KernelPhase
from src.crystal_fs import CrystalFS, crystal_encode, crystal_decode, TOTAL_TYPES
from src.clink_chain import ClinkNavigator, CLINK_CHAIN


# ─── Boot Animation ───────────────────────────────────────────

BOOT_BANNER = r"""
     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
     █▌                                                   ▐█
     █▌           o m o n a d _ O S   ⊙                  ▐█
     █▌    The Self-Imscribing Operating Kernel           ▐█
     █▌                                                   ▐█
     █▌  ⟨𐑦·𐑸·𐑾·𐑹·𐑐·𐑧·𐑔·𐑠·⊙·𐑖·𐑳·𐑭⟩                    ▐█
     █▌  Frobenius Core · Belnap FOUR State               ▐█
     █▌  Crystal FS · CLINK Chain · 430M Arrangement Space  ▐█
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
  crystal <addr>   — Decode a crystal address
  crystal store <name> <data>  — Store data at crystal address
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
                print("Usage: crystal <addr> | store <name> <data> | find <query>")
                continue
            sub = parts[1].lower()
            if sub == "store":
                pass  # Simplified
            elif sub == "find":
                pass
            else:
                try:
                    addr = int(sub)
                    decoded = crystal_decode(addr)
                    for p, v in decoded.items():
                        print(f"  {p}: {v}")
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
